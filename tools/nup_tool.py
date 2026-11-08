"""List / extract members of a Lichii NUP container.
usage: nup_tool.py list <nup> <out.tsv>
       nup_tool.py extract <nup> <outdir> <path-substring>...
"""
import struct, sys, os

def parse(path):
    f = open(path, 'rb')
    sb = f.read(0x80)
    assert sb[:4] == b'NUP\x01'
    toc_off, toc_size = struct.unpack_from('<QQ', sb, 8)
    f.seek(toc_off); toc = f.read(toc_size)
    magic, pkg_count, dir_count, file_count, pool_off, pool_size = struct.unpack_from('<IIQQQQ', toc, 0)
    pos = 0x30
    pkgs = []
    for _ in range(pkg_count):
        tid, root, exefs, romfs, ver, kind = struct.unpack_from('<QIIIIB', toc, pos)
        pkgs.append(dict(tid=tid, root=root, exefs=exefs, romfs=romfs, ver=ver, kind=kind))
        pos += 0x40
    name = lambda o, l: toc[pool_off + o: pool_off + o + l].decode('utf-8', 'replace')
    dirs = []
    for _ in range(dir_count):
        no, nl, fc, cc = struct.unpack_from('<IIII', toc, pos); pos += 0x18
        dirs.append((name(no, nl), fc, cc))
    files = []
    for _ in range(file_count):
        no, nl, size, eo, es = struct.unpack_from('<IIQQQ', toc, pos)
        codec = toc[pos + 0x40]; pos += 0x50
        files.append((name(no, nl), size, eo, es, codec))
    nchild = (pool_off - pos) // 4
    children = struct.unpack_from('<%dI' % nchild, toc, pos)
    return f, pkgs, dirs, files, children, dir_count

def walk(dirs, files, children, dc, d, prefix, out):
    _, fc, cc = dirs[d]
    for c in children[fc:fc + cc]:
        if c < dc:
            walk(dirs, files, children, dc, c, prefix + dirs[c][0] + '/', out)
        else:
            out.append((prefix + files[c - dc][0], c - dc))

def read_member(f, rec):
    _, size, eo, es, codec = rec
    f.seek(eo); data = f.read(es)
    if codec == 1:
        import zstandard
        data = zstandard.ZstdDecompressor().decompress(data, max_output_size=size)
    return data

if __name__ == '__main__':
    cmd, nup = sys.argv[1], sys.argv[2]
    f, pkgs, dirs, files, children, dc = parse(nup)
    entries = []
    for p in pkgs:
        tag = 'pkg%x_v%d_k%d' % (p['tid'], p['ver'], p['kind'])
        for kind in ('exefs', 'romfs'):
            if p[kind] != 0xFFFFFFFF:
                walk(dirs, files, children, dc, p[kind], tag + '/' + kind + '/', entries)
    if cmd == 'list':
        with open(sys.argv[3], 'w', encoding='utf-8') as o:
            for path, i in entries:
                o.write('%s\t%d\t%d\n' % (path, files[i][1], files[i][4]))
        print(len(entries), 'entries;', pkgs)
    elif cmd == 'extract':
        outdir, subs = sys.argv[3], sys.argv[4:]
        for path, i in entries:
            if any(s in path for s in subs):
                dst = os.path.join(outdir, path)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                open(dst, 'wb').write(read_member(f, files[i]))
                print('extracted', path, files[i][1])
