"""Build CJ texture atlas and write it into copies of the green hat kid's vest BNTX textures.
usage: tex_build.py <src_tex_dir> <out_dir> <cj_tex_dir> <prefix e.g. Mt_Vest_Player_Child>"""
import struct, sys, os, math
import numpy as np
from PIL import Image
import astc_encoder as A
import texture2ddecoder as T

ATLAS = 1536
GRID = int(os.environ.get('ATLAS_GRID', '2'))   # 2 = CJ (4 images), 3 = up to 9 images (Image_0..Image_8 row-major)
CELLS = ({'Image_2': (0, 0), 'Image_1': (1, 0), 'Image_3': (0, 1), 'Image_0': (1, 1)} if GRID == 2 else
         {'Image_%d' % i: (i % GRID, i // GRID) for i in range(GRID * GRID)})
MARGIN = 12

def atlas_uv(img, u, v):
    c, r = CELLS[img]; cell = ATLAS // GRID; inner = cell - 2 * MARGIN
    return ((c * cell + MARGIN + u * inner) / ATLAS, (r * cell + MARGIN + v * inner) / ATLAS)

def build_atlas(cj_tex_dir):
    at = Image.new('RGBA', (ATLAS, ATLAS), (0, 0, 0, 255)); cell = ATLAS // GRID; inner = cell - 2 * MARGIN
    for name, (c, r) in CELLS.items():
        if not os.path.exists(os.path.join(cj_tex_dir, name + '.png')): continue
        im = Image.open(os.path.join(cj_tex_dir, name + '.png')).convert('RGBA')
        big = im.resize((inner, inner), Image.LANCZOS)
        # edge-extend into the margin so mips/ASTC blocks don't bleed black
        pad = Image.fromarray(np.pad(np.array(big), ((MARGIN, MARGIN), (MARGIN, MARGIN), (0, 0)), mode='edge'))
        at.paste(pad, (c * cell, r * cell))
    return at

def brti(d):
    o = d.find(b'BRTI')
    mips = struct.unpack_from('<H', d, o + 0x16)[0]
    fmt = struct.unpack_from('<I', d, o + 0x1C)[0]
    w, h = struct.unpack_from('<ii', d, o + 0x24)
    layout = struct.unpack_from('<I', d, o + 0x34)[0]
    ptrs = struct.unpack_from('<Q', d, o + 0x70)[0]
    offs = list(struct.unpack_from('<%dQ' % mips, d, ptrs))
    data_end = struct.unpack_from('<I', d, o + 0x50)[0] + offs[0]
    sizes = [offs[i + 1] - offs[i] for i in range(mips - 1)] + [data_end - offs[-1]]
    return dict(mips=mips, fmt=fmt, w=w, h=h, bh_log2=layout & 7, offs=offs, sizes=sizes)

def mip_block_height(hb, bh):
    while bh > 1 and hb <= (bh // 2) * 8: bh //= 2
    return bh

def swizzle_index(wb, hb, bpp, bh):
    """For each linear block (row-major), its byte offset in block-linear layout."""
    gw = math.ceil(wb * bpp / 64)
    y = np.repeat(np.arange(hb), wb); x = np.tile(np.arange(wb), hb); xb = x * bpp
    gob = (y // (8 * bh)) * 512 * bh * gw + (xb // 64) * 512 * bh + ((y % (8 * bh)) // 8) * 512
    if bpp == 16:   # this game's GOB order for 16-byte blocks: y0, y1, x0, y2, x1 (measured on its own textures)
        return gob + (y & 1) * 16 + ((y >> 1) & 1) * 32 + (x & 1) * 64 + ((y >> 2) & 1) * 128 + ((x >> 1) & 1) * 256
    return gob + ((xb % 64) // 32) * 256 + ((y % 8) // 2) * 64 + ((xb % 32) // 16) * 32 + (y % 2) * 16 + (xb % 16)

def deswizzle(buf, wb, hb, bpp, bh):
    idx = swizzle_index(wb, hb, bpp, bh)
    out = bytearray(wb * hb * bpp)
    for k in range(bpp // 16 if bpp >= 16 else 1):
        pass
    src = np.frombuffer(buf, np.uint8)
    lin = np.stack([src[idx + b] for b in range(bpp)], 1)
    return lin.tobytes()

def swizzle(lin, wb, hb, bpp, bh, size):
    idx = swizzle_index(wb, hb, bpp, bh)
    out = np.zeros(size, np.uint8); src = np.frombuffer(lin, np.uint8).reshape(-1, bpp)
    for b in range(bpp): out[idx + b] = src[:, b]
    return out.tobytes()

def astc_encode(img, bw, bh, srgb):
    cfg = A.ASTCConfig(A.ASTCProfile.LDR_SRGB if srgb else A.ASTCProfile.LDR, bw, bh, 1, A.ASTCQualityPreset.MEDIUM)
    ctx = A.ASTCContext(cfg)
    w, h = img.size
    return ctx.compress(A.ASTCImage(A.ASTCType.U8, w, h, 1, img.convert('RGBA').tobytes()), A.ASTCSwizzle())

ASTC_DIMS = {0x2D: (4, 4), 0x2E: (5, 4), 0x2F: (5, 5), 0x30: (6, 5), 0x31: (6, 6), 0x32: (8, 5), 0x33: (8, 6),
             0x34: (8, 8), 0x35: (10, 5), 0x36: (10, 6), 0x37: (10, 8), 0x38: (10, 10), 0x39: (12, 10), 0x3A: (12, 12)}

def decode_mip0(d):
    t = brti(d); bw, bhp = ASTC_DIMS[t['fmt'] >> 8]
    wb, hb = math.ceil(t['w'] / bw), math.ceil(t['h'] / bhp)
    raw = d[t['offs'][0]:t['offs'][0] + t['sizes'][0]]
    lin = deswizzle(raw, wb, hb, 16, 1 << t['bh_log2'])
    px = T.decode_astc(lin, t['w'], t['h'], bw, bhp)
    return Image.frombytes('RGBA', (t['w'], t['h']), px, 'raw', 'BGRA')

def write_image(d, img):
    """Encode img into every mip of the (ASTC) texture in BNTX bytes d."""
    d = bytearray(d); t = brti(d); bw, bhp = ASTC_DIMS[t['fmt'] >> 8]; srgb = (t['fmt'] & 0xFF) == 6
    for m in range(t['mips']):
        w, h = max(1, t['w'] >> m), max(1, t['h'] >> m)
        wb, hb = math.ceil(w / bw), math.ceil(h / bhp)
        mi = img.resize((w, h), Image.LANCZOS)
        # pad to whole blocks
        pw, ph = wb * bw, hb * bhp
        padded = Image.fromarray(np.pad(np.array(mi), ((0, ph - h), (0, pw - w), (0, 0)), mode='edge'))
        lin = astc_encode(padded, bw, bhp, srgb)
        bh = mip_block_height(hb, 1 << t['bh_log2'])
        sw = swizzle(lin, wb, hb, 16, bh, t['sizes'][m])
        d[t['offs'][m]:t['offs'][m] + t['sizes'][m]] = sw
    return bytes(d)

def fill_constant(d, block):
    """Fill every mip region with one repeated compressed block (swizzle-independent)."""
    d = bytearray(d); t = brti(d)
    for m in range(t['mips']):
        n = t['sizes'][m] // len(block)
        d[t['offs'][m]:t['offs'][m] + n * len(block)] = block * n
    return bytes(d)

if __name__ == '__main__':
    src, out, cjtex, prefix = sys.argv[1:5]
    os.makedirs(out, exist_ok=True)
    alb = open(os.path.join(src, prefix + '_Alb.bntx'), 'rb').read()
    print('Alb', {k: v for k, v in brti(alb).items() if k not in ('offs', 'sizes')})
    decode_mip0(alb).save(os.path.join(out, '_orig_alb_check.png'))
    at = build_atlas(cjtex); at.save(os.path.join(out, '_atlas.png'))
    new_alb = write_image(alb, at)
    decode_mip0(new_alb).save(os.path.join(out, '_new_alb_check.png'))
    open(os.path.join(out, prefix + '_Alb.bntx'), 'wb').write(new_alb)
    # flat normal (ASTC), roughness/AO (BC4) constants
    nrm = open(os.path.join(src, prefix + '_Nrm.bntx'), 'rb').read(); tn = brti(nrm)
    bw, bhp = ASTC_DIMS[tn['fmt'] >> 8]
    flat = astc_encode(Image.new('RGBA', (bw, bhp), (128, 128, 128, 128)), bw, bhp, False)   # game packs X in RGB, Y in A
    open(os.path.join(out, prefix + '_Nrm.bntx'), 'wb').write(fill_constant(nrm, flat))
    for suf, val in (('_Rgh', 180), ('_AO', 220)):
        dd = open(os.path.join(src, prefix + suf + '.bntx'), 'rb').read()
        assert brti(dd)['fmt'] >> 8 == 0x1D, hex(brti(dd)['fmt'])
        open(os.path.join(out, prefix + suf + '.bntx'), 'wb').write(fill_constant(dd, bytes([val, val, 0, 0, 0, 0, 0, 0])))
    print('textures written to', out)
