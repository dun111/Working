# ==============================================================================
# DEPARTURE AT 4:00  -  credits_fx.rpy
# What happens when you click someone's name in the credits.
# Just the name, animated - each person in their own way:
#
#   ERIC    coding   - typed out with a cursor, then it glitches and decodes
#                      itself out of code symbols... then the lights go out
#                      and something comes for you (always, even with
#                      jumpscares turned off).
#                      (his DEBUG game is in the Arcade with the ERIC PASS)
#   HANNAH  drawing  - each letter is sketched in pencil then inked, and the
#                      characters she drew are drawn in beside it
#   AYDIN   websites - grey "loading" blocks pulse, then each letter loads in
#   RYAN    eating   - the letters are dropped in... then eaten, bite by bite
#
# Each one has a "camera" that slowly pans / zooms (the cam_* transforms).
# The little text in the corner is CREDITS_CORNER_TEXT in secrets.rpy.
# ==============================================================================

define CREDIT_FONT = "gui/Telegraphem.otf"     # the font the names are written in
define CREDIT_STEP = 0.3                        # seconds between letters
define CREDIT_SIZE = 190                        # how big the names are

init python:
    import random as _crandom

    def _esc(t):
        """Text that shows [ and { as they are."""
        return t.replace("[", "[[").replace("{", "{{")

    # ------------------------------------------- a word that decodes itself
    _GLYPHS = "01#$%&*<>/=+;:"

    def _scramble(st, at, word, delay, size, color, font):
        if st < delay:
            return Null(), 0.04
        out = ""
        for i, ch in enumerate(word):
            settle = delay + 0.35 + i * 0.14
            if st >= settle or ch == " ":
                out += ch
            else:
                out += _crandom.choice(_GLYPHS)
        return Text(_esc(out), size=size, color=color, font=font), (0.04 if st < delay + 0.4 + len(word) * 0.14 else None)

    def scramble_text(word, delay=0.0, size=180, color="#c8b27a", font=None):
        return DynamicDisplayable(_scramble, word=word, delay=delay, size=size, color=color, font=font or CREDIT_FONT)

    # ------------------------------------------------ text that types itself
    def _typed_plain(st, at, word, delay, cps, size, color, font, caret):
        n = int(max(0.0, st - delay) * cps)
        out = _esc(word[:n])
        if caret and int(st * 2.5) % 2 == 0:
            out += "|"
        return Text(out, size=size, color=color, font=font), 0.05

    def typed_text(word, delay=0.0, cps=12, size=60, color="#e8e4dc", font=None, caret=True):
        return DynamicDisplayable(_typed_plain, word=word, delay=delay, cps=cps, size=size, color=color,
                                  font=font or CREDIT_FONT, caret=caret)



# ------------------------------------------------------------------------------
# SHARED BITS
# ------------------------------------------------------------------------------

# the screen slowly dims behind the name (no flashes)
transform credit_dim(total):
    alpha 0.0
    easein 0.5 alpha 1.0
    pause total
    easeout 0.6 alpha 0.0

# a camera move: from (zoom, x, y) to (zoom, x, y), then fade out
transform cam(z0, x0, y0, z1, x1, y1, dur, r0=0, r1=0):
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    zoom z0
    xoffset x0
    yoffset y0
    rotate r0
    alpha 0.0
    parallel:
        ease 0.4 alpha 1.0
    parallel:
        ease dur zoom z1 xoffset x1 yoffset y1 rotate r1
    easeout 0.5 alpha 0.0

transform credit_in(d):
    alpha 0.0
    pause d
    easein 0.4 alpha 1.0

transform credit_grow(d, dur=0.8):
    xzoom 0.0
    pause d
    easeout dur xzoom 1.0

transform draw_in(delay, dur=0.9):
    crop_relative True
    crop (0.0, 1.0, 1.0, 0.0)
    pause delay
    linear dur crop (0.0, 0.0, 1.0, 1.0)

