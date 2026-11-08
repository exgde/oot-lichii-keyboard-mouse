# Installation

Five short steps, about five minutes. Keys and mouse speed live in **one text file** that you can edit in Notepad.

**You need:**

- Lichii (or a fork such as Fritchii) for Windows, with OOT for Switch 2 already running in it (version 2.0.0, `[0400486024dec000][v131072].nup`).
- One download: `OoT-KeyboardMouse-v1.3.0.zip` from the [latest release](../../releases/latest) (scroll down to **Assets**).

Tested on Fritchii v4 and on a locally built Lichii "build 116".

The mod files come from the game, so they are **not** in the code folders of this repository. They are only in the release zip. The settings files are also in this repository, in [`settings/`](../settings).

## What is inside the zip

```
OoT-KeyboardMouse-v1.3.0\
├─ READ-ME-FIRST.txt
├─ OoT-Keyboard-Mouse-Settings.ini                                 your keys and mouse speed (edit this)
├─ Apply-Settings.bat                                              double-click to apply the .ini
├─ Apply-Settings.ps1                                              what the .bat runs
├─ load\0400486024DEC000\ButtonPrompts-KeyboardMouse\romfs\...     the icons
└─ config\input\OoT-Keyboard-Mouse.ini                             the same keys as a Lichii profile (backup way, see below)
```

`load` and `config` have the same names and layout as Lichii's own data folder, so installing is copying everything in.

## Step 1 – Extract the zip

Right-click the zip → **Extract All**. Do not drag files out of the zip window: extract first.

## Step 2 – Open Lichii's data folder

Open Lichii and click **File → Open Lichii Folders → Root Data Folder**. A Windows folder opens. This is where Lichii keeps its settings, mods and saves (a folder named `user` next to `lichii.exe` in portable setups). Leave it open next to the extracted folder.

## Step 3 – Copy everything into it

In the extracted folder press **Ctrl+A** (select all) and drag it all into the Root Data Folder window.

If Windows says the destination already contains a folder with that name (`load` or `config`), click **Yes** (or **Continue**). Windows merges the folders: it adds our files and deletes nothing of yours.

Check the result:

```
Root Data Folder
├─ OoT-Keyboard-Mouse-Settings.ini
├─ Apply-Settings.bat
├─ Apply-Settings.ps1
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

## Step 4 – Apply the settings

1. **Close Lichii.** (It rewrites its settings when it exits, which would undo this step.)
2. In the Root Data Folder, double-click **`Apply-Settings.bat`**.
3. A black window lists the keys and mouse values it applied and ends with **Done**. Press any key to close it.

That sets up Player 1 for keyboard and mouse. It keeps a copy of your previous settings as `config\qt-config.ini.pre-keyboard-mouse`, so you can go back.

If Windows shows a blue **"Windows protected your PC"** box, click **More info → Run anyway**. The `.bat` and `.ps1` are plain text: right-click → Edit to read what they do. They only touch the files in this folder.

## Step 5 – Play (repeat this every time you open the game)

1. Start the game and wait until you can move the green hat kid. The first launch builds shaders and can take several minutes.
2. **Click once on the game window.**
3. Press **Ctrl + F9** one time.
4. Move the mouse: the camera turns and the cursor disappears after a few seconds.

Why: Lichii forgets "mouse panning" every time it closes, so it must be switched on each launch. Ctrl+F9 works like a switch, so press it only once. If the cursor came back, press it again. The key only works when the emulator window is the one in front, which is why you click it first.

A Lichii compiled with the [patches](../lichii-patches/README.md) does Step 5 by itself. Official and prebuilt builds do not have them.

## Change keys or mouse speed later

1. Open **`OoT-Keyboard-Mouse-Settings.ini`** (in the Root Data Folder) with Notepad.
2. Change a line, for example `button_a = shift` or `mouse_sens = 3.3`, and save.
3. Close Lichii and double-click **`Apply-Settings.bat`** again.

Every setting is explained inside the file, and [CONFIGURATION.md](CONFIGURATION.md) lists them all. If a line is misspelled, the script says which one and changes nothing.

## Check that it works

- Moving the mouse turns the camera and no cursor is visible.
- WASD moves the green hat kid, left click attacks, right click uses the item.
- The action button shows a key (Space) and the attack button shows a mouse with the left button filled.
- **Enter → Basic Controls** shows a keyboard and a mouse with guide lines to each key.

If you still see Switch or PlayStation buttons, the icon folder is not where Lichii looks: see [TROUBLESHOOTING.md](TROUBLESHOOTING.md). The log (`user\log\eden_log.txt`) of some builds prints `LayeredFS layer 'ButtonPrompts-KeyboardMouse'`; others only print `LayeredFS patches applied successfully`, so the in-game check above is the one to trust.

## The icons do not follow your keys

The pictures drawn in the game (HUD, Basic Controls screen) show the **default** keys. If you change a key in the settings file, the new key works but the game still shows the old picture. To redraw the pictures for your keys, rebuild the mod: [CONFIGURATION.md](CONFIGURATION.md#after-changing-keys-update-the-icons).

## Without the script (backup way)

If you do not want to run the `.bat`: skip Step 4, open Lichii, go to **Emulation → Configure → Controls**, pick **Player 1** (type **Pro Controller**), choose the profile **OoT-Keyboard-Mouse** in the **Profile** box, click **Load**, then **OK**. This gives the default keys (the settings file is not used).

## Uninstall

Delete the `ButtonPrompts-KeyboardMouse` folder from `load\0400486024DEC000`, the `.ini` and the two `Apply-Settings` files from the Root Data Folder, and `OoT-Keyboard-Mouse.ini` from `config\input`. To get your gamepad layout back, close Lichii and copy `config\qt-config.ini.pre-keyboard-mouse` over `config\qt-config.ini`. Then restart the game.

## Cautions

- Edit `qt-config.ini` **only while Lichii is closed**: the emulator rewrites the file when it exits and discards manual edits. `Apply-Settings.bat` refuses to run while Lichii is open for that reason.
- The mod's files have exactly the same size as the originals (the game keeps file sizes in an RSTB): do not re-save them with other tools.
