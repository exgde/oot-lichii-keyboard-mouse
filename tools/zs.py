"""TotK-style .zs helpers: decompress with ZsDic dictionaries, minimal SARC reader, BFRES name scan."""
import struct, sys, os, zstandard

HERE = os.path.dirname(os.path.abspath(__file__))
DIC = os.environ.get('ZSDIC') or os.path.join(os.environ.get('OOT_WORK') or os.path.join(HERE, 'work'), 'ZsDic.pack.zs')

def sarc_files(data):
    assert data[:4] == b'SARC', data[:4]
    hdr_len, bom = struct.unpack_from('<HH', data, 4)
    data_off = struct.unpack_from('<I', data, 0xC)[0]
    sfat = hdr_len
    assert data[sfat:sfat + 4] == b'SFAT'
    count = struct.unpack_from('<H', data, sfat + 6)[0]
    nodes = []
    for i in range(count):
        h, attr, s, e = struct.unpack_from('<IIII', data, sfat + 0xC + i * 16)
        nodes.append((attr, s, e))
    sfnt = sfat + 0xC + count * 16
    names_base = sfnt + 8
    out = {}
    for attr, s, e in nodes:
        name_off = (attr & 0xFFFF) * 4
        n = data[names_base + name_off: data.index(b'\0', names_base + name_off)].decode()
        out[n] = data[data_off + s: data_off + e]
    return out

_dicts = None
def dicts():
    global _dicts
    if _dicts is None:
        raw = zstandard.ZstdDecompressor().decompress(open(DIC, 'rb').read(), max_output_size=1 << 26)
        _dicts = sarc_files(raw)
    return _dicts

def decompress(blob, kind='zs.zsdic'):
    d = zstandard.ZstdCompressionDict(dicts()[kind])
    return zstandard.ZstdDecompressor(dict_data=d).decompress(blob, max_output_size=1 << 28)

def compress(raw, kind='zs.zsdic', level=16):
    d = zstandard.ZstdCompressionDict(dicts()[kind])
    return zstandard.ZstdCompressor(level=level, dict_data=d).compress(raw)

if __name__ == '__main__':
    print('dicts:', {k: len(v) for k, v in dicts().items()})
    for p in sys.argv[1:]:
        kind = 'pack.zsdic' if p.endswith('.pack.zs') else 'zs.zsdic'
        raw = decompress(open(p, 'rb').read(), kind)
        out = p[:-3]
        open(out, 'wb').write(raw)
        print(out, len(raw), raw[:16])
