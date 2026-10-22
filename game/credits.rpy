# ==============================================================================
# DEPARTURE AT 4:00  -  credits.rpy (credits fx)
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
        """Eric's credit ends with this. It always plays, even with jumpscares off.
        It's an overlay screen that closes itself (no new context, so it can't loop)."""
        if renpy.get_screen("eric_jumpscare"):
            return
        import time
        _ESCARE.start = time.time()
        _ESCARE.can_skip = False
        renpy.music.set_volume(0.0, 0.05, channel="music")
        renpy.show_screen("eric_jumpscare")

    class _ESCARE(object):
        start = 0.0
        can_skip = False

    def eric_scare_tick():
        """Ends the scare by the clock (not a one-off timer, so it can't end
        early or hang)."""
        import time
        t = time.time() - _ESCARE.start
        if t >= ES_DARK + 0.3 and not _ESCARE.can_skip:
            _ESCARE.can_skip = True
            renpy.restart_interaction()
        if t >= ES_DARK + ES_HOLD:
            eric_scare_end()

    def eric_scare_end():
        if not renpy.get_screen("eric_jumpscare"):
            return
        renpy.hide_screen("eric_jumpscare")
        renpy.music.set_volume(1.0, 1.5, channel="music")
        secret_found("eric_scare")      # after, so the "+tickets" pop-up doesn't spoil it
        renpy.restart_interaction()

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
    # once the face has hit, any click / ESC ends it early
    key "game_menu" action Function(eric_scare_end)
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
    timer 0.1 repeat True action Function(eric_scare_tick)
    if _ESCARE.can_skip:
        button:
            xysize (config.screen_width, config.screen_height)
            background None
            action Function(eric_scare_end)


# ==============================================================================
# DEPARTURE AT 4:00  -  credits.rpy (credits styles)
# The four looks the credits can have (Settings > Display > CREDITS STYLE, or
# the < > in the top-right corner of the credits):
#
#   SCROLL      the game's art drifting behind, roles and names rolling up
#   TICKETS     every member on a ticket card
#   FILM        old film credits: role on the left, name on the right
#   SPOTLIGHT   a black stage: the camera drifts over every carriage and
#               everyone on the train under a spotlight, one name at a time
#
# Every name can be clicked for its surprise (credits_fx.rpy). The people and
# their roles come from CREW in screens.rpy.
# ==============================================================================

define CREDIT_STYLES = [
    ("scroll",     _("SCROLL")),
    ("tickets",    _("TICKETS")),
    ("film",       _("FILM")),
    ("spotlight",  _("SPOTLIGHT")),
]

default persistent.credits_style = "scroll"

# every song file the game has had (game/Songs and music_source), for the credits:
# (title, artist)
define CREDIT_MUSIC = [
    ("Grekhov Theme", "Departure at 4:00"),
    ("Rendezvous (Instrumental)", "Carriage 3"),
    ("We Do What We Want (Edit)", "Alan Fitzpatrick"),
    ("We Do What We Want", "Alan Fitzpatrick"),
    ("The Days (NOTION Remix)", "Chrystal"),
    ("Dreamin", "PARTYNEXTDOOR"),
    ("MAKE IT TO THE MORNING", "PARTYNEXTDOOR"),
    ("Say It", ""),
    ("still love you (Slowed)", ""),
    ("TBH", ""),
    ("LARP Music", "larp music"),
    ("Stayin' Alive", "Bee Gees"),
    ("Slide", "Calvin Harris"),
    ("End Of Beginning", "Djo"),
    ("Walking On A Dream", "Empire Of The Sun"),
    ("Pumped Up Kicks", "Foster The People"),
    ("Grand Theft Auto VI Main Theme", "Rockstar Games"),
    ("GTA VI: An Extended Look", "Rockstar Games"),
    ("GTA VI Trailer Song (Edit)", "Rockstar Games"),
    ("Flower In A Hurricane", "Justice ft. Tame Impala, SZA, King Gizzard & the Lizard Wizard"),
    ("Earrings", "Malcolm Todd"),
    ("Midnight City", "M83"),
    ("Sunflower", "Post Malone, Swae Lee"),
    ("Somebody's Watching Me", "Rockwell"),
    ("STELLA", "SAINT PEPSI"),
    ("Music Sounds Better With You", "Stardust"),
    ("Loser", "Tame Impala"),
    ("The Less I Know The Better", "Tame Impala"),
    ("Everybody Wants To Rule The World", "Tears For Fears"),
    ("Self Aware", "Temper City"),
    ("RHYNO", "Travis Scott"),
]

