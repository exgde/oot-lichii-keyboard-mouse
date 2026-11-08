"""Extracts from YOUR OOT (Switch 2) .nup only what the generator needs, into tools/work (not tracked by git):
  work/ZsDic.pack.zs         the game's zstd dictionaries (the game's .zs files use one of them)
  work/Common.bntx           UI textures (decompressed, ~244 MB)
  work/fonts/External.bfotf  container of the button-icon font (decompressed, still obfuscated)
  work/fonts/External.otf    the same font, de-obfuscated
  work/fonts/Nin-ZeldaGlyphs-v3-Plain.otf   font of the letters/digits used on the keys
usage: python extract_game_files.py <game.nup>
The game files are never uploaded anywhere; you need the game (your own dump)."""
import os, sys
import zstandard
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nup_tool
import glyphlib
from oot_paths import WORK, FONTS

WANT = {
    "ZsDic": "romfs/Pack/ZsDic.pack.zs",
    "External": "romfs/Font2/Scalable/External.Nin_Ounce_NVN2.bfotf.zs",
    "ZeldaGlyphs": "romfs/Font2/Scalable/Nin-ZeldaGlyphs-v3-Plain.Nin_Ounce_NVN2.bfotf.zs",
    "Common": "romfs/UI/Layout2Archive/Common.Product.100.Nin_Ounce_NVN2.bntx.zs",
}


def find(entries, suffix):
    """entries '<package>/romfs/...': if a file exists in both the base package and the update, the newer one wins"""
    hits = [(p, i) for p, i in entries if p.endswith("/" + suffix)]
    if not hits:
        raise SystemExit("could not find %s inside the .nup (is it really OOT 0400486024DEC000?)" % suffix)
    return max(hits, key=lambda h: int(h[0].split("_v")[1].split("_")[0]))


def main(nup):
    f, pkgs, dirs, files, children, dc = nup_tool.parse(nup)
    entries = []
    for p in pkgs:
        tag = "pkg%x_v%d_k%d" % (p["tid"], p["ver"], p["kind"])
        for kind in ("exefs", "romfs"):
            if p[kind] != 0xFFFFFFFF:
                nup_tool.walk(dirs, files, children, dc, p[kind], tag + "/" + kind + "/", entries)
    got = {}
    for key, suffix in WANT.items():
        path, idx = find(entries, suffix)
        got[key] = nup_tool.read_member(f, files[idx]); print("extracted:", path, len(got[key]), "bytes")
    open(os.path.join(WORK, "ZsDic.pack.zs"), "wb").write(got["ZsDic"])
    os.environ["ZSDIC"] = os.path.join(WORK, "ZsDic.pack.zs")
    import zs                                              # only now: it reads ZSDIC
    cont = zs.decompress(got["External"]); open(os.path.join(FONTS, "External.bfotf"), "wb").write(cont)
    open(os.path.join(FONTS, "External.otf"), "wb").write(glyphlib.decrypt_bfotf(cont))
    zg = glyphlib.decrypt_bfotf(zs.decompress(got["ZeldaGlyphs"])); open(os.path.join(FONTS, "Nin-ZeldaGlyphs-v3-Plain.otf"), "wb").write(zg)
    bntx = zs.decompress(got["Common"]); open(os.path.join(WORK, "Common.bntx"), "wb").write(bntx)
    print("bntx %d bytes, External font %d bytes (container), Zelda glyphs %d bytes" % (len(bntx), len(cont), len(zg)))
    assert bntx[:4] == b"BNTX", bntx[:4]
    f.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
