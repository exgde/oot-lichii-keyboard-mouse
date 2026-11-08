# Installation

For Lichii "build 116" (an Eden fork) and OOT for Switch 2, version 2.0.0 (`[0400486024dec000][v131072].nup`). In portable mode the folders below live in `user\` next to `lichii.exe`; otherwise use **right-click the game → Open Mod Data Location** and the emulator's own config folder.

## 1. The icon mod

Get the `ButtonPrompts-KeyboardMouse` folder in **one** of these ways:

- **Release:** download `OoT-ButtonPrompts-KeyboardMouse.zip` from [Releases](../../releases) and extract it.
- **From your game:** `python tools/build_mod.py --nup "<your .nup>" --out output` ([BUILD-THE-MOD.md](BUILD-THE-MOD.md)). Use this if you change the keys.

Copy the folder to:

```
<Lichii>\user\load\0400486024DEC000\ButtonPrompts-KeyboardMouse\romfs\Font2\...
<Lichii>\user\load\0400486024DEC000\ButtonPrompts-KeyboardMouse\romfs\UI\...
```

**Important:** keep only **one** `ButtonPrompts-*` folder in `load` (PlayStation, Xbox, Steam Deck, Keyboard…). On a Lichii without the patches every `ButtonPrompts-*` folder is applied as an ordinary mod, and with two of them the last one alphabetically wins. Move the others out of `load`.

On a Lichii **with the patches** ([lichii-patches](../lichii-patches/README.md)) all the `ButtonPrompts-*` folders can stay, and you choose in **Graphics → Advanced → "OOT: button icons" = Keyboard and mouse**.

## 2. The input profile

1. Copy `profile/OoT-Keyboard-Mouse.ini` to `<Lichii>\user\config\input\` (create the `input` folder if it does not exist).
2. **Emulation → Configure → Controls → Player 1** (Pro Controller type): under **Profile** pick `OoT-Keyboard-Mouse`, click **Load**, then **OK**.

This writes the layout into `qt-config.ini`. If you were using a gamepad (DualSense etc.) its layout is replaced: keep a copy of your `qt-config.ini` first, or save a profile of your gamepad layout (**New**) so you can switch back.

## 3. Mouse panning (camera)

Without the patches the mouse only acts as the right stick while **mouse panning** is on, and it is **not saved**: press **Ctrl+F9** every time you start the game (it toggles). The cursor only hides if **"Hide mouse on inactivity"** (Configure → General → UI) is enabled.

With the patches, mouse panning turns on by itself when player 1's right stick is mapped to the mouse, and the cursor hides immediately. Ctrl+F9 still toggles it.

## 4. Check it works

- In the emulator log (`user\log\eden_log.txt`) look for: `LayeredFS layer 'ButtonPrompts-KeyboardMouse'`.
- In game: the action button shows a key (Space), the attack button shows a mouse with the left button filled, and **+ → Basic Controls** shows a keyboard and a mouse with guide lines to each key.
- Move the mouse: the camera turns and no cursor is visible.

## Uninstall

Delete the `ButtonPrompts-KeyboardMouse` folder from `load`, restore your gamepad layout in **Emulation → Configure → Controls**, and restart the game.

## Cautions

- Edit `qt-config.ini` **only while Lichii is closed**: the emulator rewrites the file when it exits and discards manual edits.
- The mod's files have exactly the same size as the originals (the game keeps file sizes in an RSTB): do not re-save them with other tools.
