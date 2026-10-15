# ==============================================================================
# DEPARTURE AT 4:00  -  gamepass.rpy
# Gamepasses, bought with tickets.  EXTRAS > GAMEPASS
#
# You earn tickets by playing:
#   win a minigame for the first time    +2
#   find a secret                        +3
#   see an ending for the first time     +5
#   (the DOUBLE TICKETS pass doubles all of these)
#
#   $ give_tickets(5)          hand out tickets from anywhere
#   if has_pass("gold_key"):   check whether a pass is owned
# ==============================================================================

default persistent.tickets = 0
default persistent.passes = set()

# (id, name, what it does, price)
define GAMEPASSES = [
    ("double",       _("DOUBLE TICKETS"), _("Earn twice as many tickets from now on."), 10),
    ("gold_key",     _("GOLDEN KEY"),     _("The key on the main menu turns gold."), 6),
    ("gold_credits", _("GOLD CREDITS"),   _("The ticket cards in the credits turn gold."), 4),
    ("extra_life",   _("EXTRA LIFE"),     _("+1 life in DON'T LET THEM REACH YOU, +4 battery in SEARCH IN THE DARK, +3 tries on THE LUGGAGE LOCK, +1 tear on PULL UP THE CARPET."), 8),
    ("cheats",       _("CHEAT MENU"),     _("Press F9 to open the cheat menu in any copy of the game."), 15),
    ("empty_train",  _("4:01"),           _("Board the empty train from this page whenever you like."), 12),
    ("eric",         _("ERIC PASS"),      _("Developer mode: a DEV badge on the main menu, a developer HUD in game, and Eric's DEBUG game in the Arcade."), 20),
    ("dlc",          _("DLC"),            _("Three new EXTRAS tabs: GALLERY (every character), JUKEBOX (the soundtrack) and THEATRE (the videos)."), 25),
    ("revealer",     _("CHOICE REVEALER"), _("Every choice shows where it leads: the right answers, the deadly ones, achievements, minigames, and what you picked last time."), 18),
    ("rewind",       _("REWIND"),         _("A REWIND button in the quick menu takes you straight back to your last choice so you can pick again."), 14),
    ("themes",       _("THEME PACK"),     _("Exclusive colour themes for the whole game (MIDNIGHT, BLOOD MOON, ROYAL, NOIR), the CENTERED main menu, and the TERMINAL and TICKET dialogue boxes. Switch in SETTINGS > DISPLAY."), 16),
    ("high_roller",  _("HIGH ROLLER"),    _("4:00 Casino: 100 and 250 coin bets, and double the free daily coins."), 10),
]

# passes that don't do anything yet: they show this instead of OWNED
define GAMEPASS_SOON = {}

# passes that stay hidden ("???") until you've found what they're for
define GAMEPASS_HIDDEN = {"empty_train": "empty_train_done"}

init python:
    TICKETS_FOR = {"minigame": 2, "secret": 3, "ending": 5}

    def has_pass(pid):
        return pid in persistent.passes

    def give_tickets(n):
        if has_pass("double"):
            n *= 2
        persistent.tickets = (persistent.tickets or 0) + n
        renpy.show_screen("ticket_toast", n)

    def pass_hidden(pid):
        flag = GAMEPASS_HIDDEN.get(pid)
        return bool(flag) and not getattr(persistent, flag)

    def buy_pass(pid, price):
        if has_pass(pid) or (persistent.tickets or 0) < price:
            return
        persistent.tickets -= price
        persistent.passes = set(persistent.passes) | set([pid])
        sfx("win")
        renpy.restart_interaction()

    def pass_bonus(pid, amount):
        """How much a pass adds to something: pass_bonus("extra_life", 1)"""
        return amount if has_pass(pid) else 0

    def credit_accent():
        return "#d4af37" if has_pass("gold_credits") else "#e0521f"

    # the gold key on the main menu
    KEY_IMAGE_GOLD = Transform(KEY_IMAGE, matrixcolor=SaturationMatrix(0.2) * TintMatrix("#ffd36a") * BrightnessMatrix(0.08))


# ------------------------------------------------------------------------------
# "+2 TICKETS" in the bottom-left corner
# ------------------------------------------------------------------------------

