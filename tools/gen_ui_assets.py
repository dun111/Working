"""
Generate rounded-corner masks (game/gui/round/rN.png) and the key string loop
(game/gui/key_loop.png, key_loop_front.png).  Usage:  python3 tools/gen_ui_assets.py game/gui
"""
import zlib, struct, math, os, sys
OUT = sys.argv[1]

def write_png(path, w, h, px):
    raw = b''.join(b'\x00' + bytes(px[y*w*4:(y+1)*w*4]) for y in range(h))
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
                           + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))

SS = 4
def cover(fn, x, y):
    n = 0
    for i in range(SS):
        for j in range(SS):
            if fn(x + (i + .5) / SS, y + (j + .5) / SS):
                n += 1
    return n / float(SS * SS)

os.makedirs(os.path.join(OUT, 'round'), exist_ok=True)
RADII = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 34, 38, 40, 48,
         64, 96, 128, 160, 200, 256]
for r in RADII:
    s = 2 * r + 2
    px = bytearray(s * s * 4)
    for y in range(s):
        for x in range(s):
            px_c, py_c = x + 0.5, y + 0.5
            cx = min(max(px_c, r), s - r)
            cy = min(max(py_c, r), s - r)
            d = ((px_c - cx) ** 2 + (py_c - cy) ** 2) ** 0.5
            a = min(1.0, max(0.0, r + 0.5 - d))
            px[(y*s+x)*4:(y*s+x)*4+4] = bytes((255, 255, 255, int(round(a * 255))))
    write_png(os.path.join(OUT, 'round', 'r%d.png' % r), s, s, px)

K = 4
W, H = 34 * K, 60 * K
cx, cy = W / 2.0, 34 * K
a, b, t = 11 * K, 23.5 * K, 3 * K
kx, ky, kr = cx, cy - b, 3.6 * K
def ring_d(x, y):
    nx, ny = (x - cx) / a, (y - cy) / b
    rr = math.hypot(nx, ny)
    return abs(rr - 1.0) * min(a, b) * (1 + 0.15 * abs(ny))
CORE, EDGE = (150, 150, 164), (70, 70, 84)
px = bytearray(W * H * 4)
for y in range(H):
    for x in range(W):
        on_ring = cover(lambda X, Y: ring_d(X, Y) <= t / 2.0, x, y)
        on_core = cover(lambda X, Y: ring_d(X, Y) <= t / 2.0 - K * 0.9, x, y)
        on_knot = cover(lambda X, Y: (X - kx) ** 2 + (Y - ky) ** 2 <= kr * kr, x, y)
        knot_core = cover(lambda X, Y: (X - kx) ** 2 + (Y - ky) ** 2 <= (kr - K) ** 2, x, y)
        alpha = max(on_ring, on_knot)
        core = max(on_core, knot_core)
        if alpha:
            c = [int(EDGE[i] + (CORE[i] - EDGE[i]) * (core / alpha if alpha else 0)) for i in range(3)]
            px[(y*W+x)*4:(y*W+x)*4+4] = bytes(c + [int(round(alpha * 255))])
write_png(os.path.join(OUT, 'key_loop.png'), W, H, px)

front = bytearray(px)
for y in range(H):
    for x in range(W):
        f = min(1.0, max(0.0, (cx + K - x) / (2.0 * K)))
        i = (y * W + x) * 4 + 3
        front[i] = int(front[i] * f)
write_png(os.path.join(OUT, 'key_loop_front.png'), W, H, front)
print("ok", len(RADII), "masks")
