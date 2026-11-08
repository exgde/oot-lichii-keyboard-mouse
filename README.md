# OOT (Switch 2): keyboard and mouse on Lichii

Play *OOT* (Nintendo Switch 2, title ID `0400486024DEC000`) on **Lichii** (an Eden/yuzu fork) with a **keyboard and mouse**: the mouse turns the camera and attacks, WASD moves, and the game's interface shows the matching keys instead of controller buttons.

| Part | What it does | Needs a rebuilt Lichii? |
|---|---|---|
| **Input profile** (`profile/`) | WASD, mouse as the right stick, mouse buttons, action keys | no |
| **Icon mod** (`ButtonPrompts-KeyboardMouse`) | replaces the button icons, the HUD buttons, the ocarina song-sheet notes and the "Basic Controls" screen with keyboard and mouse art | no |
| **Lichii patches** (`lichii-patches/`) | mouse acceleration; mouse panning turns on by itself and the cursor hides; a "Keyboard and mouse" option for the icons | yes (optional) |
| **Tools** (`tools/`) | build the mod from **your own** `.nup`, so you can change the keys and redo the icons | no |

> The patches are not part of any prebuilt Lichii release. If you do not compile the emulator yourself, skip them: the profile and the icon mod work on any build, you just press **Ctrl+F9** at every launch for mouse panning and enable **"Hide mouse on inactivity"** to hide the cursor. With an unpatched build the `ButtonPrompts-KeyboardMouse` folder is applied as an ordinary mod, so keep it as the only `ButtonPrompts-*` folder.

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

1. Download `OoT-ButtonPrompts-KeyboardMouse.zip` from [Releases](../../releases) (or build it from your own game, see [docs/BUILD-THE-MOD.md](docs/BUILD-THE-MOD.md)) and copy the `ButtonPrompts-KeyboardMouse` folder to `<Lichii>\user\load\0400486024DEC000\`.
2. Copy `profile/OoT-Keyboard-Mouse.ini` to `<Lichii>\user\config\input\`, open **Emulation → Configure → Controls → Player 1**, pick the profile `OoT-Keyboard-Mouse` and click **Load**.
3. Start the game and press **Ctrl+F9** (mouse panning), unless you run a Lichii with the patches.

Full walkthrough, including how to check the log: [docs/INSTALLATION.md](docs/INSTALLATION.md).

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