transform letter_sketch(d):
    crop_relative True
    crop (0.0, 0.0, 0.0, 1.0)
    pause d
    linear 0.4 crop (0.0, 0.0, 1.0, 1.0)

transform letter_drop(d):
    alpha 0.0
    yoffset -420
    pause d
    parallel:
        easein 0.2 alpha 1.0
    parallel:
        easein_bounce 0.75 yoffset 0

# a full-screen layer for the camera to move
screen credit_cam(z0, x0, y0, z1, x1, y1, dur, r0=0, r1=0):
    fixed:
        xysize (config.screen_width, config.screen_height)
        at cam(z0, x0, y0, z1, x1, y1, dur, r0, r1)
        transclude


# ==============================================================================
# ERIC  -  CODING
# ==============================================================================

transform eric_type_out(d):
    alpha 1.0
    pause d
    linear 0.05 alpha 0.0

transform eric_glitch(d):
    alpha 0.0
    pause d
    alpha 1.0
    block:
        linear 0.04 xoffset 10
        linear 0.04 xoffset -8
        linear 0.04 xoffset 0
        pause 0.5
        linear 0.03 xoffset 6
        linear 0.03 xoffset 0
        pause 1.6
        repeat

screen eric_surprise():
    zorder 200
    $ type_t = 0.5
    $ decode_t = type_t + 4 / 6.0 + 0.9
    $ total = decode_t + 2.6

    add Solid("#06060ae8") at credit_dim(total - 0.4)
    use credit_cam(1.6, 0, 0, 1.0, 0, 0, total - 0.4):
        # typed out with a cursor...
        add typed_text("ERIC", type_t, 6, CREDIT_SIZE, "#8a8f9c"):
            align (0.5, 0.46)
            at eric_type_out(decode_t)
        # ...then it decodes itself out of code symbols
        add scramble_text("ERIC", decode_t, CREDIT_SIZE, "#c8b27a"):
            align (0.5, 0.46)
            at eric_glitch(decode_t)
        add Solid("#c8b27a"):
            align (0.5, 0.62)
            xysize (480, 3)
            alpha 0.7
            at credit_grow(decode_t + 0.8, 0.6)

    timer total action [Hide("eric_surprise"), Function(eric_scare)]


# ---- Eric's game: DEBUG ------------------------------------------------------
# Each piece of code has one broken line. Click it. Three rounds.

define DEBUG_POOL = [
    (["label start:", "    scene black", "    l \"I'm gonna look around.", "    jump carriage_1_start"],
     2, _("The quote is never closed.")),
    (["init python:", "    def give_tickets(n)", "        persistent.tickets += n", "        return n"],
     1, _("def needs a : at the end.")),
    (["label ticket:", "    d \"Excuse me sir, tickets please.\"", "    $ has_ticket = True", "    jum carriage_1_hub"],
     3, _("jum should be jump.")),
    (["screen map():", "    textbutton \"Carriage 2\" action Jump(\"c2\")", "  textbutton \"Back\" action Return()", "    text \"4:00\""],
     2, _("This line isn't indented like the others.")),
    (["$ clues = 3", "if clues = 3:", "    jump accusation_scene", "else:", "    jump carriage_5_hub"],
     1, _("Use == to compare, not =.")),
    (["label carriage_6:", "    show screen dark_eyes", "    $ jumpscare(\"conductor\"", "    u \"Not me. Him.\""],
     2, _("The bracket is never closed.")),
    (["define l = Character(\"Louis\")", "label hello:", "    l \"Oh, I see.\"", "    retrun"],
     3, _("retrun should be return.")),
    (["default found_key = False", "label c4:", "    if found_key", "        jump carriage_5_start"],
     2, _("if needs a : at the end.")),
]

default dbg_rounds = []
default dbg_round = 0
default dbg_strikes = 0
default dbg_t = 45.0
default dbg_picked = None
default dbg_bad = []
default dbg_result = None

