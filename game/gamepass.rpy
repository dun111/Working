# The cheats build ships with game/cheats.flag; the normal build leaves it out.
init -10 python:
    CHEATS_BUILD = renpy.loadable("cheats.flag")

# Gamepasses, bought with tickets.  EXTRAS > GAMEPASS

default persistent.tickets = 0
default persistent.passes = set()

define GAMEPASSES = [
    ("double",       _("DOUBLE TICKETS"), _("Earn twice as many tickets from now on."), 10),
    ("extra_life",   _("EXTRA LIFE"),     _("+1 life in DON'T LET THEM REACH YOU, +4 battery in SEARCH IN THE DARK, +3 tries on THE LUGGAGE LOCK, +1 tear on PULL UP THE CARPET."), 8),
    ("cheats",       _("CHEAT MENU"),     _("Press F9 for the cheat menu: jump to any chapter, story flags, jumpscares, every minigame, unlocks and developer tools."), 15),
    ("empty_train",  _("4:01"),           _("Board the empty train from this page whenever you like."), 12),
    ("dlc",          _("DLC"),            _("Three new EXTRAS tabs: GALLERY (every character), JUKEBOX (the soundtrack) and THEATRE (the videos)."), 25),
    ("revealer",     _("CHOICE REVEALER"), _("Every choice shows where it leads: the right answers, the deadly ones, achievements, minigames, and what you picked last time."), 18),
    ("rewind",       _("REWIND"),         _("A REWIND button in the quick menu takes you straight back to your last choice so you can pick again."), 14),
    ("themes",       _("THEME PACK"),     _("Exclusive colour themes for the whole game (MIDNIGHT, BLOOD MOON, ROYAL, NOIR), the CENTERED main menu, and the TERMINAL (a plain terminal window) and TICKET dialogue boxes. Switch in SETTINGS > DISPLAY."), 16),
    ("high_roller",  _("HIGH ROLLER"),    _("4:00 Casino: 100 and 250 coin bets, and double the free daily coins."), 10),
]

define GAMEPASS_SOON = {}

define GAMEPASS_HIDDEN = {"empty_train": "empty_train_done"}

init python:
    TICKETS_FOR = {"minigame": 2, "secret": 3, "ending": 5}

    def has_pass(pid):
        return pid in persistent.passes or (pid == "cheats" and CHEATS_BUILD)

    def shown_passes():
        return [p for p in GAMEPASSES if p[0] != "cheats" or CHEATS_BUILD]

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
        return amount if has_pass(pid) else 0



# "+2 TICKETS" in the bottom-left corner

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


# EXTRAS > GAMEPASS

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

    for idx, (pid, pname, pdesc, price) in enumerate(shown_passes()):
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


# CHEAT MENU > TOOLS

default persistent.dev_coords = False

init python:
    class DEV(object):
        label = "-"

init 1 python:
    _old_label_cb = config.label_callback

    def _dev_label_cb(name, abnormal=False):
        if isinstance(name, (type(u""), type(""))) and not name.startswith("_"):
            DEV.label = name
        if _old_label_cb:
            _old_label_cb(name, abnormal)

    config.label_callback = _dev_label_cb

init python:
    def dev_all_passes():
        persistent.passes = set(persistent.passes) | set(p[0] for p in shown_passes())
        renpy.notify(_("Every gamepass unlocked."))

    def dev_state_lines():
        clues = [c for c, _t, _x in CLUE_LIST if getattr(store, c, False)]
        return [
            ("label", DEV.label),
            ("part", "2" if getattr(store, "in_loop", False) else "1"),
            ("clues", "%d / %d" % (len(clues), len(CLUE_LIST))),
            ("music", renpy.music.get_playing("music") or "-"),
            ("coins / tickets", "%d / %d" % (persistent.coins or 0, persistent.tickets or 0)),
            ("screen", "%d x %d" % (config.screen_width, config.screen_height)),
        ]

    def _dev_coords(st, at):
        x, y = renpy.get_mouse_pos()
        mx = int((x - MAP_OX) / MAP_K)
        my = int((y - MAP_OY) / MAP_K)
        return Text("screen %d, %d    map %d, %d" % (x, y, mx, my), size=16, color="#98c379", font="DejaVuSans.ttf"), 0.05

    DEV_COORDS = DynamicDisplayable(_dev_coords)

