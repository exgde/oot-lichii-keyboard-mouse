"""Shared helpers: read/write BC4 and ASTC textures inside Common.bntx, write a mod folder."""
import os, sys, math, struct, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import tex_build as T
import texture2ddecoder as TD
import zs
from oot_paths import WORK

BNTX_PATH = os.path.join(WORK, "Common.bntx")      # extracted from YOUR .nup by extract_game_files.py
BNTX_REL = "UI/Layout2Archive/Common.Product.100.Nin_Ounce_NVN2.bntx.zs"

def all_brti(b):
    out = {}
    for m in re.finditer(b"BRTI", b):
        o = m.start()
        mips = struct.unpack_from('<H', b, o + 0x16)[0]; fmt = struct.unpack_from('<I', b, o + 0x1C)[0]
        w, h = struct.unpack_from('<ii', b, o + 0x24); layout = struct.unpack_from('<I', b, o + 0x34)[0]
        ptrs = struct.unpack_from('<Q', b, o + 0x70)[0]; offs = list(struct.unpack_from('<%dQ' % mips, b, ptrs))
        data_end = struct.unpack_from('<I', b, o + 0x50)[0] + offs[0]
        name_off = struct.unpack_from("<Q", b, o + 0x60)[0]; n = struct.unpack_from("<H", b, name_off)[0]
        name = b[name_off + 2:name_off + 2 + n].decode()
        sizes = [offs[i + 1] - offs[i] for i in range(mips - 1)] + [data_end - offs[-1]]
        out[name] = dict(o=o, mips=mips, fmt=fmt, w=w, h=h, bh_log2=layout & 7, offs=offs,
                         size=data_end - offs[0], sizes=sizes)
    return out

