"""Keyboard/mouse icon font for OOT (External.Nin_Ounce_NVN2.bfotf), variant "kbm".
Every Switch button glyph becomes the matching key or mouse button (mapping in docs/KEY-MAPPING.md):
  A=Space B=C X=R Y=left click L=Q R=E ZL=Shift ZR=right click +=Enter -=Tab  D-pad 1/2/3/4  LS=WASD  RS=mouse
python build_fonts_kbm.py  -> work/out/External_kbm_subset.otf (fits in 14560 bytes) + work/preview/font_preview.png"""
import os, sys, math
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.misc.transform import Transform

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import glyphlib as BF
from oot_paths import FONTS, OUT, PREVIEW

MAX_OTF = 14560            # original External.otf size = decompressed container (14568) minus the 8 byte header
CY = 301


# ---- geometry -----------------------------------------------------------------------------------------------
def ccw(c):
    return BF.area(c) > 0


def fill(c):
    return c if ccw(c) else BF.reverse(c)


def cut(c):
    return BF.reverse(c) if ccw(c) else c


def rrect(x0, y0, x1, y1, r):
    """rounded rectangle, CCW (fill). r = number or (bottom-left, bottom-right, top-right, top-left)"""
    bl, br, tr, tl = (r, r, r, r) if not isinstance(r, tuple) else r
    k = 0.5523
    c = [("moveTo", ((x0 + bl, y0),)), ("lineTo", ((x1 - br, y0),))]
    c.append(("curveTo", ((x1 - br + k * br, y0), (x1, y0 + br - k * br), (x1, y0 + br))) if br else ("lineTo", ((x1, y0),)))
    c.append(("lineTo", ((x1, y1 - tr),)))
    c.append(("curveTo", ((x1, y1 - tr + k * tr), (x1 - tr + k * tr, y1), (x1 - tr, y1))) if tr else ("lineTo", ((x1, y1),)))
    c.append(("lineTo", ((x0 + tl, y1),)))
    c.append(("curveTo", ((x0 + tl - k * tl, y1), (x0, y1 - tl + k * tl), (x0, y1 - tl))) if tl else ("lineTo", ((x0, y1),)))
    c.append(("lineTo", ((x0, y0 + bl),)))
    c.append(("curveTo", ((x0, y0 + bl - k * bl), (x0 + bl - k * bl, y0), (x0 + bl, y0))) if bl else ("lineTo", ((x0, y0),)))
    c.append(("closePath", ()))
    return c


def tri(cx, cy, size, direction):
    h = size * 0.9
    pts = {"up": [(cx - size / 2, cy - h / 2), (cx + size / 2, cy - h / 2), (cx, cy + h / 2)],
           "down": [(cx - size / 2, cy + h / 2), (cx, cy - h / 2), (cx + size / 2, cy + h / 2)],
           "left": [(cx + h / 2, cy - size / 2), (cx + h / 2, cy + size / 2), (cx - h / 2, cy)],
           "right": [(cx - h / 2, cy - size / 2), (cx + h / 2, cy), (cx - h / 2, cy + size / 2)]}[direction]
    return fill(BF.poly(pts, cw=False))


def place(cs, dx, dy, s=1.0):
    """scale about the origin then translate"""
    return BF.transform(cs, Transform().translate(dx, dy).scale(s))


# ---- letters (Nin Zelda glyph font, cap height 640 units) ---------------------------------------------------
_z = TTFont(os.path.join(FONTS, "Nin-ZeldaGlyphs-v3-Plain.otf")); _zgs = _z.getGlyphSet(); _zc = _z.getBestCmap()


def zelda(ch, cap):
    cs = [cut(c) for c in BF.contours_of(_zgs, _zc[ord(ch)])]
    return BF.transform(cs, Transform().scale(cap / 640))


