# Lichii patches

Small changes to the Lichii source (an Eden/yuzu fork). **They are optional**: the input profile and the icon mod work on a Lichii without them, except that mouse panning then needs Ctrl+F9 every time you start the game.

| Patch | What it does |
|---|---|
| `0001-oot-button-prompts-keyboard-mouse-option.patch` | adds "Keyboard and mouse" to **Graphics → Advanced → OOT: button icons** (the `ButtonPrompts-KeyboardMouse` folder is then applied only when selected, like the PlayStation/Xbox/Steam Deck ones) |
| `0002-mouse-panning-acceleration-auto-enable-hidden-cursor.patch` | **mouse acceleration** (new `mouse_panning_acceleration` setting + a field in the mouse panning dialog); **mouse panning turns on by itself** when a game boots and player 1's right stick is bound to the mouse; the **cursor hides** with mouse panning and comes back when it is toggled off (Ctrl+F9) |

**Not in prebuilt builds.** These changes live only in a locally compiled build; official/prebuilt Lichii releases do not have them. Without them, mouse panning needs Ctrl+F9 at every launch, the cursor hides only with "Hide mouse on inactivity", there is no mouse acceleration, and the icon mod is applied as an ordinary mod (keep a single `ButtonPrompts-*` folder). If you want the behaviour on another base, port `0002` (about 230 lines, six files).

Base: Lichii branch `on-116` (zortos build 116 plus our own changes), commit `4958b344f1`. Files touched:
`src/common/settings.h`, `settings_enums.h`, `src/core/file_sys/patch_manager.cpp`, `src/qt_common/config/shared_translation.cpp`, `src/input_common/drivers/mouse.{h,cpp}`, `src/yuzu/configuration/configure_mouse_panning.{cpp,ui}`, `src/yuzu/main_window.cpp`.

## Apply and build

```
cd <Lichii source tree>
git apply --check ../oot-lichii-keyboard-mouse/lichii-patches/0001-*.patch
git apply ../oot-lichii-keyboard-mouse/lichii-patches/0001-*.patch ../oot-lichii-keyboard-mouse/lichii-patches/0002-*.patch
```

Then build Lichii the way you normally do. On another Eden base `git apply` may need context fixes (`git apply --3way`). `settings.h` and `settings_enums.h` are included by almost every file, so the first build recompiles a large part of the project; the new setting was placed at the **end** of `struct Values` so the other members do not shift.

## License

These are derivative work of Eden/yuzu and follow **GPL-3.0-or-later**, like the rest of the emulator. No Lichii binary is included in this repository.
