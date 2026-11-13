"""OOT keyboard + mouse configurator for Lichii (and its forks).

Pick keys and mouse settings, click Apply: the program installs or updates the mod in Lichii's data folder,
writes OoT-Keyboard-Mouse-Settings.ini (the same file the manual way uses), runs Apply-Settings.ps1 on it, and
redraws the in-game key icons when keys changed (that needs the game's .nup once).
"""
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import icons

APP = 'OOT keyboard + mouse settings'
TITLE = '0400486024DEC000'
HERE = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))
PAYLOAD = os.path.join(HERE, 'payload')
STATE_DIR = os.path.join(os.environ.get('LOCALAPPDATA') or os.path.expanduser('~'), 'OoT-KeyboardMouse')
CACHE = os.path.join(STATE_DIR, 'game-files')
STATE_FILE = os.path.join(STATE_DIR, 'configurator.json')
SETTINGS_NAME = 'OoT-Keyboard-Mouse-Settings.ini'
EMULATORS = re.compile(r'^(lichii|eden|yuzu|citron|sudachi|suyu|torzu|fritchii)', re.I)

BUTTONS = [  # setting, what it does in the game
    ('button_y', 'Attack (Y)'), ('button_a', 'Action / hold to run (A)'), ('button_zr', 'Use item (ZR)'),
    ('button_zl', 'Target, hold (ZL)'), ('button_l', 'Quick select items, left (L)'),
    ('button_r', 'Quick select items, right (R)'), ('button_r3', 'Reset camera (right stick press)'),
    ('button_b', 'B'), ('button_x', 'X'), ('button_plus', 'Menu (+)'), ('button_minus', 'Map (-)'),
    ('dpad_up', 'Accessory (D-pad up)'), ('dpad_left', 'Ocarina (D-pad left)'), ('dpad_right', 'Navi (D-pad right)'),
    ('dpad_down', 'Boots (D-pad down)'), ('button_l3', 'Left stick press'), ('button_home', 'Home'),
    ('button_screenshot', 'Capture'),
]
MOVES = [('move_up', 'Move forward'), ('move_down', 'Move back'), ('move_left', 'Move left'),
         ('move_right', 'Move right'), ('walk_key', 'Walk slowly (hold)')]
DEFAULTS = {
    'button_y': 'mouse_left', 'button_a': 'space', 'button_b': 'c', 'button_x': 'r', 'button_zl': 'shift',
    'button_zr': 'mouse_right', 'button_l': 'q', 'button_r': 'e', 'button_r3': 'mouse_middle', 'button_l3': 'none',
    'button_plus': 'enter', 'button_minus': 'tab', 'dpad_up': '1', 'dpad_left': '2', 'dpad_right': '3', 'dpad_down': '4',
    'button_home': 'none', 'button_screenshot': 'none', 'move_up': 'w', 'move_down': 's', 'move_left': 'a',
    'move_right': 'd', 'walk_key': 'z', 'walk_speed': '0.5', 'mouse_sens': '5.0', 'mouse_sens_x': '', 'mouse_sens_y': '',
    'mouse_invert_y': 'false', 'mouse_camera': 'stick', 'mouse_deadzone_boost': '20', 'mouse_stop_speed': '18',
    'mouse_min_decay': '6', 'hide_cursor': 'true',
}
ICON_KEYS = ['button_a', 'button_b', 'button_x', 'button_y', 'button_l', 'button_r', 'button_zl', 'button_zr',
             'button_r3', 'button_plus', 'button_minus', 'dpad_up', 'dpad_left', 'dpad_right', 'dpad_down',
             'move_up', 'move_down', 'move_left', 'move_right']
KEY_NAMES = (['mouse_left', 'mouse_right', 'mouse_middle', 'mouse_back', 'mouse_forward', 'space', 'shift', 'enter',
              'tab', 'backspace', 'capslock', 'up', 'down', 'left', 'right', 'insert', 'delete', 'home', 'end',
              'pageup', 'pagedown', 'ctrl', 'alt', 'esc'] + [chr(c) for c in range(ord('a'), ord('z') + 1)]
             + [str(d) for d in range(10)] + ['f%d' % i for i in range(1, 13)]
             + ['comma', 'period', 'minus', 'equals', 'slash', 'backslash', 'semicolon', 'apostrophe',
                'bracketleft', 'bracketright', 'grave', 'none'])
