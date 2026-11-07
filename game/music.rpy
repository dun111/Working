define SONGS = {
    "main_menu":            ("music/grekhov_theme.mp3",               _("Grekhov Theme"),                 "Departure at 4:00"),
    "carriage_1":           ("music/carriage_1_clip.mp3",         _("Carriage 1"),                    "Departure at 4:00"),
    "carriage_2":           ("music/lets_all_do_the_conga.mp3",   "Let's All Do the Conga",           "Colin Sheen"),
    "carriage_3":           ("music/rendezvous.opus",             "Rendezvous (Instrumental)",        "Carriage 3"),
    "part2_carriage_1":     ("music/part2_carriage_1.mp3",        _("Part 2 Carriage 1"),             "Departure at 4:00"),
    "part2_carriage_2":     ("music/part2_carriage_2.mp3",        _("Part 2 Carriage 2"),             "Departure at 4:00"),
    "part2_carriage_3":     ("music/part2_carriage_3.mp3",        _("Part 2 Carriage 3"),             "Departure at 4:00"),
    "carriage_4":           ("music/carriage_4.mp3",              _("Carriage 4"),                    "Departure at 4:00"),
    "carriage_5":           ("music/carriage_5.mp3",              _("Carriage 5"),                    "Departure at 4:00"),
    "accusation":           ("music/pizzicato_intrigue.mp3",      _("Pizzicato Intrigue"),            "Departure at 4:00"),
    "flower_in_a_hurricane": ("music/flower_in_a_hurricane.opus", "Flower In A Hurricane", "Justice ft. Tame Impala, SZA, King Gizzard & the Lizard Wizard (GTA VI)"),
}

define config.main_menu_music_fadein = 2.0

define SONG_ORDER = ["main_menu", "carriage_1", "carriage_2", "carriage_3", "carriage_4", "carriage_5",
                     "part2_carriage_1", "part2_carriage_2", "part2_carriage_3",
                     "accusation", "flower_in_a_hurricane"]

define MUSIC_FOR = {
    "c1": ["carriage_1"],
    "c2": ["carriage_2"],
    "c3": ["carriage_3"],
    "c4": ["carriage_4"],
    "c5": ["carriage_5"],
    "part2": ["part2_carriage_1"],
    "part2_c2": ["part2_carriage_2"],
    "part2_c3": ["part2_carriage_3"],
    "part2_c5": ["carriage_5"],
    "accusation": ["accusation"],
    "silence": None,
    "escape": ["main_menu"],
    "true": ["main_menu"],
    "menu_shuffle": ["main_menu", "carriage_3"],
    "casino": ["main_menu"],
    "credits": ["flower_in_a_hurricane"],
    "credits_tickets": ["flower_in_a_hurricane"],
    "credits_spotlight": ["flower_in_a_hurricane"],
}

define RADIO_STATIONS = [
    ("scene", _("GREKHOV FM")),
    ("off",   _("OFF AIR")),
]

define RADIO_FREQ = {"scene": "88.0", "off": "--.-"}

define LABEL_MUSIC = {
    "carriage_1_start":        ("c1", "part2"),
    "carriage_1_hub":          ("c1", "part2"),
    "carriage_2_start":        ("c2", "part2_c2"),
    "carriage_2_hub":          ("c2", "part2_c2"),
    "carriage_3_start":        ("c3", "part2_c3"),
    "carriage_3_hub":          ("c3", "part2_c3"),
    "carriage_4_start":        ("c4", "c4"),
    "carriage_4_hub":          ("c4", "c4"),
    "carriage_5_start":        ("c5", "part2_c5"),
    "carriage_5_hub":          ("c5", "part2_c5"),
    "part2_start":             ("part2", "part2"),
    "carriage_2_part2_start":  ("part2_c2", "part2_c2"),
    "carriage_2_part2_hub":    ("part2_c2", "part2_c2"),
    "c2_p2_investigation_hub": ("part2_c2", "part2_c2"),
    "carriage_2_part2_return": ("part2_c2", "part2_c2"),
    "carriage_3_part2_start":  ("part2_c3", "part2_c3"),
    "carriage_3_part2_hub":    ("part2_c3", "part2_c3"),
    "carriage_5_part2_start":  ("part2_c5", "part2_c5"),
    "carriage_5_part2_hub":    ("part2_c5", "part2_c5"),
    "accusation_scene":        ("accusation", "accusation"),
    "wrong_ending":            ("silence", "silence"),
    "carriage_6_start":        ("silence", "silence"),
    "ending_1_death":          ("silence", "silence"),
    "ending_2_escape":         ("escape", "escape"),
    "ending_3_true":           ("true", "true"),
}