def letters(s, cap, cx, cy=CY, gap=26):
    """string as cutout contours centred on (cx, cy): one shared baseline (all glyphs here are caps/digits)"""
    chars = [zelda(ch, cap) for ch in s]
    boxes = [BF.bbox(cs) for cs in chars]
    total = sum(b[2] - b[0] for b in boxes) + gap * (len(chars) - 1)
    x = cx - total / 2; out = []
    for cs, b in zip(chars, boxes):
        out += BF.transform(cs, Transform().translate(x - b[0], cy - cap / 2))
        x += (b[2] - b[0]) + gap
    return out


# ---- glyph designs (y up, cell height ~600 centred on y=301) --------------------------------------------------
def key(adv, s, cap=250, w=560, h=560, r=92):
    cx = adv / 2
    return [rrect(cx - w / 2, CY - h / 2, cx + w / 2, CY + h / 2, r)] + letters(s, cap, cx)


def wide_key(adv, content, w=600, h=330, r=70):
    cx = adv / 2
    return [rrect(cx - w / 2, CY - h / 2, cx + w / 2, CY + h / 2, r)] + content(cx)


def space_symbol(cx):                     # open box ␣
    s, x, y0, y1 = 40, 190, CY + 36, CY - 40
    pts = [(cx - x - s / 2, y0), (cx - x - s / 2, y1 - s / 2), (cx + x + s / 2, y1 - s / 2), (cx + x + s / 2, y0),
           (cx + x - s / 2, y0), (cx + x - s / 2, y1 + s / 2), (cx - x + s / 2, y1 + s / 2), (cx - x + s / 2, y0)]
    return [cut(BF.poly(pts, cw=False))]


def shift_symbol(cx):                     # hollow-ish up arrow ⇧ (solid cutout)
    p = [(0, 118), (-128, -8), (-52, -8), (-52, -112), (52, -112), (52, -8), (128, -8)]
    return [cut(BF.poly([(cx + x, CY + y) for x, y in p], cw=False))]


def enter_symbol(cx):                     # return arrow ⏎
    p = [(150, 78), (150, -40), (-34, -40), (-34, -86), (-146, -20), (-34, 46), (-34, 0), (104, 0), (104, 78)]
    return [cut(BF.poly([(cx + x, CY + y) for x, y in p], cw=False))]


def mouse(cx, s=1.0, press=None, arrows=()):
    """mouse outline (ring + split lines + wheel). press: 'L' | 'R' | 'W' -> that button solid. arrows: directions drawn beside it."""
    W, H, R, ring, lw, gap = 380, 570, 190, 48, 30, 22
    iy0, iy1, ix0, ix1 = -H / 2 + ring, H / 2 - ring, -W / 2 + ring, W / 2 - ring
    ys = 30                                                     # split line height (buttons above)
    cs = [rrect(-W / 2, -H / 2, W / 2, H / 2, R), cut(rrect(ix0, iy0, ix1, iy1, R - ring)),
          rrect(-lw / 2, ys, lw / 2, iy1 + 2, 0), rrect(ix0 - 2, ys - lw / 2, ix1 + 2, ys + lw / 2, 0)]
    ri = R - ring - gap
    if press == "L":
        cs.append(rrect(ix0 + gap, ys + lw / 2 + gap, -lw / 2 - gap, iy1 - gap, (0, 0, 0, ri)))
    elif press == "R":
        cs.append(rrect(lw / 2 + gap, ys + lw / 2 + gap, ix1 - gap, iy1 - gap, (0, 0, ri, 0)))
    wheel = 84 if press == "W" else 44
    cs.append(rrect(-wheel / 2, ys + 60, wheel / 2, ys + 60 + (190 if press == "W" else 120), wheel / 2))
    cs = [fill(c) if i not in (1,) else c for i, c in enumerate(cs)]
    out = place(cs, cx, CY, s)
    off = 205 * s + 18
    for d in arrows:
        if d == "left": out.append(tri(cx - off - 28, CY, 74, "left"))
        if d == "right": out.append(tri(cx + off + 28, CY, 74, "right"))
        if d == "up": out.append(tri(cx, CY + 285 * s + 46, 86, "up"))
        if d == "down": out.append(tri(cx, CY - 285 * s - 46, 86, "down"))
    return out


