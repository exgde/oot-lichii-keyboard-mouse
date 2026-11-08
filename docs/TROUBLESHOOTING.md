# Troubleshooting

**The cursor does not hide / the mouse does not turn the camera.** In a normal Lichii mouse panning is not saved: it is off every time the emulator starts. Click the game window and press **Ctrl+F9** once. Then:

- Ctrl+F9 only reaches the emulator when its window is in front. Click the game window first.
- It toggles: if the cursor was hidden and came back, you pressed it twice. Press it once more.
- Keep **Hide mouse on inactivity** ticked (Configure → General → UI). The cursor hides a few seconds after the mouse stops.
- Do not press it during the first-boot loading: wait until you are in the game.
- If the emulated mouse (`mouse_enabled`) is on, panning stays off: turn it off in Configure → Controls → Advanced.

With the [patches](../lichii-patches/README.md) panning turns on by itself and the cursor hides, as long as player 1's right stick is mapped to the mouse (`player_0_rstick` starts with `engine:mouse`).

**The icons are still the Switch/PlayStation ones.** The folder is not where the emulator looks. It must be `user\load\0400486024DEC000\ButtonPrompts-KeyboardMouse\romfs\Font2\...` and `...\romfs\UI\...` (see the tree in [INSTALLATION.md](INSTALLATION.md)), and the emulator must have been closed and restarted after copying. Some builds print `LayeredFS layer 'ButtonPrompts-KeyboardMouse'` in `user\log\eden_log.txt`; others only print `LayeredFS patches applied successfully`. If more than one `ButtonPrompts-*` folder exists, keep only one (a Lichii without the patches applies all of them).

**The icons are a mix of keyboard and controller.** Another `ButtonPrompts-*` folder is in `load`. Move the others out.

**I edited `qt-config.ini` and my change vanished.** The emulator rewrites the file on exit. Edit it while Lichii is closed. And for any key that Lichii shows equal to the default, keep the `key\default=false` line, otherwise the value on the next line is ignored.

**Tab does not open the map.** Qt may use Tab to move focus between windows. Change the key of the − button (`button_minus`) to another one, for example `M` (code 77), and update the icons ([CONFIGURATION.md](CONFIGURATION.md)).

**Lichii closed by itself while playing.** Probably Ctrl+Q. Do not bind Ctrl to any game button.

**The camera is too fast / too slow / jumpy.** See the recipe in [CONFIGURATION.md § Mouse sensitivity](CONFIGURATION.md). Acceleration at 0 gives the plain 1:1 behaviour back.

**I want my gamepad back.** Restore the copy of `qt-config.ini` you kept, or load a gamepad profile in Configure → Controls. For the icons, remove the `ButtonPrompts-KeyboardMouse` folder from `load`.

**The mod builder failed.** Check Python 3.10+, `pip install -r tools/requirements.txt`, and that the `.nup` is OOT `0400486024DEC000` v2.0.0. Details in [BUILD-THE-MOD.md](BUILD-THE-MOD.md).
