"""Builds the ButtonPrompts-KeyboardMouse mod from YOUR .nup, in one command:

    python build_mod.py --nup "C:/path/OOT [0400486024dec000][v131072].nup" --out output

Steps: (1) extracts fonts, textures and dictionaries from the .nup into tools/work; (2) draws the default keyboard and mouse art
if tools/assets is empty; (3) builds output/ButtonPrompts-KeyboardMouse; (4) checks sizes and content.
Then just copy the folder to  <Lichii>/user/load/0400486024DEC000/  (see docs/INSTALLATION.md)."""
import argparse, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))


def run(*args):
    print("\n>>", " ".join(args), flush=True)
    subprocess.run([sys.executable, *args], cwd=HERE, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nup", required=True, help="the OOT (Switch 2) .nup")
    ap.add_argument("--out", required=True, help="folder where ButtonPrompts-KeyboardMouse is created")
    ap.add_argument("--skip-extract", action="store_true", help="reuse tools/work if it was already extracted")
    a = ap.parse_args()
    out = os.path.abspath(a.out); os.makedirs(out, exist_ok=True)
    if not a.skip_extract:
        run("extract_game_files.py", os.path.abspath(a.nup))
    run("draw_default_art.py")
    run("build_mods_kbm.py", out)
    run("verify_mod.py", out)
    print("\nDone:", os.path.join(out, "ButtonPrompts-KeyboardMouse"))


if __name__ == "__main__":
    main()