init python:
    DEBUG_ROUNDS = 3

    def debug_reset():
        store.dbg_rounds = renpy.random.sample(DEBUG_POOL, DEBUG_ROUNDS)
        store.dbg_round = 0
        store.dbg_strikes = 0
        store.dbg_t = [60.0, 45.0, 30.0][persistent.mg_difficulty]
        store.dbg_picked = None
        store.dbg_bad = []
        store.dbg_result = None

    def debug_pick(i):
        if store.dbg_result is not None or store.dbg_picked is not None:
            return
        lines, bug, why = store.dbg_rounds[store.dbg_round]
        if i == bug:
            store.dbg_picked = i
            sfx("ui_click")
        elif i not in store.dbg_bad:
            store.dbg_bad = store.dbg_bad + [i]
            store.dbg_strikes += 1
            if store.dbg_strikes >= 3:
                store.dbg_result = "lose"
        renpy.restart_interaction()

    def debug_next():
        store.dbg_round += 1
        store.dbg_picked = None
        store.dbg_bad = []
        if store.dbg_round >= DEBUG_ROUNDS:
            store.dbg_result = "win"
            sfx("win")
        renpy.restart_interaction()

    def debug_tick():
        if store.dbg_result is not None:
            return
        store.dbg_t -= 0.1
        if store.dbg_t <= 0:
            store.dbg_t = 0
            store.dbg_result = "lose"
        renpy.restart_interaction()

    def eric_scare():
        """Eric's credit ends with this. It always plays, even with jumpscares off."""
        renpy.music.set_volume(0.0, 0.05, channel="music")
        renpy.invoke_in_new_context(renpy.call_screen, "eric_jumpscare")
        renpy.music.set_volume(1.0, 1.5, channel="music")
        secret_found("eric_scare")

screen mg_debug():
    use mg_scene(_("DEBUG"), _("Each piece of code has one broken line. Click it."), "black", skippable=False):
        if dbg_result is None:
            timer 0.1 repeat True action Function(debug_tick)
            if dbg_picked is not None:
                timer 1.4 action Function(debug_next)

        use mg_stats([_("Round %d / %d") % (min(dbg_round + 1, DEBUG_ROUNDS), DEBUG_ROUNDS),
                      _("Strikes: %d / 3") % dbg_strikes, _("Time: %d") % max(0, dbg_t)])

        if dbg_round < DEBUG_ROUNDS:
            $ lines, bug, why = dbg_rounds[dbg_round]
            frame:
                xalign 0.5
                yalign 0.55
                xysize (1300, 620)
                padding (0, 0)
                background rbox("#14161d", 22)
                vbox:
                    xfill True
                    hbox:
                        xpos 28
                        ypos 22
                        spacing 12
                        for col in ("#a5594f", "#b39a52", "#5f9a6a"):
                            add rbox(col, 9) xysize (18, 18)
                    null height 40
                    for i, ln in enumerate(lines):
                        $ good = (dbg_picked == i)
                        $ bad = (i in dbg_bad)
                        button:
                            xfill True
                            ysize 70
                            padding (0, 0)
                            background (Solid("#1f3a2a") if good else (Solid("#3a1a1a") if bad else None))
                            hover_background Solid("#1f3a2a" if good else ("#3a1a1a" if bad else "#1e212b"))
                            action Function(debug_pick, i)
                            hbox:
                                xpos 20
                                yalign 0.5
                                spacing 30
                                text str(i + 1):
                                    xsize 70
                                    text_align 1.0
                                    size 28
                                    color "#4a4f5c"
                                    font CREDIT_FONT
                                text _esc(ln):
                                    size 32
                                    color ("#98c379" if good else ("#e06c75" if bad else "#d7dae0"))
                                    font CREDIT_FONT
                    null height 30
                    if dbg_picked is not None:
                        text why:
                            xpos 130
                            size 26
                            color "#98c379"
                            font CREDIT_FONT

        if dbg_result == "win":
            use mg_end(_("BUILD SUCCEEDED"), "win")
        elif dbg_result == "lose":
            use mg_end(_("BUILD FAILED"), "lose")


