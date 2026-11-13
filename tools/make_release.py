"""Builds the release zip: OoT-KeyboardMouse-v<version>.zip

    python tools/make_release.py --version 1.4.0 --icons <folder of ButtonPrompts-KeyboardMouse> --exe <OoT-MouseCapture.exe>

Layout of the zip (one top folder, so "Extract All" gives one clean folder):
    OoT-KeyboardMouse-v<version>/
        READ-ME-FIRST.txt, LEIA-ME.txt          (from release-notes/)
        INSTALL.bat, Install.ps1                 the installer
        Apply-Settings.bat, Apply-Settings.ps1   applies the settings file again later
        OoT-Keyboard-Mouse-Settings.ini          keys and mouse
        OoT-MouseCapture.exe                     mouse helper for mouse_camera = native
        load/0400486024DEC000/ButtonPrompts-KeyboardMouse/romfs/...   the icons (from the game: not in git)
        load/0400486024DEC000/MouseCamera-Native/exefs/<build id>.ips.off   the native camera patch, off until chosen
        config/input/OoT-Keyboard-Mouse.ini     the keys as a Lichii profile (manual way)
"""
import argparse
import hashlib
import os
import sys
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TITLE = '0400486024DEC000'
BUILD_ID = 'E0F3CCFAF50065AE4EA01EB5AEB13B1A45DA3348'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', required=True)
    ap.add_argument('--icons', required=True, help='folder ButtonPrompts-KeyboardMouse (with romfs inside)')
    ap.add_argument('--exe', required=True, help='OoT-MouseCapture.exe (native-camera/helper/build.bat)')
    ap.add_argument('--out', default=os.path.join(REPO, 'out'))
    a = ap.parse_args()

    top = f'OoT-KeyboardMouse-v{a.version}'
    files = []  # (path in zip, source path)
    for name in ('READ-ME-FIRST.txt', 'LEIA-ME.txt'):
        files.append((name, os.path.join(REPO, 'release-notes', name)))
    for name in ('INSTALL.bat', 'Install.ps1', 'Apply-Settings.bat', 'Apply-Settings.ps1', 'OoT-Keyboard-Mouse-Settings.ini'):
        files.append((name, os.path.join(REPO, 'settings', name)))
    files.append(('OoT-MouseCapture.exe', a.exe))
    for root, _, names in os.walk(os.path.join(a.icons, 'romfs')):
        for n in names:
            src = os.path.join(root, n)
            rel = os.path.relpath(src, a.icons).replace(os.sep, '/')
            files.append((f'load/{TITLE}/ButtonPrompts-KeyboardMouse/{rel}', src))
    files.append((f'load/{TITLE}/MouseCamera-Native/exefs/{BUILD_ID}.ips.off',
                  os.path.join(REPO, 'native-camera', 'MouseCamera-Native', 'exefs', BUILD_ID + '.ips')))
    files.append(('config/input/OoT-Keyboard-Mouse.ini', os.path.join(REPO, 'settings', 'OoT-Keyboard-Mouse.ini')))

    missing = [s for _, s in files if not os.path.isfile(s)]
    if missing:
        sys.exit('missing:\n  ' + '\n  '.join(missing))
    if not any('/romfs/' in z for z, _ in files):
        sys.exit('no icon files found under ' + a.icons)

    os.makedirs(a.out, exist_ok=True)
    zpath = os.path.join(a.out, top + '.zip')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for arc, src in files:
            z.write(src, f'{top}/{arc}')
    h = hashlib.sha256(open(zpath, 'rb').read()).hexdigest()
    print(f'{zpath}\n  {len(files)} files, {os.path.getsize(zpath):,} bytes, sha256 {h}')


if __name__ == '__main__':
    main()
