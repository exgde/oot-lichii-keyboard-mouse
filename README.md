# OOT (Switch 2): keyboard and mouse for Lichii

Play *OOT* (Nintendo Switch 2) on **Lichii**, or any Lichii fork, with a **keyboard and mouse**, like a PC game.

- **W A S D** move the green hat kid, the **mouse** turns the camera, **left click** attacks.
- The game itself shows **keyboard and mouse icons** instead of controller buttons: on screen, in the menus, on the ocarina song sheet and on the "Basic Controls" screen.
- **Change any key and the mouse speed**, with a small program (clicks) or a text file (Notepad).
- **Two camera modes:** *As the stick* (the mouse acts like the right stick) or *Native* (the mouse turns the camera itself, 1:1, like a PC game).

> **[⬇ Download from the latest release](../../releases/latest)** (scroll down to **Assets**)

---

## 1. Which file do I download?

Pick **one** of the two:

| File | Who it is for |
|---|---|
| **`OoT-KeyboardMouse-Config-v1.4.0.zip`** | **Most people.** A small program: you click the keys you want and press **Apply**. It installs everything for you, and when you change a key it also redraws the key icons inside the game. |
| **`OoT-KeyboardMouse-v1.4.0.zip`** | People who prefer no program. A one-click installer (`INSTALL.bat`); keys and mouse are changed in a text file. |

**You need:** Windows, and Lichii (or a fork such as Fritchii) with OOT for Switch 2, version 2.0.0, already working (`[0400486024dec000][v131072]`).

---

## 2. Install

### With the program (recommended)

1. Download **`OoT-KeyboardMouse-Config-v1.4.0.zip`**.
2. **Extract it:** right-click the zip → **Extract All…** → **Extract**.
3. **Close Lichii** completely.
4. Double-click **`OoT-KeyboardMouse-Config.exe`**.
   If a blue box says *"Windows protected your PC"*, click **More info** → **Run anyway**.
5. Look at **"Lichii data folder"** at the top. If it says *(not found)*, click **Change…** and pick it.
   *Where is it?* Open Lichii and click **File → Open Lichii Folders → Root Data Folder**: the window that opens is that folder. For a portable Lichii, just pick the folder that has `lichii.exe`.
