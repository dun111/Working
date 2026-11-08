init -10 python:
    CHEATS_BUILD = renpy.loadable("cheats.flag")


default persistent.tickets = 0
default persistent.passes = set()
default persistent.passes_off = set()

define GAMEPASSES = [
    ("extra_life",   _("EXTRA LIFE"),     _("More lives, battery and tries in the harder minigames."), 8),
    ("cheats",       _("CHEAT MENU"),     _("Press F9 to open the cheat menu."), 15),
    ("revealer",     _("CHOICE REVEALER"), _("Choices show where they lead."), 18),
    ("high_roller",  _("HIGH ROLLER"),    _("Bigger casino bets and double daily coins."), 10),
]

init python:
    TICKETS_FOR = {"minigame": 2, "secret": 3, "ending": 5}

    def owns_pass(pid):
        return pid in persistent.passes or (pid == "cheats" and CHEATS_BUILD)

    def has_pass(pid):
        return owns_pass(pid) and pid not in persistent.passes_off

    def toggle_pass(pid):
        if pid in persistent.passes_off:
            persistent.passes_off = persistent.passes_off - set([pid])
        else:
            persistent.passes_off = persistent.passes_off | set([pid])
        renpy.restart_interaction()

    def shown_passes():
        return [p for p in GAMEPASSES if p[0] != "cheats" or CHEATS_BUILD]

    def give_tickets(n):
        persistent.tickets = (persistent.tickets or 0) + n
        renpy.show_screen("ticket_toast", n)

    def buy_pass(pid, price):
        if owns_pass(pid) or (persistent.tickets or 0) < price:
            return
        persistent.tickets -= price
        persistent.passes = set(persistent.passes) | set([pid])
        renpy.restart_interaction()

    def pass_bonus(pid, amount):
        return amount if has_pass(pid) else 0


transform ticket_pop:
    alpha 0.0
    yoffset 20
    easein 0.25 alpha 1.0 yoffset 0
    pause 1.6
    easeout 0.4 alpha 0.0

screen ticket_toast(n):
    zorder 400
    frame:
        xpos 28
        yanchor 1.0
        ypos (TOAST_BOTTOM - 72)
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
            text _("Earn more from minigames, secrets and endings."):
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
        $ owned = owns_pass(pid)
        $ on = has_pass(pid)
        $ afford = (persistent.tickets or 0) >= price
        frame:
            xfill True
            background rbox("#1a170c" if on else "#101014", 22)
            padding (26, 14)
            at row_pop(min(idx * 0.05, 0.5))
            fixed:
                xfill True
                ysize 70
                vbox:
                    yalign 0.5
                    spacing 4
                    xmaximum (w - 420)
                    text pname:
                        size 26
                        color ("#ffd700" if on else "#e8e4dc")
                        font GFONT
                    text pdesc:
                        size 16
                        color "#8888a0"
                        font GFONT
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 16
                    if owned:
                        use pref_toggle(_("ON"), (None if on else Function(toggle_pass, pid)), selected=on, w=110)
                        use pref_toggle(_("OFF"), (Function(toggle_pass, pid) if on else None), selected=not on, w=110)
                    else:
                        text (_("%d TICKETS") % price):
                            yalign 0.5
                            size 20
                            color ("#e6a817" if afford else "#55556a")
                            font GFONT
                        use rbtn(_("BUY"), (Function(buy_pass, pid, price) if afford else None), w=140, h=50, r=16, size=22, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")


# The carriage behind the mysterious door: nothing at all, and a door back.
screen mysterious_room():
    modal True
    zorder 500
    add Solid("#000000")
    key "game_menu" action Return()

    # The way back, on the right: Carriage 1 is that way.
    button:
        pos map_xy(*DOOR_RIGHT[:2])
        xysize map_wh(*DOOR_RIGHT[2:])
        background None
        action Return()
        alt _("Back to Carriage 1")
        text "›":
            xalign 0.5
            yalign 0.5
            size 84
            font "DejaVuSans.ttf"
            idle_color "#2a2a30"
            hover_color "#8888a0"


default persistent.dev_coords = False

init python:
    class DEV(object):
        label = "-"

init 1 python:
    def _dev_label_cb(name, abnormal=False):
        if not name.startswith("_"):
            DEV.label = name

    config.label_callbacks.append(_dev_label_cb)

init python:
    def dev_all_passes():
        persistent.passes = set(persistent.passes) | set(p[0] for p in shown_passes())
        renpy.notify(_("Every gamepass unlocked."))

    def dev_state_lines():
        clues = [c for c, _t, _x in CLUE_LIST if getattr(store, c, False)]
        return [
            ("label", DEV.label),
            ("part", "2" if store.in_loop else "1"),
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
        hover_sound None
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
    for idx, (title, f) in enumerate(THEATRE):
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
        return t if t in THEME_GRADE else "default"

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
        return ds if ds in dict(DIALOGUE_STYLES) else "classic"

    def menu_style_now():
        ms = persistent.menu_style
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


default rewind_point = None

init python:
    def rewind_mark():
        if _history_list:
            store.rewind_point = _history_list[-1].rollback_identifier

    def rewind_ready():
        return store.rewind_point is not None

    def rewind_go():
        n = renpy.get_identifier_checkpoints(store.rewind_point) if store.rewind_point else None
        if n is None:
            renpy.notify(_("Can't rewind past a minigame or a load."))
            return
        renpy.rollback(checkpoints=n, force=True)