# ==============================================================================
# HANNAH  -  DRAWING THE CHARACTERS
# ==============================================================================

define HANNAH_DRAWS = [("dorothy neutral", 0.16), ("fedora neutral", 0.84)]

transform ink_over(d):
    alpha 0.0
    pause d
    ease 0.8 alpha 1.0

screen hannah_surprise():
    zorder 200
    $ start = 0.6
    $ ink_t = start + CREDIT_STEP * 6 + 0.2
    $ total = ink_t + 4.4

    add Solid("#06060ae8") at credit_dim(total - 0.4)
    # the camera follows the pencil from left to right, then steps back
    use credit_cam(1.35, 300, 0, 1.0, 0, 0, total - 0.4):
        # the characters she drew, drawn in either side
        for i, (img, x) in enumerate(HANNAH_DRAWS):
            $ d = ink_t + 0.2 + i * 1.2
            add Transform(img, matrixcolor=flat_color("#3c3a44"), fit="contain", ysize=760):
                xcenter x
                yanchor 1.0
                ypos 1.0
                at draw_in(d, 1.0)
            add Transform(img, fit="contain", ysize=760):
                xcenter x
                yanchor 1.0
                ypos 1.0
                at ink_over(d + 1.0)
        # her name: sketched in pencil, then inked
        hbox:
            align (0.5, 0.42)
            spacing 4
            for i, ch in enumerate("HANNAH"):
                fixed:
                    fit_first True
                    text ch:
                        size CREDIT_SIZE
                        color "#8a8794"
                        font CREDIT_FONT
                        at letter_sketch(start + i * CREDIT_STEP)
                    text ch:
                        size CREDIT_SIZE
                        color "#d9c9a3"
                        font CREDIT_FONT
                        at ink_over(ink_t + i * 0.08)

    timer total action Hide("hannah_surprise")


# ==============================================================================
# AYDIN  -  MAKING WEBSITES
# ==============================================================================
# Each letter starts as a wireframe box while the page loads (with a loading %),
# then the letters render in one by one, then the whole name gets selected like
# text on a web page, and deselected.

define AYDIN_COL = "#9db8b4"

# the wireframe: an outline box that pulses while it waits
transform wire_box(d):
    alpha 0.0
    pause 0.2
    ease 0.3 alpha 0.8
    block:
        ease 0.35 alpha 0.35
        ease 0.35 alpha 0.8
        repeat int(d / 0.7) + 1
    linear 0.08 alpha 0.0

# the letter renders in: drops a little, flickers once, settles
transform web_render(d):
    alpha 0.0
    yoffset -26
    pause d
    alpha 1.0
    easein 0.22 yoffset 0
    alpha 0.4
    pause 0.04
    alpha 1.0

# the selection highlight behind each letter
transform web_select(d, off):
    alpha 0.0
    pause d
    linear 0.05 alpha 0.4
    pause (off - d)
    ease 0.3 alpha 0.0

init python:
    def _loading(st, at, start, dur):
        p = int(max(0.0, min(1.0, (st - 0.2) / dur)) * 100)
        return Text(_("LOADING  %d%%") % p, size=22, color=AYDIN_COL, font=CREDIT_FONT), 0.05

