# Installation

Step-by-step guide. It takes about five minutes. You need:

- **Lichii** (or a Lichii fork such as Fritchii) for Windows, closed while you copy files.
- *OOT* for Switch 2, version 2.0.0 (`[0400486024dec000][v131072].nup`), already working in the emulator.
- `OoT-ButtonPrompts-KeyboardMouse.zip` from [Releases](../../releases) (or your own build, see [BUILD-THE-MOD.md](BUILD-THE-MOD.md)).

Tested on Fritchii v4 and on a locally built Lichii "build 116".

## 0. Find your Lichii data folder

Below, `<Lichii>` means the folder that holds `lichii.exe`.

- If there is a **`user`** folder next to `lichii.exe`, that is where everything goes (`<Lichii>\user\...`). This is portable mode and the usual case.
- If not, use the emulator itself: **right-click the game → Open Mod Data Location**. That opens `...\load\0400486024DEC000`, the folder used in step 1. The config folder is two levels up, then `config`.

## 1. Install the icon mod

1. Extract the zip. Inside is a folder named **`ButtonPrompts-KeyboardMouse`**.
2. Copy that whole folder into:

   ```
   <Lichii>\user\load\0400486024DEC000\
   ```

3. Check the result. The tree must look exactly like this (two folders inside `romfs`, not more, not fewer levels):

   ```
   <Lichii>\user\load\0400486024DEC000\
   └── ButtonPrompts-KeyboardMouse\
       └── romfs\
           ├── Font2\Scalable\External.Nin_Ounce_NVN2.bfotf.zs
           └── UI\Layout2Archive\Common.Product.100.Nin_Ounce_NVN2.bntx.zs
   ```

4. **Keep only one `ButtonPrompts-*` folder** in `0400486024DEC000` (move any PlayStation, Xbox or Steam Deck button-prompt mods somewhere else). Two of them replace the same game files and only one wins.

## 2. Install the input profile

1. Copy `profile\OoT-Keyboard-Mouse.ini` (from this repository) into `<Lichii>\user\config\input\`. Create the `input` folder if it does not exist.
2. Open Lichii, then **Emulation → Configure → Controls → Player 1**.
3. Make sure the controller type is **Pro Controller**.
4. In the **Profile** box choose `OoT-Keyboard-Mouse` and click **Load**, then **OK**.

This overwrites your Player 1 layout. If you use a gamepad, first save its layout as a profile (**New**) or keep a copy of `user\config\qt-config.ini`.

## 3. Check the cursor setting

**Emulation → Configure → General → UI**: tick **Hide mouse on inactivity** (it is on by default). Click **OK**.

## 4. Start the game and turn on mouse panning (every launch)

The mouse only turns the camera while **mouse panning** is on, and Lichii does not remember it: it is off every time the emulator starts. So, each time:

1. Start the game and wait until you are in the game (the first launch builds shaders and can take several minutes).
2. **Click on the game window** so the emulator is the window in front.
3. Press **Ctrl+F9** once.

Now moving the mouse turns the camera, and after a few seconds without moving it the cursor disappears.

- Ctrl+F9 **toggles**. Pressing it a second time turns panning off and the cursor comes back. If that happens, press it again.
- Ctrl+F9 only works when the emulator window is in front. If another window has focus the key goes to that window instead.
- A Lichii compiled with the [patches](../lichii-patches/README.md) does steps 2–3 by itself (panning on, cursor hidden). Official and prebuilt builds do not have them.

## 5. Check that it works

In game:

- Moving the mouse turns the camera and no cursor is visible.
- WASD moves the green hat kid, left click attacks, right click uses the item.
- The action button shows a key (Space) and the attack button shows a mouse with the left button filled.
- **Enter → Basic Controls** shows a keyboard and a mouse with guide lines to each key.

If you see Switch or PlayStation buttons instead, the icon mod is not loaded: see [TROUBLESHOOTING.md](TROUBLESHOOTING.md). The log (`user\log\eden_log.txt`) of some builds prints `LayeredFS layer 'ButtonPrompts-KeyboardMouse'`; others only print `LayeredFS patches applied successfully`, so the in-game check above is the one to trust.

## Uninstall

Delete the `ButtonPrompts-KeyboardMouse` folder from `load\0400486024DEC000`, restore your gamepad layout in **Emulation → Configure → Controls**, and restart the game.

## Cautions

- Edit `qt-config.ini` **only while Lichii is closed**: the emulator rewrites the file when it exits and discards manual edits.
- The mod's files have exactly the same size as the originals (the game keeps file sizes in an RSTB): do not re-save them with other tools.
