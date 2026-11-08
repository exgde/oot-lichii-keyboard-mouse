# Configuration: keys, sensitivity and acceleration

## 1. Change a key or mouse button

### In the Lichii UI (easiest)

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

The icons drawn in the game (the keys shown in the interface) do not change by themselves. To make them show your keys, edit the layout in `tools/build_fonts_kbm.py` (function `glyph_map`), `tools/build_mods_kbm.py` (`symbols`) and `tools/make_ctrl_kbm.py` (`KEY`), then build the mod again: [BUILD-THE-MOD.md](BUILD-THE-MOD.md).

## 2. Mouse sensitivity

**Emulation → Configure → Controls → Player 1 → "Mouse panning" button** opens the settings. They are also in `qt-config.ini`, section `[Controls]`, as a pair `key\default=false` + `key=value`:

| Setting | Key | Default | What it does |
|---|---|---|---|
| X / Y sensitivity | `mouse_panning_x_sensitivity`, `..._y_sensitivity` | 50 (1–100) | how far the stick moves per pixel of mouse travel. Higher = faster camera. Useful range: 30–80 |
| Deadzone counterweight | `mouse_panning_deadzone_counterweight` | 20 (0–100) | pushes small movements past the game's stick deadzone. If short movements do not move the camera, raise it; if the camera jumps, lower it |
| Decay strength | `mouse_panning_decay_strength` | 18 (0–100) | the emulated stick returns to centre after the mouse stops. Higher = stops faster, a "drier" camera; lower = it glides more |
| Minimum decay | `mouse_panning_min_decay` | 6 (0–100) | the least decay applied per step; keeps the stick from sticking tilted |
| **Acceleration** | `mouse_panning_acceleration` | 40 (0–100) | see below (needs the patches) |

How it works underneath: each mouse movement adds `pixels × sensitivity × 0.001` (× the acceleration gain) to the stick, and every step the value decays. The emulated stick has a ceiling (1.5 in Lichii's code), so **sensitivity decides how much mouse travel it takes to reach top camera speed**, not the top speed itself: the game's camera moves according to how far the stick is pushed.

Tuning recipe: (1) set acceleration to 0; (2) raise the sensitivity until a 180° turn takes a comfortable mouse movement; (3) adjust the deadzone counterweight until fine aiming responds; (4) only then raise acceleration.

## 3. Mouse acceleration (Lichii patches)

When the mouse moves **fast** the camera turns even faster; moving slowly it stays 1:1 so aiming stays precise. Lichii measures the pointer speed (pixels per millisecond, smoothed over about 3 events) and multiplies the movement by a gain:

| Mouse speed | 0% | 20% | 40% (default) | 70% | 100% |
|---|---|---|---|---|---|
| up to 800 px/s | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 1,500 px/s | 1.00 | 1.02 | 1.03 | 1.06 | 1.08 |
| 3,000 px/s | 1.00 | 1.13 | 1.27 | 1.47 | 1.67 |
| 5,000 px/s | 1.00 | 1.37 | 1.75 | 2.31 | 2.87 |
| 8,000 px/s or more | 1.00 | 1.60 | 2.20 | 3.10 | 4.00 |

After 80 ms without movement the speed resets. The stick ceiling still applies: acceleration makes a fast movement reach the maximum sooner, it does not go past it. To change the curve, edit the constants at the top of `src/input_common/drivers/mouse.cpp` (`acceleration_threshold`, `acceleration_full_speed`, `acceleration_max_extra_gain`) and rebuild.

## 4. Useful Lichii hotkeys

| Hotkey | Action |
|---|---|
| Ctrl+F9 | toggle mouse panning (and show/hide the cursor, with the patches) |
| F11 | fullscreen |
| Esc | leave fullscreen |
| Ctrl+M | mute/unmute audio |
| Ctrl+P | capture a screenshot |
| Ctrl+Q | **quit the emulator** (which is why Ctrl is not used as a game button) |