init python:
    def credits_style_now():
        s = persistent.credits_style
        return s if s in dict(CREDIT_STYLES) else "scroll"

    def credits_style_name():
        return dict(CREDIT_STYLES)[credits_style_now()]

    def set_credits_style(s):
        persistent.credits_style = s
        if renpy.get_screen("about"):
            credits_music_on()
        renpy.restart_interaction()

    def credits_style_step(d):
        ids = [k for k, _n in CREDIT_STYLES]
        k = ids.index(credits_style_now())
        set_credits_style(ids[(k + d) % len(ids)])

    def credit_sections():
        """The longer credits after the crew - everything in the game, by name,
        taken from the game's own lists:
        [(heading, [(line, small line under it or ""), ...]), ...]"""
        passengers = [m[1] for m in MANIFEST] + ["The Passenger", "The Gentleman", "The Conductor"]
        places = []
        for t in MAP_TITLES.values():
            line = "%s - %s" % (t[0], t[1])
            if line not in places:
                places.append(line)
        places += ["CARRIAGE 6", "THE EMPTY TRAIN"]
        return [
            (_("The passengers"), [(n, "") for n in passengers]),
            (_("The carriages"), [(n, "") for n in places]),
            (_("Endings"), [("Wrong Guess", "Ending 1"), ("Partial Truth", "Ending 2"), ("The True Line", "Ending 3")]),
            (_("Clues"), [(c[1], "") for c in CLUE_LIST]),
            (_("Minigames"), [(g[1], "") for g in MINIGAME_LIST]),
            (_("The 4:00 Casino"), [(g[1], "") for g in CASINO_GAMES]),
            (_("Achievements"), [(x["title"], "") for x in ACHIEVEMENTS]),
            (_("Gamepasses"), [(g[1], "") for g in GAMEPASSES]),
            (_("Radio stations"), [(n, RADIO_FREQ.get(k, "")) for k, n in RADIO_STATIONS]),
            (_("Music"), CREDIT_MUSIC),
            (_("Fonts"), [("Graduate", ""), ("Telegraphem", ""), ("Reggae One", ""), ("DejaVu Sans", "")]),
            (_("Made with"), [("Ren'Py", renpy.version_only)]),
            (_("Special thanks"), [("Mr Kromo", "")]),
        ]


# ------------------------------------------------------------------------------
# SCROLL
# ------------------------------------------------------------------------------

