"""Redraws the button icons (HUD, menus, song sheet) for the keys the player chose.

The drawings come from the mod's own tools (tools/build_fonts_kbm.py, tools/build_mods_kbm.py); this module only
decides WHAT each Switch button shows, from the key names of the settings file. The "Basic Controls" screen keeps
the default layout (it is copied unchanged from the installed icon mod).

Game files needed (read once from the player's own .nup, kept in a cache folder): the zstd dictionaries, the
button-icon font and the letter font. Nothing from the game is shipped with the program.
"""
import os
import sys

TITLE = '0400486024DEC000'
FONT_REL = os.path.join('romfs', 'Font2', 'Scalable', 'External.Nin_Ounce_NVN2.bfotf.zs')
BNTX_REL = os.path.join('romfs', 'UI', 'Layout2Archive', 'Common.Product.100.Nin_Ounce_NVN2.bntx.zs')
NUP_WANT = {
    'ZsDic': 'romfs/Pack/ZsDic.pack.zs',
    'External': 'romfs/Font2/Scalable/External.Nin_Ounce_NVN2.bfotf.zs',
    'ZeldaGlyphs': 'romfs/Font2/Scalable/Nin-ZeldaGlyphs-v3-Plain.Nin_Ounce_NVN2.bfotf.zs',
}
CACHE_FILES = ('ZsDic.pack.zs', os.path.join('fonts', 'External.bfotf'), os.path.join('fonts', 'External.otf'),
               os.path.join('fonts', 'Nin-ZeldaGlyphs-v3-Plain.otf'))


def tools_dir():
    base = getattr(sys, '_MEIPASS', None)
    return os.path.join(base, 'tools') if base else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools')


def use_cache(work):
    """Point the mod tools at the cache folder. Must run before any of them is imported."""
    os.environ['OOT_WORK'] = work
    os.environ['ZSDIC'] = os.path.join(work, 'ZsDic.pack.zs')
    t = tools_dir()
    if t not in sys.path:
        sys.path.insert(0, t)


def cache_ready(work):
    return all(os.path.isfile(os.path.join(work, f)) for f in CACHE_FILES)


def extract_from_nup(nup, work, log=print):
    """Reads the three small game files the icons need from the player's .nup into the cache."""
    use_cache(work)
    import nup_tool, glyphlib
    import zstandard
    os.makedirs(os.path.join(work, 'fonts'), exist_ok=True)
    f, pkgs, dirs, files, children, dc = nup_tool.parse(nup)
    entries = []
    for p in pkgs:
        tag = 'pkg%x_v%d_k%d' % (p['tid'], p['ver'], p['kind'])
        for kind in ('exefs', 'romfs'):
            if p[kind] != 0xFFFFFFFF:
                nup_tool.walk(dirs, files, children, dc, p[kind], tag + '/' + kind + '/', entries)
    got = {}
    for key, suffix in NUP_WANT.items():
        hits = [(p, i) for p, i in entries if p.endswith('/' + suffix)]
        if not hits:
            f.close()
            raise RuntimeError('This .nup does not look like OOT for Switch 2 (%s is missing).' % suffix)
        path, idx = max(hits, key=lambda h: int(h[0].split('_v')[1].split('_')[0]))
        got[key] = nup_tool.read_member(f, files[idx])
    f.close()
    open(os.path.join(work, 'ZsDic.pack.zs'), 'wb').write(got['ZsDic'])
    import zs
    zs.DIC = os.environ['ZSDIC']
    zs._dicts = None
    cont = zs.decompress(got['External'])
    open(os.path.join(work, 'fonts', 'External.bfotf'), 'wb').write(cont)
    open(os.path.join(work, 'fonts', 'External.otf'), 'wb').write(glyphlib.decrypt_bfotf(cont))
    zg = glyphlib.decrypt_bfotf(zs.decompress(got['ZeldaGlyphs']))
    open(os.path.join(work, 'fonts', 'Nin-ZeldaGlyphs-v3-Plain.otf'), 'wb').write(zg)
    log('Game files read from the .nup.')