init python:
    SONG_BY_FILE = {}
    for _sid, (_f, _title, _artist) in SONGS.items():
        if _title:
            SONG_BY_FILE[_f] = (_sid, _title, _artist)

    def song_files(ids):
        return [SONGS[i][0] for i in ids]

    class _MUSIC(object):
        place = None
        scene = None

    def radio_scene():
        return radio_station_now() == "scene"

    def music_for(place, fade=2.0):
        if not radio_scene():
            return
        renpy.music.set_pause(False, channel="music")
        if place == _MUSIC.place and renpy.music.is_playing("music"):
            return
        _MUSIC.place = place
        ids = MUSIC_FOR.get(place)
        files = song_files(ids) if ids else []
        if not files:
            renpy.music.stop(channel="music", fadeout=fade)
            return
        renpy.music.play(files, channel="music", loop=True, fadein=fade, fadeout=fade, if_changed=True)

    def menu_music_files():
        ids = MUSIC_FOR["menu_shuffle"][:] if persistent.menu_music == "shuffle" else ["main_menu"]
        if persistent.menu_music == "shuffle":
            renpy.random.shuffle(ids)
        return song_files(ids)

    def _menu_music_config():
        config.main_menu_music = (menu_music_files() or None) if radio_scene() else None

    def music_menu():
        if not radio_scene():
            radio_play_station()
            return
        _MUSIC.place = "menu"
        renpy.music.set_pause(False, channel="music")
        files = menu_music_files()
        if files:
            renpy.music.play(files, channel="music", loop=True, fadein=2.0, if_changed=True)

    def set_menu_music(mode):
        persistent.menu_music = mode
        _menu_music_config()
        if main_menu and radio_scene():
            _MUSIC.place = None
            renpy.music.stop(channel="music", fadeout=0.5)
            music_menu()
        renpy.restart_interaction()

    def music_skip():
        q = renpy.music.get_playing("music")
        files = renpy.music.get_loop("music") or []
        if q in files and len(files) > 1:
            k = files.index(q)
            files = files[k + 1:] + files[:k + 1]
            renpy.music.play(files, channel="music", loop=True, fadein=0.5, fadeout=0.5)
        elif q:
            # Each carriage loops one song, so skipping used to fall silent.
            # Go on to the next song in the Jukebox order instead.
            order = song_files(SONG_ORDER)
            if q in order:
                k = order.index(q)
                order = order[k + 1:] + order[:k + 1]
            renpy.music.play(order, channel="music", loop=True, fadein=0.5, fadeout=0.5)

    class _RADIO(object):
        history = []

    def radio_station_now():
        st = persistent.radio_station
        return st if st in dict(RADIO_STATIONS) else "scene"

    def radio_play_station():
        if radio_station_now() == "off":
            _MUSIC.place = "off"
            renpy.music.stop(channel="music", fadeout=1.0)
            return
        _MUSIC.place = None
        if main_menu:
            music_menu()
        elif persistent.ingame_music and _MUSIC.scene:
            music_for(_MUSIC.scene, fade=1.0)
        else:
            renpy.music.stop(channel="music", fadeout=1.0)

    def radio_station_step(d=1):
        ids = [k for k, _n in RADIO_STATIONS]
        k = ids.index(radio_station_now())
        persistent.radio_station = ids[(k + d) % len(ids)]
        renpy.music.set_pause(False, channel="music")
        _menu_music_config()
        radio_play_station()
        renpy.restart_interaction()

    def radio_station_name():
        return dict(RADIO_STATIONS)[radio_station_now()]

    def radio_paused():
        return renpy.music.get_pause(channel="music")

    def radio_toggle_pause():
        if renpy.music.get_playing("music"):
            renpy.music.set_pause(not radio_paused(), channel="music")
        else:
            radio_play_station()
        renpy.restart_interaction()

    def radio_next():
        renpy.music.set_pause(False, channel="music")
        music_skip()
        renpy.restart_interaction()

    def radio_prev():
        h = _RADIO.history
        cur = renpy.music.get_playing("music")
        files = renpy.music.get_loop("music") or []
        target = h[-2] if len(h) >= 2 else cur
        if target:
            if len(h) >= 2:
                del h[-2:]
            rest = [f for f in files if f != target]
            renpy.music.set_pause(False, channel="music")
            renpy.music.play([target] + rest, channel="music", loop=True, fadein=0.3, fadeout=0.3)
        renpy.restart_interaction()

    _menu_music_config()

