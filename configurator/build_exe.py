"""Builds OoT-KeyboardMouse-Config.exe (one file) and its release zip.

    python configurator/build_exe.py --icons <folder ButtonPrompts-KeyboardMouse> --capture <OoT-MouseCapture.exe>
                                     [--version 1.4.0] [--out out]

Needs: Python 3.10+ with the packages of tools/requirements.txt, plus pyinstaller.
The icon files come from the game (built by tools/build_mod.py from your own .nup); they are bundled inside the exe
so that it can install the mod by itself.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TITLE = '0400486024DEC000'
BUILD_ID = 'E0F3CCFAF50065AE4EA01EB5AEB13B1A45DA3348'
TOOL_MODULES = ['oot_paths', 'zs', 'glyphlib', 'nup_tool', 'ctrl_common', 'tex_build', 'build_fonts_kbm']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--icons', required=True)
    ap.add_argument('--capture', required=True)
    ap.add_argument('--version', default='1.4.0')
    ap.add_argument('--out', default=os.path.join(REPO, 'out'))
    a = ap.parse_args()

    with tempfile.TemporaryDirectory() as t:
        pay = os.path.join(t, 'payload')
        icons_dst = os.path.join(pay, 'load', TITLE, 'ButtonPrompts-KeyboardMouse')
        shutil.copytree(a.icons, icons_dst)
        cam = os.path.join(pay, 'load', TITLE, 'MouseCamera-Native', 'exefs')
        os.makedirs(cam)
        shutil.copyfile(os.path.join(REPO, 'native-camera', 'MouseCamera-Native', 'exefs', BUILD_ID + '.ips'),
                        os.path.join(cam, BUILD_ID + '.ips.off'))
        os.makedirs(os.path.join(pay, 'config', 'input'))
        shutil.copyfile(os.path.join(REPO, 'settings', 'OoT-Keyboard-Mouse.ini'),
                        os.path.join(pay, 'config', 'input', 'OoT-Keyboard-Mouse.ini'))
        for f in ('Apply-Settings.ps1', 'Apply-Settings.bat', 'OoT-Keyboard-Mouse-Settings.ini'):
            shutil.copyfile(os.path.join(REPO, 'settings', f), os.path.join(pay, f))
        shutil.copyfile(a.capture, os.path.join(pay, 'OoT-MouseCapture.exe'))

        cmd = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--onefile', '--windowed',
               '--name', 'OoT-KeyboardMouse-Config', '--distpath', os.path.join(t, 'dist'),
               '--workpath', os.path.join(t, 'build'), '--specpath', t,
               '--paths', os.path.join(REPO, 'tools'), '--paths', HERE,
               '--add-data', pay + os.pathsep + 'payload']
        for m in TOOL_MODULES:
            cmd += ['--hidden-import', m]
        cmd += ['--hidden-import', 'fontTools.subset', '--collect-submodules', 'fontTools.ttLib.tables',
                '--collect-data', 'archspec', '--collect-all', 'astc_encoder', '--collect-all', 'texture2ddecoder',
                os.path.join(HERE, 'oot_kbm_config.py')]
        subprocess.run(cmd, check=True)
        exe = os.path.join(t, 'dist', 'OoT-KeyboardMouse-Config.exe')

        os.makedirs(a.out, exist_ok=True)
        shutil.copyfile(exe, os.path.join(a.out, 'OoT-KeyboardMouse-Config.exe'))
        top = 'OoT-KeyboardMouse-Config-v%s' % a.version
        zpath = os.path.join(a.out, top + '.zip')
        with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(exe, top + '/OoT-KeyboardMouse-Config.exe')
            for name in ('READ-ME-CONFIG.txt', 'LEIA-ME-CONFIG.txt'):
                z.write(os.path.join(REPO, 'release-notes', name), top + '/' + name)
        print('exe ', os.path.join(a.out, 'OoT-KeyboardMouse-Config.exe'), os.path.getsize(exe), 'bytes')
        print('zip ', zpath, os.path.getsize(zpath), 'bytes')


if __name__ == '__main__':
    main()
