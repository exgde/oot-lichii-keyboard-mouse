"""Keyboard + mouse art and guide lines for the "Basic Controls" screen of OOT.
  python make_ctrl_kbm.py                      -> work/preview/preview_KeyboardMouse.png / pic_KeyboardMouse.png (nothing is written to the game)
  python make_ctrl_kbm.py --write <mod_root> [<bntx.zs>]   -> writes Controller_Pro/Pro1 + ControllerGuide_Pro_00..04
Pictures: assets/keyboard.png (570x244) and assets/mouse.png (271x419); draw_default_art.py draws them if they are missing.
Mapping (Switch -> keyboard/mouse), see docs/KEY-MAPPING.md:
  LStick WASD | RStick mouse | Y (Attack) left click | ZR (Use Item) right click | ZL (Target) left Shift
  L/R (Quick Select Items) Q/E | A (Actions, hold = Dash) Space | D-pad 1/2/3/4 | + Enter | - Tab"""
import os, sys
from collections import deque
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ctrllib as M                         # controls-screen measurements + line helpers
import ctrl_common as C
from ctrllib import PW, PH, SW, SH, to_sheet, LW, DOT, line, dot, tick
from oot_paths import ASSETS, PREVIEW

KB_PNG = os.path.join(ASSETS, "keyboard.png")       # 570x244, dark keys on a white background (see draw_default_art.py)
MS_PNG = os.path.join(ASSETS, "mouse.png")          # 271x419, grey mouse seen from above
import draw_default_art
draw_default_art.ensure(KB_PNG, MS_PNG)           # draws the default art if you did not provide your own

# ---- layout inside the 1160x680 picture ------------------------------------------------------------------
KB_SC, KB_ORG = 1.15, (130, 250)            # keyboard native (17,22) -> picture (130,250), scale 1.15
MS_SC, MS_ORG = 1.10, (870, 190)            # mouse native body bbox top-left (36,81) -> picture (870,190)
MS_BBOX = (36, 81, 223, 390)


def kb(x, y):
    return ((x - 17) * KB_SC + KB_ORG[0], (y - 22) * KB_SC + KB_ORG[1])


def ms(x, y):
    return (MS_ORG[0] + (x - MS_BBOX[0]) * MS_SC, MS_ORG[1] + (y - MS_BBOX[1]) * MS_SC)


# key centres in the keyboard picture (native px of the 570x244 keyboard picture)
KEY = dict(num1=(70, 61), num4=(182, 61), tab=(41.5, 97), q=(88.5, 97), w=(126, 97), e=(163, 97),
           caps=(48, 133), a=(101, 133), s=(138.5, 133), d=(176, 133), enter=(525.5, 133),
           lshift=(57, 169), space=(269, 208))
WASD_BOX = (86, 82, 191, 148)                       # W/A/S/D cluster (tight: the number row sits just above)
NUM_BOX = (55, 46, 197, 76)                         # keys 1 2 3 4
MOUSE_PT = dict(lmb=(88, 150), rmb=(182, 150), wheel=(135, 130), body=(135, 300))