# ---------------------------------------------------------------- what a key looks like
TEXT = {'tab': 'TAB', 'esc': 'ESC', 'escape': 'ESC', 'backspace': 'BKSP', 'insert': 'INS', 'delete': 'DEL',
        'home': 'HOME', 'end': 'END', 'pageup': 'PGUP', 'pagedown': 'PGDN', 'capslock': 'CAPS', 'ctrl': 'CTRL',
        'control': 'CTRL', 'alt': 'ALT', 'mouse_back': 'M4', 'mouse_forward': 'M5'}
PUNCT = {'comma': ',', 'period': '.', 'minus': '-', 'equals': '=', 'slash': '/', 'backslash': '\\',
         'semicolon': ';', 'apostrophe': "'", 'bracketleft': '[', 'bracketright': ']', 'grave': '`'}
ARROWS = {'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right'}
MOUSE_PRESS = {'mouse_left': 'L', 'mouse_right': 'R', 'mouse_middle': 'W'}
WORDS = {',': 'COMMA', '.': 'DOT', '-': 'MINUS', '=': 'EQ', '/': 'SLASH', '\\': 'BSLSH', ';': 'SEMI', "'": 'QUOTE',
         '[': '[', ']': ']', '`': 'GRAVE'}


def kind_of(name):
    """('mouse', press) | ('space'|'shift'|'enter', None) | ('arrow', dir) | ('text', label) | ('none', None)"""
    n = (name or 'none').strip().lower()
    if n in ('', 'none'):
        return ('none', None)
    if n in MOUSE_PRESS:
        return ('mouse', MOUSE_PRESS[n])
    if n in ('space', 'shift'):
        return (n, None)
    if n in ('enter', 'return'):
        return ('enter', None)
    if n in ARROWS:
        return ('arrow', ARROWS[n])
    if len(n) == 1 and n.isalnum():
        return ('text', n.upper())
    if n in TEXT:
        return ('text', TEXT[n])
    if n.startswith('f') and n[1:].isdigit():
        return ('text', n.upper())
    if n in PUNCT:
        return ('text', PUNCT[n])
    if n.startswith('code:'):
        return ('text', '?')
    return ('text', n[:4].upper())


