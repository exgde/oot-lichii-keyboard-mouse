# Configuration: keys, sensitivity and acceleration

## The settings file

Everything you normally want to change is in **`OoT-Keyboard-Mouse-Settings.ini`**, in Lichii's Root Data Folder. To change something: edit the file in Notepad, save, **close Lichii**, double-click **`Apply-Settings.bat`**.

The script checks the file first. If it has a mistake (or Lichii is open) it stops and changes nothing. Otherwise it writes the keys and the mouse values into `config\qt-config.ini` (Player 1) and into the profile `config\input\OoT-Keyboard-Mouse.ini`, and keeps your previous settings as `config\qt-config.ini.pre-keyboard-mouse`.

Format: `name = value`, one per line. A `;` starts a comment. Delete a line to get its default. Names and values are not case sensitive; for numbers both `3.3` and `3,3` work.

**Key names** (any of these as a value): `a` … `z`, `0` … `9`, `space`, `enter`, `tab`, `backspace`, `esc`, `shift`, `ctrl`, `alt`, `capslock`, `up`, `down`, `left`, `right`, `insert`, `delete`, `home`, `end`, `pageup`, `pagedown`, `f1` … `f12`, `comma`, `period`, `minus`, `equals`, `slash`, `backslash`, `semicolon`, `apostrophe`, `bracketleft`, `bracketright`, `grave`; mouse buttons `mouse_left`, `mouse_right`, `mouse_middle`, `mouse_back`, `mouse_forward`; `none` to leave a button unassigned. A raw Qt code also works: `code:16777250`. Avoid `ctrl`, `alt` and `esc` (Lichii uses them: Ctrl+Q quits, Ctrl+F9 toggles mouse panning, Alt opens the menu bar, Esc leaves fullscreen); the script warns you.