screen dev_coords():
    zorder 1500
    if cheats_allowed() and persistent.dev_coords:
        frame:
            xalign 1.0
            yalign 1.0
            offset (-20, -70)
            padding (14, 6)
            background rbox("#0a0e14dd", 8)
            add DEV_COORDS

init python:
    config.always_shown_screens.append("dev_coords")


# DLC  -  GALLERY, JUKEBOX, THEATRE   (EXTRAS tabs)

define GALLERY = [
    ("louis neutral", "Louis"), ("dorothy neutral", "Dorothy"), ("dorothy sad", "Dorothy"),
    ("fedora neutral", "Fedora"), ("eduard neutral", "Eduard"), ("shunyu neutral", "Shunyu"),
    ("kimmy neutral", "Kimmy"), ("himmel neutral", "Himmel"), ("sebastian neutral", "Sebastian"),
    ("misha neutral", "Misha"), ("agatha neutral", "Agatha"), ("ichora neutral", "Ichora"),
    ("pattison neutral", "Pattison"), ("alexander neutral", "Alexander"),
    ("shunyu_monster neutral", "The Passenger"), ("himmel_monster neutral", "The Gentleman"),
    ("conductor_monster neutral", "The Conductor"),
]


define THEATRE = [
    (_("ENDING"), "movies/ending_video.webm"),
]

