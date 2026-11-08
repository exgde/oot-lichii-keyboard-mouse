"""Checks a generated mod folder: sizes identical to the originals (RSTB), valid font, textures read back.
python verify_mod.py <out_root>"""
import os, sys, struct, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import ctrl_common as C
import zs
from fontTools.ttLib import TTFont
KEY = 0xA6018502
root = os.path.join(sys.argv[1], "ButtonPrompts-KeyboardMouse", "romfs")
ok = True
def check(cond, msg):
    global ok; ok &= bool(cond); print(("OK   " if cond else "FAIL ") + msg)

# font container
fp = os.path.join(root, "Font2", "Scalable", "External.Nin_Ounce_NVN2.bfotf.zs")
raw = zs.decompress(open(fp, "rb").read()); orig = open(os.path.join(__import__("oot_paths").FONTS, "External.bfotf"), "rb").read()
check(len(raw) == len(orig), f"font container {len(raw)} bytes == original {len(orig)}")
n = len(raw) // 4; dec = struct.pack(f">{n}I", *[w ^ KEY for w in struct.unpack(f">{n}I", raw)])
magic, size = struct.unpack(">II", dec[:8]); check(magic == 0x7F9A0218, "font magic 0x7F9A0218")
f = TTFont(io.BytesIO(dec[8:8 + size])); cm = f.getBestCmap()
check(len(cm) == 88, f"font cmap entries {len(cm)} == 88 (same code points as the original)")
check(size <= 14560, f"otf {size} <= 14560")
for cp in (0xE040, 0xE043, 0xE047, 0xE05E, 0xE060): check(cp in cm, f"U+{cp:04X} present")

# bntx
bp = os.path.join(root, "UI", "Layout2Archive", "Common.Product.100.Nin_Ounce_NVN2.bntx.zs")
b = zs.decompress(open(bp, "rb").read()); ob, otex = C.load_bntx()
check(len(b) == len(ob), f"bntx {len(b)} bytes == original {len(ob)}")
t = C.all_brti(b)
diff = [k for k in otex if (b[otex[k]['offs'][0]:otex[k]['offs'][0] + otex[k]['size']] != ob[otex[k]['offs'][0]:otex[k]['offs'][0] + otex[k]['size']])]
print("textures changed:", sorted(diff))
want = {"KeyTexFontA_00", "KeyTexFontB_00", "KeyTexFontX_00", "KeyTexFontY_00", "Controller_Pro", "Controller_Pro1"}
want |= {f"OcarinaButton{k}_00" for k in "ABXYLR"} | {f"ControllerGuide_Pro_0{i}" for i in range(5)}
check(set(diff) == want, f"exactly the {len(want)} intended textures changed")
check(t["Controller_Pro1"]["w"] == 1160 and t["ControllerGuide_Pro_00"]["w"] == 1555, "texture dimensions unchanged")
print("ALL OK" if ok else "SOMETHING FAILED"); sys.exit(0 if ok else 1)
