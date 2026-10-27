# Fit the game to the player's monitor instead of letterboxing it.

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


default persistent.jumpscares = True


# JUMPSCARE FACES

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
        "conductor": scare_face("images/dorothy_normal.png", (90, 0, 400, 540), [(133, 220), (238, 220)]),
    }

transform scare_lunge:
    xanchor 0.5
    yanchor 0.42
    xpos 0.5
    ypos 0.5
    zoom 1.4
    parallel:
        easein 0.22 zoom 2.7
        linear 0.6 zoom 3.0
    parallel:
        block:
            linear 0.03 xoffset 22 yoffset -10
            linear 0.03 xoffset -20 yoffset 12
            linear 0.03 xoffset 12 yoffset 6
            linear 0.03 xoffset -14 yoffset -8
            repeat

transform scare_still:
    xanchor 0.5
    yanchor 0.42
    xpos 0.5
    ypos 0.5
    zoom 2.6

transform scare_red:
    alpha 0.0
    pause 0.05
    linear 0.04 alpha 0.55
    linear 0.25 alpha 0.15

screen jumpscare(face, hold=0.85):
    zorder 300
    modal True
    timer hold action Return()
    add Solid("#000000")
    add SCARE_FACES.get(face, SCARE_FACES["passenger"]) at (scare_still if persistent.reduce_motion else scare_lunge)
    add Solid("#7a0000"):
        blend "add"
        at scare_red
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)

init python:
    JUMPSCARE_KINDS = {
        "passenger": ("sting", 0.85),
        "conductor": ("sting", 0.85),
        "flicker":   ("static", 1.0),
        "crawler":   ("screech", 1.0),
        "claws":     ("screech", 0.9),
        "glitch":    ("static", 0.8),
        "window":    ("thud", 1.1),
        "eyes":      ("sting", 1.5),
    }

    def jumpscare(kind="passenger", hold=None):
        if not persistent.jumpscares:
            return
        snd, default_hold = JUMPSCARE_KINDS.get(kind, JUMPSCARE_KINDS["passenger"])
        hold = default_hold if hold is None else hold
        sfx(snd)
        if kind in SCARE_FACES:
            renpy.call_screen("jumpscare", kind, hold)
        else:
            renpy.call_screen("scare_" + kind, hold)
        renpy.with_statement(Dissolve(0.25))

    class _SCARE(object):
        last = 0.0
        count = 0

    def random_scare(chance=0.12):
        import time
        if not (store.in_loop and persistent.jumpscares):
            return
        if _SCARE.count >= 4 or time.time() - _SCARE.last < 75:
            return
        if renpy.random.random() < chance:
            _SCARE.last = time.time()
            _SCARE.count += 1
            jumpscare(renpy.random.choice(["flicker", "glitch", "eyes", "crawler"]))


# MORE KINDS OF SCARE

transform flicker_face:
    alpha 0.0
    pause 0.12
    alpha 1.0
    pause 0.07
    alpha 0.0
    pause 0.16
    alpha 1.0
    pause 0.06
    alpha 0.0
    pause 0.2
    alpha 1.0
    linear 0.3 zoom 3.2

transform flicker_face_soft:
    alpha 0.0
    ease 0.5 alpha 1.0
    linear 0.3 zoom 3.2

screen scare_flicker(hold=1.0):
    zorder 300
    modal True
    timer hold action Return()
    add Solid("#000000")
    add SCARE_FACES[renpy.random.choice(["passenger", "conductor"])]:
        xanchor 0.5
        yanchor 0.42
        xpos 0.5
        ypos 0.5
        zoom 2.4
        at (flicker_face_soft if persistent.reduce_flashes else flicker_face)

transform crawl_across:
    xpos 1.15
    ypos 1.02
    yanchor 1.0
    xanchor 0.5
    parallel:
        easein 0.75 xpos -0.2
    parallel:
        block:
            linear 0.05 yoffset -12 rotate -84
            linear 0.05 yoffset 0 rotate -96
            repeat

screen scare_crawler(hold=1.0):
    zorder 300
    modal True
    timer hold action Return()
    add Solid("#2a0606")
    add Transform("images/louis_neutral.png", matrixcolor=flat_color("#050002"), zoom=0.9, xzoom=1.6):
        transform_anchor True
        at (scare_still if persistent.reduce_motion else crawl_across)
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)

