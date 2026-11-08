"""Builds the ButtonPrompts-KeyboardMouse mod folder (keyboard/mouse icons) for OOT on Lichii.
  python build_mods_kbm.py <out_root>      (writes <out_root>/ButtonPrompts-KeyboardMouse/romfs/... and work/preview/tex_preview.png)
Steps: External font (build_fonts_kbm.py) + Common.bntx with KeyTexFont{A,B,X,Y}, OcarinaButton{A,B,X,Y,L,R},
Controller_Pro/Pro1 and ControllerGuide_Pro_00..04 (make_ctrl_kbm.py). Nothing is installed: copy the folder to
<Lichii>/user/load/0400486024DEC000 yourself (see docs/INSTALLATION.md)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageDraw
import ctrl_common as C
import glyphlib as BF
from oot_paths import FONTS, OUT, PREVIEW
import build_fonts_kbm as K
import make_ctrl_kbm as MK
import zs

FONT_REL = os.path.join("Font2", "Scalable", "External.Nin_Ounce_NVN2.bfotf.zs")
ORIG_FONT_TOTAL = os.path.getsize(os.path.join(FONTS, "External.bfotf"))


def flatten(c):
    pts, cur = [], None
    for op, a in c:
        if op in ("moveTo", "lineTo"):
            cur = a[0]; pts.append(cur)
        elif op == "curveTo":
            p0, (p1, p2, p3) = cur, a
            for i in range(1, 13):
                t = i / 12; u = 1 - t
                pts.append((u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0],
                            u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]))
            cur = p3
    return pts


def ink(contours, sign, size, cx, cy, fit_w, fit_h, ss=8):
    """rasterise font-unit contours into a size x size float mask (1 = ink), centred on (cx, cy) px and uniformly
    scaled to fit fit_w x fit_h px. sign=-1: cutouts (negative area) are ink; sign=+1: positive-area fills are ink."""
    x0, y0, x1, y1 = BF.bbox(contours)
    s = min(fit_w / (x1 - x0), fit_h / (y1 - y0))
    tf = lambda x, y: ((cx + (x - (x0 + x1) / 2) * s) * ss, (cy - (y - (y0 + y1) / 2) * s) * ss)
    im = Image.new("L", (size * ss, size * ss), 0); d = ImageDraw.Draw(im)
    for c in sorted(contours, key=lambda c: -abs(BF.area(c))):
        d.polygon([tf(x, y) for x, y in flatten(c)], fill=255 if BF.area(c) * sign > 0 else 0)
    return np.asarray(im.resize((size, size), Image.BOX)).astype(np.float32) / 255


# what each Switch button shows on the HUD / song sheet: (contours, sign, width frac, height frac)
def symbols():
    return {
        "A": (K.space_symbol(0), -1, 0.70, 0.42),
        "B": (K.letters("C", 250, 0), -1, 0.46, 0.52),
        "X": (K.letters("R", 250, 0), -1, 0.46, 0.52),
        "Y": (K.mouse(0, press="L"), +1, 0.50, 0.74),
        "L": (K.letters("Q", 250, 0), -1, 0.46, 0.52),
        "R": (K.letters("E", 250, 0), -1, 0.46, 0.52),
    }


def key_tex(k):                       # 64x64 BC4, white symbol on black (the layout supplies the button shape)
    cs, sign, fw, fh = symbols()[k]
    m = ink(cs, sign, 64, 32, 32, 64 * fw * 1.15, 64 * fh * 1.15)
    return np.clip(m * 255 + 0.5, 0, 255).astype(np.uint8)


def ocarina_tex(orig, k):             # 93x93 ASTC, black symbol on the white shape; alpha (silhouette) untouched
    cs, sign, fw, fh = symbols()[k]
    a = np.array(orig.convert("RGBA")); alpha = a[..., 3]
    ys, xs = np.where(alpha >= 128); cx, cy = (xs.min() + xs.max() + 1) / 2, (ys.min() + ys.max() + 1) / 2
    w, h = xs.max() + 1 - xs.min(), ys.max() + 1 - ys.min()
    m = ink(cs, sign, 93, cx, cy, w * fw * 1.2, h * fh * 1.2)
    out = np.empty_like(a); out[..., :3] = np.clip(255 * (1 - m), 0, 255).astype(np.uint8)[..., None]; out[..., 3] = alpha
    return Image.fromarray(out)


def main():
    out_root = sys.argv[1]; root = os.path.join(out_root, "ButtonPrompts-KeyboardMouse")
    fin, size, blank = K.build_fitting(OUT)
    otf = open(fin, "rb").read()
    bf = BF.encrypt_bfotf(otf, ORIG_FONT_TOTAL); assert len(bf) == ORIG_FONT_TOTAL, (len(bf), ORIG_FONT_TOTAL)
    p = os.path.join(root, "romfs", FONT_REL); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(zs.compress(bf, "zs.zsdic")); print("font", p, size, "bytes otf")

    orig_bntx, otex = C.load_bntx(); b = bytearray(orig_bntx); t = C.all_brti(bytes(b))
    for k in "ABXY": C.write_bc4(b, t[f"KeyTexFont{k}_00"], key_tex(k))
    oc = {}
    for k in "ABXYLR":
        oc[k] = ocarina_tex(C.read_astc(orig_bntx, otex[f"OcarinaButton{k}_00"]), k)
        C.write_astc(b, t[f"OcarinaButton{k}_00"], oc[k])
    pic, light = MK.build_picture(True), MK.build_picture(False)
    sheets, _ = MK.build_sheets()
    C.write_astc(b, t["Controller_Pro1"], pic); C.write_astc(b, t["Controller_Pro"], light)
    for i, s in enumerate(sheets): C.write_bc4(b, t["ControllerGuide_Pro_0%d" % i], np.array(s))
    print("bntx ->", C.write_mod_bntx(b, root))

    # preview: row 1 originals, row 2 what was written (read back from the patched texture)
    bb = bytes(b); tt = C.all_brti(bb); cell = 100
    sheet = Image.new("RGBA", (cell * 10, cell * 2), (110, 90, 60, 255))
    for i, k in enumerate("ABXY"):
        sheet.alpha_composite(Image.fromarray(C.read_bc4(orig_bntx, otex[f"KeyTexFont{k}_00"])).convert("RGBA"), (i * cell + 4, 4))
        sheet.alpha_composite(Image.fromarray(C.read_bc4(bb, tt[f"KeyTexFont{k}_00"])).convert("RGBA"), (i * cell + 4, cell + 4))
    for i, k in enumerate("ABXYLR"):
        sheet.alpha_composite(C.read_astc(orig_bntx, otex[f"OcarinaButton{k}_00"]).convert("RGBA"), (4 + (i + 4) * cell, 4))
        sheet.alpha_composite(C.read_astc(bb, tt[f"OcarinaButton{k}_00"]).convert("RGBA"), (4 + (i + 4) * cell, cell + 4))
    sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST)
    sheet.convert("RGB").save(os.path.join(PREVIEW, "tex_preview.png")); print("preview", os.path.join(PREVIEW, "tex_preview.png"))


if __name__ == "__main__":
    main()
