default persistent.cheat_nuke = False
default persistent.window_aspect = None
default persistent.window_relaunched_for = None
default persistent.window_relaunched_at = 0

init -100 python:
    DESIGN_W, DESIGN_H = 1920, 1080

    def _monitor_aspect():
        try:
            import pygame_sdl2
            if not pygame_sdl2.display.get_init():
                pygame_sdl2.display.init()
            x, y, w, h = pygame_sdl2.display.get_display_bounds(0)
            if w > 0 and h > 0:
                return float(w) / h
        except Exception:
            pass
        return 16.0 / 9.0

    def _window_aspect():
        # On a Mac the game window is shorter than the screen (menu bar, title bar,
        # Dock), so the screen's shape leaves black bars. The real window shape is
        # measured at startup (check_window_shape) and used from then on; the
        # screen's shape is only used in fullscreen or before it has been measured.
        try:
            if not getattr(renpy.game.preferences, "fullscreen", False) and persistent.window_aspect:
                return float(persistent.window_aspect)
        except Exception:
            pass
        return _monitor_aspect()

    def _size_for(aspect):
        aspect = min(max(aspect, 4.0 / 3.0), 32.0 / 9.0)
        if aspect >= 16.0 / 9.0:
            return int(round(DESIGN_H * aspect)) // 2 * 2, DESIGN_H
        return DESIGN_W, int(round(DESIGN_W / aspect)) // 2 * 2

    def _game_size():
        # The game always takes the shape of the screen it's on, so there are no black bars.
        if renpy.variant("mobile") or renpy.variant("web"):
            return DESIGN_W, DESIGN_H
        return _size_for(_window_aspect())

    GAME_W, GAME_H = _game_size()
    MAP_X0 = (GAME_W - DESIGN_W) // 2
    MAP_Y0 = (GAME_H - DESIGN_H) // 2

    MAP_K = min(1.5, max(1.0, GAME_W / float(DESIGN_W)))
    MAP_OX = int((GAME_W - DESIGN_W * MAP_K) / 2)
    MAP_OY = int((GAME_H - DESIGN_H * MAP_K) / 2)

    def map_xy(x, y):
        return (int(MAP_OX + x * MAP_K), int(MAP_OY + y * MAP_K))

    def map_wh(w, h):
        return (int(w * MAP_K), int(h * MAP_K))


