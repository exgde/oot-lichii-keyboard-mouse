# Changelog

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