class Drawer:
    """Glyph contours for the icon font and the HUD textures, on top of build_fonts_kbm."""

    def __init__(self):
        import build_fonts_kbm as K
        self.K = K
        self.zcmap = K._zc

    def text(self, s):
        # letters the game's letter font cannot draw get a word instead
        if all(ord(c) in self.zcmap for c in s):
            return s
        if s in WORDS and all(ord(c) in self.zcmap for c in WORDS[s]):
            return WORDS[s]
        return ''.join(c for c in s if ord(c) in self.zcmap) or '?'

    def letters_fit(self, s, cx, cy=None, box=420):
        K = self.K
        cy = K.CY if cy is None else cy
        cap = 250 if len(s) == 1 else 200 if len(s) == 2 else 130 if len(s) == 3 else 110
        cs = K.letters(s, cap, cx, cy)
        x0, y0, x1, y1 = K.BF.bbox(cs) if cs else (0, 0, 1, 1)
        if x1 - x0 > box:                                  # long labels: shrink to fit the key
            from fontTools.misc.transform import Transform
            k = box / (x1 - x0)
            cs = K.BF.transform(cs, Transform().translate(cx, cy).scale(k).translate(-cx, -cy))
        return cs

    def arrow_cut(self, cx, direction, size=200, cy=None):
        K = self.K
        return [K.cut(K.tri(cx, K.CY if cy is None else cy, size, direction))]

    # one key, as a font glyph of width adv
    def glyph(self, adv, name):
        K = self.K
        kind, v = kind_of(name)
        cx = adv / 2
        if kind == 'mouse':
            return K.mouse(cx, press=v)
        if kind == 'space':
            return K.wide_key(adv, K.space_symbol, 600, 300)
        if kind == 'shift':
            return K.wide_key(adv, K.shift_symbol, 640, 330)
        if kind == 'enter':
            return K.wide_key(adv, K.enter_symbol, 560, 330)
        if kind == 'arrow':
            return [K.rrect(cx - 280, K.CY - 280, cx + 280, K.CY + 280, 92)] + self.arrow_cut(cx, v, 230)
        if kind == 'none':
            return [K.rrect(cx - 280, K.CY - 280, cx + 280, K.CY + 280, 92)]
        s = self.text(v)
        if len(s) <= 2:
            return [K.rrect(cx - 280, K.CY - 280, cx + 280, K.CY + 280, 92)] + self.letters_fit(s, cx, box=420)
        return K.wide_key(adv, lambda c: self.letters_fit(s, c, box=480), 560, 330)

    # small key inside a group (WASD, rows)
    def small(self, name, x, y, s, cap=112, r=38):
        K = self.K
        kind, v = kind_of(name)
        out = [K.rrect(x - s / 2, y - s / 2, x + s / 2, y + s / 2, r)]
        if kind == 'arrow':
            out += self.arrow_cut(x, v, s * 0.5, y)
        elif kind == 'mouse':
            out += [K.cut(c) for c in K.letters({'L': 'L', 'R': 'R', 'W': 'M'}[v], 100, x, y, 12)]
        elif kind in ('space', 'shift', 'enter'):
            out += self.letters_fit({'space': 'SP', 'shift': 'SH', 'enter': 'EN'}[kind], x, y, box=s * 0.8)
        elif kind == 'text':
            t = self.text(v)
            cs = self.letters_fit(t, x, y, box=s * 0.78)
            if len(t) == 1:
                cs = K.letters(t, cap, x, y, 12)
            out += cs
        return out

    def wasd(self, adv, up, left, down, right):
        K = self.K
        cx, s, g = adv / 2, 190, 18
        pos = [(up, cx, K.CY + (s + g) / 2), (left, cx - (s + g), K.CY - (s + g) / 2),
               (down, cx, K.CY - (s + g) / 2), (right, cx + (s + g), K.CY - (s + g) / 2)]
        out = []
        for name, x, y in pos:
            out += self.small(name, x, y, s)
        return out

    def row(self, adv, names):
        n = len(names)
        s = 230 if n == 2 else 190
        g = 22
        total = n * s + (n - 1) * g
        x0 = adv / 2 - total / 2
        out = []
        for i, name in enumerate(names):
            out += self.small(name, x0 + s / 2 + i * (s + g), self.K.CY, s, 150 if n == 2 else 112, 46)
        return out

    def dpad(self, adv, up, left, right, down):
        K = self.K
        labels = [kind_of(n) for n in (up, left, right, down)]
        if all(k == 'text' and len(v) == 1 and v.isdigit() for k, v in labels):
            ds = [int(v) for _, v in labels]
            if sorted(ds) == list(range(min(ds), min(ds) + 4)):            # four digits in a row: "1-4"
                return K.wide_key(adv, lambda cx: K.letters('%d-%d' % (min(ds), max(ds)), 150, cx), 600, 330)
        return self.row(adv, [up, left, right, down])

    def glyph_map(self, keys, adv_of):
        """same code points as build_fonts_kbm.glyph_map, drawn from the chosen keys"""
        a, k, K = adv_of, keys, self.K
        new = {
            0xE040: self.glyph(a(0xE040), k['button_a']),
            0xE041: self.glyph(a(0xE041), k['button_b']),
            0xE042: self.glyph(a(0xE042), k['button_x']),
            0xE043: self.glyph(a(0xE043), k['button_y']),
            0xE044: self.glyph(a(0xE044), k['button_l']),
            0xE045: self.glyph(a(0xE045), k['button_r']),
            0xE046: self.glyph(a(0xE046), k['button_zl']),
            0xE047: self.glyph(a(0xE047), k['button_zr']),
            0xE049: self.dpad(a(0xE049), k['dpad_up'], k['dpad_left'], k['dpad_right'], k['dpad_down']),
            0xE04B: self.glyph(a(0xE04B), k['button_plus']),
            0xE04C: self.glyph(a(0xE04C), k['button_minus']),
            0xE050: self.glyph(a(0xE050), k['move_down']), 0xE052: self.glyph(a(0xE052), k['move_up']),
            0xE05A: self.glyph(a(0xE05A), k['move_left']), 0xE058: self.glyph(a(0xE058), k['move_right']),
            0xE054: self.row(a(0xE054), [k['move_left'], k['move_right']]),
            0xE05C: self.row(a(0xE05C), [k['move_up'], k['move_down']]),
            0xE05E: self.wasd(a(0xE05E), k['move_up'], k['move_left'], k['move_down'], k['move_right']),
            0xE05F: K.mouse(a(0xE05F) / 2),                                          # camera stays the mouse
            0xE057: self.glyph(a(0xE057), k['button_r3']),
            0xE051: K.mouse(a(0xE051) / 2, 0.8, arrows=('down',)), 0xE053: K.mouse(a(0xE053) / 2, 0.8, arrows=('up',)),
            0xE05B: K.mouse(a(0xE05B) / 2, 0.8, arrows=('left',)), 0xE059: K.mouse(a(0xE059) / 2, 0.8, arrows=('right',)),
            0xE055: K.mouse(a(0xE055) / 2, 0.8, arrows=('left', 'right')),
            0xE05D: K.mouse(a(0xE05D) / 2, 0.8, arrows=('up', 'down')),
            0xE068: K.mouse(a(0xE068) / 2, 0.8, arrows=('left', 'right')),
            0xE060: self.glyph(a(0xE060), k['dpad_up']), 0xE062: self.glyph(a(0xE062), k['dpad_left']),
            0xE063: self.glyph(a(0xE063), k['dpad_right']), 0xE061: self.glyph(a(0xE061), k['dpad_down']),
            0xE064: self.row(a(0xE064), [k['dpad_up'], k['dpad_down']]),
            0xE065: self.row(a(0xE065), [k['dpad_left'], k['dpad_right']]),
            0xE06A: self.row(a(0xE06A), [k['dpad_left'], k['dpad_down'], k['dpad_right']]),
        }
        return new

    # HUD buttons and ocarina notes: (contours, sign, width frac, height frac) like build_mods_kbm.symbols
    def symbol(self, name):
        K = self.K
        kind, v = kind_of(name)
        if kind == 'mouse':
            return (K.mouse(0, press=v), +1, 0.50, 0.74)
        if kind == 'space':
            return (K.space_symbol(0), -1, 0.70, 0.42)
        if kind == 'shift':
            return (K.shift_symbol(0), -1, 0.50, 0.52)
        if kind == 'enter':
            return (K.enter_symbol(0), -1, 0.58, 0.46)
        if kind == 'arrow':
            return (self.arrow_cut(0, v, 300), -1, 0.46, 0.46)
        if kind == 'none':
            return (K.letters('-', 250, 0) if ord('-') in self.zcmap else self.arrow_cut(0, 'right', 60), -1, 0.30, 0.10)
        s = self.text(v)
        w = {1: 0.46, 2: 0.62, 3: 0.74}.get(len(s), 0.80)
        h = {1: 0.52, 2: 0.46, 3: 0.40}.get(len(s), 0.34)
        return (K.letters(s, 250, 0), -1, w, h)