TK_KEYS = {'space': 'space', 'Return': 'enter', 'KP_Enter': 'enter', 'Tab': 'tab', 'BackSpace': 'backspace',
           'Escape': 'esc', 'Shift_L': 'shift', 'Shift_R': 'shift', 'Control_L': 'ctrl', 'Control_R': 'ctrl',
           'Alt_L': 'alt', 'Alt_R': 'alt', 'Caps_Lock': 'capslock', 'Up': 'up', 'Down': 'down', 'Left': 'left',
           'Right': 'right', 'Insert': 'insert', 'Delete': 'delete', 'Home': 'home', 'End': 'end', 'Prior': 'pageup',
           'Next': 'pagedown', 'comma': 'comma', 'period': 'period', 'minus': 'minus', 'equal': 'equals',
           'slash': 'slash', 'backslash': 'backslash', 'semicolon': 'semicolon', 'apostrophe': 'apostrophe',
           'quoteright': 'apostrophe', 'bracketleft': 'bracketleft', 'bracketright': 'bracketright', 'grave': 'grave',
           'quoteleft': 'grave'}


# ---------------------------------------------------------------- Lichii data folder
def is_data_folder(p):
    return bool(p) and os.path.isfile(os.path.join(p, 'config', 'qt-config.ini'))


def normalise_folder(p):
    """Accepts the data folder itself, a portable Lichii folder (with user\\) or the user folder."""
    if not p:
        return None
    p = os.path.abspath(p)
    if is_data_folder(p):
        return p
    if is_data_folder(os.path.join(p, 'user')):
        return os.path.join(p, 'user')
    return None


def find_data_folders():
    out = []
    appdata = os.environ.get('APPDATA', '')
    for name in ('lichii', 'Lichii', 'fritchii', 'Fritchii', 'eden', 'Eden'):
        p = normalise_folder(os.path.join(appdata, name))
        if p and p.lower() not in [o.lower() for o in out]:
            out.append(p)
    return out


def load_state():
    try:
        return json.load(open(STATE_FILE, encoding='utf-8'))
    except Exception:
        return {}


def save_state(st):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        json.dump(st, open(STATE_FILE, 'w', encoding='utf-8'), indent=1)
    except Exception:
        pass