# ---- BC4 (8-byte blocks, NX2 swizzle measured by the button-prompts session) ----
def swizzle_offsets(wb, hb, bh):
    gw = math.ceil(wb * 8 / 64)
    ys, xs = np.mgrid[0:hb, 0:wb]
    gob = (ys // (8 * bh)) * 512 * bh * gw + ((xs * 8) // 64) * 512 * bh + ((ys % (8 * bh)) // 8) * 512
    return (gob + ((xs & 1) << 3) + ((ys & 1) << 4) + (((ys >> 1) & 1) << 5) + (((xs >> 1) & 1) << 6)
            + (((ys >> 2) & 1) << 7) + (((xs >> 2) & 1) << 8)).astype(np.int64)

def bc4_decode(lin, w, h):
    wb, hb = w // 4, h // 4
    blocks = np.frombuffer(lin, np.uint8).reshape(hb, wb, 8)
    r0 = blocks[:, :, 0].astype(np.int32); r1 = blocks[:, :, 1].astype(np.int32)
    bits = np.zeros((hb, wb), np.uint64)
    for i in range(6):
        bits |= blocks[:, :, 2 + i].astype(np.uint64) << np.uint64(8 * i)
    pal = np.zeros((hb, wb, 8), np.int32)
    pal[:, :, 0] = r0; pal[:, :, 1] = r1
    big = r0 > r1
    for i in range(1, 7):
        pal[:, :, 1 + i] = np.where(big, ((7 - i) * r0 + i * r1) // 7,
                                    (((5 - i) * r0 + i * r1) // 5) if i <= 4 else (0 if i == 5 else 255))
    img = np.zeros((hb, wb, 16), np.uint8)
    for i in range(16):
        idx = ((bits >> np.uint64(3 * i)) & np.uint64(7)).astype(np.int32)
        img[:, :, i] = np.take_along_axis(pal, idx[:, :, None], 2)[:, :, 0]
    return img.reshape(hb, wb, 4, 4).transpose(0, 2, 1, 3).reshape(h, w)

def bc4_encode(img):
    """img uint8 HxW (multiples of 4) -> linear BC4 blocks; 8-level palette, exact for 2-level content."""
    h, w = img.shape; hb, wb = h // 4, w // 4
    blk = img.reshape(hb, 4, wb, 4).transpose(0, 2, 1, 3).reshape(hb, wb, 16).astype(np.int32)
    r0 = blk.max(2); r1 = blk.min(2)
    pal = np.stack([r0, r1] + [((7 - i) * r0 + i * r1) // 7 for i in range(1, 7)], 2)  # hb,wb,8
    d = np.abs(blk[:, :, :, None] - pal[:, :, None, :])
    idx = d.argmin(3).astype(np.uint64)
    flat = r0 == r1
    idx[flat] = 0
    bits = np.zeros((hb, wb), np.uint64)
    for i in range(16):
        bits |= idx[:, :, i] << np.uint64(3 * i)
    out = np.zeros((hb, wb, 8), np.uint8)
    out[:, :, 0] = r0; out[:, :, 1] = r1
    for i in range(6):
        out[:, :, 2 + i] = ((bits >> np.uint64(8 * i)) & np.uint64(0xFF)).astype(np.uint8)
    return out.tobytes()

def read_bc4(b, t):
    w4, h4 = (t['w'] + 3) // 4 * 4, (t['h'] + 3) // 4 * 4
    wb, hb = w4 // 4, h4 // 4; bh = T.mip_block_height(hb, 1 << t['bh_log2'])
    raw = np.frombuffer(b[t['offs'][0]:t['offs'][0] + t['size']], np.uint8)
    offs = swizzle_offsets(wb, hb, bh)
    lin = raw[(offs[:, :, None] + np.arange(8)).reshape(-1)].tobytes()
    return bc4_decode(lin, w4, h4)[:t['h'], :t['w']]

def write_bc4(b, t, img):
    """b: bytearray of the bntx; img: uint8 HxW (texture size). Pads to whole blocks."""
    w4, h4 = (t['w'] + 3) // 4 * 4, (t['h'] + 3) // 4 * 4
    full = np.zeros((h4, w4), np.uint8); full[:t['h'], :t['w']] = img[:t['h'], :t['w']]
    wb, hb = w4 // 4, h4 // 4; bh = T.mip_block_height(hb, 1 << t['bh_log2'])
    lin = np.frombuffer(bc4_encode(full), np.uint8).reshape(hb, wb, 8)
    offs = swizzle_offsets(wb, hb, bh)
    base = t['offs'][0]
    target = np.frombuffer(bytes(b[base:base + t['size']]), np.uint8).copy()
    target[(offs[:, :, None] + np.arange(8)).reshape(-1)] = lin.reshape(-1)
    b[base:base + t['size']] = target.tobytes()

# ---- ASTC (16-byte blocks, tex_build's swizzle) ----
def read_astc(b, t):
    bw, bhp = T.ASTC_DIMS[t['fmt'] >> 8]
    wb, hb = math.ceil(t['w'] / bw), math.ceil(t['h'] / bhp)
    raw = b[t['offs'][0]:t['offs'][0] + t['size']]
    lin = T.deswizzle(raw, wb, hb, 16, 1 << t['bh_log2'])
    px = TD.decode_astc(lin, t['w'], t['h'], bw, bhp)
    return Image.frombytes('RGBA', (t['w'], t['h']), px, 'raw', 'BGRA')

def write_astc(b, t, img):
    """img: RGBA PIL image of the texture size; writes mip 0 (these textures have 1 mip)."""
    assert t['mips'] == 1, t['mips']
    bw, bhp = T.ASTC_DIMS[t['fmt'] >> 8]; srgb = (t['fmt'] & 0xFF) == 6
    wb, hb = math.ceil(t['w'] / bw), math.ceil(t['h'] / bhp)
    pw, ph = wb * bw, hb * bhp
    arr = np.array(img.convert('RGBA'))
    padded = Image.fromarray(np.pad(arr, ((0, ph - t['h']), (0, pw - t['w']), (0, 0)), mode='edge'))
    lin = T.astc_encode(padded, bw, bhp, srgb)
    bh = T.mip_block_height(hb, 1 << t['bh_log2'])
    sw = T.swizzle(lin, wb, hb, 16, bh, t['sizes'][0])
    assert len(sw) == t['size'], (len(sw), t['size'])
    b[t['offs'][0]:t['offs'][0] + t['size']] = sw

def load_bntx():
    b = open(BNTX_PATH, "rb").read()
    return b, all_brti(b)

def write_mod_bntx(b, root):
    p = os.path.join(root, "romfs", BNTX_REL); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(zs.compress(bytes(b), 'zs.zsdic'))
    return p
