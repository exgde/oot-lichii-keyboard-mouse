# Build the mod from your own game

The tools read **your** OOT `.nup`, extract only what they need (the icon font, the interface textures and the compression dictionaries) into `tools/work/`, and assemble the `ButtonPrompts-KeyboardMouse` folder. Nothing from the game goes into git (see `.gitignore`).

## Requirements

- Python 3.10 or newer
- `pip install -r tools/requirements.txt` (numpy, Pillow, fonttools, zstandard, texture2ddecoder, astc-encoder-py)
- the game's `.nup` (`OOT [0400486024dec000][v131072].nup`)

## One command

```
cd tools
python build_mod.py --nup "C:\path\OOT [0400486024dec000][v131072].nup" --out output
```

It takes a few minutes (the 244 MB texture file is recompressed). At the end it prints `ALL OK` and the folder `output\ButtonPrompts-KeyboardMouse`. Copy it to `<Lichii>\user\load\0400486024DEC000\` ([INSTALLATION.md](INSTALLATION.md)).

Options: `--skip-extract` reuses what is already in `tools/work/`. The environment variables `OOT_WORK` (working folder) and `OOT_ASSETS` (pictures) change the locations.

## What changes in the game

| Game file | What the mod replaces |
|---|---|
| `Font2/Scalable/External.Nin_Ounce_NVN2.bfotf.zs` | the button glyphs used in texts (A, B, X, Y, L, R, ZL, ZR, +, −, D-pad, sticks) become keys and mouse icons |
| `UI/Layout2Archive/Common.Product.100.Nin_Ounce_NVN2.bntx.zs` | 17 textures: `KeyTexFont{A,B,X,Y}_00` (HUD letters), `OcarinaButton{A,B,X,Y,L,R}_00` (song-sheet notes), `Controller_Pro` and `Controller_Pro1` (the picture on the "Basic Controls" screen) and `ControllerGuide_Pro_00..04` (the guide lines) |

Both files keep **exactly the same decompressed size** as the originals, because the game stores sizes in an RSTB. `verify_mod.py` checks this.

## Redo the icons after changing the keys

| File | What to edit |
|---|---|
| `build_fonts_kbm.py` → `glyph_map` | which key/icon each game glyph shows (`key(adv, "R")` draws the R key; `mouse(..., press="L")` the mouse with the left button) |
| `build_mods_kbm.py` → `symbols` | the drawing of the HUD buttons and ocarina notes (A, B, X, Y, L, R) |
| `make_ctrl_kbm.py` → `KEY`, `WASD_BOX`, `NUM_BOX`, `MOUSE_PT` and `build_sheets` | where the lines on the "Basic Controls" screen point (positions on the keyboard/mouse picture) |

The game's font has a size limit (14,560 bytes). `build_fonts_kbm.py` prints the size and fails if it does not fit.

## The keyboard and mouse art

`tools/assets/keyboard.png` (570×244, dark keys on a white background) and `mouse.png` (271×419, grey mouse seen from above) are drawn by `draw_default_art.py` when they do not exist. To use other pictures, put them there with the **same key layout** (ANSI, same boxes) or adjust `KEY`, `WASD_BOX`, `NUM_BOX` and `MOUSE_PT` in `make_ctrl_kbm.py`. The release uses art made from two pictures supplied by the author, so it looks slightly different from the default art generated here.

## Preview without writing anything

`python make_ctrl_kbm.py` writes `tools/work/preview/preview_KeyboardMouse.png` (the controls screen with the lines over the game's background) and `python build_fonts_kbm.py` writes `font_preview.png` (every glyph). Neither touches the game.

## Included tools

| File | Purpose |
|---|---|
| `build_mod.py` | runs everything |
| `extract_game_files.py`, `nup_tool.py` | read the `.nup` and extract the files |
| `zs.py` | decompress/compress the `.zs` files (zstd with the game's dictionaries) |
| `ctrl_common.py`, `tex_build.py` | read and write BC4/ASTC textures in the NX2 layout inside the `.bntx` |
| `glyphlib.py`, `build_fonts_kbm.py` | the icon font and the `.bfotf` container cipher |
| `ctrllib.py`, `make_ctrl_kbm.py`, `draw_default_art.py` | the controls-screen picture and lines |
| `build_mods_kbm.py`, `verify_mod.py` | assemble the mod folder and check it |