screen credits_scroll():
    default cred_adj = ui.adjustment()
    add Solid("#000000")
    add ("credits_art_still" if persistent.reduce_motion else "credits_art")
    # dark enough to read over, darkest down the middle
    add Solid("#000000a8")
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)

    # ---- the roll ----
    viewport:
        xalign 0.5
        xsize 1600
        ysize config.screen_height
        yadjustment cred_adj
        mousewheel True
        draggable True

        vbox:
            xsize 1600
            spacing 0

            null height config.screen_height

            add "game_logo_cycle":
                xalign 0.5
                xsize 720
                ysize 440
                fit "contain"

            null height 180

            # psst: every name does something when you click it (credits_fx.rpy)
            for roles, people in credit_roles():
                for role in roles:
                    text role.upper():
                        xalign 0.5
                        size 26
                        color credit_accent()
                        font GFONT
                null height 8
                for c in people:
                    textbutton c["name"]:
                        xalign 0.5
                        padding (20, 0)
                        background None
                        action Function(credits_click, c["key"])
                        text_size 72
                        text_color "#f2ead8"
                        text_hover_color credit_accent()
                        text_font CREDIT_FONT
                        text_outlines [(0, "#00000099", 3, 4)]
                null height 90

            # the passengers, the music, the fonts, the engine
            for heading, lines in credit_sections():
                text heading.upper():
                    xalign 0.5
                    size 26
                    color credit_accent()
                    font GFONT
                null height 12
                for ln, sub in lines:
                    text ln:
                        xalign 0.5
                        size 56
                        color "#f2ead8"
                        font CREDIT_FONT
                        outlines [(0, "#00000099", 3, 4)]
                    if sub:
                        text sub:
                            xalign 0.5
                            size 22
                            color "#a8a8a8"
                            font GFONT
                    null height 14
                null height 110

            text _("SPECIAL CREDITS"):
                xalign 0.5
                size 26
                color credit_accent()
                font GFONT
            null height 8
            text _("larp music"):
                xalign 0.5
                size 72
                color "#f2ead8"
                font CREDIT_FONT
            null height 200

            text _("THANKS FOR PLAYING!"):
                xalign 0.5
                size 80
                color "#ffffff"
                font CREDIT_FONT
            null height 30
            text _("Version [config.version]   ·   Made with Ren'Py [renpy.version_only]"):
                xalign 0.5
                size 18
                color "#8888a0"
                font GFONT

            null height config.screen_height

    timer 0.03 repeat True action Function(credits_step, cred_adj)


# ------------------------------------------------------------------------------
# TICKETS  (the original credits)
# ------------------------------------------------------------------------------

# the little badge next to each name (what they did)
define CREW_BADGES = {"eric": "</>", "hannah": "✎", "aydin": "www", "ryan": "☕"}

# one ticket card in the credits: number stub, name, every role they took on
screen crew_card(ci, c):
    $ card_h = max(150, 96 + 34 * len(c["roles"]))
    hbox:
        frame:
            xsize 150
            ysize card_h
            background rbox(credit_accent(), 26)
            text ("%02d" % (ci + 1)):
                align (0.5, 0.5)
                size 54
                color "#0a0a0e"
                font GFONT

        # perforation dots
        vbox:
            xsize 24
            yalign 0.5
            spacing 10
            for _d in range(max(6, len(c["roles"]) + 3)):
                add rbox("#33334a", 4):
                    xalign 0.5
                    xsize 8
                    ysize 8

        vbox:
            yalign 0.5
            spacing 4
            xoffset 14
            hbox:
                spacing 18
                text c["name"]:
                    size 60
                    color "#f2ead8"
                    hover_color credit_accent()
                    font CREDIT_FONT
                    outlines [(0, "#00000080", 2, 3)]
                if c["key"] in CREW_BADGES:
                    frame:
                        yalign 0.6
                        padding (12, 4)
                        background rbox("#22222c", 10)
                        text CREW_BADGES[c["key"]]:
                            size 22
                            color "#8888a0"
                            hover_color "#e8e4dc"
                            font "DejaVuSans.ttf"
            null height 4
            for role in c["roles"]:
                hbox:
                    spacing 12
                    add rbox(credit_accent(), 2):
                        xysize (8, 8)
                        yalign 0.5
                    text role:
                        size 22
                        color "#e6a817"
                        font GFONT

# credits: cards slide in one after another, lean out when you point at them,
# and the logo floats
transform card_in(d):
    alpha 0.0
    xoffset 260
    pause d
    easein 0.6 alpha 1.0 xoffset 0

transform card_hover:
    on idle:
        ease 0.25 xoffset 0 zoom 1.0
    on hover:
        ease 0.25 xoffset -18 zoom 1.01



