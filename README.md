# OOT (Switch 2): keyboard and mouse on Lichii

Play *OOT* (Nintendo Switch 2, title ID `0400486024DEC000`) on **Lichii** (an Eden/yuzu fork) with a **keyboard and mouse**: the mouse turns the camera and attacks, WASD moves, and the game's interface shows the matching keys instead of controller buttons.

**Download:** open the [latest release](../../releases/latest) and click **`OoT-KeyboardMouse-v1.2.0.zip`** under **Assets**. It has everything. Then follow [Download and install](#download-and-install) (5 steps).

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

## Download and install

**Where are the mod files?** They come from the game, so they are not in the code folders of this page. They are in the zip on the **Releases** page:

1. Open the [latest release](../../releases/latest).
2. Scroll down to **Assets** and click **`OoT-KeyboardMouse-v1.2.0.zip`**.

That one zip has everything: the icons and the keys file (`OoT-Keyboard-Mouse.ini`), already in the right folders. (The `.ini` is also attached to the release on its own.)

Now close Lichii and follow these 5 steps.

**Step 1 – Extract the zip**

Right-click the zip → **Extract All**. Do not drag files out of the zip window: extract first. You get a folder with two folders inside, **`load`** and **`config`**, and a `READ-ME-FIRST.txt`.

**Step 2 – Open Lichii's data folder**

Open Lichii and click **File → Open Lichii Folders → Root Data Folder**. A Windows folder opens. Leave it open next to the extracted one.

**Step 3 – Copy `load` and `config` into it**

Select the folders **`load`** and **`config`** from the extracted folder and drag them into the window from Step 2. If Windows says the destination already contains a folder with that name, click **Yes** (or **Continue**): it only adds our files and deletes nothing of yours.

Check that these two files now exist (open the folders to see):

```
Root Data Folder
├─ load
│  └─ 0400486024DEC000
│     └─ ButtonPrompts-KeyboardMouse        ← the icons
│        └─ romfs  (with Font2 and UI inside)
└─ config
   └─ input
      └─ OoT-Keyboard-Mouse.ini             ← the keys
```

**Step 4 – Load the keys in Lichii**

1. Click **Emulation → Configure → Controls**.
2. Pick **Player 1** and make sure the type is **Pro Controller**.
3. In the **Profile** box choose **OoT-Keyboard-Mouse**, click **Load**, then **OK**.

This replaces your current Player 1 layout. To keep a gamepad layout, click **New** in the Profile box and save it under a name before loading.

**Step 5 – Play (repeat this every time you open the game)**

1. Start the game and wait until you can move the green hat kid.
2. **Click once on the game window.**
3. Press **Ctrl + F9** one time.
4. Move the mouse: the camera turns and the cursor disappears after a few seconds.

Ctrl+F9 works like a switch, so press it only once. If the cursor came back, press it again.

**Not working?**

- **Profile `OoT-Keyboard-Mouse` is not in the list:** the `.ini` is not in `config\input`. Check Step 3, then close and reopen Lichii.
- **Cursor still visible:** click the game window, press Ctrl+F9 once, and check that **Emulation → Configure → General → UI → Hide mouse on inactivity** is ticked.
- **Icons still look like the Switch:** check the folder tree above, make sure no other folder starting with `ButtonPrompts-` is inside `load\0400486024DEC000`, then close and reopen the game.
- **No "Root Data Folder" in the File menu:** right-click the game → **Open Mod Data Location**, then go up two folders: that is the Root Data Folder.

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
