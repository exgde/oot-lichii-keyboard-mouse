# Installation

Five short steps, about five minutes. Close Lichii before you start.

**You need:**

- Lichii (or a fork such as Fritchii) for Windows, with OOT for Switch 2 already running in it (version 2.0.0, `[0400486024dec000][v131072].nup`).
- One download: `OoT-KeyboardMouse-v1.2.0.zip` from the [latest release](../../releases/latest) (scroll down to **Assets**).

Tested on Fritchii v4 and on a locally built Lichii "build 116".

The mod files come from the game, so they are **not** in the code folders of this repository. They are only in the release zip. The keys file is also in this repository as [`profile/OoT-Keyboard-Mouse.ini`](../profile/OoT-Keyboard-Mouse.ini) and is attached to the release on its own.

## What is inside the zip

```
OoT-KeyboardMouse-v1.2.0\
├─ READ-ME-FIRST.txt
├─ load\0400486024DEC000\ButtonPrompts-KeyboardMouse\romfs\...    the icons
└─ config\input\OoT-Keyboard-Mouse.ini                            the keys
```

The two folders `load` and `config` have the same names and layout as Lichii's own data folder, so installing is just copying them in.

## Step 1 – Extract the zip

Right-click the zip → **Extract All**. Do not drag files out of the zip window: extract first.

## Step 2 – Open Lichii's data folder

Open Lichii and click **File → Open Lichii Folders → Root Data Folder**. A Windows folder opens. This is where Lichii keeps its settings, mods and saves (a folder named `user` next to `lichii.exe` in portable setups). Leave it open next to the extracted folder.

## Step 3 – Copy `load` and `config` into it

Select the folders **`load`** and **`config`** from the extracted folder and drag them into the Root Data Folder window.

If Windows says the destination already contains a folder with that name, click **Yes** (or **Continue**). Windows merges the folders: it adds our files and deletes nothing of yours.

Check the result by opening the folders:

```
Root Data Folder
├─ load
│  └─ 0400486024DEC000
│     └─ ButtonPrompts-KeyboardMouse
│        └─ romfs
│           ├─ Font2\Scalable\External.Nin_Ounce_NVN2.bfotf.zs
│           └─ UI\Layout2Archive\Common.Product.100.Nin_Ounce_NVN2.bntx.zs
└─ config
   └─ input
      └─ OoT-Keyboard-Mouse.ini
```

Keep `ButtonPrompts-KeyboardMouse` as the **only** folder starting with `ButtonPrompts-` inside `0400486024DEC000` (move any PlayStation, Xbox or Steam Deck button-prompt mods out). Two of them replace the same game files and only one wins.

If your Lichii has no "Root Data Folder" entry: right-click the game in the game list → **Open Mod Data Location**, then go up two folders. That is the Root Data Folder.

## Step 4 – Load the keys in Lichii

1. Click **Emulation → Configure → Controls**.
2. Pick **Player 1** and make sure the type is **Pro Controller**.
3. In the **Profile** box choose **OoT-Keyboard-Mouse**, click **Load**, then **OK**.

This replaces your current Player 1 layout. To keep a gamepad layout, click **New** in the Profile box and save it under a name before loading the keyboard profile.

If `OoT-Keyboard-Mouse` is not in the Profile list, the `.ini` is not in `config\input`. Check Step 3, then close and reopen Lichii.

## Step 5 – Play (repeat this every time you open the game)

1. Start the game and wait until you can move the green hat kid. The first launch builds shaders and can take several minutes.
2. **Click once on the game window.**
3. Press **Ctrl + F9** one time.
4. Move the mouse: the camera turns and the cursor disappears after a few seconds.

Why: Lichii forgets "mouse panning" every time it closes, so it must be switched on each launch. Ctrl+F9 works like a switch, so press it only once. If the cursor came back, press it again. The key only works when the emulator window is the one in front, which is why you click it first.

A Lichii compiled with the [patches](../lichii-patches/README.md) does Step 5 by itself. Official and prebuilt builds do not have them.

## Check that it works

- Moving the mouse turns the camera and no cursor is visible.
- WASD moves the green hat kid, left click attacks, right click uses the item.
- The action button shows a key (Space) and the attack button shows a mouse with the left button filled.
- **Enter → Basic Controls** shows a keyboard and a mouse with guide lines to each key.

If you still see Switch or PlayStation buttons, the icon folder is not where Lichii looks: see [TROUBLESHOOTING.md](TROUBLESHOOTING.md). The log (`user\log\eden_log.txt`) of some builds prints `LayeredFS layer 'ButtonPrompts-KeyboardMouse'`; others only print `LayeredFS patches applied successfully`, so the in-game check above is the one to trust.

## If you change keys later

The icons in the game are pictures of the default keys and do not follow your changes. If you rebind a key in Lichii, the new key works but the game still shows the old one. To make the icons match, rebuild the mod: [CONFIGURATION.md](CONFIGURATION.md#after-changing-keys-update-the-icons).

## Uninstall

Delete the `ButtonPrompts-KeyboardMouse` folder from `load\0400486024DEC000` and the `.ini` from `config\input`, restore your gamepad layout in **Emulation → Configure → Controls**, and restart the game.

## Cautions

- Edit `qt-config.ini` **only while Lichii is closed**: the emulator rewrites the file when it exits and discards manual edits.
- The mod's files have exactly the same size as the originals (the game keeps file sizes in an RSTB): do not re-save them with other tools.