screen credits_tickets():
    default cred_adj = ui.adjustment()
    add Solid("#08080c")

    if persistent.menu_fx and not persistent.reduce_motion:
        for sy, sdur, sdelay, slen in MENU_STREAKS:
            add Solid("#ffffff10", xsize=slen, ysize=2):
                ypos sy
                at streak(sdur, sdelay)

    # ---- left title panel ----
    frame:
        xpos 80
        ypos 70
        xsize 560
        ysize 830
        padding (2, 2)
        background rbox("#ffffff1e", 40)
        at fade_slide_in(0.0, xoff=-50)

        frame:
            xfill True
            yfill True
            padding (40, 40)
            background rbox("#14141aee", 38)

            vbox:
                spacing 26
                xfill True

                text _("CREDITS"):
                    xalign 0.5
                    size 54
                    color "#ffffff"
                    font GFONT

                add rbox("#e0521f", 2):
                    xalign 0.5
                    xsize 160
                    ysize 6

                add "game_logo_cycle":
                    xsize 440
                    ysize 260
                    fit "contain"
                    xalign 0.5
                    at logo_float

                fixed:
                    xfill True
                    ysize 22
                    use menu_tagline

                null height 10

                text _("Version [config.version]"):
                    xalign 0.5
                    size 20
                    color "#e6a817"
                    font GFONT

                text _("Made with Ren'Py [renpy.version_only]"):
                    xalign 0.5
                    size 16
                    color "#8888a0"
                    font GFONT

    # ---- scrolling ticket cards ----
    viewport:
        xpos 720
        ypos 70
        xsize (config.screen_width - 800)
        ysize 830
        yadjustment cred_adj
        mousewheel True
        draggable True

        vbox:
            xsize (config.screen_width - 820)
            spacing 22

            null height 760

            for ci, c in enumerate(CREW):
                # psst: everyone's card does something when you click it (credits_fx.rpy)
                frame:
                    xfill True
                    padding (0, 0)
                    background None
                    at card_in(0.3 + ci * 0.15)
                    button:
                        xfill True
                        padding (0, 0)
                        background rbox("#14141a", 26)
                        hover_background rbox("#1d1820", 26)
                        action Function(credits_click, c["key"])
                        at card_hover
                        use crew_card(ci, c)

            for heading, lines in credit_sections():
                frame:
                    xfill True
                    background rbox("#14141a", 26)
                    padding (40, 30)
                    vbox:
                        spacing 8
                        xalign 0.5
                        text heading.upper():
                            xalign 0.5
                            size 20
                            color "#e6a817"
                            font GFONT
                        for ln, sub in lines:
                            text ((ln + "   ·   " + sub) if sub else ln):
                                xalign 0.5
                                size 34
                                color "#ffffff"
                                font GFONT

            frame:
                xfill True
                background rbox("#14141a", 26)
                padding (40, 34)
                vbox:
                    spacing 10
                    xalign 0.5
                    text _("SPECIAL CREDITS"):
                        xalign 0.5
                        size 20
                        color "#e6a817"
                        font GFONT
                    text _("larp music"):
                        xalign 0.5
                        size 44
                        color "#ffffff"
                        font GFONT

            text _("THANKS FOR PLAYING!"):
                xalign 0.5
                size 64
                italic True
                color "#8888a0"
                font GFONT

            null height 760

    timer 0.03 repeat True action Function(credits_step, cred_adj)


# ------------------------------------------------------------------------------
# FILM
# ------------------------------------------------------------------------------

transform film_flicker:
    alpha 0.05
    block:
        linear 0.08 alpha 0.09
        linear 0.11 alpha 0.04
        linear 0.07 alpha 0.07
        repeat