def _flatten(c):
    pts, cur = [], None
    for op, a in c:
        if op in ('moveTo', 'lineTo'):
            cur = a[0]
            pts.append(cur)
        elif op == 'curveTo':
            p0, (p1, p2, p3) = cur, a
            for i in range(1, 13):
                t = i / 12
                u = 1 - t
                pts.append((u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
                            u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1]))
            cur = p3
    return pts


def _ink(BF, contours, sign, size, cx, cy, fit_w, fit_h, ss=8):
    import numpy as np
    from PIL import Image, ImageDraw
    x0, y0, x1, y1 = BF.bbox(contours)
    s = min(fit_w / max(1e-6, x1 - x0), fit_h / max(1e-6, y1 - y0))
    tf = lambda x, y: ((cx + (x - (x0 + x1) / 2) * s) * ss, (cy - (y - (y0 + y1) / 2) * s) * ss)
    im = Image.new('L', (size * ss, size * ss), 0)
    d = ImageDraw.Draw(im)
    for c in sorted(contours, key=lambda c: -abs(BF.area(c))):
        d.polygon([tf(x, y) for x, y in _flatten(c)], fill=255 if BF.area(c) * sign > 0 else 0)
    return np.asarray(im.resize((size, size), Image.BOX)).astype(np.float32) / 255


