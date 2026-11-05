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
    def wide_bg(path):
        if (GAME_W, GAME_H) == (DESIGN_W, DESIGN_H):
            return path
        tiny = Flatten(Transform(path, xysize=(64, 36)))
        back = Transform(tiny, fit="cover", xysize=(GAME_W, GAME_H),
                         matrixcolor=BrightnessMatrix(-0.22))
        front = Transform(path, xysize=map_wh(DESIGN_W, DESIGN_H), pos=map_xy(0, 0))
        return Fixed(back, front, xysize=(GAME_W, GAME_H))

    def check_window_shape():
        # Called once at startup. If the window isn't the shape the game started
        # at, remember its shape and restart once so the game fills it exactly.
        if renpy.variant("mobile") or renpy.variant("web") or _preferences.fullscreen:
            return
        pw, ph = renpy.get_physical_size()
        if pw <= 0 or ph <= 0:
            return
        aspect = round(pw / float(ph), 4)
        persistent.window_aspect = aspect
        want = _size_for(aspect)
        if want == (config.screen_width, config.screen_height):
            return
        # Only restart once for a given window shape, and never twice within two
        # minutes, so it can never loop.
        import time
        if persistent.window_relaunched_for == aspect or time.time() - (persistent.window_relaunched_at or 0) < 120:
            return
        persistent.window_relaunched_for = aspect
        persistent.window_relaunched_at = time.time()
        renpy.save_persistent()
        renpy.quit(relaunch=True)

    def map_bg(path, top, bottom, ceiling=None, floor=None):
        # Carriage art sits exactly where the hotspots expect it. Its picture has flat
        # dark bands above and below the carriage (top and bottom are where the carriage
        # starts and ends, as fractions of the picture's height), so the carriage's own
        # top and bottom edges are stretched out to the edges of the screen instead.
        # `ceiling` / `floor` use one flat colour instead, for art whose edge rows have
        # things in them (drips, a dark corner) that would turn into stripes.
        w, h = map_wh(DESIGN_W, DESIGN_H)
        ox, oy = map_xy(0, 0)
        art = Transform(path, xysize=(w, h))
        t = int(h * top) + 3
        b = int(h * bottom) - 3
        parts = []
        if ox > 0:
            tiny = Flatten(Transform(art, xysize=(64, 36)))
            parts.append(Transform(tiny, fit="cover", xysize=(GAME_W, GAME_H), matrixcolor=BrightnessMatrix(-0.22)))
        parts.append(Transform(art, pos=(ox, oy)))
        if oy + t > 0:
            above = Solid(ceiling) if ceiling else Transform(art, crop=(0, t, w, 2))
            parts.append(Transform(above, xysize=(w, oy + t), pos=(ox, 0)))
        if oy + b < GAME_H:
            below = Solid(floor) if floor else Transform(art, crop=(0, b - 2, w, 2))
            parts.append(Transform(below, xysize=(w, GAME_H - (oy + b)), pos=(ox, oy + b)))
        return Fixed(*parts, xysize=(GAME_W, GAME_H))

    def full_cover(path, **kwargs):
        return Transform(path, fit="cover", xysize=(GAME_W, GAME_H), **kwargs)


define config.default_textshader = "typewriter"