screen credits_film():
    default cred_adj = ui.adjustment()
    add Solid("#050505")
    add Transform("gui/grain.png", xysize=(config.screen_width, config.screen_height)):
        at (film_flicker if not persistent.reduce_motion else Transform(alpha=0.06))
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)

    viewport:
        xalign 0.5
        xsize 1700
        ysize config.screen_height
        yadjustment cred_adj
        mousewheel True
        draggable True
        vbox:
            xsize 1700
            null height config.screen_height
            text _("A BLACKBERRY STUDIOS GAME"):
                xalign 0.5
                size 26
                color "#9a9a9a"
                font GFONT
            null height 40
            add Transform("images/Game_Logo_Yellow.webp", matrixcolor=SaturationMatrix(0.0)):
                xalign 0.5
                xsize 640
                ysize 400
                fit "contain"
            null height 200
            for roles, people in credit_roles():
                hbox:
                    xalign 0.5
                    spacing 60
                    vbox:
                        xsize 800
                        spacing 6
                        for role in roles:
                            text role:
                                xalign 1.0
                                text_align 1.0
                                size 30
                                color "#a8a8a8"
                                font GFONT
                    vbox:
                        xsize 800
                        spacing 0
                        for c in people:
                            textbutton c["name"]:
                                padding (0, 0)
                                background None
                                action Function(credits_click, c["key"])
                                text_size 46
                                text_color "#ededed"
                                text_hover_color credit_accent()
                                text_font CREDIT_FONT
                null height 70
            null height 60
            for heading, lines in credit_sections():
                hbox:
                    xalign 0.5
                    spacing 60
                    text heading:
                        xsize 800
                        text_align 1.0
                        size 30
                        color "#a8a8a8"
                        font GFONT
                    vbox:
                        xsize 800
                        spacing 4
                        for ln, sub in lines:
                            text ln:
                                size 40
                                color "#ededed"
                                font CREDIT_FONT
                            if sub:
                                text sub:
                                    size 22
                                    color "#8a8a8a"
                                    font GFONT
                null height 80
            null height 60
            hbox:
                xalign 0.5
                spacing 60
                text _("Special credits"):
                    xsize 800
                    text_align 1.0
                    size 30
                    color "#a8a8a8"
                    font GFONT
                text _("larp music"):
                    xsize 800
                    size 46
                    color "#ededed"
                    font CREDIT_FONT
            null height 260
            text _("THE END"):
                xalign 0.5
                size 90
                color "#ededed"
                font CREDIT_FONT
            null height config.screen_height

    timer 0.03 repeat True action Function(credits_step, cred_adj)


# ------------------------------------------------------------------------------
# SPOTLIGHT
# A black stage with one spotlight. The camera drifts and zooms over a picture
# (a carriage, the train, or one of the passengers) for SPOT_TIME seconds, then
# the light moves on to the next, while the crew's roles and names fade in
# beside it. Light textures: gui/spotlight.png, gui/spot_hole.png, gui/spot_cone.png
# ------------------------------------------------------------------------------

define SPOT_TIME = 7.0          # seconds on each picture
define SPOT_X = 0.36            # where the light falls (fraction of the screen)
define SPOT_Y = 0.52
define SPOT_RX = 0.85           # the light's half-width and half-height (x screen height)
define SPOT_RY = 1.25

# (picture, "person" or "place"). People stand in the light; places are seen
# through it while the camera moves across them.
# "thing" = an object or a logo, shown whole in the middle of the light
define SPOT_SLIDES = [
    ("images/Carriage_1_With_CharacterS.webp", "place"),
    ("images/Game_Logo_Yellow.webp", "thing"),
    ("images/louis_neutral.png", "person"),
    ("images/dorothy_normal.png", "person"),
    ("images/fedora.png", "person"),
    ("images/Train_BP.webp", "place"),
    ("eduard neutral", "person"),
    ("shunyu neutral", "person"),
    ("images/Kimmy_Idle.png", "person"),
    ("himmel neutral", "person"),
    ("images/bg_carriage_5.webp", "place"),
    ("sebastian neutral", "person"),
    ("misha neutral", "person"),
    ("agatha neutral", "person"),
    ("ichora neutral", "person"),
    ("images/PT2_Carriage_1_With_CharacterS.webp", "place"),
    ("pattison neutral", "person"),
    ("alexander neutral", "person"),
    ("images/dorothy_sad.png", "person"),
    ("images/1st_carriage_Visualnovel_Background.webp", "place"),
    ("images/Key.webp", "thing"),
    ("shunyu_monster neutral", "person"),
    ("himmel_monster neutral", "person"),
    ("conductor_monster neutral", "person"),
    ("images/bg_carriage_1.webp", "place"),
    ("images/cfr27dc3e0e7c6aws3.webp", "thing"),
    ("images/Achievement_Unlock.webp", "thing"),
    ("images/Blackberry_Studios_Full.webp", "thing"),
]

