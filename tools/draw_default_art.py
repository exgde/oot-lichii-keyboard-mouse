"""Draws the default keyboard (ANSI, 570x244) and mouse (271x419) art used on the "Basic Controls" screen.
The key boxes are the same ones make_ctrl_kbm.py uses to aim the guide lines; if you put other pictures in tools/assets/,
keep the same layout (or adjust KEY / WASD_BOX / NUM_BOX / MOUSE_PT in make_ctrl_kbm.py).
  python draw_default_art.py [folder]   -> writes keyboard.png and mouse.png (only if missing, unless --force)"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

# (y0, y1, [(x0, x1, label)...])
ROWS = [
    (22, 40, [(17, 49, "Esc"), (56, 88, "F1"), (95, 127, "F2"), (133, 166, "F3"), (172, 204, "F4"), (211, 243, "F5"),
              (250, 282, "F6"), (288, 321, "F7"), (327, 359, "F8"), (366, 398, "F9"), (405, 437, "F10"), (443, 475, "F11"),
              (482, 514, "F12"), (521, 553, "PrtSc")]),
    (46, 76, [(17, 47, "~"), (55, 85, "1"), (92, 122, "2"), (130, 159, "3"), (167, 197, "4"), (205, 234, "5"), (242, 272, "6"),
              (280, 309, "7"), (317, 347, "8"), (354, 384, "9"), (392, 422, "0"), (429, 459, "-"), (467, 497, "="),
              (504, 553, "Backspace")]),
    (82, 112, [(17, 66, "Tab"), (74, 103, "Q"), (111, 141, "W"), (148, 178, "E"), (186, 216, "R"), (223, 253, "T"),
               (261, 291, "Y"), (298, 328, "U"), (336, 365, "I"), (373, 403, "O"), (411, 440, "P"), (448, 478, "["),
               (486, 515, "]"), (523, 553, "\\")]),
    (118, 148, [(17, 79, "Caps"), (86, 116, "A"), (124, 153, "S"), (161, 191, "D"), (198, 228, "F"), (236, 266, "G"),
                (273, 303, "H"), (311, 340, "J"), (348, 378, "K"), (386, 415, "L"), (423, 453, ";"), (461, 490, "'"),
                (498, 553, "Enter")]),
    (154, 184, [(17, 97, "Shift"), (104, 134, "Z"), (142, 171, "X"), (179, 209, "C"), (217, 246, "V"), (254, 284, "B"),
                (292, 321, "N"), (329, 359, "M"), (366, 396, ","), (404, 434, "."), (441, 471, "/"), (479, 553, "Shift")]),
    (190, 226, [(17, 47, "Ctrl"), (55, 84, ""), (92, 122, "Fn"), (130, 172, "Alt"), (179, 359, ""), (367, 409, "Alt"),
                (416, 446, "Ctrl")]),
]
ARROWS = [(452, 210, 482, 226, "<"), (488, 190, 518, 206, "^"), (488, 210, 518, 226, "v"), (523, 210, 553, 226, ">")]
KEY_FILL, KEY_TEXT = (35, 31, 32), (255, 255, 255)


def _font(size):
    try:
        return ImageFont.load_default(size=size)       # Pillow >= 10.1: built-in vector font
    except TypeError:
        return ImageFont.load_default()


def keyboard():
    im = Image.new("RGB", (570, 244), (255, 255, 255)); d = ImageDraw.Draw(im)
    for y0, y1, keys in ROWS:
        for x0, x1, label in keys:
            d.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=KEY_FILL)
            if label:
                size = 10 if len(label) > 2 else 15
                if y1 - y0 < 20:
                    size = 9
                f = _font(size); bb = d.textbbox((0, 0), label, font=f)
                d.text(((x0 + x1) / 2 - (bb[0] + bb[2]) / 2, (y0 + y1) / 2 - (bb[1] + bb[3]) / 2), label, font=f, fill=KEY_TEXT)
    for x0, y0, x1, y1, ch in ARROWS:
        d.rounded_rectangle((x0, y0, x1, y1), radius=3, fill=KEY_FILL)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        tri = {"<": [(cx + 4, cy - 5), (cx + 4, cy + 5), (cx - 4, cy)], ">": [(cx - 4, cy - 5), (cx - 4, cy + 5), (cx + 4, cy)],
               "^": [(cx - 5, cy + 3), (cx + 5, cy + 3), (cx, cy - 4)], "v": [(cx - 5, cy - 3), (cx + 5, cy - 3), (cx, cy + 4)]}[ch]
        d.polygon(tri, fill=KEY_TEXT)
    return im


def mouse():
    im = Image.new("RGB", (271, 419), (255, 255, 255)); d = ImageDraw.Draw(im)
    body, ink = (140, 140, 140), (52, 52, 52)
    d.rounded_rectangle((36, 81, 223, 390), radius=92, fill=body, outline=ink, width=3)
    d.line([(135, 84), (135, 208)], fill=ink, width=3)                      # button divider
    d.arc((38, 150, 222, 270), 215, 325, fill=ink, width=3)                  # base of the buttons (slight curve)
    d.line([(60, 213), (210, 213)], fill=ink, width=3)
    d.rounded_rectangle((122, 108, 148, 152), radius=11, fill=(72, 72, 72), outline=(34, 34, 34), width=2)   # wheel
    return im


def ensure(kb_path, ms_path, force=False):
    for path, make in ((kb_path, keyboard), (ms_path, mouse)):
        if force or not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True); make().save(path); print("default art:", path)


if __name__ == "__main__":
    from oot_paths import ASSETS
    out = next((a for a in sys.argv[1:] if not a.startswith("--")), ASSETS)
    ensure(os.path.join(out, "keyboard.png"), os.path.join(out, "mouse.png"), "--force" in sys.argv)