screen aydin_surprise():
    zorder 200
    $ start = 1.4
    $ n = 5
    $ loaded = start + CREDIT_STEP * n
    $ sel_t = loaded + 0.5
    $ desel_t = sel_t + 0.07 * n + 0.9
    $ total = desel_t + 1.6

    add Solid("#06060ae8") at credit_dim(total - 0.4)
    # the camera comes down from above, like scrolling a page
    use credit_cam(1.3, 0, 260, 1.0, 0, 0, total - 0.4):
        hbox:
            align (0.5, 0.44)
            spacing 10
            for i, ch in enumerate("AYDIN"):
                $ d = start + i * CREDIT_STEP
                fixed:
                    fit_first True
                    text ch:
                        size CREDIT_SIZE
                        color "#00000000"
                        font CREDIT_FONT
                    # selected, like text on a page
                    fixed:
                        xfill True
                        yfill True
                        at web_select(sel_t + i * 0.07, desel_t)
                        add rbox("#3fa8a0", 6)
                    # wireframe box
                    fixed:
                        align (0.5, 0.38)
                        xysize (120, 160)
                        at wire_box(d)
                        add rbox(AYDIN_COL, 12)
                        add rbox("#06060a", 10):
                            pos (3, 3)
                            xysize (114, 154)
                    text ch:
                        size CREDIT_SIZE
                        color AYDIN_COL
                        font CREDIT_FONT
                        at web_render(d)
        # the loading bar and %
        add rbox(AYDIN_COL, 3):
            align (0.5, 0.63)
            xysize (520, 4)
            at credit_grow(0.2, loaded - 0.2)
        add DynamicDisplayable(_loading, start=0.2, dur=loaded - 0.2):
            align (0.5, 0.68)

    timer total action Hide("aydin_surprise")


# ==============================================================================
# RYAN  -  EATING
# ==============================================================================
# The letters are dropped in like food (they squash when they land), then
# eaten: each one wiggles, then three bites, crumbs flying everywhere.

define RYAN_LETTERS = ["R", "Y", "A", "N", "", "", "", "Y", "A"]
define RYAN_FOOD = ["#c98a4a", "#b5653a", "#d6a85a", "#9a6a3a", "#c98a4a", "#b5653a"]

# dropped in, squashing as it lands
transform food_drop(d):
    alpha 0.0
    yoffset -460
    yanchor 1.0
    ypos 1.0
    pause d
    alpha 1.0
    easein 0.42 yoffset 0
    ease 0.08 yzoom 0.72 xzoom 1.25
    ease 0.12 yzoom 1.1 xzoom 0.94
    ease 0.1 yzoom 1.0 xzoom 1.0

# a little wiggle, then three bites (each one makes it jump)
transform bite(d):
    crop_relative True
    crop (0.0, 0.0, 1.0, 1.0)
    pause (d - 0.3)
    linear 0.05 rotate 6
    linear 0.05 rotate -6
    linear 0.05 rotate 4
    linear 0.05 rotate 0
    pause 0.1
    ease 0.1 crop (0.0, 0.0, 0.64, 1.0) zoom 1.1
    ease 0.12 zoom 1.0
    pause 0.12
    ease 0.1 crop (0.0, 0.0, 0.32, 1.0) zoom 1.1
    ease 0.12 zoom 1.0
    pause 0.12
    ease 0.1 crop (0.0, 0.0, 0.0, 1.0)

# a crumb flies out and falls
transform crumb(d, dx, dy):
    alpha 0.0
    pause d
    alpha 1.0
    parallel:
        easeout 0.35 yoffset (-dy)
        easein 0.55 yoffset 140
    parallel:
        linear 0.9 xoffset dx rotate (dx * 3)
    parallel:
        pause 0.6
        linear 0.3 alpha 0.0