init python:
    def spot_slide(i):
        img, kind = SPOT_SLIDES[i % len(SPOT_SLIDES)]
        sw, sh = config.screen_width, config.screen_height
        if kind == "person":
            return Transform(img, fit="contain", ysize=int(sh * 0.92))
        if kind == "thing":
            return Transform(img, fit="contain", xysize=(int(sh * 0.62), int(sh * 0.62)))
        return Transform(img, fit="cover", xysize=(int(sw * 1.3), int(sh * 1.3)))

    def spot_credit(i):
        """The crew block shown with picture i (the logo comes first)."""
        blocks = list(credit_roles())
        for heading, lines in credit_sections():
            if len(lines) <= 4 or any(sub for _l, sub in lines):
                # small sections, and anything with a small line (every song and its
                # artist): a slide each, the small line flashing as a role
                for ln, sub in lines:
                    blocks.append(([heading] + ([sub] if sub else []), [{"key": None, "name": ln}]))
            else:
                # long lists: three names a slide
                for k in range(0, len(lines), 3):
                    blocks.append(([heading], [{"key": None, "name": ln} for ln, _s in lines[k:k + 3]]))
        blocks.append(([_("Special credits")], [{"key": None, "name": "larp music"}]))
        if i == 0:
            return None
        return blocks[(i - 1) % len(blocks)]

    # each picture gets its own camera move, so it never feels repeated
    SPOT_MOVES = [
        (1.00, 1.18, -60, 60, 30, -20),
        (1.15, 1.02, 70, -50, -20, 20),
        (1.05, 1.25, 0, 0, 60, -40),
        (1.22, 1.05, -80, 40, -30, 10),
    ]

    def spot_move(i):
        return SPOT_MOVES[i % len(SPOT_MOVES)]

define SPOT_ROLE = 1.1          # seconds each role is up before the next one flashes in

init python:
    def spot_duration(i):
        """How long picture i stays up: longer when there are more roles to flash."""
        block = spot_credit(i)
        if block is None:
            return SPOT_TIME
        return max(SPOT_TIME, 2.2 + len(block[0]) * SPOT_ROLE + 1.8)

# the camera: fade up, drift and zoom, fade down (d = how long it's up)
transform spot_cam(z0, z1, x0, x1, y0, y1, d, key):
    alpha 0.0
    zoom z0
    xoffset x0
    yoffset y0
    parallel:
        ease 1.0 alpha 1.0
        pause (d - 2.0)
        ease 1.0 alpha 0.0
    parallel:
        linear d zoom z1 xoffset x1 yoffset y1

# a hard cut from black at the start of every picture, like a film edit
transform spot_cut(key):
    alpha 1.0
    pause 0.08
    ease 0.55 alpha 0.0

# the beam flares as the light lands on the next person
transform spot_flare(key):
    alpha 0.0
    pause 0.15
    easein 0.25 alpha 0.55
    easeout 1.4 alpha 0.0

# the light itself sways a little, like someone is holding it
transform spot_sway:
    xoffset 0
    yoffset 0
    block:
        ease 3.1 xoffset 26 yoffset -10
        ease 2.7 xoffset -18 yoffset 8
        ease 3.4 xoffset 8 yoffset 14
        ease 2.9 xoffset 0 yoffset 0
        repeat

transform spot_flicker:
    alpha 0.9
    block:
        linear 0.12 alpha 1.0
        linear 0.18 alpha 0.92
        linear 0.10 alpha 0.98
        repeat

# ---- text effects ---------------------------------------------------------

# one letter of a name: drops in from above, blurred, and lands
transform spot_letter(d):
    alpha 0.0
    yoffset -60
    zoom 1.5
    blur 10
    pause d
    parallel:
        easein_back 0.45 yoffset 0 zoom 1.0
    parallel:
        easein 0.3 alpha 1.0 blur 0