transform claw_rip(delay=0.0):
    transform_anchor True
    rotate -32
    xzoom 0.0
    pause delay
    easein 0.12 xzoom 1.0
    pause 0.45
    linear 0.25 alpha 0.0

screen scare_claws(hold=0.9):
    zorder 300
    modal True
    timer hold action Return()
    add Solid("#00000088")
    for i in range(3):
        add rbox("#b0100a", 10):
            xysize (int(config.screen_width * 0.9), 22)
            xanchor 0.5
            yanchor 0.5
            xpos 0.5
            ypos 0.36 + i * 0.14
            at claw_rip(i * 0.07)
    add Solid("#7a0000"):
        blend "add"
        at scare_red

init python:
    def _glitch_bands(n=14):
        r = renpy.random
        return [(r.random(), r.randint(8, 70), r.choice(["#000000", "#ffffff", "#b0100a", "#1a1a24"]),
                 r.randint(-140, 140)) for _i in range(n)]

transform glitch_band(dx=0):
    xoffset 0
    block:
        linear 0.04 xoffset dx
        linear 0.04 xoffset -dx // 2
        linear 0.03 xoffset 0
        repeat

screen scare_glitch(hold=0.8):
    zorder 300
    modal True
    timer hold action Return()
    timer 0.08 repeat True action Function(renpy.restart_interaction)
    add SCARE_FACES["passenger"]:
        xanchor 0.5
        yanchor 0.42
        xpos 0.5
        ypos 0.5
        zoom 2.0
        alpha 0.8
    for by, bh, bc, bdx in _glitch_bands():
        add Solid(bc):
            xysize (config.screen_width, bh)
            ypos by
            alpha 0.85
            at glitch_band(bdx)

transform window_slam:
    zoom 0.3
    alpha 0.0
    pause 0.25
    alpha 1.0
    easein 0.12 zoom 1.6
    pause 0.6

transform crack_in(delay=0.0, a=0):
    transform_anchor True
    rotate a
    xzoom 0.0
    pause delay
    easein 0.08 xzoom 1.0

screen scare_window(hold=1.1):
    zorder 300
    modal True
    timer hold action Return()
    add Solid("#05070c")
    add rbox("#2a2a33", 40):
        align (0.5, 0.5)
        xysize (900, 640)
    add rbox("#0a0e18", 30):
        align (0.5, 0.5)
        xysize (860, 600)
    add SCARE_FACES["conductor"]:
        xanchor 0.5
        yanchor 0.42
        xpos 0.5
        ypos 0.5
        at window_slam
    for i, a in enumerate((18, -40, 75, 130, -110)):
        add Solid("#d8e4ff"):
            xysize (420, 3)
            xanchor 0.0
            yanchor 0.5
            xpos 0.5
            ypos 0.5
            at crack_in(0.37 + i * 0.02, a)

init python:
    def _eye_field(n=16):
        r = renpy.random
        return [(r.uniform(0.08, 0.92), r.uniform(0.1, 0.85), r.uniform(0.0, 0.6)) for _i in range(n)]

transform eyes_open(delay=0.0):
    alpha 0.0
    yzoom 0.1
    pause delay
    easein 0.15 alpha 1.0 yzoom 1.0
    pause (1.0 - delay)
    easein 0.25 zoom 4.0 alpha 0.0

screen scare_eyes(hold=1.5):
    zorder 300
    modal True
    timer hold action Return()
    add Solid("#000000")
    for ex, ey, ed in _eye_field():
        fixed:
            xysize (1, 1)
            pos (ex, ey)
            at eyes_open(ed)
            add _eye(-30, 0, 24, 9)
            add _eye(30, 0, 24, 9)


# EYES IN THE DARK

transform eyes_blink(delay=0.0):
    alpha 0.0
    pause delay
    ease 1.2 alpha 1.0
    block:
        pause 2.2
        linear 0.06 yzoom 0.1
        linear 0.08 yzoom 1.0
        pause 1.1
        repeat

screen dark_eyes(pairs=((0.3, 0.38, 0.0), (0.68, 0.46, 0.9))):
    zorder 60
    for ex, ey, ed in pairs:
        fixed:
            xysize (1, 1)
            pos (ex, ey)
            at eyes_blink(ed)
            add _eye(-34, 0, 26, 9)
            add _eye(34, 0, 26, 9)


# DO OR DIE