# ---- reference pictures -> game-style art ------------------------------------------------------------------
def _outside(bright):
    """pixels of `bright` connected to the image border"""
    h, w = bright.shape; out = np.zeros_like(bright); q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if bright[y, x] and not out[y, x]: out[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if bright[y, x] and not out[y, x]: out[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and bright[ny, nx] and not out[ny, nx]:
                out[ny, nx] = True; q.append((ny, nx))
    return out


def _largest(mask):
    h, w = mask.shape; seen = np.zeros_like(mask); best = None
    for y in range(h):
        for x in range(w):
            if mask[y, x] and not seen[y, x]:
                q = deque([(y, x)]); seen[y, x] = True; pts = [(y, x)]
                while q:
                    cy, cx = q.popleft()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; q.append((ny, nx)); pts.append((ny, nx))
                if best is None or len(pts) > len(best): best = pts
    out = np.zeros_like(mask)
    for y, x in best: out[y, x] = True
    return out


def keyboard_art(dark=True):
    a = np.asarray(Image.open(KB_PNG).convert("RGB")).astype(np.float32); lum = a.mean(2)
    # background = the big bright regions (outside + the gaps between keys); letters = small bright islands inside keys
    bright = lum > 200; h, w = bright.shape; lab = np.zeros((h, w), np.int32); sizes = [0]
    for y0 in range(h):
        for x0 in range(w):
            if bright[y0, x0] and not lab[y0, x0]:
                n = len(sizes); lab[y0, x0] = n; q = deque([(y0, x0)]); cnt = 0
                while q:
                    cy, cx = q.popleft(); cnt += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and bright[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = n; q.append((ny, nx))
                sizes.append(cnt)
    big = np.array([s > 900 for s in sizes]); bgm = big[lab] & (lab > 0)
    mask = ~bgm                                                     # keys + their letters (+ the thin outer frame)
    m_img = Image.fromarray(mask.astype(np.uint8) * 255)
    edge = mask & ~(np.asarray(m_img.filter(ImageFilter.MinFilter(3))) > 0)   # 1px rim: avoid a light fringe
    body, letter = (28, 226) if dark else (74, 244)
    t = np.clip((lum - 40) / 200.0, 0, 1)
    val = body + t * (letter - body); val[edge] = body
    rgba = np.zeros(lum.shape + (4,), np.uint8)
    rgba[..., 0] = val; rgba[..., 1] = val; rgba[..., 2] = val * 0.92
    rgba[..., 3] = np.asarray(m_img.filter(ImageFilter.GaussianBlur(0.6)))
    return Image.fromarray(rgba, "RGBA")


def mouse_art(dark=True):
    a = np.asarray(Image.open(MS_PNG).convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    neutral = (np.abs(r - g) < 14) & (np.abs(g - b) < 14) & (r < 215)
    sil = _largest(neutral)
    filled = ~_outside(~sil)                                        # fill the holes (wheel, split lines)
    x0, y0, x1, y1 = MS_BBOX
    lum = a.mean(2)
    lo, hi = (30, 170) if dark else (76, 215)
    val = np.clip(lo + (150 - lum) * 1.25, lo, hi)                  # dark outlines -> light strokes, body -> dark
    m_img = Image.fromarray(filled.astype(np.uint8) * 255)
    rim = filled & ~(np.asarray(m_img.filter(ImageFilter.MinFilter(5))) > 0)
    val[rim] = np.maximum(val[rim], lo + 70)                        # lighter silhouette rim like the other art
    rgba = np.zeros(lum.shape + (4,), np.uint8)
    rgba[..., 0] = val; rgba[..., 1] = val; rgba[..., 2] = val * 0.92
    rgba[..., 3] = np.asarray(m_img.filter(ImageFilter.GaussianBlur(0.8)))
    return Image.fromarray(rgba, "RGBA")


def build_picture(dark=True):
    out = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    k = keyboard_art(dark).crop((14, 18, 557, 230))                 # tight crop keeps KB_ORG = native (17,22)
    k = k.resize((int(round(k.width * KB_SC)), int(round(k.height * KB_SC))), Image.LANCZOS)
    out.alpha_composite(k, (int(round(KB_ORG[0] - 3 * KB_SC)), int(round(KB_ORG[1] - 4 * KB_SC))))
    mo = mouse_art(dark).crop((MS_BBOX[0] - 4, MS_BBOX[1] - 4, MS_BBOX[2] + 5, MS_BBOX[3] + 5))
    mo = mo.resize((int(round(mo.width * MS_SC)), int(round(mo.height * MS_SC))), Image.LANCZOS)
    out.alpha_composite(mo, (int(round(MS_ORG[0] - 4 * MS_SC)), int(round(MS_ORG[1] - 4 * MS_SC))))
    return out


# ---- guide lines ---------------------------------------------------------------------------------------------
def P(p):
    return to_sheet(p)


def poly(d, pts, end=True):
    line(d, pts)
    if end: dot(d, pts[-1])


def box(d, b, pad=0):
    """rounded rectangle outline around a native-coordinate box"""
    (x0, y0), (x1, y1) = P(kb(b[0], b[1])), P(kb(b[2], b[3]))
    d.rounded_rectangle((x0 - pad, y0 - pad, x1 + pad, y1 + pad), radius=12, outline=255, width=LW - 1)
    return (x0, y0, x1, y1)


def build_sheets():
    LXs, RXs, R = M.LX, M.RX, M.ROWS
    sheets = [Image.new("L", (SW, SH), 0) for _ in range(5)]
    d = [ImageDraw.Draw(s) for s in sheets]
    pt = {k: P(kb(*v)) for k, v in KEY.items()}
    mp = {k: P(ms(*v)) for k, v in MOUSE_PT.items()}
    f = dict(pt); f.update({"m_" + k: v for k, v in mp.items()})

    # sheet 0 --------------------------------------------------------------------------------------------
    # ZL (Target) -> left Shift
    tick(d[0], LXs, R["zl"]); poly(d[0], [(LXs, R["zl"]), (218, R["zl"]), (218, pt["lshift"][1]), pt["lshift"]])
    # + (Open Menu) -> Enter
    tick(d[0], RXs, R["plus"]); poly(d[0], [(RXs, R["plus"]), (pt["enter"][0], R["plus"]), pt["enter"]])
    # LStick (Move) -> WASD cluster
    wb = box(d[0], WASD_BOX)
    tick(d[0], LXs, R["lstick"]); line(d[0], [(LXs, R["lstick"]), (170, R["lstick"]), (170, (wb[1] + wb[3]) / 2), (wb[0], (wb[1] + wb[3]) / 2)])
    # RStick (Rotate Camera) -> mouse body
    tick(d[0], RXs, R["rstick"]); poly(d[0], [(RXs, R["rstick"]), (mp["body"][0], R["rstick"]), mp["body"]])
    # A (Actions) -> Space, Y (Attack) -> left mouse button
    tick(d[0], RXs, R["abxy"]); jx = 1385
    poly(d[0], [(RXs, R["abxy"]), (jx, R["abxy"]), (jx, 1075), (pt["space"][0], 1075), pt["space"]])
    poly(d[0], [(jx, R["abxy"]), (jx, 640), (mp["lmb"][0], 640), mp["lmb"]])
    # sheet 1: - (Open Map) -> Tab
    tick(d[1], LXs, R["minus"]); poly(d[1], [(LXs, R["minus"]), (186, R["minus"]), (186, pt["tab"][1]), pt["tab"]])
    # sheet 2: ZR (Use Item) -> right mouse button
    tick(d[2], RXs, R["zr"]); poly(d[2], [(RXs, R["zr"]), (1360, R["zr"]), (1360, mp["rmb"][1]), mp["rmb"]])
    # sheet 3: D-pad -> 1 2 3 4
    nb = box(d[3], NUM_BOX)
    tick(d[3], LXs, R["dpad"]); line(d[3], [(LXs, R["dpad"]), (154, R["dpad"]), (154, (nb[1] + nb[3]) / 2), (nb[0], (nb[1] + nb[3]) / 2)])
    # sheet 4: L (Quick Select Items, left) -> Q, R (Quick Select Items, right) -> E
    tick(d[4], LXs, R["l"]); poly(d[4], [(LXs, R["l"]), (pt["q"][0], R["l"]), pt["q"]])
    tick(d[4], RXs, R["r"]); poly(d[4], [(RXs, R["r"]), (pt["e"][0], R["r"]), pt["e"]])
    return sheets, f


def preview(pic, sheets, f, path, width=1300):
    """picture + guide sheets on the tan screen background, like the game draws them (centre 777.5,842)"""
    canvas = Image.new("RGBA", (SW, SH), (176, 140, 84, 255))
    p = pic.resize((int(PW * M.S), int(PH * M.S)), Image.LANCZOS)
    canvas.alpha_composite(p, (int(M.CX - p.width / 2), int(M.CY - p.height / 2)))
    over = np.zeros((SH, SW), np.uint8)
    for s in sheets: over = np.maximum(over, np.array(s))
    white = Image.new("RGBA", (SW, SH), (245, 240, 225, 255)); white.putalpha(Image.fromarray(over))
    canvas.alpha_composite(white)
    d = ImageDraw.Draw(canvas)
    for k, (x, y) in f.items():
        d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=(255, 40, 40, 255), width=2)
    canvas.crop((0, 300, SW, 1260)).resize((width, int(960 * width / SW)), Image.LANCZOS).convert("RGB").save(path)


def main():
    pic = build_picture(True); light = build_picture(False)
    sheets, f = build_sheets()
    pic.save(os.path.join(PREVIEW, "pic_KeyboardMouse.png"))
    preview(pic, sheets, f, os.path.join(PREVIEW, "preview_KeyboardMouse.png"))
    print("preview:", os.path.join(PREVIEW, "preview_KeyboardMouse.png"))
    if "--write" in sys.argv:
        import zs
        i = sys.argv.index("--write"); root = sys.argv[i + 1]
        src = sys.argv[i + 2] if len(sys.argv) > i + 2 else None
        b = bytearray(zs.decompress(open(src, "rb").read())) if src else bytearray(open(C.BNTX_PATH, "rb").read())
        tex = C.all_brti(bytes(b))
        C.write_astc(b, tex["Controller_Pro1"], pic); C.write_astc(b, tex["Controller_Pro"], light)
        for n, s in enumerate(sheets):
            C.write_bc4(b, tex["ControllerGuide_Pro_0%d" % n], np.array(s))
        print("wrote", C.write_mod_bntx(b, root))


if __name__ == "__main__":
    main()