# a role: flashes in big and bright, settles into gold, then whips away
transform spot_role(d, hold):
    alpha 0.0
    zoom 1.7
    blur 14
    xoffset 0
    matrixcolor BrightnessMatrix(0.0)
    pause d
    parallel:
        easein 0.2 zoom 1.0 blur 0 alpha 1.0
    parallel:
        matrixcolor BrightnessMatrix(0.8)
        ease 0.45 matrixcolor BrightnessMatrix(0.0)
    pause (hold - 0.45)
    easeout 0.22 alpha 0.0 xoffset -70 blur 8

# the last role stays up under the name
transform spot_role_last(d):
    alpha 0.0
    zoom 1.7
    blur 14
    matrixcolor BrightnessMatrix(0.0)
    pause d
    parallel:
        easein 0.2 zoom 1.0 blur 0 alpha 1.0
    parallel:
        matrixcolor BrightnessMatrix(0.8)
        ease 0.45 matrixcolor BrightnessMatrix(0.0)

# a line drawing itself in under the name
transform spot_underline(d):
    xzoom 0.0
    pause d
    easeout 0.6 xzoom 1.0

# a streak of light across the name
transform spot_sweep(d):
    alpha 0.0
    xpos -0.1
    pause d
    alpha 0.5
    linear 0.7 xpos 1.0
    alpha 0.0

# the whole credit: floats gently, fades out at the end
transform spot_hold(d):
    alpha 1.0
    yoffset 0
    parallel:
        pause (d - 0.7)
        ease 0.6 alpha 0.0
    parallel:
        block:
            ease 2.2 yoffset -6
            ease 2.2 yoffset 6
            repeat

transform spot_logo_in(d):
    alpha 0.0
    zoom 0.85
    blur 12
    pause 0.4
    easein 1.2 alpha 1.0 zoom 1.0 blur 0
    pause (d - 2.4)
    ease 0.7 alpha 0.0

# a name, letter by letter (click it for that person's surprise)
screen spot_name(c, start):
    # long names get smaller so they fit beside the light
    $ nsz = 96 if len(c["name"]) <= 11 else max(50, int(96 * 11 / len(c["name"])))
    button:
        padding (0, 0)
        background None
        action (Function(credits_click, c["key"]) if c.get("key") else None)
        hbox:
            for li, ch in enumerate(c["name"]):
                text ch:
                    size nsz
                    color "#f2ead8"
                    hover_color credit_accent()
                    font CREDIT_FONT
                    outlines [(6, credit_accent() + "38", 0, 0), (2, "#00000099", 0, 0)]
                    at spot_letter(start + li * 0.07)

