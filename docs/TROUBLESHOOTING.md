# Troubleshooting

## The settings file and `Apply-Settings.bat`

**I cannot find the settings `.ini`.** It is `OoT-Keyboard-Mouse-Settings.ini`. It is in the release zip, and after Step 3 of the [installation](INSTALLATION.md) it sits in Lichii's Root Data Folder (File → Open Lichii Folders → Root Data Folder), next to `Apply-Settings.bat`. A copy is in this repository in [`settings/`](../settings). The Lichii profile `OoT-Keyboard-Mouse.ini` (in `config\input`) is a different file: `Apply-Settings.bat` writes it for you.

**`Apply-Settings.bat` says Lichii is running.** Close Lichii completely (check the system tray and Task Manager) and run it again. Lichii rewrites its settings when it exits, which would undo the change.

**`Apply-Settings.bat` lists problems in my settings file.** Each line names the setting and the line number in the `.ini`. The usual causes: a misspelled setting name, a key name that does not exist (the list is at the top of the file), a number outside its range, or a line without `=`. Nothing is changed until the file is correct.

**Windows shows "Windows protected your PC".** Click **More info → Run anyway**. The `.bat` and `.ps1` are plain text (right-click → Edit) and only read the `.ini` and write Lichii's `config` files. If your PC blocks scripts completely, use the "Without the script" section of [INSTALLATION.md](INSTALLATION.md).

**The window flashes and closes, or says the settings file was not found.** `Apply-Settings.bat`, `Apply-Settings.ps1` and `OoT-Keyboard-Mouse-Settings.ini` must be in the same folder, and that folder must be the Root Data Folder (the one that contains `config`). Do not run them from inside the zip: extract first.

**It says `qt-config.ini` was not found, so only the profile was written.** Lichii has never run with this data folder. Start Lichii once, close it, and run `Apply-Settings.bat` again.

**I changed a key and the game still shows the old picture.** Expected: the pictures are fixed images of the default keys. See [CONFIGURATION.md](CONFIGURATION.md#after-changing-keys-update-the-icons).

**I want my gamepad back.** Close Lichii and copy `config\qt-config.ini.pre-keyboard-mouse` over `config\qt-config.ini` (the script made that copy the first time you applied). Or load a gamepad profile in Configure → Controls. For the icons, remove the `ButtonPrompts-KeyboardMouse` folder from `load`.

## In the game

**The profile `OoT-Keyboard-Mouse` is not in the Profile list** (only matters for the backup way). The file is not in `config\input`, or Lichii was open when you copied it. Run `Apply-Settings.bat` or check the path, then close and reopen Lichii.

**I cannot find the mod folder in the repository.** The icon files come from the game, so they are not stored in the code folders. They are only in the release zip (`load\0400486024DEC000\ButtonPrompts-KeyboardMouse`).

**The cursor does not hide / the mouse does not turn the camera.** In a normal Lichii mouse panning is not saved: it is off every time the emulator starts. Click the game window and press **Ctrl+F9** once. Then:

- Ctrl+F9 only reaches the emulator when its window is in front. Click the game window first.
- It toggles: if the cursor was hidden and came back, you pressed it twice. Press it once more.
- Keep `hide_cursor = true` in the settings file (it is Configure → General → UI → **Hide mouse on inactivity**). The cursor hides a few seconds after the mouse stops.
- Do not press it during the first-boot loading: wait until you are in the game.
- If the emulated mouse (`mouse_enabled`) is on, panning stays off: turn it off in Configure → Controls → Advanced.

With the [patches](../lichii-patches/README.md) panning turns on by itself and the cursor hides, as long as player 1's right stick is mapped to the mouse (`player_0_rstick` starts with `engine:mouse`).

**The icons are still the Switch/PlayStation ones.** The folder is not where the emulator looks. It must be `user\load\0400486024DEC000\ButtonPrompts-KeyboardMouse\romfs\Font2\...` and `...\romfs\UI\...` (see the tree in [INSTALLATION.md](INSTALLATION.md)), and the emulator must have been closed and restarted after copying. Some builds print `LayeredFS layer 'ButtonPrompts-KeyboardMouse'` in `user\log\eden_log.txt`; others only print `LayeredFS patches applied successfully`. If more than one `ButtonPrompts-*` folder exists, keep only one (a Lichii without the patches applies all of them).

**The icons are a mix of keyboard and controller.** Another `ButtonPrompts-*` folder is in `load`. Move the others out.

**Tab does not open the map.** Qt may use Tab to move focus between windows. Set `button_minus = m` (or another key) in the settings file, apply it, and redraw the icons if you want them to match ([CONFIGURATION.md](CONFIGURATION.md)).

**Lichii closed by itself while playing.** Probably Ctrl+Q. Do not bind Ctrl to any game button (the script warns you if you do).

**The camera is too fast / too slow / jumpy.** Change `mouse_sens` (1.0 slow … 10.0 fast, 5.0 default) and, if small movements do nothing or the camera jumps, `mouse_deadzone_boost`. See [CONFIGURATION.md § Mouse](CONFIGURATION.md#mouse-speed-and-feel). Acceleration at 0 gives the plain 1:1 behaviour back (patched builds only).

## Editing by hand

**I edited `qt-config.ini` and my change vanished.** The emulator rewrites the file on exit. Edit it while Lichii is closed. And for any key that Lichii shows equal to the default, keep the `key\default=false` line, otherwise the value on the next line is ignored. `Apply-Settings.bat` does both for you.

## Building the mod

**The mod builder failed.** Check Python 3.10+, `pip install -r tools/requirements.txt`, and that the `.nup` is OOT `0400486024DEC000` v2.0.0. Details in [BUILD-THE-MOD.md](BUILD-THE-MOD.md).
