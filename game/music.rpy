# ==============================================================================
# DEPARTURE AT 4:00  -  music.rpy
# Every song lives in game/Songs/. This file says which ones play where.
#
#   SONGS          id -> (file, title, artist)      add a song here
#   MUSIC_FOR      a place in the game -> the songs that play there (in order,
#                  then round again). None = silence.
#   LABEL_MUSIC    which place each story label belongs to
#
#   $ music_for("casino")      switch to a place's songs (fades)
#   $ music_menu()             back to the main menu music
#
# Settings > AUDIO: IN-GAME MUSIC, MAIN MENU MUSIC (theme / shuffle), SONG POPUPS
# ==============================================================================

define SONGS = {
    "main_menu":            ("Songs/main_menu.mp3",               _("Main Theme"),                       "Departure at 4:00"),
    "larp":                 ("Songs/larp.mp3",                    _("LARP Music"),                       "larp music"),
    "end_of_beginning":     ("Songs/end_of_beginning.opus",       "End Of Beginning",                    "Djo"),
    "earrings":             ("Songs/earrings.opus",               "Earrings",                            "Malcolm Todd"),
    "music_sounds_better":  ("Songs/music_sounds_better.opus",    "Music Sounds Better With You",        "Stardust"),
    "stayin_alive":         ("Songs/stayin_alive.opus",           "Stayin' Alive",                       "Bee Gees"),
    "everybody_wants_to_rule": ("Songs/everybody_wants_to_rule.opus", "Everybody Wants To Rule The World", "Tears For Fears"),
    "slide":                ("Songs/slide.opus",                  "Slide",                               "Calvin Harris"),
    "the_less_i_know":      ("Songs/the_less_i_know.opus",        "The Less I Know The Better",          "Tame Impala"),
    "somebodys_watching_me": ("Songs/somebodys_watching_me.opus", "Somebody's Watching Me",              "Rockwell"),
    "self_aware":           ("Songs/self_aware.opus",             "Self Aware",                          "Temper City"),
    "loser":                ("Songs/loser.opus",                  "Loser",                               "Tame Impala"),
    "walking_on_a_dream":   ("Songs/walking_on_a_dream.opus",     "Walking On A Dream",                  "Empire Of The Sun"),
    "sunflower":            ("Songs/sunflower.opus",              "Sunflower",                           "Post Malone, Swae Lee"),
    "stella":               ("Songs/stella.opus",                 "STELLA",                              "SAINT PEPSI"),
    "pumped_up_kicks":      ("Songs/pumped_up_kicks.opus",        "Pumped Up Kicks",                     "Foster The People"),
    "gta6_main_theme":      ("Songs/gta6_main_theme.opus",        "Grand Theft Auto VI Main Theme",      "Rockstar Games"),
    "gta6_trailer_song":    ("Songs/gta6_trailer_song.opus",      "GTA VI Trailer Song (Edit)",          "Rockstar Games"),
    "flower_in_a_hurricane": ("Songs/flower_in_a_hurricane.opus", "Flower In A Hurricane",               "Justice ft. Tame Impala, SZA, King Gizzard & the Lizard Wizard"),
    "rhyno":                ("Songs/rhyno.opus",                  "RHYNO",                               "Travis Scott"),
    "midnight_city":        ("Songs/midnight_city.opus",          "Midnight City",                       "M83"),
    "gta6_extended_look":   ("Songs/gta6_extended_look.opus",     "GTA VI: An Extended Look",            "Rockstar Games"),
}

# the order the jukebox lists them in
define SONG_ORDER = [
    "main_menu", "larp", "end_of_beginning", "earrings", "music_sounds_better", "stayin_alive",
    "everybody_wants_to_rule", "slide", "the_less_i_know", "somebodys_watching_me", "self_aware",
    "loser", "walking_on_a_dream", "sunflower", "stella", "pumped_up_kicks",
    "gta6_main_theme", "gta6_trailer_song", "flower_in_a_hurricane", "rhyno", "midnight_city",
    "gta6_extended_look",
]