screen credits_spotlight():
    default slide = 0
    $ sw, sh = config.screen_width, config.screen_height
    $ z0, z1, x0, x1, y0, y1 = spot_move(slide)
    $ kind = SPOT_SLIDES[slide % len(SPOT_SLIDES)][1]
    $ dur = spot_duration(slide)
    $ still = persistent.reduce_motion

    # on to the next picture once this one's done (its own timer, see "index k")
    # SetLocalVariable: this screen is "use"d by about, so it has its own scope
    for k index k in [slide]:
        timer dur action SetLocalVariable("slide", slide + 1)

    add Solid("#000000")

    # ---- what's under the light, with the camera moving over it
    fixed:
        at (spot_sway if not still else Transform())
        # "index k": a new picture is a new displayable, so its camera move
        # starts from the beginning instead of carrying on from the last one
        for k index k in [slide]:
            add spot_slide(k):
                xcenter SPOT_X
                yanchor (1.0 if kind == "person" else 0.5)
                ypos (1.04 if kind == "person" else SPOT_Y)
                at spot_cam(z0, (z1 if not still else z0), x0, (x1 if not still else x0), y0, (y1 if not still else y0), dur, k)

        # the dark all around the light: a tall oval of light, black beyond
        add "gui/spot_hole.png":
            xysize (int(sh * SPOT_RX * 2), int(sh * SPOT_RY * 2))
            xcenter SPOT_X
            ycenter SPOT_Y
        # black past every edge too, so nothing peeks out while the light sways
        add Solid("#000000"):
            pos (-100, -100)
            xysize (max(0, int(sw * SPOT_X - sh * SPOT_RX) + 102), sh + 200)
        add Solid("#000000"):
            pos (int(sw * SPOT_X + sh * SPOT_RX) - 2, -100)
            xysize (max(0, sw - int(sw * SPOT_X + sh * SPOT_RX) + 102), sh + 200)
        add Solid("#000000"):
            pos (-100, -100)
            xysize (sw + 200, max(0, int(sh * SPOT_Y - sh * SPOT_RY) + 102))
        add Solid("#000000"):
            pos (-100, sh - 2)
            xysize (sw + 200, 102)

        # warm light on the floor of the stage, and the beam from above
        add Transform("gui/spotlight.png", alpha=0.10, xysize=(int(sh * 1.1), int(sh * 1.1))):
            xcenter SPOT_X
            ycenter SPOT_Y
        add Transform("gui/spot_cone.png", xysize=(int(sh * 1.0), int(sh * 1.25))):
            xcenter SPOT_X
            yanchor 1.0
            ypos (SPOT_Y + 0.2)
            at spot_flicker
        if not still:
            for k index k in [slide]:
                add Transform("gui/spot_cone.png", xysize=(int(sh * 1.15), int(sh * 1.3)), blend="add"):
                    xcenter SPOT_X
                    yanchor 1.0
                    ypos (SPOT_Y + 0.2)
                    at spot_flare(k)

    # a hard cut from black as each picture starts
    if not still:
        for k index k in [slide]:
            add Solid("#000000") at spot_cut(k)

    # dust drifting through the beam
    if not still:
        for ex, esz, edur, edelay, esway in MENU_EMBERS[:14]:
            add Solid("#fff4dc88"):
                xpos (SPOT_X - 0.12 + ex * 0.24)
                xsize max(2, esz - 2)
                ysize max(2, esz - 2)
                at ember(edur * 1.4, edelay, esway // 2)

    # ---- the credit beside the light
    $ block = spot_credit(slide)
    for k index k in [slide]:
      fixed:
        xpos 0.6
        ypos 0
        xsize int(sw * 0.37)
        ysize sh
        if block is None:
            vbox:
                yalign 0.5
                spacing 14
                at spot_logo_in(dur)
                add Transform("images/Game_Logo_Yellow.webp", fit="contain", xysize=(620, 400))
                text _("A BLACKBERRY STUDIOS GAME"):
                    size 22
                    color "#8a8a8a"
                    font GFONT
        else:
            $ roles, people = block
            $ n = len(roles)
            vbox:
                yalign 0.5
                spacing 4
                at spot_hold(dur)
                # the roles, one at a time, all in the same spot
                fixed:
                    xsize int(sw * 0.37)
                    ysize 40
                    for j, role in enumerate(roles):
                        text role.upper():
                            yalign 0.5
                            size 26
                            color credit_accent()
                            font GFONT
                            outlines [(3, "#00000099", 0, 0)]
                            at (spot_role_last(1.4 + j * SPOT_ROLE) if j == n - 1 else spot_role(1.4 + j * SPOT_ROLE, SPOT_ROLE))
                # how many roles (so a long list reads as a list)
                if n > 1:
                    text (_("%d ROLES") % n):
                        size 14
                        color "#6a6a6a"
                        font GFONT
                        at spot_letter(1.0)
                null height 6
                # the name(s), letter by letter, with a line and a streak of light
                for pi, c in enumerate(people):
                    fixed:
                        fit_first True
                        use spot_name(c, 0.35 + pi * 0.35)
                        if not still:
                            # a soft streak of light (a glow, so it has no hard edges)
                            add Transform("gui/glow.png", xysize=(110, 150), alpha=0.6):
                                yalign 0.5
                                blend "add"
                                at spot_sweep(1.0 + pi * 0.35)
                add Solid(credit_accent()):
                    xysize (360, 3)
                    at spot_underline(0.9)