transform ticket_pop:
    alpha 0.0
    yoffset 20
    easein 0.25 alpha 1.0 yoffset 0
    pause 1.6
    easeout 0.4 alpha 0.0

screen ticket_toast(n):
    zorder 400
    frame:
        xpos 40
        yalign 0.93
        padding (24, 12)
        background rbox("#14141aee", 18)
        at ticket_pop
        hbox:
            spacing 12
            add rbox("#e6a817", 6):
                yalign 0.5
                xysize (34, 22)
            text (_("+%d TICKETS") % n):
                size 22
                color "#e6a817"
                font GFONT
    timer 2.4 action Hide("ticket_toast")


# ------------------------------------------------------------------------------
# EXTRAS > GAMEPASS
# ------------------------------------------------------------------------------

screen gamepass_list(w):
    frame:
        xfill True
        background rbox("#17150d", 22)
        padding (26, 18)
        hbox:
            spacing 20
            add rbox("#e6a817", 8):
                yalign 0.5
                xysize (56, 36)
            text (_("TICKETS: %d") % (persistent.tickets or 0)):
                yalign 0.5
                size 34
                color "#ffd700"
                font GFONT
            text _("Win minigames, find secrets and see endings to earn more."):
                yalign 0.5
                size 16
                color "#8888a0"
                font GFONT

    # trade coins (from the slot machine) for tickets
    frame:
        xfill True
        background rbox("#101014", 22)
        padding (26, 14)
        fixed:
            xfill True
            ysize 50
            hbox:
                yalign 0.5
                spacing 14
                add circ_coin(30):
                    yalign 0.5
                text (_("COINS: %d") % (persistent.coins or 0)):
                    yalign 0.5
                    size 26
                    color "#ffd76a"
                    font GFONT
            hbox:
                xalign 1.0
                yalign 0.5
                use rbtn((_("TRADE %d COINS FOR 1 TICKET") % COINS_PER_TICKET), (Function(coins_to_ticket) if (persistent.coins or 0) >= COINS_PER_TICKET else None), w=420, h=50, r=16, size=18, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")

    for idx, (pid, pname, pdesc, price) in enumerate(GAMEPASSES):
        $ owned = has_pass(pid)
        $ hidden = pass_hidden(pid)
        $ afford = (persistent.tickets or 0) >= price
        frame:
            xfill True
            background rbox("#1a170c" if owned else "#101014", 22)
            padding (26, 14)
            at row_pop(min(idx * 0.05, 0.5))
            fixed:
                xfill True
                ysize 70
                vbox:
                    yalign 0.5
                    spacing 4
                    xmaximum (w - 420)
                    text ("???" if hidden else pname):
                        size 26
                        color ("#ffd700" if owned else "#e8e4dc")
                        font GFONT
                    text ("???" if hidden else pdesc):
                        size 16
                        color "#8888a0"
                        font GFONT
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 16
                    if owned and pid == "empty_train":
                        use rbtn(_("BOARD"), Start("empty_train"), w=170, h=50, r=16, size=22, bg="#3a0a0a", hov="#5a1010", col="#f2d8d8", hcol="#ffffff")
                    elif owned and pid == "eric":
                        use rbtn((_("HUD: ON") if persistent.dev_hud else _("HUD: OFF")), ToggleField(persistent, "dev_hud"), w=170, h=50, r=16, size=20, bg="#14202e", hov="#1f3048", col="#61afef", hcol="#ffffff")
                    elif owned:
                        text GAMEPASS_SOON.get(pid, _("OWNED")):
                            yalign 0.5
                            size 22
                            color "#6dffa5"
                            font GFONT
                    elif not hidden:
                        text (_("%d TICKETS") % price):
                            yalign 0.5
                            size 20
                            color ("#e6a817" if afford else "#55556a")
                            font GFONT
                        use rbtn(_("BUY"), (Function(buy_pass, pid, price) if afford else None), w=140, h=50, r=16, size=22, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")


# ==============================================================================
# ERIC PASS  -  developer mode
# ==============================================================================

default persistent.dev_hud = True

init python:
    class DEV(object):
        label = "-"

    _old_label_cb = config.label_callback

    def _dev_label_cb(name, abnormal=False):
        if isinstance(name, (type(u""), type(""))) and not name.startswith("_"):
            DEV.label = name
        if _old_label_cb:
            _old_label_cb(name, abnormal)

    config.label_callback = _dev_label_cb

    def dev_hud_lines():
        clues = len([c for c, _t, _x in CLUE_LIST if getattr(store, c, False)])
        return [
            "label   %s" % DEV.label,
            "part    %s" % ("2" if getattr(store, "in_loop", False) else "1"),
            "clues   %d / %d" % (clues, len(CLUE_LIST)),
            "tickets %d" % (persistent.tickets or 0),
            "runs    %d" % (persistent.runs or 0),
        ]

# the developer HUD (top-left, in game only)
screen dev_hud():
    zorder 90
    if has_pass("eric") and persistent.dev_hud and not main_menu:
        frame:
            xpos 20
            ypos 20
            padding (16, 10)
            background rbox("#0a0e14cc", 10)
            vbox:
                spacing 2
                text "DEV":
                    size 14
                    color "#61afef"
                    font GFONT
                for ln in dev_hud_lines():
                    text _esc(ln):
                        size 14
                        color "#98c379"
                        font "DejaVuSans.ttf"

init python:
    config.overlay_screens.append("dev_hud")


# ==============================================================================
# DLC  -  GALLERY, JUKEBOX, THEATRE   (EXTRAS tabs)
# ==============================================================================

# (picture, name)
define GALLERY = [
    ("louis neutral", "Louis"), ("dorothy neutral", "Dorothy"), ("dorothy sad", "Dorothy"),
    ("fedora neutral", "Fedora"), ("eduard neutral", "Eduard"), ("shunyu neutral", "Shunyu"),
    ("kimmy neutral", "Kimmy"), ("himmel neutral", "Himmel"), ("sebastian neutral", "Sebastian"),
    ("misha neutral", "Misha"), ("agatha neutral", "Agatha"), ("ichora neutral", "Ichora"),
    ("pattison neutral", "Pattison"), ("alexander neutral", "Alexander"),
    ("shunyu_monster neutral", "The Passenger"), ("himmel_monster neutral", "The Gentleman"),
    ("conductor_monster neutral", "The Conductor"),
]

# (title, file)
define JUKEBOX = [
    (_("MAIN MENU"), "gui/main_menu.mp3"),
    (_("LARP MUSIC"), "gui/larp.mp3"),
]

# (title, file)
define THEATRE = [
    (_("ENDING"), "movies/ending_video.webm"),
]

init python:
    def dlc_tabs():
        if not has_pass("dlc"):
            return []
        return [("gallery", _("GALLERY")), ("jukebox", _("JUKEBOX")), ("theatre", _("THEATRE"))]

    def jukebox_play(f):
        renpy.music.play(f, channel="music", fadein=0.6, loop=True)
        renpy.restart_interaction()

    def jukebox_stop():
        renpy.music.stop(channel="music", fadeout=0.6)
        renpy.restart_interaction()

    def theatre_play(f):
        if renpy.loadable(f):
            renpy.invoke_in_new_context(renpy.movie_cutscene, f)
            if main_menu and config.main_menu_music:
                renpy.music.play(config.main_menu_music, fadein=1.0)
            renpy.restart_interaction()

# a slow pan over one character, full screen; click to close
transform gallery_pan:
    xalign 0.5
    yalign 1.0
    zoom 1.0
    alpha 0.0
    parallel:
        ease 0.4 alpha 1.0
    parallel:
        ease 8.0 zoom 1.12 yoffset 60

screen gallery_view(img, name):
    modal True
    zorder 300
    add Solid("#08080cf4")
    add Transform(img, fit="contain", ysize=int(config.screen_height * 0.95)) at gallery_pan
    text name:
        xpos 60
        yalign 0.92
        size 64
        color "#e8e4dc"
        font CREDIT_FONT
        at fade_slide_in(0.3)
    button:
        xysize (config.screen_width, config.screen_height)
        background None
        action Hide("gallery_view")
    key "game_menu" action Hide("gallery_view")

screen gallery_list(w):
    hbox:
        box_wrap True
        spacing 18
        xmaximum (w - 60)
        for idx, (img, name) in enumerate(GALLERY):
            button:
                xysize (220, 330)
                padding (0, 0)
                background rbox("#101014", 18)
                hover_background rbox("#1d1820", 18)
                action Show("gallery_view", None, img, name)
                at row_pop(min(idx * 0.03, 0.5))
                add Transform(img, fit="contain", xysize=(210, 280)):
                    align (0.5, 0.15)
                text name:
                    xalign 0.5
                    yalign 0.95
                    size 20
                    color "#e8e4dc"
                    hover_color "#ffd700"
                    font GFONT

screen jukebox_list(w):
    $ playing = renpy.music.get_playing(channel="music")
    for idx, (title, f) in enumerate(JUKEBOX):
        $ on = (playing == f)
        frame:
            xfill True
            background rbox("#17150d" if on else "#101014", 22)
            padding (26, 14)
            at row_pop(min(idx * 0.05, 0.5))
            fixed:
                xfill True
                ysize 56
                text (("♪  " if on else "") + title):
                    yalign 0.5
                    size 26
                    color ("#ffd700" if on else "#e8e4dc")
                    font GFONT
                hbox:
                    xalign 1.0
                    yalign 0.5
                    if on:
                        use rbtn(_("STOP"), Function(jukebox_stop), w=150, h=50, r=16, size=22)
                    else:
                        use rbtn(_("PLAY"), Function(jukebox_play, f), w=150, h=50, r=16, size=22, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")

screen theatre_list(w):
    # only videos that are actually on this device
    for idx, (title, f) in enumerate([(t, f) for t, f in THEATRE if renpy.loadable(f)]):
        frame:
            xfill True
            background rbox("#101014", 22)
            padding (26, 14)
            at row_pop(min(idx * 0.05, 0.5))
            fixed:
                xfill True
                ysize 56
                text title:
                    yalign 0.5
                    size 26
                    color "#e8e4dc"
                    font GFONT
                hbox:
                    xalign 1.0
                    yalign 0.5
                    use rbtn(_("WATCH"), Function(theatre_play, f), w=150, h=50, r=16, size=22, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")



# ==============================================================================
# THEME PACK  -  colour themes, the CENTERED main menu, TERMINAL / TICKET boxes
# ==============================================================================

default persistent.ui_theme = "default"

# (id, name)
define UI_THEMES = [
    ("default",  _("DEFAULT")),
    ("midnight", _("MIDNIGHT")),
    ("blood",    _("BLOOD MOON")),
    ("royal",    _("ROYAL")),
    ("noir",     _("NOIR")),
]

# the dialogue boxes and main menus only the THEME PACK unlocks
define THEME_DIALOGUE = ("terminal", "ticket")
define THEME_MENUS = ("centered",)

init python:
    # menus, buttons and boxes get their colours turned...
    THEME_UI = {
        "midnight": HueMatrix(200) * SaturationMatrix(0.85),
        "blood":    HueMatrix(-28) * SaturationMatrix(1.6) * BrightnessMatrix(-0.04),
        "royal":    HueMatrix(255),
        "noir":     SaturationMatrix(0.0) * ContrastMatrix(1.1),
    }
    # ...and the scenes get a gentle colour grade, so the people still look right
    THEME_SCENE = {
        "midnight": SaturationMatrix(0.75) * TintMatrix("#c4d0ff"),
        "blood":    TintMatrix("#ffb0a0"),
        "royal":    TintMatrix("#e6d4ff"),
        "noir":     SaturationMatrix(0.0) * ContrastMatrix(1.15),
    }

    def theme_now():
        t = persistent.ui_theme
        return t if (t in THEME_UI and has_pass("themes")) else "default"

    def _theme_layer(table):
        def apply(d):
            m = table.get(theme_now())
            return Transform(d, matrixcolor=m) if m is not None else d
        return apply

    config.layer_transforms["screens"] = [_theme_layer(THEME_UI)]
    config.layer_transforms["master"] = [_theme_layer(THEME_SCENE)]

    def set_theme(t):
        persistent.ui_theme = t
        renpy.restart_interaction()

    def dialogue_style_now():
        ds = persistent.dialogue_style
        if ds in THEME_DIALOGUE and not has_pass("themes"):
            return "classic"
        return ds

    def menu_style_now():
        ms = persistent.menu_style
        if ms in THEME_MENUS and not has_pass("themes"):
            return "new"
        return ms

    def say_background(ds, op):
        if ds == "minimal":
            return None
        if ds == "film":
            return Solid(Color("#000000").replace_opacity(op))
        if ds == "paper":
            return rbox(Color("#e9dfc8").replace_opacity(op), 26)
        if ds == "terminal":
            return rbox(Color("#020a05").replace_opacity(op), 10)
        if ds == "ticket":
            return rbox(Color("#efe3c4").replace_opacity(op), 18)
        return rbox(Color("#0a0a0e").replace_opacity(op), 26)

    def say_ink(ds):
        if ds in ("paper", "ticket"):
            return "#2a1f10"
        if ds == "terminal":
            return "#7dff9a"
        return TEXT_COLORS.get(persistent.text_color, "#e8e4dc")


# ==============================================================================
# CHOICE REVEALER  -  tags on choices (screen choice in screens.rpy)
# ==============================================================================
# Keyed by the choice's exact text. A ("label", "text") key is used when the
# same text appears in more than one menu ("Yes", "No"...).
# (tag, colour)

define CHOICE_GOOD = "#6dffa5"
define CHOICE_BAD = "#ff6b5a"
define CHOICE_INFO = "#e6a817"

define CHOICE_HINTS = {
    # the accusation
    "Accuse Misha": (_("THE TRUTH"), CHOICE_GOOD),
    "Accuse Eduard": (_("WRONG · DEATH"), CHOICE_BAD),
    "Accuse Alexander": (_("WRONG · DEATH"), CHOICE_BAD),
    "Accuse Agatha": (_("WRONG · DEATH"), CHOICE_BAD),
    # carriage 6: all three right for the true ending
    "“Your life.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“Your winning streak.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“Nothing. You never really understood what you were risking.”": (_("RIGHT ANSWER"), CHOICE_GOOD),
    "“Peace.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“Kimmy's approval.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“Nothing real. Just a feeling that let you stop feeling everything else.”": (_("RIGHT ANSWER"), CHOICE_GOOD),
    "“To keep the train running forever.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“To punish the ones who did wrong.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“To help everyone finally understand it's over, so they can stop waiting for a stop that isn't coming.”": (_("RIGHT ANSWER"), CHOICE_GOOD),
    # minigames and achievements
    ("c2_shunyu_dialogue", "Yes"): (_("MINIGAME · ACHIEVEMENT"), CHOICE_INFO),
    ("c5_alexander_dialogue", "Yes"): (_("ACHIEVEMENT"), CHOICE_INFO),
    "Pick it": (_("MINIGAME"), CHOICE_INFO),
    "Sweep it up": (_("MINIGAME"), CHOICE_INFO),
    "Play": (_("MINIGAME"), CHOICE_INFO),
    "Take the controls": (_("MINIGAME"), CHOICE_INFO),
    "Sort mail": (_("MINIGAME"), CHOICE_INFO),
}

init python:
    def choice_hint(caption):
        """(tag, colour) for a choice, or None. Only with the CHOICE REVEALER pass."""
        if not has_pass("revealer"):
            return None
        return CHOICE_HINTS.get((DEV.label, caption)) or CHOICE_HINTS.get(caption)


# ==============================================================================
# REWIND  -  back to the last choice (quick menu)
# ==============================================================================

default rewind_point = None

init python:
    def rewind_mark():
        """Called when a choice appears: remember the line just before it."""
        try:
            if _history_list:
                store.rewind_point = _history_list[-1].rollback_identifier
        except Exception:
            pass

    def rewind_ready():
        return has_pass("rewind") and store.rewind_point is not None

    def rewind_go():
        n = renpy.get_identifier_checkpoints(store.rewind_point) if store.rewind_point else None
        if n is None:
            renpy.notify(_("Can't rewind past a minigame or a loaded save."))
            return
        renpy.rollback(checkpoints=n, force=True)
