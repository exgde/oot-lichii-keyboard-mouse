# Installation

There are two ways to install. **Pick one**; they install the same mod and use the same settings file.

| Way | Download | Best for |
|---|---|---|
| **A. The program** | `OoT-KeyboardMouse-Config-v1.4.1.zip` | Most people: choose keys with clicks; the in-game key icons follow your keys. |
| **B. Manual** | `OoT-KeyboardMouse-v1.4.1.zip` | People who prefer no program: a one-click installer and a text file for the keys. |

Both are on the [latest release](../../releases/latest) page, under **Assets**.

**You need:** Windows, and Lichii (or a fork such as Fritchii) for Windows with OOT for Switch 2 already working (version 2.0.0, `[0400486024dec000][v131072]`).

---

## A. Install with the program

1. **Download** `OoT-KeyboardMouse-Config-v1.4.1.zip`.
2. **Extract it:** right-click the zip → **Extract All…** → **Extract**. A folder opens with `OoT-KeyboardMouse-Config.exe` in it.
3. **Close Lichii** completely (stopping the game is not enough: Lichii saves its settings when it closes and would undo the changes).
4. Double-click **`OoT-KeyboardMouse-Config.exe`**.
   - A blue box says *"Windows protected your PC"*? Click **More info → Run anyway**.
5. Check **Lichii data folder** at the top of the window.
   - It shows a folder: fine.
   - It says *(not found)*: click **Change…** and pick it. To see where it is, open Lichii and click **File → Open Lichii Folders → Root Data Folder** (a window opens: that is the folder). For a portable Lichii, pick the folder that has `lichii.exe`.
6. **Choose your keys** (or keep the defaults):
   - **Buttons** and **Movement** tabs: next to each action, pick a key from the list, or click **Press a key…** and press the key (or click a mouse button in that small window).
   - **Mouse and camera** tab: camera mode (*As the stick* or *Native*), camera speed, invert up/down.
   - Orange text under the tabs warns you about a key used twice or a key that clashes with Lichii.
7. Click **Apply** and wait for **Done**.
   - Changed keys? The first time, the program needs your game file (`.nup`) to draw the new key icons. It looks for it by itself in Lichii's game folders and asks you to pick it if it cannot find it.

**What Apply does:** it installs (or updates) the mod in Lichii's data folder, saves your choices in `OoT-Keyboard-Mouse-Settings.ini`, writes them into Lichii's settings (Player 1, keeping a copy of the old ones as `config\qt-config.ini.pre-keyboard-mouse`), switches the Native camera patch on or off, and redraws the in-game key icons when keys changed (HUD, menus, ocarina song sheet; the "Basic Controls" screen keeps the default layout).

To change something later: close Lichii, open the program, change it, click **Apply**.

---

## B. Install manually

1. **Download** `OoT-KeyboardMouse-v1.4.1.zip`.
2. **Extract it:** right-click the zip → **Extract All…** → **Extract**. A folder opens with `INSTALL.bat` in it.
   - Do not run anything from inside the zip window: extract first.
