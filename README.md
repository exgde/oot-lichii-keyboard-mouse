# OOT (Switch 2): keyboard and mouse on Lichii

Play *OOT* (Nintendo Switch 2, title ID `0400486024DEC000`) on **Lichii** (an Eden/yuzu fork) with a **keyboard and mouse**: the mouse turns the camera and attacks, WASD moves, and the game's interface shows the matching keys instead of controller buttons.

**Download:** open the [latest release](../../releases/latest) and click **`OoT-KeyboardMouse-v1.3.0.zip`** under **Assets**. It has everything. Then follow [Download and install](#download-and-install) (5 steps). Keys and mouse speed are set in [one text file](#change-keys-and-mouse-speed).

| Part | What it does | Needs a rebuilt Lichii? |
|---|---|---|
| **Settings file** (`settings/`) | one plain-text `.ini` for every key and the mouse speed, plus `Apply-Settings.bat` that writes it into Lichii (also builds the input profile) | no |
| **Icon mod** (`ButtonPrompts-KeyboardMouse`) | replaces the button icons, the HUD buttons, the ocarina song-sheet notes and the "Basic Controls" screen with keyboard and mouse art | no |
| **Lichii patches** (`lichii-patches/`) | mouse acceleration; mouse panning turns on by itself and the cursor hides; a "Keyboard and mouse" option for the icons | yes (optional) |
| **Tools** (`tools/`) | build the mod from **your own** `.nup`, so you can change the keys and redo the icons | no |

> The patches are not part of any prebuilt Lichii release. If you do not compile the emulator yourself, skip them: the settings file and the icon mod work on any build (tested on Fritchii v4), you just press **Ctrl+F9** once at every launch for mouse panning, with **"Hide mouse on inactivity"** enabled to hide the cursor. With an unpatched build the `ButtonPrompts-KeyboardMouse` folder is applied as an ordinary mod, so keep it as the only `ButtonPrompts-*` folder.

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

## Download and install

**Where are the mod files?** They come from the game, so they are not in the code folders of this page. They are in the zip on the **Releases** page:

1. Open the [latest release](../../releases/latest).
2. Scroll down to **Assets** and click **`OoT-KeyboardMouse-v1.3.0.zip`**.

That one zip has everything: the icons, the settings file where you change keys and mouse speed, and the script that applies it, already in the right folders.

Now follow these 5 steps.

**Step 1 – Extract the zip**

Right-click the zip → **Extract All**. Do not drag files out of the zip window: extract first.

**Step 2 – Open Lichii's data folder**

Open Lichii and click **File → Open Lichii Folders → Root Data Folder**. A Windows folder opens. Leave it open next to the extracted one.

**Step 3 – Copy everything into it**

In the extracted folder press **Ctrl+A** and drag it all into the window from Step 2. If Windows says the destination already contains a folder with that name, click **Yes** (or **Continue**): it only adds our files and deletes nothing of yours.

```
Root Data Folder
├─ OoT-Keyboard-Mouse-Settings.ini        ← your keys and mouse speed (edit this)
├─ Apply-Settings.bat                     ← double-click to apply them
├─ load\0400486024DEC000\ButtonPrompts-KeyboardMouse\romfs\...   ← the icons
└─ config\input\OoT-Keyboard-Mouse.ini
```

**Step 4 – Apply the settings**

**Close Lichii**, then double-click **`Apply-Settings.bat`** in the Root Data Folder. A black window shows the keys it applied and ends with **Done**. This sets up Player 1 for keyboard and mouse and keeps a copy of your old settings (`config\qt-config.ini.pre-keyboard-mouse`).

If Windows shows a blue "Windows protected your PC" box, click **More info → Run anyway** (the `.bat` is plain text; right-click → Edit to read it).

**Step 5 – Play (repeat this every time you open the game)**

1. Start the game and wait until you can move the green hat kid.
2. **Click once on the game window.**
3. Press **Ctrl + F9** one time.
4. Move the mouse: the camera turns and the cursor disappears after a few seconds.

Ctrl+F9 works like a switch, so press it only once. If the cursor came back, press it again.

**Not working?**

- **`Apply-Settings.bat` says Lichii is running:** close Lichii completely and run it again.
- **It reports a problem in the settings file:** it names the line; fix it and run again. Nothing is changed until the file is correct.
- **Cursor still visible:** click the game window, press Ctrl+F9 once, and keep `hide_cursor = true` in the settings file.
- **Icons still look like the Switch:** check that `load\0400486024DEC000\ButtonPrompts-KeyboardMouse` is in the Root Data Folder, that no other folder starting with `ButtonPrompts-` is inside `0400486024DEC000`, then close and reopen the game.
- **No "Root Data Folder" in the File menu:** right-click the game → **Open Mod Data Location**, then go up two folders: that is the Root Data Folder.

More help: [docs/INSTALLATION.md](docs/INSTALLATION.md) and [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## Change keys and mouse speed

Open **`OoT-Keyboard-Mouse-Settings.ini`** with Notepad, change a line, save, close Lichii and double-click **`Apply-Settings.bat`** again:

```ini
button_a  = space          ; change to: shift, f, mouse_back ...
button_y  = mouse_left
mouse_sens = 5.0           ; camera speed, 1.0 (slow) ... 10.0 (fast)
mouse_invert_y = false
```

Every key, the mouse values and what they mean are listed in [docs/CONFIGURATION.md](docs/CONFIGURATION.md). One limit: the key pictures drawn inside the game are fixed images of the default keys, so after you rebind a key the game still shows the old picture until you [rebuild the icons](docs/CONFIGURATION.md#after-changing-keys-update-the-icons) from your own game file.

## Documentation

- [Installation](docs/INSTALLATION.md)
- [Configuration: the settings file, keys, mouse speed, acceleration](docs/CONFIGURATION.md)
- [Key mapping](docs/KEY-MAPPING.md)
- [Build the mod from your own game](docs/BUILD-THE-MOD.md)
- [Lichii patches](lichii-patches/README.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Changelog](CHANGELOG.md)

## License

Tools, profile and documentation: MIT ([LICENSE](LICENSE)). The Lichii patches are derived from Eden/yuzu and follow GPL-3.0-or-later. The texture and font files inside the release are derived from the game and remain Nintendo's property: use them only with a copy you own.
