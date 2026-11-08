# Troubleshooting

**The cursor does not hide / the mouse does not turn the camera.** In a normal Lichii mouse panning is not saved: press **Ctrl+F9** every time you start the game. With the [patches](../lichii-patches/README.md) it turns on by itself and the cursor hides, as long as player 1's right stick is mapped to the mouse (`player_0_rstick` starts with `engine:mouse`). If the emulated mouse (`mouse_enabled`) is on, panning stays off: turn it off in Configure → Controls → Advanced.

**The icons are still the Switch/PlayStation ones.** Look in `user\log\eden_log.txt` for the line `LayeredFS layer 'ButtonPrompts-KeyboardMouse'`. Without it the folder is not in `user\load\0400486024DEC000\` or the inner path is wrong (it needs `ButtonPrompts-KeyboardMouse\romfs\Font2\...` and `...\romfs\UI\...`). If more than one `ButtonPrompts-*` shows up in the log, keep only one (a Lichii without the patches applies all of them).

**The icons are a mix of keyboard and controller.** Another `ButtonPrompts-*` folder is in `load`. Move the others out.

**I edited `qt-config.ini` and my change vanished.** The emulator rewrites the file on exit. Edit it while Lichii is closed. And for any key that Lichii shows equal to the default, keep the `key\default=false` line, otherwise the value on the next line is ignored.

**Tab does not open the map.** Qt may use Tab to move focus between windows. Change the key of the − button (`button_minus`) to another one, for example `M` (code 77), and update the icons ([CONFIGURATION.md](CONFIGURATION.md)).

**Lichii closed by itself while playing.** Probably Ctrl+Q. Do not bind Ctrl to any game button.

**The camera is too fast / too slow / jumpy.** See the recipe in [CONFIGURATION.md § Mouse sensitivity](CONFIGURATION.md). Acceleration at 0 gives the plain 1:1 behaviour back.

**I want my gamepad back.** Restore the copy of `qt-config.ini` you kept, or load a gamepad profile in Configure → Controls. For the icons, remove the `ButtonPrompts-KeyboardMouse` folder from `load`.

**The mod builder failed.** Check Python 3.10+, `pip install -r tools/requirements.txt`, and that the `.nup` is OOT `0400486024DEC000` v2.0.0. Details in [BUILD-THE-MOD.md](BUILD-THE-MOD.md).