init 2 python:
    def _music_label_cb(name, abnormal=False):
        if not main_menu and name in LABEL_MUSIC:
            normal, looped = LABEL_MUSIC[name]
            _MUSIC.scene = looped if store.in_loop else normal
            if persistent.ingame_music:
                music_for(_MUSIC.scene)

    config.label_callbacks.append(_music_label_cb)

init python:
    def set_ingame_music(on):
        persistent.ingame_music = on
        if not on and not main_menu:
            _MUSIC.place = None
            renpy.music.stop(channel="music", fadeout=1.0)
        renpy.restart_interaction()

    class _NP(object):
        last = None

    def now_playing_check():
        cur = renpy.music.get_playing("music")
        if cur == _NP.last:
            return
        _NP.last = cur
        if cur:
            _RADIO.history = (_RADIO.history + [cur])[-30:]
        if cur in SONG_BY_FILE and persistent.song_popups and not popup_blocked():
            sid, title, artist = SONG_BY_FILE[cur]
            renpy.show_screen("now_playing", title, artist)

    def popup_blocked():
        m = renpy.get_screen("menu")
        return bool(m) and not renpy.get_screen("main_menu")

    def now_playing_title():
        cur = renpy.music.get_playing("music")
        if cur in SONG_BY_FILE:
            sid, title, artist = SONG_BY_FILE[cur]
            return "%s  -  %s" % (title, artist)
        return _("Nothing")

    config.always_shown_screens.append("now_playing_watch")

transform np_slide:
    alpha 0.0
    yoffset -30
    easein 0.4 alpha 1.0 yoffset 0
    pause 4.0
    easeout 0.6 alpha 0.0 yoffset -30

screen now_playing_watch():
    timer 1.0 repeat True action Function(now_playing_check)

screen now_playing(title, artist):
    zorder 1300
    frame:
        xalign 1.0
        xoffset -40
        ypos (110 if main_menu else 30) + (170 if renpy.get_screen("ach_toast") else 0)
        padding (22, 12)
        background rbox("#3a2412f0", 14)
        at np_slide
        hbox:
            spacing 16
            frame:
                yalign 0.5
                padding (10, 4)
                background rbox("#e8d9b0", 6)
                text _("ON AIR"):
                    size 14
                    color "#7a1f12"
                    font GFONT
            vbox:
                spacing 2
                text title:
                    size 22
                    color "#f2e6d8"
                    font GFONT
                text artist:
                    size 15
                    color "#c9a982"
                    font GFONT
    timer 5.2 action Hide("now_playing")


define RADIO_W = 640
define RADIO_H = 96
define RADIO_WIN_W = 360
define RADIO_RIGHT = 150
define RADIO_BOTTOM = 8
define RADIO_TAB_W = 92
define RADIO_ABOVE_SAY = 330
define RADIO_TAB_H = 30

init python:
    class _RADIOUI(object):
        hover = False
        pinned = False
        booting = True

    def radio_hover(on):
        if _RADIOUI.hover != on:
            _RADIOUI.hover = on
            renpy.restart_interaction()

    def radio_pin(on):
        _RADIOUI.pinned = on
        renpy.restart_interaction()

    def radio_open():
        return _RADIOUI.hover or _RADIOUI.pinned

transform radio_unfold:
    alpha 0.0
    yoffset 20
    easein 0.15 alpha 1.0 yoffset 0

transform radio_marquee(dist, key):
    xoffset 0
    pause 2.0
    block:
        linear (dist / 40.0) xoffset -dist
        pause 1.5
        xoffset 0
        pause 2.0
        repeat

transform radio_still:
    xoffset 0

init python:
    def radio_song_text():
        cur = renpy.music.get_playing("music")
        if not cur:
            return _("Nothing on air")
        song = SONG_BY_FILE.get(cur)
        if not song:
            return _("Untitled")
        return ("%s - %s" % (song[1], song[2])) if song[2] else song[1]

    _overflow_cache = {}

    def radio_overflow(t, size, width):
        key = (t, size, width)
        if key not in _overflow_cache:
            w = renpy.render(Text(t, size=size, font=GFONT), 4000, 100, 0, 0).width
            _overflow_cache[key] = max(0, int(w - width))
        return _overflow_cache[key]

