# Installation

Six short steps, about five minutes. Close Lichii before you start.

**You need:**

- Lichii (or a fork such as Fritchii) for Windows, with *OOT* for Switch 2 already running in it (version 2.0.0, `[0400486024dec000][v131072].nup`).
- Two files, downloaded in Step 1.

Tested on Fritchii v4 and on a locally built Lichii "build 116".

## Step 1 – Download two files

- **The mod:** open the [latest release](../../releases/latest), scroll down to **Assets** and click `OoT-ButtonPrompts-KeyboardMouse.zip`.
- **The keys file:** [OoT-Keyboard-Mouse.ini](https://github.com/exgde/oot-lichii-keyboard-mouse/raw/main/profile/OoT-Keyboard-Mouse.ini). Right-click the link → **Save link as…**

(Prefer to build the icons yourself, for example after changing keys? See [BUILD-THE-MOD.md](BUILD-THE-MOD.md).)

## Step 2 – Open the game's mod folder

Open Lichii, right-click the game (OOT) in the game list and click **Open Mod Data Location**. A Windows folder opens. Its name ends in `0400486024DEC000`. Leave it open.

## Step 3 – Add the icons

1. Right-click the zip you downloaded → **Extract All**.
2. Open the extracted folder and drag the folder **`ButtonPrompts-KeyboardMouse`** into the folder from Step 2.
3. Check: inside `0400486024DEC000` there is now `ButtonPrompts-KeyboardMouse`, and inside it a folder called `romfs`.

If other folders in `0400486024DEC000` start with `ButtonPrompts-` (PlayStation, Xbox, Steam Deck…), move them out. Two of them replace the same game files and only one wins.

## Step 4 – Add the keys file

1. Go up two folders, to the one that contains `load`. In the address bar at the top, click the name just before `load` (it is usually `user`).
2. Open `config`, then `input`. If `input` does not exist, create it: right-click → **New** → **Folder**, and name it `input`.
3. Put `OoT-Keyboard-Mouse.ini` there.

When you are done the folders look like this:

```
user
├─ load
│  └─ 0400486024DEC000
│     └─ ButtonPrompts-KeyboardMouse        ← Step 3
│        └─ romfs
│           ├─ Font2\Scalable\External.Nin_Ounce_NVN2.bfotf.zs
│           └─ UI\Layout2Archive\Common.Product.100.Nin_Ounce_NVN2.bntx.zs
└─ config
   └─ input
      └─ OoT-Keyboard-Mouse.ini             ← Step 4
```

If you do not have the "Open Mod Data Location" option, the same folders are inside the folder that holds `lichii.exe`: `user\load\0400486024DEC000` and `user\config\input`. Create any that are missing.

## Step 5 – Load the keys in Lichii

1. Open Lichii and click **Emulation → Configure → Controls**.
2. Pick **Player 1** and make sure the type is **Pro Controller**.
3. In the **Profile** box choose **OoT-Keyboard-Mouse**, click **Load**, then **OK**.

This replaces your current Player 1 layout. To keep a gamepad layout, click **New** in the Profile box and save it under a name before loading the keyboard profile.

## Step 6 – Play (repeat this every time you open the game)

1. Start the game and wait until you can move the green hat kid. The first launch builds shaders and can take several minutes.
2. **Click once on the game window.**
3. Press **Ctrl + F9** one time.
4. Move the mouse: the camera turns and the cursor disappears after a few seconds.

Why: Lichii forgets "mouse panning" every time it closes, so it must be switched on each launch. Ctrl+F9 works like a switch, so press it only once. If the cursor came back, press it again. The key only works when the emulator window is the one in front, which is why you click it first.

A Lichii compiled with the [patches](../lichii-patches/README.md) does Step 6 by itself. Official and prebuilt builds do not have them.

## Check that it works

- Moving the mouse turns the camera and no cursor is visible.
- WASD moves the green hat kid, left click attacks, right click uses the item.
- The action button shows a key (Space) and the attack button shows a mouse with the left button filled.
- **Enter → Basic Controls** shows a keyboard and a mouse with guide lines to each key.

If you still see Switch or PlayStation buttons, the icon folder is not where Lichii looks: see [TROUBLESHOOTING.md](TROUBLESHOOTING.md). The log (`user\log\eden_log.txt`) of some builds prints `LayeredFS layer 'ButtonPrompts-KeyboardMouse'`; others only print `LayeredFS patches applied successfully`, so the in-game check above is the one to trust.

## If you change keys later

The icons in the game are pictures of the default keys and do not follow your changes. If you rebind a key in Lichii, the new key works but the game still shows the old one. To make the icons match, rebuild the mod: [CONFIGURATION.md](CONFIGURATION.md#after-changing-keys-update-the-icons).

## Uninstall

Delete the `ButtonPrompts-KeyboardMouse` folder from `load\0400486024DEC000`, restore your gamepad layout in **Emulation → Configure → Controls**, and restart the game.

## Cautions

- Edit `qt-config.ini` **only while Lichii is closed**: the emulator rewrites the file when it exits and discards manual edits.
- The mod's files have exactly the same size as the originals (the game keeps file sizes in an RSTB): do not re-save them with other tools.
