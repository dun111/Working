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

    def _game_size():
        if persistent.fill_screen is False or renpy.variant("mobile") or renpy.variant("web"):
            return DESIGN_W, DESIGN_H
        aspect = min(max(_monitor_aspect(), 4.0 / 3.0), 32.0 / 9.0)
        if aspect >= 16.0 / 9.0:
            return int(round(DESIGN_H * aspect)) // 2 * 2, DESIGN_H
        return DESIGN_W, int(round(DESIGN_W / aspect)) // 2 * 2

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

default persistent.fill_screen = True

init -2 python:
    def wide_bg(path):
        if (GAME_W, GAME_H) == (DESIGN_W, DESIGN_H):
            return path
        tiny = Flatten(Transform(path, xysize=(64, 36)))
        back = Transform(tiny, fit="cover", xysize=(GAME_W, GAME_H),
                         matrixcolor=BrightnessMatrix(-0.22))
        front = Transform(path, xysize=map_wh(DESIGN_W, DESIGN_H), pos=map_xy(0, 0))
        return Fixed(back, front, xysize=(GAME_W, GAME_H))

    def full_cover(path, **kwargs):
        return Transform(path, fit="cover", xysize=(GAME_W, GAME_H), **kwargs)


init python:
    def _pill(color, w, h):
        return Transform(rbox(color, h // 2), xysize=(int(w), int(h)))

    def _eye(x, y, w=34, h=12):
        layers = [
            ("#ff1a0a", 3.4, 4.2, 0.10),
            ("#ff1a0a", 2.4, 2.8, 0.18),
            ("#ff2a10", 1.6, 1.8, 0.35),
            ("#ff3a1a", 1.0, 1.0, 1.0),
            ("#ffe0d0", 0.45, 0.45, 1.0),
        ]
        kids = []
        for col, sw, sh, al in layers:
            kids.append(At(Transform(_pill(col, w * sw, h * sh), alpha=al),
                           Transform(xcenter=x, ycenter=y)))
        return Fixed(*kids, xysize=(1, 1))

    def scare_face(path, crop, eyes):
        shadow = Transform(path, crop=crop, matrixcolor=flat_color("#120206"))
        return Fixed(shadow, *[_eye(x, y) for x, y in eyes], xysize=crop[2:], fit_first=False)

    SCARE_FACES = {
        "passenger": scare_face("images/louis_neutral.png", (150, 0, 480, 560), [(205, 232), (310, 232)]),
        "conductor": scare_face("images/dorothy_neutral.png", (90, 0, 400, 540), [(133, 220), (238, 220)]),
    }


define config.default_textshader = "typewriter"