screen ryan_surprise():
    zorder 200
    $ eat_t = 0.6 + CREDIT_STEP * len(RYAN_LETTERS) + 0.9
    $ total = eat_t + 0.62 * 6 + 1.6

    add Solid("#06060ae8") at credit_dim(total - 0.4)
    # the camera leans in, tilted, then settles
    use credit_cam(1.4, 0, 80, 1.0, 0, 0, total - 0.4, -4, 0):
        hbox:
            align (0.5, 0.46)
            spacing 6
            $ k = 0
            for i, ch in enumerate(RYAN_LETTERS):
                if ch:
                    $ col = RYAN_FOOD[i % len(RYAN_FOOD)]
                    $ chomp = eat_t + k * 0.62
                    $ k += 1
                    fixed:
                        fit_first True
                        # an invisible copy keeps the space, so the other
                        # letters don't slide over as it's eaten
                        text ch:
                            size CREDIT_SIZE
                            color "#00000000"
                            font CREDIT_FONT
                        fixed:
                            fit_first True
                            at food_drop(0.6 + i * CREDIT_STEP)
                            text ch:
                                size CREDIT_SIZE
                                color col
                                font CREDIT_FONT
                                outlines [(0, "#00000066", 3, 6)]
                                at bite(chomp)
                        # crumbs from each bite
                        for b in range(3):
                            for c in range(3):
                                add rbox(RYAN_FOOD[(i + c) % len(RYAN_FOOD)], 5):
                                    xysize (10 + c * 3, 10 + c * 3)
                                    pos (70 - b * 22, 110)
                                    at crumb(chomp + 0.12 + b * 0.24, ((c - 1) * 60) + (b - 1) * 15, 40 + c * 25)

    timer total action Hide("ryan_surprise")


# ==============================================================================
# ERIC'S JUMPSCARE
# ==============================================================================
# The lights go out. Silence. Two red eyes open far away in the dark and
# slowly get closer... then Louis, blacked out, lunges at the screen.

define ES_DARK = 2.6        # how long the dark lasts before it comes for you
define ES_HOLD = 1.1        # how long the face stays in yours

transform es_eyes_far:
    xalign 0.5
    yalign 0.42
    alpha 0.0
    zoom 0.25
    pause 0.9
    linear 0.4 alpha 1.0
    parallel:
        linear (ES_DARK - 1.3) zoom 0.55
    parallel:
        pause 0.6
        alpha 0.0
        pause 0.12
        alpha 1.0
        pause 0.5
        linear 0.05 alpha 0.0
        pause 0.08
        alpha 1.0

transform es_lunge:
    xanchor 0.5
    yanchor 0.42
    xpos 0.5
    ypos 0.5
    zoom 0.5
    alpha 0.0
    pause ES_DARK
    alpha 1.0
    easein 0.1 zoom 3.4
    block:
        linear 0.025 xoffset 26 yoffset -14
        linear 0.025 xoffset -24 yoffset 16
        linear 0.025 xoffset 18 yoffset 10
        linear 0.025 xoffset -20 yoffset -12
        repeat

transform es_red:
    alpha 0.0
    pause ES_DARK
    block:
        alpha 0.55
        pause 0.06
        alpha 0.15
        pause 0.05
        alpha 0.45
        pause 0.08
        alpha 0.1
        pause 0.06
        repeat

transform es_band(y, dx, delay):
    ypos y
    alpha 0.0
    pause (ES_DARK + delay)
    alpha 0.9
    block:
        linear 0.03 xoffset dx
        linear 0.03 xoffset (-dx)
        alpha 0.0
        pause 0.07
        alpha 0.9
        repeat

screen eric_jumpscare():
    modal True
    zorder 400
    add Solid("#000000")
    # the eyes in the dark
    fixed:
        xysize (1, 1)
        at es_eyes_far
        add _eye(-46, 0, 46, 16)
        add _eye(46, 0, 46, 16)
    # the face
    add SCARE_FACES["passenger"] at es_lunge
    # red pulses and torn bars
    add Solid("#6a0000") at es_red
    for k, (y, dx) in enumerate([(0.18, 60), (0.41, -90), (0.57, 120), (0.76, -70), (0.9, 40)]):
        add Solid("#000000"):
            xysize (config.screen_width, 40 + k * 9)
            at es_band(y, dx, k * 0.04)
    timer (ES_DARK + ES_HOLD) action Return()