def emulator_running():
    try:
        out = subprocess.run(['tasklist', '/FO', 'CSV', '/NH'], capture_output=True, text=True,
                             creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout
    except Exception:
        return None
    for line in out.splitlines():
        name = line.split('","')[0].strip('"')
        if EMULATORS.match(name):
            return name
    return None


def helper_running():
    try:
        out = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq OoT-MouseCapture.exe', '/FO', 'CSV', '/NH'],
                             capture_output=True, text=True,
                             creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout
    except Exception:
        return False
    return 'oot-mousecapture.exe' in out.lower()


# ---------------------------------------------------------------- settings file (same format as the manual way)
def read_settings(path):
    vals = dict(DEFAULTS)
    if not os.path.isfile(path):
        return vals
    for raw in open(path, encoding='utf-8-sig', errors='replace'):
        line = raw.strip()
        if not line or line[0] in ';#[' or '=' not in line:
            continue
        name, value = line.split('=', 1)
        name = name.strip().lower()
        if name in vals:
            vals[name] = value.split(';', 1)[0].strip()
    return vals


def write_settings(template, path, vals):
    lines = open(template, encoding='utf-8-sig').read().splitlines()
    out, seen = [], set()
    for line in lines:
        m = re.match(r'^(\s*([A-Za-z0-9_]+)\s*=)([^;]*?)(\s*(;.*)?)$', line)
        if m and m.group(2).lower() in vals:
            name = m.group(2).lower()
            seen.add(name)
            old = m.group(3)
            new = ' ' + vals[name]
            pad = len(old) - len(new)
            line = m.group(1) + new + (' ' * pad if pad > 0 and m.group(5) else '') + (m.group(4) if m.group(5) else '')
        out.append(line)
    missing = [n for n in vals if n not in seen]
    if missing:
        out.append('')
        out.append('[configurator]')
        out += ['%s = %s' % (n, vals[n]) for n in missing]
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('\n'.join(out) + '\n')
    os.replace(tmp, path)


# ---------------------------------------------------------------- the .nup for the icons
def guess_nup(root):
    """Looks for the OOT .nup in Lichii's game folders and recent files."""
    qt = os.path.join(root, 'config', 'qt-config.ini')
    dirs, files = [], []
    try:
        for line in open(qt, encoding='utf-8', errors='replace'):
            if '=' not in line:
                continue
            k, v = line.rstrip('\n').split('=', 1)
            v = v.strip().strip('"')
            if k.endswith('\\path') and os.path.isdir(v):
                dirs.append(v)
            for part in v.split(', '):
                part = part.strip().strip('"')
                if part.lower().endswith('.nup'):
                    files.append(part)
    except Exception:
        pass
    for p in files:
        if os.path.isfile(p) and TITLE.lower() in os.path.basename(p).lower():
            return p
    for d in dirs:
        try:
            for n in os.listdir(d):
                if n.lower().endswith('.nup') and TITLE.lower() in n.lower():
                    return os.path.join(d, n)
        except Exception:
            pass
    return None


# ---------------------------------------------------------------- install + apply (runs in a worker thread)
def install_payload(root, log):
    load = os.path.join(root, 'load', TITLE)
    os.makedirs(load, exist_ok=True)
    for d in sorted(os.listdir(load)):
        if d.startswith('ButtonPrompts-') and d != 'ButtonPrompts-KeyboardMouse' and os.path.isdir(os.path.join(load, d)):
            backup = os.path.join(root, 'mod-backups')
            os.makedirs(backup, exist_ok=True)
            dest = os.path.join(backup, d)
            n = 2
            while os.path.exists(dest):
                dest = os.path.join(backup, '%s-%d' % (d, n))
                n += 1
            shutil.move(os.path.join(load, d), dest)
            log('Moved %s to mod-backups (only one button-icon mod can be active).' % d)
    src_icons = os.path.join(PAYLOAD, 'load', TITLE, 'ButtonPrompts-KeyboardMouse')
    dst_icons = os.path.join(load, 'ButtonPrompts-KeyboardMouse')
    for rel in (icons.FONT_REL, icons.BNTX_REL):
        os.makedirs(os.path.dirname(os.path.join(dst_icons, rel)), exist_ok=True)
        shutil.copyfile(os.path.join(src_icons, rel), os.path.join(dst_icons, rel))
    cam_src = os.path.join(PAYLOAD, 'load', TITLE, 'MouseCamera-Native', 'exefs')
    cam_dst = os.path.join(load, 'MouseCamera-Native', 'exefs')
    os.makedirs(cam_dst, exist_ok=True)
    for f in os.listdir(cam_src):                          # <build id>.ips.off
        on = os.path.join(cam_dst, f[:-4])
        shutil.copyfile(os.path.join(cam_src, f), on if os.path.exists(on) else os.path.join(cam_dst, f))
    os.makedirs(os.path.join(root, 'config', 'input'), exist_ok=True)
    shutil.copyfile(os.path.join(PAYLOAD, 'config', 'input', 'OoT-Keyboard-Mouse.ini'),
                    os.path.join(root, 'config', 'input', 'OoT-Keyboard-Mouse.ini'))
    for f in ('Apply-Settings.ps1', 'Apply-Settings.bat', 'OoT-MouseCapture.exe'):
        shutil.copyfile(os.path.join(PAYLOAD, f), os.path.join(root, f))
    log('Mod files are in place.')


def run_apply_settings(root, log):
    cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', os.path.join(root, 'Apply-Settings.ps1'),
           '-Root', root]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=root,
                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    text = (p.stdout or '') + (p.stderr or '')
    for line in text.splitlines():
        s = line.rstrip()
        skip = ('Keys', 'Mouse', 'Note: you changed keys', 'default keys (see docs', 'Each time you play', '1. Start', '2. Start',
                'Alt+Tab gives')
        if s.strip() and not s.lstrip().startswith(skip) and 'Done.' not in s and not s.startswith('    '):
            log(s.strip())
    if p.returncode != 0:
        raise RuntimeError('Apply-Settings stopped:\n' + '\n'.join(l.strip() for l in text.splitlines() if 'ERROR' in l))


# ---------------------------------------------------------------- undo: Lichii back to how it was before the mod
# The qt-config.ini lines the mod changes (Apply-Settings.ps1): Player 1 and the mouse values. Everything else
# (graphics, other players, games...) stays as it is now.
MOD_QT_KEYS = {
    'Controls': re.compile(r'^(player_0_\w+|mouse_enabled|mouse_panning_(x_sensitivity|y_sensitivity|'
                           r'deadzone_counterweight|decay_strength|min_decay))(\\default)?='),
    'UI': re.compile(r'^hideInactiveMouse(\\default)?='),
}
QT_BACKUP = '.pre-keyboard-mouse'          # Apply-Settings.ps1 copies qt-config.ini to this once, before its first change


def _read_lines(path):
    text = open(path, encoding='utf-8', newline='').read()
    eol = '\r\n' if '\r\n' in text else '\n'
    return text.replace('\r\n', '\n').split('\n'), eol


def _section_range(lines, name):
    start = None
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith('[') and s.endswith(']'):
            if start is not None:
                return start, i
            if s[1:-1] == name:
                start = i
    return (start, len(lines)) if start is not None else None


