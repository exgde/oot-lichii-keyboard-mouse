"""Small glyph-outline helpers (fontTools) and the cipher of the game's .bfotf font container.
Outlines are lists of (op, args) like RecordingPen's. Fills are counter-clockwise (area > 0); cut-outs (letters) are clockwise."""
import struct
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.transformPen import TransformPen

KEY = 0xA6018502            # XOR (4-byte big-endian words) of this game's .bfotf container
MAGIC = 0x7F9A0218


def contours_of(glyphset, gname):
    p = RecordingPen(); glyphset[gname].draw(p); out, cur = [], []
    for op, a in p.value:
        cur.append((op, a))
        if op in ("closePath", "endPath"):
            out.append(cur); cur = []
    return out


def pts(c):
    return [pt for op, a in c for pt in a]


def area(c):
    P = [a[-1] for op, a in c if a]
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2


def bbox(cs):
    P = [pt for c in cs for pt in pts(c)]
    return min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P)


def replay(c, pen):
    for op, a in c:
        getattr(pen, op)(*a)


def reverse(c):
    r = RecordingPen(); replay(c, ReverseContourPen(r)); return r.value


def transform(cs, t):
    out = []
    for c in cs:
        r = RecordingPen(); replay(c, TransformPen(r, t)); out.append(r.value)
    return out


def poly(points, cw=True):
    """closed polygon outline; points are given counter-clockwise (y up); cw=True reverses it (cut-out)"""
    if cw:
        points = points[::-1]
    return [("moveTo", (points[0],))] + [("lineTo", (p,)) for p in points[1:]] + [("closePath", ())]


def xor_words(raw):
    n = len(raw) // 4
    return struct.pack(f">{n}I", *[w ^ KEY for w in struct.unpack(f">{n}I", raw[:n * 4])])


def decrypt_bfotf(container):
    """a .bfotf container (already decompressed from the .zs) -> OTF bytes"""
    dec = xor_words(container)
    magic, size = struct.unpack(">II", dec[:8])
    if magic != MAGIC:
        raise ValueError("unexpected .bfotf container (magic %#x)" % magic)
    return dec[8:8 + size]


def encrypt_bfotf(otf_bytes, orig_total):
    """OTF -> container with the same size as the original (the game's RSTB stores file sizes)"""
    body = otf_bytes + b"\0" * ((-len(otf_bytes)) % 4)
    raw = struct.pack(">II", MAGIC, len(otf_bytes)) + body
    if len(raw) < orig_total:
        raw += b"\0" * (orig_total - len(raw))
    return xor_words(raw)