3. **Close Lichii** completely.
4. Double-click **`INSTALL.bat`**. A black window:
   1. finds Lichii's data folder (normally `C:\Users\<you>\AppData\Roaming\lichii`);
   2. copies the icons, the settings file, `Apply-Settings` and `OoT-MouseCapture.exe` there;
   3. moves other button-icon mods (PlayStation, Xbox, Steam Deck) to `mod-backups\`, because only one can be active;
   4. sets up Player 1 for keyboard and mouse (keeping your old settings as `config\qt-config.ini.pre-keyboard-mouse`).

   It ends with **Done** in green. Press any key to close it.
   - A blue box says *"Windows protected your PC"*? Click **More info → Run anyway**. `INSTALL.bat` is plain text: right-click → **Edit** shows what it does.
   - It asks for a *"Folder"*? Your Lichii keeps its data somewhere else (a portable Lichii uses a `user` folder next to `lichii.exe`). Open Lichii, click **File → Open Lichii Folders → Root Data Folder**, click the address bar of the window that opens and copy it (**Ctrl+C**), close Lichii, paste it into the black window (right-click or **Ctrl+V**) and press **Enter**.

Running it again later is safe: it keeps your `OoT-Keyboard-Mouse-Settings.ini` (the newest version of the file is put next to it as `OoT-Keyboard-Mouse-Settings.new.ini`).

**Change keys or mouse speed later:**

1. Close Lichii.
2. In Lichii's data folder, open **`OoT-Keyboard-Mouse-Settings.ini`** with Notepad.
3. Change a line, for example `button_a = shift`, `mouse_sens = 3.3` or `mouse_camera = native`, and save.
4. Double-click **`Apply-Settings.bat`** in the same folder.

Every setting is explained inside the file and in [CONFIGURATION.md](CONFIGURATION.md). If a line is misspelled, the script says which one and changes nothing. In this way the in-game key pictures keep showing the default keys (the program redraws them; you can also [rebuild them yourself](CONFIGURATION.md#after-changing-keys-update-the-icons)).

### Install by hand (no scripts at all)

1. Open Lichii → **File → Open Lichii Folders → Root Data Folder**, then close Lichii.
2. From the extracted folder, copy `load`, `config`, `OoT-Keyboard-Mouse-Settings.ini`, `Apply-Settings.bat`, `Apply-Settings.ps1` and `OoT-MouseCapture.exe` into that folder. If Windows asks about folders with the same name, click **Yes**: it adds files and deletes nothing.
3. Keep `ButtonPrompts-KeyboardMouse` as the **only** folder starting with `ButtonPrompts-` inside `load\0400486024DEC000`.
4. Open Lichii → **Emulation → Configure → Controls**, **Player 1** (type **Pro Controller**), choose the profile **OoT-Keyboard-Mouse** in **Profile**, click **Load**, then **OK** (default keys, *As the stick* camera).

---

## Play (every time you open the game)

1. Start the game and wait until you can move the green hat kid. The first launch prepares the graphics and can take several minutes.
2. **Click once** on the game picture.
3. Press **Ctrl + F9** once. The pointer disappears and the mouse turns the camera.

Ctrl+F9 is Lichii's "mouse panning" switch. Lichii does not save it, so it is needed at every launch, and it toggles, so press it only once (if the pointer comes back, press it again). It only works when the emulator window is in front, which is why you click first. **Alt+Tab** always gives the normal mouse back.

**Native camera:** before starting the game, also open **`OoT-MouseCapture.exe`** (in Lichii's data folder) and leave it open. It waits for the game and only acts while the game is in front: it keeps the pointer in the middle of the picture and turns off Windows mouse acceleration while you play. Everything goes back to normal on Alt+Tab or when it closes. More in [NATIVE-CAMERA.md](NATIVE-CAMERA.md).

## Check that it works

- Moving the mouse turns the camera and no pointer is visible.
- WASD moves the green hat kid, left click attacks, right click uses the item.
- The action button shows a key (Space) and the attack button shows a mouse with the left button filled.
- **Enter → Basic Controls** shows a keyboard and a mouse with guide lines to each key.

If you still see Switch or PlayStation buttons, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Uninstall

Close Lichii. In Lichii's data folder delete `load\0400486024DEC000\ButtonPrompts-KeyboardMouse` and `load\0400486024DEC000\MouseCamera-Native`. To get your gamepad layout back, copy `config\qt-config.ini.pre-keyboard-mouse` over `config\qt-config.ini`. Any button-icon mod the installers moved is in `mod-backups\`.

## Cautions

- Lichii must be closed while the program, the installer or `Apply-Settings.bat` runs: it rewrites `qt-config.ini` when it exits and would discard the changes. All of them refuse to run while it is open.
- The icon files have exactly the same size as the originals (the game keeps file sizes in an RSTB): do not re-save them with other tools.
- The Native camera patch is for game version 2.0.0 (main build `E0F3CCFAF50065AE…`). Another version ignores it.