def wasd(adv):
    cx, s, g = adv / 2, 190, 18
    pos = {"W": (cx, CY + (s + g) / 2), "A": (cx - (s + g), CY - (s + g) / 2), "S": (cx, CY - (s + g) / 2), "D": (cx + (s + g), CY - (s + g) / 2)}
    out = []
    for ch, (x, y) in pos.items():
        out.append(rrect(x - s / 2, y - s / 2, x + s / 2, y + s / 2, 38)); out += letters(ch, 112, x, y, 12)
    return out


def keys_row(adv, labels, cap=150):
    n = len(labels); s = 230 if n == 2 else 190; g = 22
    total = n * s + (n - 1) * g; x0 = adv / 2 - total / 2; out = []
    for i, ch in enumerate(labels):
        x = x0 + s / 2 + i * (s + g)
        out.append(rrect(x - s / 2, CY - s / 2, x + s / 2, CY + s / 2, 46)); out += letters(ch, cap if n == 2 else 112, x, CY, 12)
    return out


def glyph_map(adv_of):
    """code point -> contours for every glyph that has a keyboard/mouse equivalent"""
    a = adv_of
    new = {
        0xE040: wide_key(a(0xE040), space_symbol, 600, 300),                       # A  -> Space
        0xE041: key(a(0xE041), "C"),                                                # B  -> C (Ctrl/Alt clash with Lichii hotkeys)
        0xE042: key(a(0xE042), "R"),                                                # X  -> R
        0xE043: mouse(a(0xE043) / 2, press="L"),                                     # Y  -> left click
        0xE044: key(a(0xE044), "Q"),                                                # L  -> Q
        0xE045: key(a(0xE045), "E"),                                                # R  -> E
        0xE046: wide_key(a(0xE046), shift_symbol, 640, 330),                        # ZL -> Shift
        0xE047: mouse(a(0xE047) / 2, press="R"),                                     # ZR -> right click
        0xE049: wide_key(a(0xE049), lambda cx: letters("1-4", 150, cx), 600, 330),   # D-pad (up/down/left/right) -> 1-4
        0xE04B: wide_key(a(0xE04B), enter_symbol, 560, 330),                         # +  -> Enter
        0xE04C: wide_key(a(0xE04C), lambda cx: letters("TAB", 130, cx), 560, 330),   # -  -> Tab
        0xE050: key(a(0xE050), "S"), 0xE052: key(a(0xE052), "W"),                    # LS down / up
        0xE05A: key(a(0xE05A), "A"), 0xE058: key(a(0xE058), "D"),                    # LS left / right
        0xE054: keys_row(a(0xE054), "AD"), 0xE05C: keys_row(a(0xE05C), "WS"),        # LS left-right / up-down
        0xE05E: wasd(a(0xE05E)),                                                     # LS -> WASD
        0xE05F: mouse(a(0xE05F) / 2),                                                # RS -> mouse
        0xE057: mouse(a(0xE057) / 2, press="W"),                                     # RS press -> wheel
        0xE051: mouse(a(0xE051) / 2, 0.8, arrows=("down",)), 0xE053: mouse(a(0xE053) / 2, 0.8, arrows=("up",)),
        0xE05B: mouse(a(0xE05B) / 2, 0.8, arrows=("left",)), 0xE059: mouse(a(0xE059) / 2, 0.8, arrows=("right",)),
        0xE055: mouse(a(0xE055) / 2, 0.8, arrows=("left", "right")), 0xE05D: mouse(a(0xE05D) / 2, 0.8, arrows=("up", "down")),
        0xE068: mouse(a(0xE068) / 2, 0.8, arrows=("left", "right")),                 # RS shake
        0xE060: key(a(0xE060), "1"), 0xE062: key(a(0xE062), "2"),                    # D-pad up / left
        0xE063: key(a(0xE063), "3"), 0xE061: key(a(0xE061), "4"),                    # D-pad right / down
        0xE064: keys_row(a(0xE064), "14"), 0xE065: keys_row(a(0xE065), "23"),        # D-pad up-down / left-right
        0xE06A: keys_row(a(0xE06A), "243"),                                          # D-pad left-down-right
    }
    return new