init python:
    def dlc_tabs():
        if not has_pass("dlc"):
            return []
        return [("gallery", _("GALLERY")), ("jukebox", _("JUKEBOX")), ("theatre", _("THEATRE"))]

    def jukebox_play(f):
        files = song_files(SONG_ORDER)
        if f in files:
            k = files.index(f)
            files = files[k:] + files[:k]
        _MUSIC.place = "jukebox"
        menu_music_filter_off()
        renpy.music.play(files or f, channel="music", fadein=0.6, fadeout=0.6, loop=True)
        renpy.restart_interaction()

    def jukebox_shuffle():
        files = song_files(SONG_ORDER)
        renpy.random.shuffle(files)
        _MUSIC.place = "jukebox"
        menu_music_filter_off()
        renpy.music.play(files, channel="music", fadein=0.6, fadeout=0.6, loop=True)
        renpy.restart_interaction()

    def jukebox_stop():
        renpy.music.stop(channel="music", fadeout=0.6)
        _MUSIC.place = None
        renpy.restart_interaction()

    def theatre_play(f):
        if renpy.loadable(f):
            renpy.invoke_in_new_context(renpy.movie_cutscene, f)
            if main_menu and config.main_menu_music:
                renpy.music.play(config.main_menu_music, fadein=1.0)
            renpy.restart_interaction()

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
    frame:
        xfill True
        background rbox("#17150d", 22)
        padding (26, 14)
        fixed:
            xfill True
            ysize 56
            vbox:
                yalign 0.5
                spacing 4
                text _("NOW PLAYING"):
                    size 15
                    color "#8888a0"
                    font GFONT
                text now_playing_title():
                    size 22
                    color "#ffd700"
                    font GFONT
            hbox:
                xalign 1.0
                yalign 0.5
                spacing 12
                use rbtn(_("SHUFFLE ALL"), Function(jukebox_shuffle), w=190, h=50, r=16, size=18, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")
                use rbtn(_("NEXT"), (Function(music_skip) if playing else None), w=120, h=50, r=16, size=18)
                use rbtn(_("STOP"), (Function(jukebox_stop) if playing else None), w=120, h=50, r=16, size=18)
    for idx, sid in enumerate(SONG_ORDER):
        $ f, title, artist = SONGS[sid]
        $ on = (playing == f)
        frame:
            xfill True
            background rbox("#17150d" if on else "#101014", 22)
            padding (26, 10)
            at row_pop(min(idx * 0.03, 0.5))
            fixed:
                xfill True
                ysize 50
                vbox:
                    yalign 0.5
                    spacing 2
                    text ((_("PLAYING:  ") if on else "") + title):
                        size 22
                        color ("#ffd700" if on else "#e8e4dc")
                        font GFONT
                    text artist:
                        size 15
                        color "#8888a0"
                        font GFONT
                hbox:
                    xalign 1.0
                    yalign 0.5
                    if on:
                        use rbtn(_("STOP"), Function(jukebox_stop), w=130, h=44, r=14, size=18)
                    else:
                        use rbtn(_("PLAY"), Function(jukebox_play, f), w=130, h=44, r=14, size=18, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")

screen theatre_list(w):
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


# THEME PACK  -  colour themes, the CENTERED main menu, TERMINAL / TICKET boxes

default persistent.ui_theme = "default"

define UI_THEMES = [
    ("default",  _("DEFAULT")),
    ("soft",     _("SOFT")),
    ("midnight", _("MIDNIGHT")),
    ("blood",    _("BLOOD MOON")),
    ("royal",    _("ROYAL")),
    ("noir",     _("NOIR")),
    ("sepia",    _("SEPIA")),
    ("sunset",   _("SUNSET")),
    ("forest",   _("FOREST")),
    ("frost",    _("FROST")),
    ("dusk",     _("DUSK")),
]

define THEME_DIALOGUE = ("terminal", "ticket")
define THEME_MENUS = ("centered",)

init python:
    THEME_GRADE = {
        "soft":     ContrastMatrix(0.78) * BrightnessMatrix(-0.07),
        "midnight": SaturationMatrix(0.75) * TintMatrix("#b8c6ff"),
        "blood":    SaturationMatrix(1.1) * TintMatrix("#ffaa98"),
        "royal":    TintMatrix("#d2bcff"),
        "noir":     SaturationMatrix(0.0),
        "sepia":    SaturationMatrix(0.15) * TintMatrix("#ffdcae"),
        "sunset":   TintMatrix("#ffc890"),
        "forest":   TintMatrix("#c2e6b6"),
        "frost":    SaturationMatrix(0.7) * TintMatrix("#c4e4ff"),
        "dusk":     SaturationMatrix(0.8) * TintMatrix("#e2bcd8"),
    }

    def theme_now():
        t = persistent.ui_theme
        return t if (t in THEME_GRADE and has_pass("themes")) else "default"

    def theme_matrix():
        return THEME_GRADE.get(theme_now(), IdentityMatrix())

    _THEMED = {}

    def _themed(st, at, d):
        key = (id(d), theme_now())
        t = _THEMED.get(key)
        if t is None:
            t = _THEMED[key] = Transform(d, matrixcolor=theme_matrix())
        return t, None

    def themed(d):
        return DynamicDisplayable(_themed, d=d)

    def theme_step(d):
        ids = [t for t, _n in UI_THEMES]
        k = ids.index(theme_now()) if theme_now() in ids else 0
        set_theme(ids[(k + d) % len(ids)])

    def theme_name():
        return dict(UI_THEMES).get(theme_now(), _("DEFAULT"))

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
        if ms not in [m[0] for m in MENU_STYLES]:
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
            return rbox(Color("#0c0c0c").replace_opacity(max(op, 0.96)), 10)
        if ds == "ticket":
            return rbox(Color("#efe3c4").replace_opacity(op), 18)
        return rbox(Color("#0a0a0e").replace_opacity(op), 26)

    def say_ink(ds):
        if ds in ("paper", "ticket"):
            return "#2a1f10"
        if ds == "terminal":
            return "#d8d8d8"
        return TEXT_COLORS.get(persistent.text_color, "#e8e4dc")


# CHOICE REVEALER  -  tags on choices (screen choice in screens.rpy)

define CHOICE_GOOD = "#6dffa5"
define CHOICE_BAD = "#ff6b5a"
define CHOICE_INFO = "#e6a817"

define CHOICE_HINTS = {
    "Accuse Misha": (_("THE TRUTH"), CHOICE_GOOD),
    "Accuse Eduard": (_("WRONG · DEATH"), CHOICE_BAD),
    "Accuse Alexander": (_("WRONG · DEATH"), CHOICE_BAD),
    "Accuse Agatha": (_("WRONG · DEATH"), CHOICE_BAD),
    "“Your life.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“Your winning streak.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“Nothing. You never really understood what you were risking.”": (_("RIGHT ANSWER"), CHOICE_GOOD),
    "“Peace.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“Kimmy's approval.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“Nothing real. Just a feeling that let you stop feeling everything else.”": (_("RIGHT ANSWER"), CHOICE_GOOD),
    "“To keep the train running forever.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“To punish the ones who did wrong.”": (_("WRONG ANSWER"), CHOICE_BAD),
    "“To help everyone finally understand it's over, so they can stop waiting for a stop that isn't coming.”": (_("RIGHT ANSWER"), CHOICE_GOOD),
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
        if not has_pass("revealer"):
            return None
        return CHOICE_HINTS.get((DEV.label, caption)) or CHOICE_HINTS.get(caption)


# REWIND  -  back to the last choice (quick menu)

default rewind_point = None

init python:
    def rewind_mark():
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