# a place -> its songs
define MUSIC_FOR = {
    # Part 1: an ordinary (ish) train ride
    "c1": ["end_of_beginning", "earrings"],                 # waking up, confused
    "c2": ["music_sounds_better", "stayin_alive"],          # the bar and the gambler
    "c3": ["everybody_wants_to_rule"],                      # the expensive cabin
    "c4": ["slide"],                                        # the engine
    "c5": ["the_less_i_know"],                              # Alexander's corner
    # Part 2: someone's dead and the train keeps looping
    "part2": ["somebodys_watching_me"],
    "part2_c3": ["self_aware"],
    "part2_c5": ["loser"],
    # nothing while it matters most
    "silence": None,
    # the way out
    "escape": ["sunflower"],
    "true": ["walking_on_a_dream"],
    # away from the story
    "menu_shuffle": ["main_menu", "walking_on_a_dream", "stella", "end_of_beginning", "sunflower"],
    "casino": ["stella", "stayin_alive", "pumped_up_kicks", "music_sounds_better"],
    "credits": ["gta6_main_theme", "flower_in_a_hurricane", "rhyno", "gta6_trailer_song", "midnight_city", "gta6_extended_look"],
    "credits_tickets": ["larp"],
    # radio stations (the radio bar at the bottom)
    "station_gta": ["gta6_main_theme", "flower_in_a_hurricane", "rhyno", "gta6_trailer_song", "midnight_city", "gta6_extended_look"],
    "station_chill": ["walking_on_a_dream", "stella", "end_of_beginning", "sunflower", "earrings", "the_less_i_know", "slide"],
}

# (id, name). SCENE MUSIC = the songs that fit where you are (MUSIC_FOR);
# the others play their own list everywhere until you change station.
define RADIO_STATIONS = [
    ("scene", _("SCENE MUSIC")),
    ("all",   _("ALL SONGS")),
    ("gta",   _("GTA RADIO")),
    ("chill", _("CHILL")),
    ("off",   _("RADIO OFF")),
]

# story label -> place. (label, place, place while in the loop)
define LABEL_MUSIC = {
    "carriage_1_start":        ("c1", "part2"),
    "carriage_1_hub":          ("c1", "part2"),
    "carriage_2_start":        ("c2", "part2"),
    "carriage_2_hub":          ("c2", "part2"),
    "carriage_3_start":        ("c3", "part2_c3"),
    "carriage_3_hub":          ("c3", "part2_c3"),
    "carriage_4_start":        ("c4", "c4"),
    "carriage_4_hub":          ("c4", "c4"),
    "carriage_5_start":        ("c5", "part2_c5"),
    "carriage_5_hub":          ("c5", "part2_c5"),
    "part2_start":             ("part2", "part2"),
    "carriage_2_part2_start":  ("part2", "part2"),
    "carriage_2_part2_hub":    ("part2", "part2"),
    "c2_p2_investigation_hub": ("part2", "part2"),
    "carriage_2_part2_return": ("part2", "part2"),
    "carriage_3_part2_start":  ("part2_c3", "part2_c3"),
    "carriage_3_part2_hub":    ("part2_c3", "part2_c3"),
    "carriage_5_part2_start":  ("part2_c5", "part2_c5"),
    "carriage_5_part2_hub":    ("part2_c5", "part2_c5"),
    "accusation_scene":        ("silence", "silence"),
    "carriage_6_start":        ("silence", "silence"),
    "ending_1_death":          ("silence", "silence"),
    "ending_2_escape":         ("escape", "escape"),
    "ending_3_true":           ("true", "true"),
    "empty_train":             ("silence", "silence"),
}

default persistent.ingame_music = True
default persistent.menu_music = "theme"        # "theme" or "shuffle"
default persistent.song_popups = True
default persistent.radio_station = "scene"
default persistent.radio_bar = True