init -2 python:
    def check_window_shape():
        # Called once at startup. If the window isn't the shape the game started
        # at, remember its shape and restart once so the game fills it exactly.
        if renpy.variant("mobile") or renpy.variant("web") or _preferences.fullscreen:
            return
        pw, ph = renpy.get_physical_size()
        if pw <= 0 or ph <= 0:
            return
        aspect = round(pw / float(ph), 4)
        current = config.screen_width / float(config.screen_height)
        # macOS gives the window a slightly different height on different launches
        # (779-782 pixels on this Mac). Only a real change of shape is worth a
        # restart; a few pixels leave a sliver nobody can see.
        if abs(aspect - current) / current < 0.02:
            return
        persistent.window_aspect = aspect
        # Only restart once for a given window shape, and never twice within two
        # minutes, so it can never loop.
        import time
        if persistent.window_relaunched_for == aspect or time.time() - (persistent.window_relaunched_at or 0) < 120:
            return
        persistent.window_relaunched_for = aspect
        persistent.window_relaunched_at = time.time()
        renpy.save_persistent()
        renpy.quit(relaunch=True)

    def map_bg(path, top, bottom, ceiling=None, floor=None, lamp=None, lamps=6, eerie=False, backdrop=None, nearest=False):
        # Carriage art sits exactly where the hotspots expect it. Its picture has flat
        # dark bands above and below the carriage (top and bottom are where the carriage
        # starts and ends, as fractions of the picture's height), so the carriage's own
        # top and bottom edges are stretched out to the edges of the screen instead.
        # `ceiling` / `floor` use one flat colour instead, for art whose edge rows have
        # things in them (drips, a dark corner) that would turn into stripes.
        w, h = map_wh(DESIGN_W, DESIGN_H)
        ox, oy = map_xy(0, 0)
        art = Transform(path, xysize=(w, h), nearest=nearest)
        t = int(h * top) + 3
        b = int(h * bottom) - 3
        parts = []
        if ox > 0:
            tiny = Flatten(Transform(art, xysize=(64, 36)))
            parts.append(Transform(tiny, fit="cover", xysize=(GAME_W, GAME_H), matrixcolor=BrightnessMatrix(-0.22)))
        if backdrop:
            # For art with see-through gaps (e.g. a cut-out corner): fill them with a flat colour.
            parts.append(Transform(Solid(backdrop), xysize=(w, h), pos=(ox, oy)))
        parts.append(Transform(art, pos=(ox, oy)))
        if oy + t > 0:
            above = Solid(ceiling) if ceiling else Transform(art, crop=(0, t, w, 2))
            parts.append(Transform(above, xysize=(w, oy + t), pos=(ox, 0)))
        if oy + b < GAME_H:
            below = Solid(floor) if floor else Transform(art, crop=(0, b - 2, w, 2))
            parts.append(Transform(below, xysize=(w, GAME_H - (oy + b)), pos=(ox, oy + b)))
        if lamp:
            parts += map_ambience(ox, oy + t, w, oy + b, lamp, lamps, eerie)
        return Fixed(*parts, xysize=(GAME_W, GAME_H))

    # ---------- Ambience on the carriage maps: edge shadows and dust ----------
    # Made only from shapes and effects (no pictures), so it sits under any ceiling or
    # floor art added later.

    def _glow(color, w, h, strength):
        # A soft pool of light: stacked rounded shapes, brightest in the middle.
        kids = []
        n = 14
        for i in range(n):
            f = 1.0 - i / float(n)
            ww, hh = max(2, int(w * f)), max(2, int(h * f))
            kids.append(Transform(rbox(color, hh // 2), xysize=(ww, hh), pos=((w - ww) // 2, (h - hh) // 2), alpha=0.028 * strength))
        return Transform(Fixed(*kids, xysize=(w, h)), blend="add")

    def _shade(width, height, at_top, strength=0.55, steps=40):
        # A soft darkening toward the top or bottom edge of the screen.
        kids = []
        step = max(1, height // steps)
        for i in range(steps):
            a = strength * (1.0 - i / float(steps)) ** 1.6
            y = i * step if at_top else height - (i + 1) * step
            kids.append(Transform(Solid("#000000"), xysize=(width, step + 1), pos=(0, y), alpha=a))
        return Fixed(*kids, xysize=(width, height))

    def map_ambience(x0, ceil_y, width, floor_y, color, lamps, eerie):
        import random as _r
        rng = _r.Random(int(ceil_y) * 7 + lamps)
        parts = [
            _shade(GAME_W, int(ceil_y + 60), True),
            Transform(_shade(GAME_W, int(GAME_H - floor_y + 60), False), ypos=int(floor_y - 60)),
        ]
        # NUKE (type "nuke" on the main menu, or F9 > TOOLS): the old lamp light, blown out to blinding.
        for i in range(lamps):
            cx = x0 + int(width * (i + 0.5) / lamps)
            pool = Fixed(
                Transform(_glow(color, 900, 420, 3.0), pos=(-450, -210)),
                Transform(_glow(color, 640, 1000, 1.5), pos=(-320, 0)),
                xysize=(1, 1))
            lit = At(pool, nuke_flicker(rng.uniform(0.0, 3.0), eerie))
            glow = ConditionSwitch("persistent.reduce_motion", pool, "True", lit)
            parts.append(Transform(ConditionSwitch("persistent.cheat_nuke", glow, "True", Null()), pos=(cx, int(ceil_y))))
        for i in range(14):
            speck = Solid("#fff2d6", xysize=(3, 3))
            moving = At(speck, dust_fall(rng.uniform(9.0, 15.0), rng.uniform(0.0, 9.0), rng.choice([20, 30, 45])))
            still = Transform(speck, alpha=0.25, ypos=rng.uniform(0.1, 0.9))
            parts.append(Transform(ConditionSwitch("persistent.reduce_motion", still, "True", moving),
                                   xpos=x0 + int(width * rng.uniform(0.03, 0.97))))
        return parts

    def full_cover(path, **kwargs):
        return Transform(path, fit="cover", xysize=(GAME_W, GAME_H), **kwargs)


# NUKE lamp light: flickers like a failing reactor.
transform nuke_flicker(d=0.0, eerie=False):
    alpha 1.0
    pause d
    block:
        pause (0.6 if eerie else 1.2)
        linear 0.05 alpha 0.4
        linear 0.06 alpha 1.0
        pause 0.5
        linear 0.04 alpha 0.2
        linear 0.08 alpha 1.0
        ease 1.0 alpha 0.8
        ease 1.0 alpha 1.0
        repeat

# A dust speck drifting slowly down through the light.
transform dust_fall(dur, delay, sway):
    alpha 0.0
    ypos 0.0
    pause delay
    block:
        ypos 0.05
        xoffset 0
        alpha 0.0
        parallel:
            linear dur ypos 0.95
        parallel:
            ease (dur * 0.3) alpha 0.45
            pause (dur * 0.4)
            ease (dur * 0.3) alpha 0.0
        parallel:
            ease (dur * 0.5) xoffset sway
            ease (dur * 0.5) xoffset (-sway)
        repeat

define config.default_textshader = "typewriter"

