# ==============================================================================
# DEPARTURE AT 4:00  -  horror.rpy
# Jumpscares and the creepy stuff.
#
#   $ jumpscare("passenger")   a face lunges at the screen (or "conductor")
#   $ jumpscare("crawler")     other kinds: flicker, crawler, claws, glitch,
#                              window, eyes  (see JUMPSCARE_KINDS)
#   $ random_scare()           small chance of a scare (Part 2 maps)
#   show screen dark_eyes      eyes watching from the dark
#   $ ticket_flash()           "DO OR DIE" burns onto the screen
#   $ shadow_flash()           a figure flickers at the edge of the screen
#
# Everything here can be turned off with Settings > Accessibility > JUMPSCARES.
# Sounds and the vignette are made by tools/gen_horror_assets.py.
# ==============================================================================

default persistent.jumpscares = True


# ------------------------------------------------------------------------------
# JUMPSCARE FACES
# ------------------------------------------------------------------------------
# A shadow cut from a character's head with glowing eyes. The passenger uses
# Louis's outline, the conductor uses Dorothy's (it took her voice, so...).

init python:
    def _pill(color, w, h):
        return Transform(rbox(color, h // 2), xysize=(int(w), int(h)))

    def _eye(x, y, w=34, h=12):
        """A glowing slit: stacked pills fading outwards, hot core in the middle."""
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

    # crop (x, y, w, h) of the head in the png, eye centres inside that crop
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

# modal so clicks can't skip it; it ends itself with its own timer (a modal
# screen would block an ordinary pause underneath it)
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
    # kind -> (sound, how long it holds)
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
        """$ jumpscare("crawler")  - does nothing if jumpscares are turned off."""
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
        """Random scares on the Part 2 maps: rare, spaced out, capped per session."""
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


# ------------------------------------------------------------------------------
# MORE KINDS OF SCARE
# ------------------------------------------------------------------------------

# FLICKER - the lights stutter and a face is there between flashes
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
        at flicker_face

# CRAWLER - something low and fast drags itself across the floor
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
    # a dim red backdrop so the black shape reads against it
    add Solid("#2a0606")
    add Transform("images/louis_neutral.png", matrixcolor=flat_color("#050002"), zoom=0.9, xzoom=1.6):
        transform_anchor True
        at (scare_still if persistent.reduce_motion else crawl_across)
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)

# CLAWS - three red slashes rip across the screen
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

# GLITCH - the picture tears into bands and a face shows through
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

# WINDOW - a face slams against the glass
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

# EYES - the dark is full of them, then they all come for you
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


# ------------------------------------------------------------------------------
# EYES IN THE DARK
# ------------------------------------------------------------------------------

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


# ------------------------------------------------------------------------------
# DO OR DIE
# ------------------------------------------------------------------------------

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


# ------------------------------------------------------------------------------
# SHADOWS ON THE MAP  (Part 2 only)
# ------------------------------------------------------------------------------
# While you're looking at a carriage map in the loop, every so often a figure
# flickers at the edge of the screen for a split second, with a crackle.

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
        """Somewhere near the left or right edge of the screen."""
        w = config.screen_width
        return _hrandom.choice((90, 160, w - 90, w - 160))

    def shadow_flash(x=None):
        """$ shadow_flash()  - one figure flickers at the edge of the screen."""
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