def build(keys, work, base_mod_dir, out_mod_dir, log=print):
    """Writes ButtonPrompts-KeyboardMouse (font + Common bntx) for `keys` into out_mod_dir.
    base_mod_dir: the default icon mod (its Basic Controls screen is kept)."""
    use_cache(work)
    import numpy as np
    from PIL import Image
    import glyphlib as BF
    import zs
    zs.DIC = os.environ['ZSDIC']
    zs._dicts = None
    import build_fonts_kbm as K
    import ctrl_common as C
    from oot_paths import OUT

    d = Drawer()
    log('Drawing the icon font...')
    K.glyph_map = lambda adv_of: d.glyph_map(keys, adv_of)
    fin, size, blank = K.build_fitting(OUT)
    total = os.path.getsize(os.path.join(work, 'fonts', 'External.bfotf'))
    bf = BF.encrypt_bfotf(open(fin, 'rb').read(), total)
    if len(bf) != total:
        raise RuntimeError('icon font size changed (%d, expected %d)' % (len(bf), total))
    font_out = os.path.join(out_mod_dir, FONT_REL)
    os.makedirs(os.path.dirname(font_out), exist_ok=True)
    font_bytes = zs.compress(bf, 'zs.zsdic')

    log('Drawing the HUD buttons (this takes a little while)...')
    base = zs.decompress(open(os.path.join(base_mod_dir, BNTX_REL), 'rb').read())
    b = bytearray(base)
    t = C.all_brti(bytes(b))
    syms = {'A': keys['button_a'], 'B': keys['button_b'], 'X': keys['button_x'], 'Y': keys['button_y'],
            'L': keys['button_l'], 'R': keys['button_r']}
    for k in 'ABXY':
        cs, sign, fw, fh = d.symbol(syms[k])
        m = _ink(BF, cs, sign, 64, 32, 32, 64 * fw * 1.15, 64 * fh * 1.15)
        C.write_bc4(b, t['KeyTexFont%s_00' % k], np.clip(m * 255 + 0.5, 0, 255).astype(np.uint8))
    for k in 'ABXYLR':
        orig = C.read_astc(base, t['OcarinaButton%s_00' % k])         # the mod keeps the game's silhouette (alpha)
        a = np.array(orig.convert('RGBA'))
        alpha = a[..., 3]
        ys, xs = np.where(alpha >= 128)
        cx, cy = (xs.min() + xs.max() + 1) / 2, (ys.min() + ys.max() + 1) / 2
        w, h = xs.max() + 1 - xs.min(), ys.max() + 1 - ys.min()
        cs, sign, fw, fh = d.symbol(syms[k])
        m = _ink(BF, cs, sign, 93, cx, cy, w * fw * 1.2, h * fh * 1.2)
        out = np.empty_like(a)
        out[..., :3] = np.clip(255 * (1 - m), 0, 255).astype(np.uint8)[..., None]
        out[..., 3] = alpha
        C.write_astc(b, t['OcarinaButton%s_00' % k], Image.fromarray(out))
    log('Packing the textures...')
    bntx_bytes = zs.compress(bytes(b), 'zs.zsdic', level=9)
    bntx_out = os.path.join(out_mod_dir, BNTX_REL)
    os.makedirs(os.path.dirname(bntx_out), exist_ok=True)
    for path, data in ((font_out, font_bytes), (bntx_out, bntx_bytes)):
        tmp = path + '.tmp'
        open(tmp, 'wb').write(data)
        os.replace(tmp, path)
    log('Icons written.')