6. Choose your keys, or keep the defaults (see [Change keys and mouse](#4-change-keys-and-mouse)).
7. Click **Apply** and wait for **"Done"**.

### Without the program (manual)

1. Download **`OoT-KeyboardMouse-v1.4.0.zip`**.
2. **Extract it:** right-click the zip → **Extract All…** → **Extract**.
3. **Close Lichii** completely.
4. In the extracted folder, double-click **`INSTALL.bat`**. A black window finds Lichii's data folder, copies everything and sets up the keyboard and mouse. It ends with **"Done"**.
   If it asks for a *"Folder"*: open Lichii, click **File → Open Lichii Folders → Root Data Folder**, copy the address bar of that window (**Ctrl+C**), close Lichii, paste it into the black window and press **Enter**.

Step-by-step guide, with what you will see at each step: [docs/INSTALLATION.md](docs/INSTALLATION.md).

---

## 3. Play (every time)

1. Start the game in Lichii and wait until you can move.
2. **Click once** on the game picture.
3. Press **Ctrl + F9** once. The mouse pointer disappears and the mouse now turns the camera.

Ctrl+F9 switches on and off, so press it only once; if the pointer comes back, press it again. **Alt+Tab** always gives you the normal mouse back.

**Native camera only:** before starting the game, also open **`OoT-MouseCapture.exe`** (it is in Lichii's data folder) and leave it open.

### Default controls

| In the game | Keyboard / mouse |
|---|---|
| Move | **W A S D** (hold **Z** to walk slowly) |
| Camera | **move the mouse** |
| Reset camera | **middle click** |
| Attack | **left click** |
| Use item | **right click** |
| Target (hold) | **Shift** |
| Action / hold to run | **Space** |
| B / X (no label in the game) | **C** / **R** |
| Switch items | **Q / E** |
| Accessory / Ocarina / Navi / Boots | **1 / 2 / 3 / 4** |
| Menu / Map | **Enter** / **Tab** |

Ctrl and Alt are left free on purpose: in Lichii, Ctrl+Q quits and Alt opens the menu bar.

---

## 4. Change keys and mouse

**With the program:** close Lichii, open `OoT-KeyboardMouse-Config.exe`, change what you want, click **Apply**.

- **Buttons** and **Movement** tabs: for each action, pick a key from the list, or click **Press a key…** and press it (or click with a mouse button).
- **Mouse and camera** tab: camera mode, camera speed (also separately left/right and up/down), invert up/down, hide the pointer.
- When you change keys, the in-game key icons are redrawn for them. For that the program needs your game file (`.nup`) once: it finds it by itself in Lichii's game folders, or asks you to pick it.

**Without the program:** close Lichii, open **`OoT-Keyboard-Mouse-Settings.ini`** (in Lichii's data folder) with Notepad, change a line and save, then double-click **`Apply-Settings.bat`** in the same folder:

```ini
button_a     = space        ; try: shift, f, mouse_back ...
button_y     = mouse_left
mouse_sens   = 5.0          ; camera speed, 1.0 (slow) ... 10.0 (fast)
mouse_camera = stick        ; stick or native
```

Every option is explained inside the file and in [docs/CONFIGURATION.md](docs/CONFIGURATION.md). In this way the key icons in the game keep showing the default keys.

Both ways read and write the **same** settings file, so you can switch between them at any time.

---

## 5. Camera modes

| Mode | What it feels like |
|---|---|
| **As the stick** (default) | The mouse stands in for the right stick: the camera keeps the game's own curve and top speed. |
| **Native** | The mouse turns the camera itself, **1:1**, like a PC game: the same hand movement always gives the same turn, slow or fast, at any frame rate. Needs `OoT-MouseCapture.exe` open while you play. |

How Native works (a small patch in the game and a mouse helper): [docs/NATIVE-CAMERA.md](docs/NATIVE-CAMERA.md).

---

## Something is wrong?

| Problem | Fix |
|---|---|
| "Lichii is open" | Close Lichii completely (check the taskbar) and try again. |
| "Cannot bind argument to parameter 'Path'" | A bug of version 1.3. Download version 1.4 and install again (your settings are kept). |
| The mouse does not turn the camera | Click the game picture and press **Ctrl+F9** once. In Native mode, check that `OoT-MouseCapture.exe` is open. |
| Still Switch or PlayStation buttons on screen | Restart the game. Only one button-icon mod can be active; the installers move the others to the `mod-backups` folder. |
| I want my gamepad back | Close Lichii and copy `config\qt-config.ini.pre-keyboard-mouse` over `config\qt-config.ini` in Lichii's data folder. |

More answers: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

**Uninstall:** close Lichii; in Lichii's data folder delete `load\0400486024DEC000\ButtonPrompts-KeyboardMouse` and `load\0400486024DEC000\MouseCamera-Native`.

---

## What is in this repository

| Folder | What it is |
|---|---|
| [`settings/`](settings) | The manual way: `INSTALL.bat`, `Apply-Settings.bat`, the settings file and the Lichii input profile. |
| [`configurator/`](configurator) | Source of the settings program `OoT-KeyboardMouse-Config.exe`. |
| [`native-camera/`](native-camera) | The Native camera: the game patch (`MouseCamera-Native`, built and source) and the mouse helper `OoT-MouseCapture.exe` (source). |
| [`tools/`](tools) | Build the icon mod from **your own** game file, and build the release zips. |
| [`release-notes/`](release-notes) | The read-me files that go inside the zips. |
| [`lichii-patches/`](lichii-patches) | Optional changes for people who compile Lichii themselves. Not needed. |
| [`docs/`](docs) | The guides below. |

The icon files come from the game, so they are only in the release zips, not in these folders.

### Guides

- [Installation, step by step](docs/INSTALLATION.md)
- [Every setting explained](docs/CONFIGURATION.md)
- [Key mapping](docs/KEY-MAPPING.md)
- [Native camera: how it works](docs/NATIVE-CAMERA.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Build the mod and the program yourself](docs/BUILD-THE-MOD.md)
- [Changelog](CHANGELOG.md)

## License

Code, scripts and documentation: MIT ([LICENSE](LICENSE)). The Lichii patches are derived from Eden/yuzu and follow GPL-3.0-or-later. The icon files in the release are derived from the game and remain Nintendo's property: use them only with a copy you own. Fan project, not affiliated with Nintendo or with Lichii/Eden ([NOTICE](NOTICE.md)). Made with the help of AI (Claude).
