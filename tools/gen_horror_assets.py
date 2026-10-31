"""
Generate the horror sounds and the vignette:
  game/audio/sting.wav   - jumpscare hit (screech sliding down + thump + noise)
  game/audio/static.wav  - short static crackle (shadow flashes on the maps)
  game/gui/vignette.png  - dark edges, stretched to full screen in-game
  game/audio/thud.wav    - heavy hit
  game/audio/screech.wav - metal scrape for the crawler / claws
  game/gui/flashlight.png - black square with a soft round hole (flashlight minigame)
  game/gui/glow.png      - soft white radial glow (tint it: smoke, backlight)
Usage:  python3 tools/gen_horror_assets.py game
"""
import math, os, random, struct, sys, wave, zlib

GAME = sys.argv[1]
RATE = 44100
random.seed(4)

def write_wav(path, samples):
    peak = max(abs(s) for s in samples) or 1.0
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(32767 * 0.85 * s / peak)) for s in samples))

def sting():
    n = int(RATE * 1.15)
    out = []
    phases = [0.0] * 5
    detune = [1.0, 1.013, 0.987, 1.5, 2.02]
    lp = 0.0
    for i in range(n):
        t = i / float(RATE)
        f = 180 + 1220 * math.exp(-t * 3.2)
        s = 0.0
        for k, d in enumerate(detune):
            phases[k] = (phases[k] + f * d / RATE) % 1.0
            s += (2 * phases[k] - 1) * (0.5 if k < 3 else 0.25)
        env = min(1.0, t / 0.006) * math.exp(-t * 2.4)
        thump = math.sin(2 * math.pi * 48 * t) * math.exp(-t * 9) * 1.4
        lp += 0.35 * (random.uniform(-1, 1) - lp)
        noise = lp * math.exp(-t * 7) * 0.9
        out.append(s * env * 0.6 + thump + noise)
    return out

def static():
    n = int(RATE * 0.28)
    out, lp = [], 0.0
    for i in range(n):
        t = i / float(RATE)
        lp += 0.6 * (random.uniform(-1, 1) - lp)
        crackle = random.uniform(-1, 1) if random.random() < 0.02 else 0.0
        env = min(1.0, t / 0.01) * (1 - t / 0.28)
        out.append((lp * 0.7 + crackle) * env)
    return out

def write_png(path, w, h, px):
    raw = b"".join(b"\x00" + bytes(px[y*w*4:(y+1)*w*4]) for y in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
                           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

def vignette(w=480, h=270):
    px = bytearray(w * h * 4)
    for y in range(h):
        for x in range(w):
            dx = (x - w / 2.0) / (w / 2.0)
            dy = (y - h / 2.0) / (h / 2.0)
            d = math.sqrt(dx * dx * 0.8 + dy * dy)
            a = max(0.0, min(1.0, (d - 0.45) / 0.75)) ** 1.6
            px[(y*w+x)*4 + 3] = int(a * 235)
    return w, h, px

def thud():
    n = int(RATE * 0.6)
    out, lp = [], 0.0
    for i in range(n):
        t = i / float(RATE)
        lp += 0.08 * (random.uniform(-1, 1) - lp)
        body = math.sin(2 * math.pi * (60 - 25 * t) * t) * math.exp(-t * 7)
        out.append(body * 1.2 + lp * 4 * math.exp(-t * 20))
    return out

def screech():
    n = int(RATE * 0.9)
    out, ph, ph2 = [], 0.0, 0.0
    for i in range(n):
        t = i / float(RATE)
        f = 2300 + 900 * math.sin(t * 37) + 400 * random.uniform(-1, 1)
        ph = (ph + f / RATE) % 1.0
        ph2 = (ph2 + f * 1.01 / RATE) % 1.0
        env = min(1.0, t / 0.02) * (1 - t / 0.9) ** 1.5
        out.append(((2 * ph - 1) + (2 * ph2 - 1) * 0.7 + random.uniform(-0.6, 0.6)) * env)
    return out

def flashlight(size=400, inner=118, outer=196):
    px = bytearray(size * size * 4)
    c = size / 2.0
    for y in range(size):
        for x in range(size):
            d = math.hypot(x + 0.5 - c, y + 0.5 - c)
            a = min(1.0, max(0.0, (d - inner) / float(outer - inner)))
            a = a * a * (3 - 2 * a)
            px[(y*size+x)*4 + 3] = int(a * 250)
    return size, size, px

def glow(size=256):
    px = bytearray(size * size * 4)
    c = size / 2.0
    for y in range(size):
        for x in range(size):
            d = math.hypot(x + 0.5 - c, y + 0.5 - c) / c
            a = max(0.0, 1.0 - d) ** 1.8
            px[(y*size+x)*4:(y*size+x)*4+4] = bytes((255, 255, 255, int(a * 255)))
    return size, size, px

os.makedirs(os.path.join(GAME, "audio"), exist_ok=True)
write_png(os.path.join(GAME, "gui", "glow.png"), *glow())
write_wav(os.path.join(GAME, "audio", "thud.wav"), thud())
write_wav(os.path.join(GAME, "audio", "screech.wav"), screech())
write_png(os.path.join(GAME, "gui", "flashlight.png"), *flashlight())
write_wav(os.path.join(GAME, "audio", "sting.wav"), sting())
write_wav(os.path.join(GAME, "audio", "static.wav"), static())
write_png(os.path.join(GAME, "gui", "vignette.png"), *vignette())
print("ok")