transform ticket_burn:
    alpha 0.0
    zoom 1.25
    easein 0.12 alpha 1.0 zoom 1.0
    pause 1.2
    linear 0.5 alpha 0.0

screen ticket_flash():
    zorder 250
    modal True
    add Solid("#0a0000cc")
    text _("DO OR DIE"):
        align (0.5, 0.45)
        size 150
        color "#c4100a"
        font GFONT
        outlines [(4, "#000000", 0, 0)]
        textshader ("jitter:u__jitter=(6.0, 6.0)" if not persistent.reduce_motion else None)
        at ticket_burn
    timer 1.9 action Return()

init python:
    def ticket_flash():
        if persistent.jumpscares:
            sfx("static")
        renpy.call_screen("ticket_flash")


# SHADOWS ON THE MAP  (Part 2 only)

transform shadow_blip:
    alpha 0.0
    linear 0.03 alpha 0.85
    pause 0.08
    linear 0.03 alpha 0.0
    pause 0.05
    linear 0.02 alpha 0.6
    linear 0.12 alpha 0.0

screen haunt_flash(sx):
    zorder 46
    add Transform("images/louis_neutral.png", matrixcolor=flat_color("#050002"), zoom=0.95):
        xanchor 0.5
        xpos sx
        yanchor 1.0
        ypos 1.08
        at shadow_blip
    timer 0.5 action Hide("haunt_flash")

init python:
    import random as _hrandom

    def _edge_x():
        w = config.screen_width
        return _hrandom.choice((90, 160, w - 90, w - 160))

    def shadow_flash(x=None):
        if not persistent.jumpscares:
            return
        sfx("static")
        renpy.show_screen("haunt_flash", x if x is not None else _edge_x())

    def haunt_tick():
        if not (store.in_loop and persistent.jumpscares) or not active_map_title():
            return
        if _hrandom.random() < 0.3:
            sfx("static")
            renpy.show_screen("haunt_flash", _edge_x())

screen loop_haunt():
    zorder 45
    if in_loop and persistent.jumpscares:
        timer 6.0 repeat True action Function(haunt_tick)

init python:
    config.overlay_screens.append("loop_haunt")


define config.default_textshader = "typewriter"

init python:
    def _fx_shader(shader, contents):
        if persistent.reduce_motion or persistent.text_fx != "full":
            return contents
        return [(renpy.TEXT_TAG, u"shader=" + shader)] + contents + [(renpy.TEXT_TAG, u"/shader")]

    def _fx_wrap(open_tags, close_tags, contents):
        if persistent.text_fx == "off":
            return contents
        return ([(renpy.TEXT_TAG, t) for t in open_tags] + contents +
                [(renpy.TEXT_TAG, t) for t in close_tags])

    def fx_shake(tag, argument, contents):
        return _fx_shader(u"jitter:u__jitter=3.0, 3.0", contents)

    def fx_tremble(tag, argument, contents):
        return _fx_shader(u"jitter:u__jitter=1.2, 1.2", contents)

    def fx_wave(tag, argument, contents):
        return _fx_shader(u"wave:u__amplitude=5.0:u__frequency=2.0:u__wavelength=20.0", contents)

    def fx_scream(tag, argument, contents):
        inner = _fx_shader(u"jitter:u__jitter=4.0, 4.0", contents)
        return _fx_wrap([u"size=+14", u"b", u"color=#ff5a4a"], [u"/color", u"/b", u"/size"], inner)

    def fx_whisper(tag, argument, contents):
        return _fx_wrap([u"alpha=0.6", u"size=-4", u"i"], [u"/i", u"/size", u"/alpha"], contents)

    def fx_glitch(tag, argument, contents):
        inner = _fx_shader(u"jitter:u__jitter=6.0, 0.8", contents)
        return _fx_wrap([u"color=#e8a49c"], [u"/color"], inner)

    def fx_big(tag, argument, contents):
        return _fx_wrap([u"size=+12", u"b"], [u"/b", u"/size"], contents)

    config.custom_text_tags["shake"] = fx_shake
    config.custom_text_tags["tremble"] = fx_tremble
    config.custom_text_tags["wave"] = fx_wave
    config.custom_text_tags["scream"] = fx_scream
    config.custom_text_tags["whisper"] = fx_whisper
    config.custom_text_tags["glitch"] = fx_glitch
    config.custom_text_tags["big"] = fx_big