def restore_input_settings(qt_path, backup_path):
    """Puts the mod's lines (MOD_QT_KEYS) of qt-config.ini back to their values in backup_path, in place: a line the
    old file did not have is removed, one only the old file had is added. Returns how many lines changed."""
    cur, eol = _read_lines(qt_path)
    old, _ = _read_lines(backup_path)
    changed = 0
    for section, pat in MOD_QT_KEYS.items():
        orng = _section_range(old, section)
        old_lines = [l for l in old[orng[0] + 1:orng[1]] if pat.match(l)] if orng else []
        old_by_key = {l.split('=', 1)[0]: l for l in old_lines}
        crng = _section_range(cur, section)
        if crng is None:
            if old_lines:
                cur += ['[%s]' % section] + old_lines + ['']
                changed += len(old_lines)
            continue
        body, seen = [], set()
        for l in cur[crng[0] + 1:crng[1]]:
            if not pat.match(l):
                body.append(l)
                continue
            key = l.split('=', 1)[0]
            if key in old_by_key:
                seen.add(key)
                body.append(old_by_key[key])
                changed += old_by_key[key] != l
            else:
                changed += 1                    # added by the mod
        missing = [l for l in old_lines if l.split('=', 1)[0] not in seen]
        at = len(body)
        while at > 0 and body[at - 1].strip() == '':
            at -= 1
        body[at:at] = missing
        changed += len(missing)
        cur = cur[:crng[0] + 1] + body + cur[crng[1]:]
    tmp = qt_path + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write(eol.join(cur))
    os.replace(tmp, qt_path)
    return changed


def _move_unique(path, folder):
    os.makedirs(folder, exist_ok=True)
    base = os.path.basename(path)
    dest, n = os.path.join(folder, base), 2
    while os.path.exists(dest):
        dest = os.path.join(folder, '%s-%d' % (base, n))
        n += 1
    shutil.move(path, dest)
    return dest


def undo_mod(root, log):
    """Lichii as it was before the mod: Player 1 and mouse settings from the copy made before the first change,
    the mod's files removed, other button-icon mods the installers moved to mod-backups put back. The settings file
    (your keys) and the old qt-config.ini copy are kept in mod-backups. Returns False when there was no copy."""
    load = os.path.join(root, 'load', TITLE)
    backups = os.path.join(root, 'mod-backups')
    qt = os.path.join(root, 'config', 'qt-config.ini')
    restored = False
    if os.path.isfile(qt + QT_BACKUP):
        n = restore_input_settings(qt, qt + QT_BACKUP)
        _move_unique(qt + QT_BACKUP, backups)
        log('Controls: Player 1 and the mouse settings are back to what they were before the mod (%d lines).' % n)
        restored = True
    else:
        log('Controls: no copy of your old settings was found (config\\qt-config.ini%s), so they were not changed.'
            % QT_BACKUP)
    for d in ('ButtonPrompts-KeyboardMouse', 'MouseCamera-Native'):
        p = os.path.join(load, d)
        if os.path.isdir(p):
            shutil.rmtree(p)
            log('Removed the mod folder load\\%s\\%s.' % (TITLE, d))
    if os.path.isdir(backups):
        for d in sorted(os.listdir(backups)):
            src = os.path.join(backups, d)
            if not (os.path.isdir(src) and d.startswith('ButtonPrompts-') and not d.startswith('ButtonPrompts-KeyboardMouse')):
                continue
            name = re.sub(r'-\d+$', '', d)
            dst = os.path.join(load, name)
            if os.path.exists(dst):
                log('Left %s in mod-backups (load already has %s).' % (d, name))
                continue
            os.makedirs(load, exist_ok=True)
            shutil.move(src, dst)
            log('Put back the mod %s (it was in mod-backups).' % name)
    for rel in (('config', 'input', 'OoT-Keyboard-Mouse.ini'), ('Apply-Settings.ps1',), ('Apply-Settings.bat',),
                ('OoT-MouseCapture.exe',)):
        p = os.path.join(root, *rel)
        if os.path.isfile(p):
            os.remove(p)
    for f in (SETTINGS_NAME, 'OoT-Keyboard-Mouse-Settings.new.ini'):
        p = os.path.join(root, f)
        if os.path.isfile(p):
            _move_unique(p, backups)
    log('Removed the mod\'s files. Your settings file (your keys) is kept in the mod-backups folder.')
    return restored


