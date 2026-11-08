# OOT (Switch 2): keyboard and mouse on Lichii

Play *OOT* (Nintendo Switch 2, title ID `0400486024DEC000`) on **Lichii** (an Eden/yuzu fork) with a **keyboard and mouse**: the mouse turns the camera and attacks, WASD moves, and the game's interface shows the matching keys instead of controller buttons.

| Part | What it does | Needs a rebuilt Lichii? |
|---|---|---|
| **Input profile** (`profile/`) | WASD, mouse as the right stick, mouse buttons, action keys | no |
| **Icon mod** (`ButtonPrompts-KeyboardMouse`) | replaces the button icons, the HUD buttons, the ocarina song-sheet notes and the "Basic Controls" screen with keyboard and mouse art | no |
| **Lichii patches** (`lichii-patches/`) | mouse acceleration; mouse panning turns on by itself and the cursor hides; a "Keyboard and mouse" option for the icons | yes (optional) |
| **Tools** (`tools/`) | build the mod from **your own** `.nup`, so you can change the keys and redo the icons | no |

> The patches are not part of any prebuilt Lichii release. If you do not compile the emulator yourself, skip them: the profile and the icon mod work on any build (tested on Fritchii v4), you just press **Ctrl+F9** once at every launch for mouse panning, with **"Hide mouse on inactivity"** enabled to hide the cursor. With an unpatched build the `ButtonPrompts-KeyboardMouse` folder is applied as an ordinary mod, so keep it as the only `ButtonPrompts-*` folder.

> Fan project, not affiliated with Nintendo or with Lichii/Eden. Read the [NOTICE](NOTICE.md).

## Default keys

| In-game action | Switch | Keyboard / mouse |
|---|---|---|
| Move | left stick | **W A S D** (hold **Z** to walk slowly) |
| Rotate Camera | right stick | **move the mouse** |
| Reset Camera (Press) | press the right stick | **middle click** |
| Attack | Y | **left click** |
| Use Item | ZR | **right click** |
| Target | ZL | **Shift** (hold) |
| Actions / Dash (Hold) | A | **Space** |
| (no label in game) | B | **C** |
| (no label in game) | X | **R** |
| Quick Select Items | L / R | **Q / E** |
| Toggle Accessory / Play Ocarina / Talk to Navi / Toggle Boots | D-pad up / left / right / down | **1 / 2 / 3 / 4** |
| Open Menu | + | **Enter** |
| Open Map | − | **Tab** |

Ctrl and Alt are not used on purpose: in Lichii, Ctrl+Q quits the emulator and Alt opens the menu bar. B and X have no text on the game's controls screen, so check in game what they do.

## Quick install

Close Lichii first. There are 6 short steps.

**Step 1 – Download two files**

- The mod: open the [latest release](../../releases/latest), scroll down to **Assets** and click `OoT-ButtonPrompts-KeyboardMouse.zip`.
- The keys file: [OoT-Keyboard-Mouse.ini](https://github.com/exgde/oot-lichii-keyboard-mouse/raw/main/profile/OoT-Keyboard-Mouse.ini). Right-click the link → **Save link as…**

**Step 2 – Open the game's mod folder**

Open Lichii, right-click the game (OOT) in the game list and click **Open Mod Data Location**. A Windows folder opens (its name ends in `0400486024DEC000`). Leave it open.

**Step 3 – Add the icons**

1. Right-click the zip you downloaded → **Extract All**.
2. Open the extracted folder and drag the folder **`ButtonPrompts-KeyboardMouse`** into the folder from Step 2.
3. Check: inside `0400486024DEC000` there is now `ButtonPrompts-KeyboardMouse`, and inside it a folder called `romfs`. If other folders there start with `ButtonPrompts-`, move them out.

**Step 4 – Add the keys file**

1. Go up two folders, to the one that contains `load` (in the address bar at the top, click the name just before `load`; it is usually `user`).
2. Open `config`, then `input`. If `input` does not exist, create it (right-click → **New** → **Folder**, name it `input`).
3. Put `OoT-Keyboard-Mouse.ini` there.

When you are done the folders look like this:

```
user
├─ load
│  └─ 0400486024DEC000
│     └─ ButtonPrompts-KeyboardMouse     ← Step 3
└─ config
   └─ input
      └─ OoT-Keyboard-Mouse.ini          ← Step 4
```

**Step 5 – Load the keys in Lichii**

1. Open Lichii and click **Emulation → Configure → Controls**.
2. Pick **Player 1** and make sure the type is **Pro Controller**.
3. In the **Profile** box choose **OoT-Keyboard-Mouse**, click **Load**, then **OK**.

This replaces your current Player 1 layout. To keep a gamepad layout, click **New** in the Profile box and save it under a name before loading.

**Step 6 – Play (repeat this every time you open the game)**

1. Start the game and wait until you can move the green hat kid.
2. **Click once on the game window.**
3. Press **Ctrl + F9** one time.
4. Move the mouse: the camera turns and the cursor disappears after a few seconds.

Ctrl+F9 works like a switch, so press it only once. If the cursor came back, press it again.

**Not working?**

- Cursor still visible: click the game window, press Ctrl+F9 once, and check that **Emulation → Configure → General → UI → Hide mouse on inactivity** is ticked.
- Icons still look like the Switch: check the folders against the picture above, then close and reopen the game.

More help: [docs/INSTALLATION.md](docs/INSTALLATION.md) and [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## Change keys, sensitivity and acceleration

Everything is in [docs/CONFIGURATION.md](docs/CONFIGURATION.md): how to rebind each key (in the UI or by editing the profile), the key-code table, what every sensitivity control does with suggested values, and how to redo the icons if you change the layout.

## Documentation

- [Installation](docs/INSTALLATION.md)
- [Configuration: keys, sensitivity, acceleration](docs/CONFIGURATION.md)
- [Key mapping](docs/KEY-MAPPING.md)
- [Build the mod from your own game](docs/BUILD-THE-MOD.md)
- [Lichii patches](lichii-patches/README.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Changelog](CHANGELOG.md)

## License

Tools, profile and documentation: MIT ([LICENSE](LICENSE)). The Lichii patches are derived from Eden/yuzu and follow GPL-3.0-or-later. The texture and font files inside the release are derived from the game and remain Nintendo's property: use them only with a copy you own.
