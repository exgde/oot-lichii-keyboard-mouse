# Changelog

## v1.4.1 – 2026-11-12

- **Native camera: no more small jerks or stops with other screen settings.** `OoT-MouseCapture.exe` now reads Lichii's *Aspect Ratio* setting (16:9, 4:3, 21:9, 16:10 or Stretch, including a per-game setting) and lays the picture out exactly like the emulator, and it works in real screen pixels, so Windows display scaling (125 %, 150 %) no longer breaks the exact clock-hand jumps. Before, anything other than 16:9 at 100 % scaling could make the camera jerk back a little at times or stop at the edge of the picture.
- `OoT-MouseCapture.exe` finds the game by its emulator window (Lichii, Eden, yuzu and forks), so a browser tab with the same title is ignored.

## v1.4.0 – 2026-11-12

- **Fix:** `Apply-Settings.bat` stopped at once with *"Cannot bind argument to parameter 'Path' because it is an empty string"* on Windows PowerShell 5.1 (the PowerShell built into Windows). It now finds its own folder in every case.
- **New installer, `INSTALL.bat`:** finds Lichii's data folder by itself (or asks for it, with instructions), copies the mod there, moves other button-icon mods to `mod-backups\`, and applies the settings. Installing is now: extract, close Lichii, double-click `INSTALL.bat`. Running it again keeps your settings file.
- `Apply-Settings.bat` explains, step by step, how to find the right folder when it is run from the wrong one, and works when the files sit next to a portable `lichii.exe` (it uses the `user` folder).
- **New: native mouse camera** (`mouse_camera = native`, optional). A small game patch (`MouseCamera-Native`, an IPS for game version 2.0.0) reads the mouse through the game's own `nn::hid::GetMouseStates` and adds the movement to the camera's turn for that frame, after the stick curve: no curve, no top speed, the same turn for the same hand movement at any frame rate. `mouse_sens` and `mouse_invert_y` work in both modes. Needs `OoT-MouseCapture.exe` running: while the game is in front it keeps the pointer near the middle of the picture (jumps the patch undoes exactly, so fast turns never snap back) and turns off Windows mouse acceleration, and gives everything back on Alt+Tab. Default stays `stick`, which behaves as before.
- **New settings program** (`OoT-KeyboardMouse-Config-v1.4.0.zip`, optional): a Windows program with the mod inside. Pick keys and mouse settings, click Apply: it installs or updates the mod in any Lichii fork's data folder, writes the usual settings file, applies it, and redraws the in-game key icons for the chosen keys (from three small files of the player's own `.nup`, read once). The manual ways are unchanged.
- New `READ-ME-FIRST.txt` / `LEIA-ME.txt` in the zip, rewritten as three steps with what you will see at each one.

## v1.3.0 – 2026-11-08

One settings file for everything. The mod files (icons, controls screen) are unchanged and identical to v1.0.0.

- New **`OoT-Keyboard-Mouse-Settings.ini`**: every key and mouse value as `name = value` lines in a plain text file (`button_a = shift`, `mouse_sens = 3.3`, `mouse_invert_y = true`, …). Documented inside the file and in [docs/CONFIGURATION.md](docs/CONFIGURATION.md).
- New **`Apply-Settings.bat`** (runs `Apply-Settings.ps1`, PowerShell 5.1 or newer, already part of Windows): checks the settings file, then writes Player 1's keys and the mouse values straight into Lichii's `qt-config.ini` and the profile `config\input\OoT-Keyboard-Mouse.ini`. It stops if Lichii is open or the file has a mistake, and keeps a copy of the old settings as `config\qt-config.ini.pre-keyboard-mouse`. With the default settings it produces a profile identical to `profile/OoT-Keyboard-Mouse.ini`.
- The installation is still 5 steps, but step 4 is now "double-click `Apply-Settings.bat`" instead of loading the profile by hand in Configure → Controls. The profile route still works and is documented as the backup way.
- The zip now holds the settings file and the script at its top level; step 3 is "select everything in the extracted folder and drag it into the Root Data Folder".

## v1.2.0 – 2026-11-08

The mod files (icons, controls screen, input profile) are unchanged and identical to v1.0.0.

- The release now ships **one zip with everything**, `OoT-KeyboardMouse-v1.2.0.zip`: the icons and the keys file (`OoT-Keyboard-Mouse.ini`) already in the right folders (`load\...` and `config\input\...`). Installing is copying two folders. The `.ini` is also attached to the release on its own.
- The installation guide is down to 5 steps and uses **File → Open Lichii Folders → Root Data Folder** instead of navigating up from the mod folder.
- Troubleshooting: where the `.ini` is, why the mod files are not in the code folders, and what to do when the profile is not listed.

## v1.1.0 – 2026-11-08

Documentation release. The mod files (icons, controls screen, input profile) are unchanged and byte-identical to v1.0.0.

- Rewrote the installation guide as numbered steps: how to find the data folder, the exact folder tree to copy, loading the profile, the cursor setting, and the checks.
- Documented how mouse panning works on a stock Lichii: it is not saved, so click the game window and press **Ctrl+F9** once per launch; the cursor then hides on its own. Confirmed on Fritchii v4 without any patch.
- Troubleshooting now covers the common Ctrl+F9 mistakes (emulator not in front, pressing it twice, pressing it during the first-boot load).
- Noted that some builds do not print the per-mod `LayeredFS layer` log line, so the in-game check is the reliable one.

## v1.0.0 – 2026-11-08

- `OoT-Keyboard-Mouse` input profile (WASD, mouse = camera, mouse buttons, Q/E, 1–4, Shift, Space, Enter, Tab).
- `ButtonPrompts-KeyboardMouse` icon mod: button font, HUD letters, ocarina song-sheet notes and the "Basic Controls" screen with a keyboard, a mouse and guide lines.
- Lichii patches: mouse acceleration (`mouse_panning_acceleration`, default 40%), automatic mouse panning with a hidden cursor, and a "Keyboard and mouse" icon option.
- Tools (`tools/`) that build the mod from the user's `.nup`, with default keyboard and mouse art drawn by `draw_default_art.py`.