init python:
    SONG_BY_FILE = dict((f, (sid, title, artist)) for sid, (f, title, artist) in SONGS.items())

    def song_files(ids):
        return [SONGS[i][0] for i in ids if i in SONGS and renpy.loadable(SONGS[i][0])]

    class _MUSIC(object):
        place = None        # what's playing now: a MUSIC_FOR place, "menu", "jukebox", a station
        scene = None        # the story place we're in (for SCENE MUSIC)

    def radio_scene():
        return persistent.radio_station == "scene"

    def music_for(place, fade=2.0, carry=False):
        """Switch to a place's songs. Already playing them: carry on.
        carry: let the song that's playing finish first, then go on to these
        (used when the story starts, so the menu song doesn't cut off)."""
        if not radio_scene():
            return          # a radio station is on: it keeps playing
        if place == _MUSIC.place and renpy.music.is_playing("music"):
            return
        before = _MUSIC.place
        _MUSIC.place = place
        ids = MUSIC_FOR.get(place)
        files = song_files(ids) if ids else []
        if not files:
            renpy.music.stop(channel="music", fadeout=fade)
            return
        if carry and before in ("menu", "jukebox", None) and renpy.music.is_playing("music"):
            renpy.music.queue(files, channel="music", loop=True, clear_queue=True)
            return
        renpy.music.play(files, channel="music", loop=True, fadein=fade, fadeout=fade, if_changed=True)

    def menu_music_files():
        ids = MUSIC_FOR["menu_shuffle"][:] if persistent.menu_music == "shuffle" else ["main_menu"]
        if persistent.menu_music == "shuffle":
            renpy.random.shuffle(ids)
        return song_files(ids)

    def _menu_music_config():
        # Ren'Py starts config.main_menu_music by itself on the main menu, so
        # only set it while SCENE MUSIC is the station
        config.main_menu_music = (menu_music_files() or None) if radio_scene() else None

    def music_menu():
        """Back to the main menu's music (or whatever station is on)."""
        if not radio_scene():
            radio_play_station(restart=False)
            return
        _MUSIC.place = "menu"
        files = menu_music_files()
        if files:
            renpy.music.play(files, channel="music", loop=True, fadein=1.0, if_changed=True)

    def set_menu_music(mode):
        persistent.menu_music = mode
        _menu_music_config()
        if main_menu and radio_scene():
            _MUSIC.place = None
            renpy.music.stop(channel="music", fadeout=0.5)
            music_menu()
        renpy.restart_interaction()

    def music_skip():
        """NEXT: on to the next song in what's playing."""
        q = renpy.music.get_playing("music")
        files = renpy.music.get_loop("music") or []
        if q in files and len(files) > 1:
            k = files.index(q)
            files = files[k + 1:] + files[:k + 1]
            renpy.music.play(files, channel="music", loop=True, fadein=0.5, fadeout=0.5)
        elif q:
            renpy.music.stop(channel="music", fadeout=0.5)

    # ---- the radio ------------------------------------------------------------
    class _RADIO(object):
        history = []        # songs played, newest last (for PREVIOUS)

    def radio_play_station(restart=True):
        st = persistent.radio_station
        if st == "off":
            _MUSIC.place = "off"
            renpy.music.stop(channel="music", fadeout=1.0)
        elif st == "scene":
            _MUSIC.place = None
            if main_menu:
                music_menu()
            elif persistent.ingame_music and _MUSIC.scene:
                music_for(_MUSIC.scene, fade=1.0)
            else:
                renpy.music.stop(channel="music", fadeout=1.0)
        else:
            if not restart and _MUSIC.place == "station_" + st and renpy.music.is_playing("music"):
                return
            ids = SONG_ORDER[:] if st == "all" else MUSIC_FOR["station_" + st][:]
            renpy.random.shuffle(ids)
            files = song_files(ids)
            _MUSIC.place = "station_" + st
            try:
                menu_music_filter_off()
            except Exception:
                pass
            renpy.music.play(files, channel="music", loop=True, fadein=1.0, fadeout=1.0)

    def radio_station_step(d=1):
        ids = [k for k, _n in RADIO_STATIONS]
        k = ids.index(persistent.radio_station) if persistent.radio_station in ids else 0
        persistent.radio_station = ids[(k + d) % len(ids)]
        renpy.music.set_pause(False, channel="music")
        _menu_music_config()
        radio_play_station()
        renpy.restart_interaction()

    def radio_station_name():
        return dict(RADIO_STATIONS).get(persistent.radio_station, _("SCENE MUSIC"))

    def radio_paused():
        try:
            return renpy.music.get_pause(channel="music")
        except Exception:
            return False

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
        """Back to the song before this one (or the start of this one)."""
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