# ---------------------------------------------------------------- the window
class App:
    def __init__(self, tk_root):
        self.tk = tk_root
        self.state = load_state()
        self.q = queue.Queue()
        self.vars = {}
        tk_root.title(APP)
        tk_root.minsize(640, 600)
        try:
            tk_root.iconbitmap(os.path.join(HERE, 'icon.ico'))
        except Exception:
            pass
        self.build()
        self.pick_initial_folder()
        self.tk.after(100, self.poll)

    # ---- layout
    def build(self):
        pad = dict(padx=8, pady=4)
        top = ttk.Frame(self.tk)
        top.pack(fill='x', **pad)
        ttk.Label(top, text='Lichii data folder:').pack(side='left')
        self.folder = tk.StringVar()
        ttk.Entry(top, textvariable=self.folder, state='readonly').pack(side='left', fill='x', expand=True, padx=6)
        ttk.Button(top, text='Change...', command=self.choose_folder).pack(side='left')

        nb = ttk.Notebook(self.tk)
        nb.pack(fill='both', expand=True, **pad)
        nb.add(self.key_page(nb, BUTTONS), text='Buttons')
        mv = self.key_page(nb, MOVES)
        ttk.Label(mv, text='Walk speed while holding the walk key (0.1 = very slow, 1.0 = no change):').grid(
            row=len(MOVES) + 1, column=0, columnspan=3, sticky='w', pady=(12, 0))
        self.vars['walk_speed'] = tk.DoubleVar(value=0.5)
        self.scale(mv, 'walk_speed', 0.1, 1.0, len(MOVES) + 2)
        nb.add(mv, text='Movement')
        nb.add(self.mouse_page(nb), text='Mouse and camera')

        self.warn = ttk.Label(self.tk, foreground='#a04000', wraplength=600, justify='left')
        self.warn.pack(fill='x', **pad)
        bar = ttk.Frame(self.tk)
        bar.pack(fill='x', **pad)
        ttk.Button(bar, text='Default settings', command=self.defaults).pack(side='left')
        self.undo_btn = ttk.Button(bar, text='Undo mod changes...', command=self.undo)
        self.undo_btn.pack(side='left', padx=(8, 0))
        self.apply_btn = ttk.Button(bar, text='Apply', command=self.apply)
        self.apply_btn.pack(side='right')
        self.log_box = tk.Text(self.tk, height=9, state='disabled', wrap='word', relief='flat', background='#f4f4f4')
        self.log_box.pack(fill='both', expand=False, **pad)
        self.log('Close Lichii, choose your keys and mouse settings, then click Apply.')

    def key_page(self, parent, rows):
        f = ttk.Frame(parent, padding=10)
        ttk.Label(f, text='In the game', font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky='w')
        ttk.Label(f, text='Key or mouse button', font=('Segoe UI', 9, 'bold')).grid(row=0, column=1, sticky='w')
        for i, (name, label) in enumerate(rows, start=1):
            ttk.Label(f, text=label).grid(row=i, column=0, sticky='w', pady=2)
            v = tk.StringVar(value=DEFAULTS[name])
            v.trace_add('write', lambda *_: self.check())
            self.vars[name] = v
            ttk.Combobox(f, textvariable=v, values=KEY_NAMES, width=16).grid(row=i, column=1, sticky='w', padx=6)
            ttk.Button(f, text='Press a key...', command=lambda n=name, l=label: self.capture(n, l)).grid(
                row=i, column=2, sticky='w')
        f.columnconfigure(0, weight=1)
        return f

    def scale(self, parent, name, lo, hi, row, label=None):
        v = self.vars[name]
        if label:
            ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w')
        val = ttk.Label(parent, width=6)
        s = ttk.Scale(parent, from_=lo, to=hi, variable=v, orient='horizontal', length=280,
                      command=lambda *_: val.configure(text=('%.1f' if hi <= 10 else '%.0f') % v.get()))
        s.grid(row=row, column=1, sticky='w', padx=6)
        val.grid(row=row, column=2, sticky='w')
        val.configure(text=('%.1f' if hi <= 10 else '%.0f') % v.get())
        v.trace_add('write', lambda *_: val.configure(text=('%.1f' if hi <= 10 else '%.0f') % v.get()))
        return s

    def mouse_page(self, parent):
        f = ttk.Frame(parent, padding=10)
        self.vars['mouse_camera'] = tk.StringVar(value='stick')
        cam = ttk.LabelFrame(f, text='How the mouse turns the camera', padding=8)
        cam.grid(row=0, column=0, columnspan=3, sticky='ew')
        ttk.Radiobutton(cam, text='As the stick: the mouse stands in for the right stick (the game\'s curve and top speed)',
                        variable=self.vars['mouse_camera'], value='stick', command=self.check).pack(anchor='w')
        ttk.Radiobutton(cam, text='Native: the mouse turns the camera itself, 1:1, like a PC game '
                                  '(open OoT-MouseCapture.exe before playing)',
                        variable=self.vars['mouse_camera'], value='native', command=self.check).pack(anchor='w')
        for n, d in (('mouse_sens', 5.0), ('mouse_sens_x', 5.0), ('mouse_sens_y', 5.0)):
            self.vars[n] = tk.DoubleVar(value=d)
        self.scale(f, 'mouse_sens', 0.1, 10.0, 1, 'Camera speed (1 slow ... 10 fast)')
        self.split = tk.BooleanVar(value=False)
        ttk.Checkbutton(f, text='Different speed left/right and up/down', variable=self.split,
                        command=self.check).grid(row=2, column=0, columnspan=3, sticky='w', pady=(6, 0))
        self.sx = self.scale(f, 'mouse_sens_x', 0.1, 10.0, 3, '   left/right')
        self.sy = self.scale(f, 'mouse_sens_y', 0.1, 10.0, 4, '   up/down')
        self.vars['mouse_invert_y'] = tk.BooleanVar(value=False)
        ttk.Checkbutton(f, text='Invert up/down (moving the mouse up looks down)',
                        variable=self.vars['mouse_invert_y']).grid(row=5, column=0, columnspan=3, sticky='w', pady=(6, 0))
        self.vars['hide_cursor'] = tk.BooleanVar(value=True)
        ttk.Checkbutton(f, text='Hide the mouse pointer after a few idle seconds',
                        variable=self.vars['hide_cursor']).grid(row=6, column=0, columnspan=3, sticky='w')
        feel = ttk.LabelFrame(f, text='Feel of the "As the stick" mode', padding=8)
        feel.grid(row=7, column=0, columnspan=3, sticky='ew', pady=(10, 0))
        for n, d in (('mouse_deadzone_boost', 20), ('mouse_stop_speed', 18), ('mouse_min_decay', 6)):
            self.vars[n] = tk.DoubleVar(value=d)
        self.scale(feel, 'mouse_deadzone_boost', 0, 100, 0, 'Small-movement boost')
        self.scale(feel, 'mouse_stop_speed', 0, 100, 1, 'How fast it stops')
        self.scale(feel, 'mouse_min_decay', 0, 100, 2, 'Minimum slow-down')
        self.feel = feel
        f.columnconfigure(0, weight=1)
        return f

    # ---- values
    def get_values(self):
        v = {}
        for n in DEFAULTS:
            var = self.vars.get(n)
            if var is None:
                v[n] = DEFAULTS[n]
            elif isinstance(var, tk.BooleanVar):
                v[n] = 'true' if var.get() else 'false'
            elif isinstance(var, tk.DoubleVar):
                v[n] = ('%.1f' % var.get()) if n in ('mouse_sens', 'mouse_sens_x', 'mouse_sens_y', 'walk_speed') else str(int(round(var.get())))
            else:
                v[n] = var.get().strip().lower() or 'none'
        if not self.split.get():
            v['mouse_sens_x'] = v['mouse_sens_y'] = ''
        return v

    def set_values(self, vals):
        for n, val in vals.items():
            var = self.vars.get(n)
            if var is None:
                continue
            try:
                if isinstance(var, tk.BooleanVar):
                    var.set(str(val).strip().lower() in ('true', 'yes', 'on', '1'))
                elif isinstance(var, tk.DoubleVar):
                    if val != '':
                        var.set(float(str(val).replace(',', '.')))
                else:
                    var.set(val)
            except ValueError:
                pass
        split = bool(vals.get('mouse_sens_x') or vals.get('mouse_sens_y'))
        self.split.set(split)
        if split:
            for n in ('mouse_sens_x', 'mouse_sens_y'):
                if not vals.get(n):
                    self.vars[n].set(self.vars['mouse_sens'].get())
        self.check()

    def defaults(self):
        self.set_values(DEFAULTS)
        self.log('Default settings loaded (not applied yet).')

    def check(self):
        try:
            v = self.get_values()
        except Exception:
            return
        for w in (self.sx, self.sy):
            w.state(['!disabled'] if self.split.get() else ['disabled'])
        for child in self.feel.winfo_children():
            if isinstance(child, ttk.Scale):
                child.state(['!disabled'] if v['mouse_camera'] == 'stick' else ['disabled'])
        msgs, seen = [], {}
        for n, _ in BUTTONS + MOVES:
            k = v[n]
            if k in ('', 'none'):
                continue
            if k not in KEY_NAMES and not re.match(r'^code:\d{1,10}$', k):
                msgs.append('"%s" is not a key name.' % k)
            if k in seen:
                msgs.append('"%s" is used twice (%s and %s).' % (k, seen[k], n))
            seen[k] = n
            if k in ('ctrl', 'alt', 'esc'):
                msgs.append('"%s" clashes with Lichii (Ctrl+Q quits, Ctrl+F9 mouse panning, Alt menu bar, Esc fullscreen).' % k)
        if any(v[n] != DEFAULTS[n] for n in ICON_KEYS):
            msgs.append('Keys changed: on Apply the in-game key icons are redrawn for them (needs the game\'s .nup once).')
        self.warn.configure(text='\n'.join(msgs))

    # ---- folder
    def pick_initial_folder(self):
        p = normalise_folder(self.state.get('folder'))
        if not p:
            found = find_data_folders()
            p = found[0] if found else None
        self.set_folder(p)
        if not p:
            self.log('Lichii\'s data folder was not found: click "Change..." and pick it '
                     '(Lichii: File > Open Lichii Folders > Root Data Folder; portable Lichii: the folder of lichii.exe).')

    def set_folder(self, p):
        self.folder.set(p or '(not found)')
        if p:
            self.state['folder'] = p
            save_state(self.state)
            self.set_values(read_settings(os.path.join(p, SETTINGS_NAME)))

    def choose_folder(self):
        d = filedialog.askdirectory(title='Lichii data folder (or the folder of a portable lichii.exe)')
        if not d:
            return
        p = normalise_folder(d)
        if not p:
            messagebox.showerror(APP, 'That is not Lichii\'s data folder: it has no config\\qt-config.ini.\n\n'
                                      'In Lichii click File > Open Lichii Folders > Root Data Folder to see where it is. '
                                      'Never started Lichii? Start it once and close it.')
            return
        self.set_folder(p)
        self.log('Lichii data folder: ' + p)

    # ---- key capture
    def capture(self, name, label):
        w = tk.Toplevel(self.tk)
        w.title('Press a key')
        w.transient(self.tk)
        w.resizable(False, False)
        ttk.Label(w, text='%s\n\nPress a key on the keyboard, or click here with a mouse button.' % label,
                  padding=20, justify='center').pack()
        ttk.Button(w, text='Cancel', command=w.destroy).pack(pady=(0, 12))

        def done(key):
            self.vars[name].set(key)
            w.destroy()

        def on_key(e):
            k = e.keysym
            if len(k) == 1 and k.isalnum():
                done(k.lower())
            elif re.match(r'^F([1-9]|1[0-2])$', k):
                done(k.lower())
            elif k in TK_KEYS:
                done(TK_KEYS[k])
            return 'break'

        def on_click(e):
            if isinstance(e.widget, ttk.Button):
                return
            m = {1: 'mouse_left', 2: 'mouse_middle', 3: 'mouse_right', 4: 'mouse_back', 5: 'mouse_forward'}.get(e.num)
            if m:
                done(m)
        w.bind('<KeyPress>', on_key)
        w.bind('<ButtonPress>', on_click)
        w.grab_set()
        w.focus_force()

    # ---- apply
    def apply(self):
        root = normalise_folder(self.folder.get())
        if not root:
            messagebox.showerror(APP, 'Pick Lichii\'s data folder first (button "Change...").')
            return
        running = emulator_running()
        if running:
            messagebox.showwarning(APP, 'Close Lichii (%s) first.\n\nIt saves its settings when it closes, which would undo '
                                        'these changes.' % running)
            return
        vals = self.get_values()
        bad = [vals[n] for n, _ in BUTTONS + MOVES if vals[n] not in KEY_NAMES and vals[n] != 'none'
               and not re.match(r'^code:\d{1,10}$', vals[n])]
        if bad:
            messagebox.showerror(APP, 'Not a key name: %s' % ', '.join(bad))
            return
        keys = {n: vals[n] for n in ICON_KEYS}
        custom = any(vals[n] != DEFAULTS[n] for n in ICON_KEYS)
        nup = None
        if custom and not icons.cache_ready(CACHE):
            nup = self.state.get('nup') if os.path.isfile(self.state.get('nup') or '') else guess_nup(root)
            if not nup:
                messagebox.showinfo(APP, 'To draw the icons for your keys, the program needs your game file once '
                                         '(the .nup of OOT for Switch 2). Pick it in the next window.')
                nup = filedialog.askopenfilename(title='OOT for Switch 2 game file (.nup)',
                                                 filetypes=[('Game file', '*.nup'), ('All files', '*.*')])
            if not nup:
                if not messagebox.askyesno(APP, 'Without the game file the keys still work, but the icons keep showing '
                                                'the default keys. Apply anyway?'):
                    return
                custom = False
            else:
                self.state['nup'] = nup
                save_state(self.state)
        self.apply_btn.state(['disabled'])
        self.log('---')
        threading.Thread(target=self.work, args=(root, vals, keys, custom, nup), daemon=True).start()

    def work(self, root, vals, keys, custom, nup):
        log = lambda s: self.q.put(('log', s))
        try:
            install_payload(root, log)
            write_settings(os.path.join(PAYLOAD, SETTINGS_NAME), os.path.join(root, SETTINGS_NAME), vals)
            log('Settings saved to ' + os.path.join(root, SETTINGS_NAME))
            run_apply_settings(root, log)
            if custom:
                if not icons.cache_ready(CACHE):
                    log('Reading the game file (once)...')
                    icons.extract_from_nup(nup, CACHE, log)
                icons.build(keys, CACHE, os.path.join(PAYLOAD, 'load', TITLE, 'ButtonPrompts-KeyboardMouse'),
                            os.path.join(root, 'load', TITLE, 'ButtonPrompts-KeyboardMouse'), log)
            else:
                log('Icons: default keys.')
            msg = 'Done. Start the game, click its picture once and press Ctrl+F9 once.'
            if vals['mouse_camera'] == 'native':
                msg = ('Done. Open OoT-MouseCapture.exe (in the Lichii data folder), then start the game, click its '
                       'picture once and press Ctrl+F9 once.')
            self.q.put(('done', msg))
        except Exception as e:
            self.q.put(('error', str(e)))

    def undo(self):
        root = normalise_folder(self.folder.get())
        if not root:
            messagebox.showerror(APP, 'Pick Lichii\'s data folder first (button "Change...").')
            return
        running = emulator_running()
        if running:
            messagebox.showwarning(APP, 'Close Lichii (%s) first.\n\nIt saves its settings when it closes, which would undo '
                                        'these changes.' % running)
            return
        if helper_running():
            messagebox.showwarning(APP, 'Close OoT-MouseCapture.exe first (the mouse helper window).')
            return
        if not messagebox.askyesno(APP, 'Put Lichii back the way it was before this mod?\n\n'
                                        '- Player 1 controls and the mouse settings go back to your old ones\n'
                                        '- the keyboard and mouse icons and the native camera patch are removed\n'
                                        '- button-icon mods the mod had moved to mod-backups are put back\n\n'
                                        'Your other Lichii settings are not touched. You can install the mod again '
                                        'at any time with Apply.'):
            return
        self.apply_btn.state(['disabled'])
        self.undo_btn.state(['disabled'])
        self.log('---')
        threading.Thread(target=self.undo_work, args=(root,), daemon=True).start()

    def undo_work(self, root):
        log = lambda s: self.q.put(('log', s))
        try:
            if undo_mod(root, log):
                self.q.put(('done', 'Done. Lichii is back to how it was before the mod: start it and play with your '
                                    'controller as before.'))
            else:
                self.q.put(('done', 'Done. The mod is removed, but there was no copy of your old controls. In Lichii, '
                                    'open Emulation > Configure > Controls and set Player 1 to your controller.'))
        except Exception as e:
            self.q.put(('error', 'Undo stopped: %s' % e))

    def poll(self):
        try:
            while True:
                kind, text = self.q.get_nowait()
                self.log(text)
                if kind in ('done', 'error'):
                    self.apply_btn.state(['!disabled'])
                    self.undo_btn.state(['!disabled'])
                    (messagebox.showinfo if kind == 'done' else messagebox.showerror)(APP, text)
        except queue.Empty:
            pass
        self.tk.after(100, self.poll)

    def log(self, s):
        self.log_box.configure(state='normal')
        self.log_box.insert('end', s + '\n')
        self.log_box.see('end')
        self.log_box.configure(state='disabled')