| Setting | Default | Switch button / meaning |
|---|---|---|
| `button_y` | `mouse_left` | Y: attack |
| `button_a` | `space` | A: action, hold to run |
| `button_b`, `button_x` | `c`, `r` | B, X (no label in the game) |
| `button_zl` | `shift` | ZL: hold to target |
| `button_zr` | `mouse_right` | ZR: use item |
| `button_l`, `button_r` | `q`, `e` | L, R: quick select items |
| `button_r3` | `mouse_middle` | right stick press: reset the camera |
| `button_l3` | `none` | left stick press |
| `button_plus`, `button_minus` | `enter`, `tab` | +: menu, −: map |
| `dpad_up`, `dpad_left`, `dpad_right`, `dpad_down` | `1`, `2`, `3`, `4` | D-pad: accessory, ocarina, Navi, boots |
| `button_home`, `button_screenshot` | `none` | Home, Capture |
| `move_up`, `move_down`, `move_left`, `move_right` | `w`, `s`, `a`, `d` | left stick |
| `walk_key` | `z` | hold to walk slowly |
| `walk_speed` | `0.5` | how slow: `0.1` … `1.0` (1.0 = no change) |
| `mouse_sens` | `5.0` | camera speed, `1.0` (slow) … `10.0` (fast). The number × 10 is Lichii's sensitivity (1–100), so `5.0` is its default 50 |
| `mouse_sens_x`, `mouse_sens_y` | empty | left/right and up/down speed on their own (empty = use `mouse_sens`) |
| `mouse_invert_y` | `false` | `true`: moving the mouse up looks down |
| `mouse_camera` | `stick` | `stick`: the mouse stands in for the right stick (the game's curve and top speed). `native`: the mouse turns the camera itself, 1:1 (see [Native camera](#native-camera)) |
| `mouse_deadzone_boost` | `20` | 0–100, Lichii's "deadzone counterweight" (see [Mouse speed and feel](#mouse-speed-and-feel)) |
| `mouse_stop_speed` | `18` | 0–100, Lichii's "decay strength": higher = the camera stops sooner |
| `mouse_min_decay` | `6` | 0–100, Lichii's "minimum decay" |
| `hide_cursor` | `true` | hide the pointer after a few idle seconds ("Hide mouse on inactivity") |

Not in the file, on purpose: **mouse acceleration** exists only in a patched Lichii ([below](#mouse-acceleration-lichii-patches)); **mouse panning** is switched on with Ctrl+F9 because Lichii does not save it; and the **pictures** drawn in the game cannot follow your keys ([below](#after-changing-keys-update-the-icons)).

The sections that follow explain how it works underneath and how to change things without the script.

## Advanced: change a key in the Lichii UI or by hand

### In the Lichii UI (easiest without the script)

**Emulation → Configure → Controls → Player 1**: click the button you want to change (for example "A") and press the new key or mouse button. Right-click a button to clear it. **Save** the result as a profile (Profile → New) so you do not lose it.

### By editing the profile `OoT-Keyboard-Mouse.ini`

The file has one entry per button, written as two lines:

```ini
button_a\default=false
button_a="engine:keyboard,code:32,toggle:0"
```

The first line (`\default=false`) **must** be there, otherwise Lichii ignores the value. To move button A from Space to F, change the code (`32` → `70`).

| Format | Meaning |
|---|---|
| `engine:keyboard,code:<n>,toggle:0` | the key with code `n` (table below); `toggle:1` makes the key switch on/off |
| `engine:mouse,button:<n>` | mouse button: `0` left, `1` right, `2` middle (wheel click), `3` back, `4` forward |
| `engine:keyboard,code:0,toggle:0` | no key (button unbound) |

Buttons in the file: `button_a b x y`, `button_l r zl zr`, `button_plus minus`, `button_dup ddown dleft dright` (D-pad), `button_lstick rstick` (stick presses), `button_home`, `button_screenshot`, and `slleft srleft slright srright` (single Joy-Con buttons, leave them unbound).

**Left stick (WASD)** uses `analog_from_button`:

```ini
lstick="engine:analog_from_button,right:engine$0keyboard$1code$068$1toggle$00,modifier_scale:0.500000,up:engine$0keyboard$1code$087$1toggle$00,down:engine$0keyboard$1code$083$1toggle$00,left:engine$0keyboard$1code$065$1toggle$00,modifier:engine$0keyboard$1code$090$1toggle$00"
```

Inside it, `:` is written `$0` and `,` is written `$1`. The number after `code$0` is the key code (`$087` = `W` = 87). `modifier` is the key that scales the stick down (here **Z**, walk slowly) and `modifier_scale` is by how much (0.5 = half). To use the arrow keys instead of WASD, replace the four codes with 16777235 (↑), 16777237 (↓), 16777234 (←) and 16777236 (→).

**Right stick (mouse)** is fixed: `rstick="engine:mouse,axis_x:0,axis_y:1,threshold:0.500000,range:1.000000,deadzone:0.000000"`. Keep the deadzone at 0 and the range at 1.

After editing, **Load** the profile again in Configure → Controls (or copy the lines into `qt-config.ini`, renaming `button_a` to `player_0_button_a`, with Lichii closed).

### Key codes (Qt)

| Key | Code | Key | Code |
|---|---|---|---|
| A … Z | 65 … 90 (A=65, W=87, Z=90) | 0 … 9 | 48 … 57 |
| Space | 32 | Enter (Return) | 16777220 |
| Tab | 16777217 | Backspace | 16777219 |
| ← ↑ → ↓ | 16777234, 16777235, 16777236, 16777237 | Shift | 16777248 |
| Insert / Delete | 16777222 / 16777223 | Home / End | 16777232 / 16777233 |
| Page Up / Down | 16777238 / 16777239 | Caps Lock | 16777252 |
| F1 … F12 | 16777264 … 16777275 | Esc | 16777216 |
| Ctrl | 16777249 | Alt | 16777251 |

**Avoid Ctrl, Alt and Esc** for gameplay: Ctrl+Q quits the emulator, Ctrl+F9 toggles mouse panning, Alt opens the menu bar and Esc leaves fullscreen.

### After changing keys: update the icons

The icons drawn in the game (the keys shown in the interface) are pictures of the default keys and do not change by themselves, whether you rebind in the settings file, in the Lichii UI or in the profile. To make them show your keys, edit the layout in `tools/build_fonts_kbm.py` (function `glyph_map`), `tools/build_mods_kbm.py` (`symbols`) and `tools/make_ctrl_kbm.py` (`KEY`), then build the mod again: [BUILD-THE-MOD.md](BUILD-THE-MOD.md).

## Native camera

With `mouse_camera = native`, `Apply-Settings.bat`:

- switches on the game patch `load\0400486024DEC000\MouseCamera-Native\exefs\E0F3CCFAF50065AE4EA01EB5AEB13B1A45DA3348.ips` (with `stick` it is renamed to `.ips.off`), and writes your speed into it;
- sets Lichii's `mouse_enabled = true`, so the game receives the real mouse;
- unbinds the right stick for Player 1 (with `mouse_enabled`, Lichii turns "mouse moved while a button is held" into right-stick input, so attacking would move the camera).

Speed: `mouse_sens` × 0.012 degrees per mouse count (`5.0` = 0.06°, about 15 cm of mouse for a full turn at 1600 DPI). `OoT-MouseCapture.exe` sets the Windows pointer speed so that one mouse count is one pixel of the game's 1280×720 picture, so this holds at any window size. The `mouse_deadzone_boost`, `mouse_stop_speed` and `mouse_min_decay` values only apply to `stick`.

The game still applies its own pitch limits and, when the mouse rests for a while, its usual slow return of the camera behind the green hat kid, exactly as with the stick.

## Mouse speed and feel

`mouse_sens`, `mouse_deadzone_boost`, `mouse_stop_speed` and `mouse_min_decay` in the settings file are these Lichii values. You can also change them in **Emulation → Configure → Controls → Player 1 → "Mouse panning" button**. They are stored in `qt-config.ini`, section `[Controls]`, as a pair `key\default=false` + `key=value`:

| Setting | Key | Default | What it does |
|---|---|---|---|
| X / Y sensitivity | `mouse_panning_x_sensitivity`, `..._y_sensitivity` | 50 (1–100) | how far the stick moves per pixel of mouse travel. Higher = faster camera. Useful range: 30–80 |
| Deadzone counterweight | `mouse_panning_deadzone_counterweight` | 20 (0–100) | pushes small movements past the game's stick deadzone. If short movements do not move the camera, raise it; if the camera jumps, lower it |
| Decay strength | `mouse_panning_decay_strength` | 18 (0–100) | the emulated stick returns to centre after the mouse stops. Higher = stops faster, a "drier" camera; lower = it glides more |
| Minimum decay | `mouse_panning_min_decay` | 6 (0–100) | the least decay applied per step; keeps the stick from sticking tilted |
| **Acceleration** | `mouse_panning_acceleration` | 40 (0–100) | see below (needs the patches) |

How it works underneath: each mouse movement adds `pixels × sensitivity × 0.001` (× the acceleration gain) to the stick, and every step the value decays. The emulated stick has a ceiling (1.5 in Lichii's code), so **sensitivity decides how much mouse travel it takes to reach top camera speed**, not the top speed itself: the game's camera moves according to how far the stick is pushed.

Tuning recipe: (1) set acceleration to 0; (2) raise the sensitivity until a 180° turn takes a comfortable mouse movement; (3) adjust the deadzone counterweight until fine aiming responds; (4) only then raise acceleration.

## Mouse acceleration (Lichii patches)

When the mouse moves **fast** the camera turns even faster; moving slowly it stays 1:1 so aiming stays precise. Lichii measures the pointer speed (pixels per millisecond, smoothed over about 3 events) and multiplies the movement by a gain:

| Mouse speed | 0% | 20% | 40% (default) | 70% | 100% |
|---|---|---|---|---|---|
| up to 800 px/s | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 1,500 px/s | 1.00 | 1.02 | 1.03 | 1.06 | 1.08 |
| 3,000 px/s | 1.00 | 1.13 | 1.27 | 1.47 | 1.67 |
| 5,000 px/s | 1.00 | 1.37 | 1.75 | 2.31 | 2.87 |
| 8,000 px/s or more | 1.00 | 1.60 | 2.20 | 3.10 | 4.00 |

After 80 ms without movement the speed resets. The stick ceiling still applies: acceleration makes a fast movement reach the maximum sooner, it does not go past it. To change the curve, edit the constants at the top of `src/input_common/drivers/mouse.cpp` (`acceleration_threshold`, `acceleration_full_speed`, `acceleration_max_extra_gain`) and rebuild.

## Useful Lichii hotkeys

| Hotkey | Action |
|---|---|
| Ctrl+F9 | toggle mouse panning (and show/hide the cursor, with the patches) |
| F11 | fullscreen |
| Esc | leave fullscreen |
| Ctrl+M | mute/unmute audio |
| Ctrl+P | capture a screenshot |
| Ctrl+Q | **quit the emulator** (which is why Ctrl is not used as a game button) |