# init 2: after every other label callback is set up, chaining onto them
init 2 python:
    # every story label: switch to the music for where we are
    _old_label_cb_music = config.label_callback

    def _music_label_cb(name, abnormal=False):
        try:
            if not main_menu and name in LABEL_MUSIC:
                normal, looped = LABEL_MUSIC[name]
                _MUSIC.scene = looped if getattr(store, "in_loop", False) else normal
                if persistent.ingame_music:
                    music_for(_MUSIC.scene, carry=True)
        except Exception:
            pass
        if _old_label_cb_music:
            _old_label_cb_music(name, abnormal)

    config.label_callback = _music_label_cb

init python:
    def set_ingame_music(on):
        persistent.ingame_music = on
        if not on and not main_menu:
            _MUSIC.place = None
            renpy.music.stop(channel="music", fadeout=1.0)
        renpy.restart_interaction()

    # ---- "now playing" popup, like a radio station changing song -----------
    class _NP(object):
        last = None

    def now_playing_check():
        try:
            cur = renpy.music.get_playing("music")
        except Exception:
            cur = None
        if cur == _NP.last:
            return
        _NP.last = cur
        if cur:
            _RADIO.history = (_RADIO.history + [cur])[-30:]
        if cur in SONG_BY_FILE and persistent.song_popups:
            sid, title, artist = SONG_BY_FILE[cur]
            renpy.show_screen("now_playing", title, artist)

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
        xalign 0.5
        ypos 30
        padding (22, 12)
        background rbox("#0a0a0ee0", 16)
        at np_slide
        hbox:
            spacing 16
            text "♪":
                yalign 0.5
                size 34
                color "#e6a817"
                font "DejaVuSans.ttf"
            vbox:
                spacing 2
                text title:
                    size 22
                    color "#f2e6d8"
                    font GFONT
                text artist:
                    size 15
                    color "#8888a0"
                    font GFONT
    timer 5.2 action Hide("now_playing")


# ------------------------------------------------------------------------------
# THE RADIO BAR  (bottom right, on every screen; Settings > Audio > RADIO BAR)
# ------------------------------------------------------------------------------

transform radio_fade:
    on idle:
        ease 0.25 alpha 0.75
    on hover:
        ease 0.15 alpha 1.0

screen radio_btn(label, act, w=46, size=18):
    button:
        xysize (w, 36)
        padding (0, 0)
        background None
        hover_background rbox("#ffffff1c", 12)
        action act
        text label:
            align (0.5, 0.5)
            size size
            color "#cfcac0"
            hover_color "#ffd700"
            font "DejaVuSans.ttf"

screen radio_bar():
    zorder 1250
    if persistent.radio_bar:
        $ cur = renpy.music.get_playing("music")
        $ song = SONG_BY_FILE.get(cur)
        button:
            xalign 1.0
            yalign 1.0
            offset (-170, -12)
            padding (10, 4)
            background rbox("#0a0a0ee6", 18)
            action NullAction()
            at radio_fade
            hbox:
                spacing 4
                yalign 0.5
                use radio_btn("|◄", Function(radio_prev), size=16)
                use radio_btn(("►" if (radio_paused() or not cur) else "II"), Function(radio_toggle_pause), size=16)
                use radio_btn("►|", Function(radio_next), size=16)
                null width 6
                vbox:
                    yalign 0.5
                    xsize 300
                    spacing 0
                    text ((song[1] if song else _("Nothing playing"))[:30]):
                        size 15
                        color "#f2e6d8"
                        layout "nobreak"
                        font GFONT
                    text ((song[2] if song else "")[:34]):
                        size 12
                        color "#8888a0"
                        layout "nobreak"
                        font GFONT
                button:
                    yalign 0.5
                    ysize 36
                    padding (12, 0)
                    background rbox("#ffffff10", 12)
                    hover_background rbox("#e6a81744", 12)
                    action Function(radio_station_step, 1)
                    tooltip _("Change station")
                    text radio_station_name():
                        yalign 0.5
                        size 13
                        color "#e6a817"
                        hover_color "#ffd700"
                        font GFONT

init python:
    config.always_shown_screens.append("radio_bar")