screen radio_key(label, act, w=74):
    button:
        xysize (w, 32)
        padding (0, 0)
        background rbox("#3e2814", 8)
        hover_background rbox("#c9a24a", 8)
        action act
        text label:
            align (0.5, 0.5)
            size 13
            color "#f2e6d0"
            hover_color "#2a1a0c"
            font GFONT

init python:
    RADIO_AVOID = ["slot_machine", "roulette", "horses", "cheat_menu", "gallery_view"]

    def radio_where():
        if not persistent.radio_bar or _RADIOUI.booting:
            return None
        names = RADIO_AVOID + [g[2] for g in MINIGAME_LIST] + ["mg_debug"]
        for n in names:
            if renpy.get_screen(n):
                return None
        if not main_menu and renpy.get_screen("quick_menu") and not renpy.context()._menu:
            return "game"
        return "corner"

    def radio_toggle():
        _RADIOUI.pinned = not _RADIOUI.pinned
        renpy.restart_interaction()

screen radio_panel(px, py):
    $ cur = renpy.music.get_playing("music")
    $ st = radio_station_now()
    $ line = radio_song_text()
    $ over = radio_overflow(line, 15, RADIO_WIN_W - 24)
    frame:
        pos (px, py)
        xysize (RADIO_W, RADIO_H)
        padding (14, 10)
        background rbox("#6b4524", 14)
        at radio_unfold
        vbox:
            spacing 8
            hbox:
                spacing 8
                use radio_key("<", Function(radio_station_step, -1), w=32)
                frame:
                    xysize (RADIO_WIN_W - 80, 32)
                    padding (12, 0)
                    background rbox("#e8d9b0", 8)
                    text radio_station_name():
                        yalign 0.5
                        size 14
                        color "#7a1f12"
                        font GFONT
                    text RADIO_FREQ.get(st, ""):
                        xalign 1.0
                        yalign 0.5
                        size 13
                        color "#6b5534"
                        font GFONT
                use radio_key(">", Function(radio_station_step, 1), w=32)
                null width 10
                use radio_key(_("HIDE") if _RADIOUI.pinned else _("PIN"), Function(radio_pin, not _RADIOUI.pinned), w=62)
            hbox:
                spacing 8
                fixed:
                  xysize (RADIO_WIN_W, 32)
                  add rbox("#1a0f06", 8):
                      xysize (RADIO_WIN_W, 32)
                  viewport:
                    xysize (RADIO_WIN_W, 32)
                    frame:
                        xysize (max(RADIO_WIN_W, RADIO_WIN_W + over + 24), 32)
                        padding (12, 0)
                        background None
                        text line:
                            yalign 0.5
                            size 15
                            layout "nobreak"
                            color ("#ffb84a" if cur else "#7a5a34")
                            font GFONT
                            at (radio_marquee(over + 24, line) if over else radio_still)
                use radio_key(_("PREV"), Function(radio_prev))
                use radio_key((_("PLAY") if (radio_paused() or not cur) else _("PAUSE")), Function(radio_toggle_pause))
                use radio_key(_("NEXT"), Function(radio_next))

screen radio_bar():
    zorder 1250
    $ where = radio_where()
    $ sw, sh = config.screen_width, config.screen_height

    if where == "game":
        if _RADIOUI.pinned:
            use radio_panel(40, sh - RADIO_ABOVE_SAY - RADIO_H)

    elif where == "corner":
        if radio_open():
            mousearea:
                area (sw - RADIO_RIGHT - RADIO_W, sh - RADIO_BOTTOM - RADIO_H, RADIO_W, RADIO_H)
                hovered Function(radio_hover, True)
                unhovered Function(radio_hover, False)
            use radio_panel(sw - RADIO_RIGHT - RADIO_W, sh - RADIO_BOTTOM - RADIO_H)
        else:
            mousearea:
                area (sw - RADIO_RIGHT - RADIO_TAB_W, sh - RADIO_BOTTOM - RADIO_TAB_H, RADIO_TAB_W, RADIO_TAB_H)
                hovered Function(radio_hover, True)
            button:
                xalign 1.0
                yalign 1.0
                offset (-RADIO_RIGHT, -RADIO_BOTTOM)
                xysize (RADIO_TAB_W, RADIO_TAB_H)
                padding (0, 0)
                background rbox("#6b4524cc", 10)
                hover_background rbox("#8a5a2e", 10)
                action Function(radio_pin, True)
                text _("RADIO"):
                    align (0.5, 0.5)
                    size 14
                    color "#f2e6d0"
                    font GFONT

init python:
    config.always_shown_screens.append("radio_bar")