# glyphs the game never draws (not in any message string): emptied only if the font would not fit otherwise
SPARE = [0xE048, 0xE04A, 0xE066, 0xE069, 0xE083, 0xE084, 0xE067, 0xE06B, 0xE06C, 0xE06D, 0xE06E, 0xE06F, 0xE070]


def build(out_path, blank=()):
    f = TTFont(os.path.join(FONTS, "External.otf")); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    adv_of = lambda cp: f["hmtx"][cmap[cp]][0]
    new = glyph_map(adv_of)
    for cp in blank:
        if cp in cmap: new[cp] = []
    cff = f["CFF "].cff; td = cff.topDictIndex[0]; cs_index = td.CharStrings
    for cp, cs in new.items():
        g = cmap[cp]; pen = T2CharStringPen(gs[g].width, gs)
        for c in cs: BF.replay(c, pen)
        cs_index[g] = pen.getCharString(private=td.Private, globalSubrs=cff.GlobalSubrs)
    f.save(out_path)
    return new


def subset_font(src, dst):
    o = subset.Options(); o.name_IDs = ["*"]; o.glyph_names = False; o.notdef_outline = True; o.hinting = False
    f = subset.load_font(src, o); s = subset.Subsetter(o); s.populate(unicodes=list(f.getBestCmap().keys())); s.subset(f)
    subset.save_font(f, dst, o)
    return os.path.getsize(dst)


def build_fitting(out_dir):
    """build, subset to the mapped code points, and empty unused glyphs one at a time until it fits MAX_OTF"""
    raw = os.path.join(out_dir, "External_kbm.otf"); fin = os.path.join(out_dir, "External_kbm_subset.otf")
    blank = []
    while True:
        build(raw, blank); size = subset_font(raw, fin)
        print("glyph blanks:", [hex(c) for c in blank], "-> subset", size, "bytes (limit", MAX_OTF, ")")
        if size <= MAX_OTF: return fin, size, blank
        if len(blank) >= len(SPARE): raise SystemExit("font does not fit even after emptying the spare glyphs")
        blank.append(SPARE[len(blank)])


def preview(otf, path):
    from PIL import Image, ImageDraw, ImageFont
    cps = [0xE040, 0xE041, 0xE042, 0xE043, 0xE044, 0xE045, 0xE046, 0xE047, 0xE049, 0xE04B, 0xE04C, 0xE050, 0xE052, 0xE058, 0xE05A,
           0xE054, 0xE05C, 0xE05E, 0xE05F, 0xE057, 0xE051, 0xE053, 0xE059, 0xE05B, 0xE055, 0xE05D, 0xE068, 0xE060, 0xE061, 0xE062,
           0xE063, 0xE064, 0xE065, 0xE06A, 0xE056, 0xE048]
    cell, cols = 130, 12; rows = (len(cps) + cols - 1) // cols
    im = Image.new("RGB", (cell * cols, (cell + 16) * rows), (44, 44, 48)); d = ImageDraw.Draw(im)
    fnt = ImageFont.truetype(otf, 92); lab = ImageFont.load_default()
    for i, cp in enumerate(cps):
        x, y = (i % cols) * cell, (i // cols) * (cell + 16)
        d.text((x + 6, y + 4), chr(cp), font=fnt, fill=(255, 255, 255)); d.text((x + 4, y + cell), "%04X" % cp, font=lab, fill=(255, 200, 80))
    im.save(path)


if __name__ == "__main__":
    fin, size, blank = build_fitting(OUT)
    preview(fin, os.path.join(PREVIEW, "font_preview.png"))
    print("ok:", fin, size, "bytes; preview work/preview/font_preview.png")