def selftest(folder, nup, logfile):
    """oot_kbm_config --selftest <data folder> <.nup> <log>: Apply with changed keys, no window (for testing builds)."""
    out = open(logfile, 'w', encoding='utf-8')
    log = lambda s: (out.write(s + '\n'), out.flush())
    try:
        root = normalise_folder(folder)
        vals = read_settings(os.path.join(root, SETTINGS_NAME))
        vals.update(button_a='f', button_y='mouse_right', move_up='up', move_down='down', move_left='left', move_right='right')
        install_payload(root, log)
        write_settings(os.path.join(PAYLOAD, SETTINGS_NAME), os.path.join(root, SETTINGS_NAME), vals)
        run_apply_settings(root, log)
        if not icons.cache_ready(CACHE):
            icons.extract_from_nup(nup, CACHE, log)
        icons.build({n: vals[n] for n in ICON_KEYS}, CACHE, os.path.join(PAYLOAD, 'load', TITLE, 'ButtonPrompts-KeyboardMouse'),
                    os.path.join(root, 'load', TITLE, 'ButtonPrompts-KeyboardMouse'), log)
        log('SELFTEST OK')
    except Exception as e:
        import traceback
        log('SELFTEST FAILED: %r\n%s' % (e, traceback.format_exc()))


def selftest_undo(folder, logfile):
    """oot_kbm_config --selftest-undo <data folder> <log>: the Undo button, no window (for testing builds)."""
    out = open(logfile, 'w', encoding='utf-8')
    log = lambda s: (out.write(s + '\n'), out.flush())
    try:
        undo_mod(normalise_folder(folder), log)
        log('SELFTEST UNDO OK')
    except Exception as e:
        import traceback
        log('SELFTEST UNDO FAILED: %r\n%s' % (e, traceback.format_exc()))


def main():
    if len(sys.argv) == 5 and sys.argv[1] == '--selftest':
        selftest(*sys.argv[2:5])
        return
    if len(sys.argv) == 4 and sys.argv[1] == '--selftest-undo':
        selftest_undo(*sys.argv[2:4])
        return
    root = tk.Tk()
    try:
        ttk.Style().theme_use('vista')
    except tk.TclError:
        pass
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
