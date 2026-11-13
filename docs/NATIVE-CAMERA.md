# Native camera: how it works

With `mouse_camera = native` (or **Native** in the program) the mouse turns the camera **1:1**: the same hand movement always gives the same turn, slow or fast, at any frame rate. With `stick` (the default) the mouse only pretends to be the right stick, so the game's stick curve and top speed apply.

## Using it

1. Switch it on: in the program, **Mouse and camera → Native**, then **Apply**; or in `OoT-Keyboard-Mouse-Settings.ini` set `mouse_camera = native` and run `Apply-Settings.bat`.
2. Every time you play: open **`OoT-MouseCapture.exe`** (in Lichii's data folder), start the game, click the picture and press **Ctrl+F9** once.
3. Speed: `mouse_sens` (or the speed slider). `5.0` = 0.06° per mouse count, about 15 cm of mouse for a full turn at 1600 DPI. `mouse_sens_x` / `mouse_sens_y` set each direction, `mouse_invert_y` flips up/down. The speed does not depend on the window size.

The game keeps its own limits: how far up and down you can look, and the slow return of the camera behind the green hat kid after the mouse rests for a while, exactly as with the stick.

## The three parts

**1. Lichii gives the game the real mouse.** `Apply-Settings` sets Lichii's `mouse_enabled = true`. The game already initialises and reads the mouse itself (its engine calls `nn::hid::InitializeMouse` and `GetMouseStates`), it just never uses it for the camera. `Apply-Settings` also unbinds the right stick, because with `mouse_enabled` Lichii turns "mouse moved while a button is held" into right-stick input, so attacking would move the camera.

**2. A small game patch uses it** (`MouseCamera-Native`, an IPS file for main build `E0F3CCFAF50065AE…`). It replaces one instruction in the player camera update (module offset `0x625370`), right where the game has turned the right stick into this frame's turn in degrees, and adds the mouse movement read through `GetMouseStates`. The game then takes its normal "turned by hand" path, so everything else (pitch limits, collisions, auto-return) stays the game's own. The code lives in unused space after the game's code. `Apply-Settings` writes your speed into the patch (after the marker `OOTMCAM1`) and renames it to `.ips.off` when you go back to `stick`.

**3. `OoT-MouseCapture.exe` keeps the pointer in the picture.** Lichii hands the game the pointer *position*, so on its own the camera would stop at the edge of the window. While the game is in front and the pointer is over the picture, the helper:

- moves the pointer back by exactly 512 (left/right) or 384 (up/down) game pixels whenever it gets half of that from the middle, like a clock hand going from 12 to 1. The patch undoes any jump of exactly that size, so the camera never sees it, however fast the mouse moves;
- turns off Windows *Enhance pointer precision* (mouse acceleration) and sets the pointer speed so that one mouse count is one pixel of the game's 1280×720 picture, which makes the camera follow the hand exactly at any window size.

It never hides, clips or locks the pointer (Lichii hides it after Ctrl+F9), and it changes nothing permanently: the Windows settings come back as soon as the game loses focus or closes, and if it ever crashes, its next start puts them back.

## Building

- Patch: `native-camera/patch/build_native_camera_ips.py` (LLVM clang + ld.lld) writes `native-camera/MouseCamera-Native/exefs/<build id>.ips`; `--main <decompressed main as ELF>` checks the replaced instruction first. `test_cave.c` tests the mouse logic on the PC.
- Helper: `native-camera/helper/build.bat` (Visual Studio C compiler).
- `WRAP_X` / `WRAP_Y` in `cave.c` and `MC_WRAP_X` / `MC_WRAP_Y` in `mouse_capture.h` must match.
