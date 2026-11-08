# Key mapping

The labels on the "Basic Controls" screen come from the game's own text (`Mals/USen.Product.110.sarc.zs` → `LayoutMsg/PlusMenu_00.msbt`). The actions below are the game's.

| In-game action | Switch button | Keyboard / mouse | Icon in the interface |
|---|---|---|---|
| Move | left stick | **W A S D** (hold **Z** = walk slowly) | WASD cluster |
| Rotate Camera | right stick | **move the mouse** (mouse panning) | mouse |
| Reset Camera (Press) | R3 | **middle click** | mouse, wheel filled |
| Attack | Y | **left click** | mouse, left button filled |
| Use Item | ZR | **right click** | mouse, right button filled |
| Target | ZL | **left Shift** (hold) | ⇧ arrow |
| Actions / Dash (Hold) | A | **Space** | ␣ |
| (no label of its own) | B | **C** | C |
| (no label of its own) | X | **R** | R |
| Quick Select Items | L / R | **Q / E** | Q / E |
| Toggle Accessory / Play Ocarina / Talk to Navi / Toggle Boots | D-pad up / left / right / down | **1 / 2 / 3 / 4** | 1 2 3 4 |
| Open Menu | + | **Enter** | ⏎ |
| Open Map | − | **Tab** | TAB |

## Font glyphs the mod replaces

The game's `External` font stores the buttons as characters `U+E040…U+E06A`. The mod replaces:

| Code point | Was | Now shows |
|---|---|---|
| E040 / E041 / E042 / E043 | A / B / X / Y | Space / C / R / mouse with left button |
| E044 / E045 | L / R | Q / E |
| E046 / E047 | ZL / ZR | Shift / mouse with right button |
| E04B / E04C | + / − | Enter / Tab |
| E049 | whole D-pad | `1-4` |
| E060 / E062 / E063 / E061 | D-pad up / left / right / down | 1 / 2 / 3 / 4 |
| E064 / E065 / E06A | D-pad up-down / left-right / left-down-right | `1 4` / `2 3` / `2 4 3` |
| E050 / E052 / E05A / E058 | left stick down / up / left / right | S / W / A / D |
| E054 / E05C | left stick left-right / up-down | `A D` / `W S` |
| E05E | left stick | WASD |
| E05F / E057 | right stick / press | mouse / mouse with the wheel filled |
| E051 / E053 / E059 / E05B / E055 / E05D / E068 | right stick in one direction / shake | mouse with arrows |

The other glyphs (HOME, power, …) are left as they were.

## Why not Ctrl, Alt or Esc

In Lichii, **Ctrl+Q quits the emulator**, Ctrl+M changes the audio, Ctrl+F9 toggles mouse panning, **Alt** opens the menu bar and **Esc** leaves fullscreen. Those hotkeys would fire together with the game action, so the action keys are letters, digits, Space, Shift, Enter and Tab.
