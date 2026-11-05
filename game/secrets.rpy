default persistent.cheat_autowin = False
default persistent.cheat_hotspots = False

init 1 python:
    MINIGAME_LIST = [
        ("ticket",     _("Find your ticket"),          "mg_ticket",         ticket_reset,     _("Start")),
        ("door",       _("Open the door"),             "mg_door",           door_reset,       _("Carriage doors")),
        ("lockpick",   _("Pick the lock"),             "mg_lockpick",       lockpick_reset,   _("Carriage 1 / 6")),
        ("shards",     _("Sweep up the glass"),        "mg_shards",         shards_reset,     _("Carriage 2")),
        ("mahjong",    _("Mahjong"),                   "mahjong_minigame",  mahjong_reset,    _("Carriage 2")),
        ("blocks",     _("Misha's blocks"),            "mg_blocks",         blocks_reset,     _("Carriage 3")),
        ("engine",     _("Keep steam pressure steady"), "mg_engine",        engine_reset,     _("Carriage 4")),
        ("mail",       _("Sort the mail"),             "mg_mail",           mail_reset,       _("Carriage 5")),
        ("combo",      _("The luggage lock"),          "mg_combo",          combo_reset,      _("Part 2, Carriage 3")),
        ("pry",        _("Pull up the carpet"),        "mg_pry",            pry_reset,        _("Part 2, Carriage 3")),
        ("evidence",   _("Present the evidence"),      "mg_evidence",       evidence_reset,   _("Part 2")),
    ]

    def arcade_play(scr, reset):
        store.mg_required = False
        reset()
        renpy.call_screen(scr)

    def play_minigame(scr, reset):
        renpy.invoke_in_new_context(arcade_play, scr, reset)

init python:
    def cheats_allowed():
        return bool(config.developer or has_pass("cheats"))

    def toggle_cheats():
        toggle_pass("cheats")
        renpy.notify(_("Cheats ON (F9)") if has_pass("cheats") else _("Cheats OFF"))

    P1_TALKS = [
        ["c1_talked_fedora", "door_c2_open"],
        ["c2_talked_eduard", "c2_talked_shunyu"],
        ["c3_talked_kimmy", "c3_talked_himmel", "c3_talked_sebastian", "c3_talked_misha", "door_c4_open"],
        ["c4_talked_agatha", "c4_talked_ichora", "has_key"],
        ["c5_talked_pattison", "c5_talked_alexander"],
    ]
    P2_STEPS = [
        ["door_c2_open_loop"],
        ["c2_p2_found_body", "c2_p2_reinterviewed_eduard", "c2_p2_reinterviewed_agatha",
         "clue_tile_mismatch", "clue_body_moved"],
        ["clue_drug_wrapper", "clue_hidden_tile", "kimmy_reinterviewed", "himmel_reinterviewed",
         "sebastian_reinterviewed", "misha_reinterviewed"],
        ["alexander_reinterviewed", "pattison_reinterviewed", "clue_alexander_alibi"],
    ]

    CHEAT_CHAPTERS = [
        (_("Start: the ticket"), "start", 0),
        (_("Carriage 1"), "carriage_1_start", 0),
        (_("Carriage 2"), "carriage_2_start", 1),
        (_("Carriage 3"), "carriage_3_start", 2),
        (_("Carriage 4"), "carriage_4_start", 3),
        (_("Carriage 5"), "carriage_5_start", 4),
        (_("Carriage 6 door"), "c5_carriage6_door", 5),
        (_("Part 2: wake up"), "part2_start", 5),
        (_("Part 2: crime scene"), "carriage_2_part2_start", 6),
        (_("Part 2: Carriage 3"), "carriage_3_part2_start", 7),
        (_("Part 2: Carriage 5"), "carriage_5_part2_start", 8),
        (_("Accusation"), "accusation_scene", 9),
        (_("Carriage 6"), "carriage_6_start", 9),
        (_("Ending 1"), "ending_1_death", 9),
        (_("Ending 2"), "ending_2_escape", 9),
        (_("Ending 3"), "ending_3_true", 9),
    ]

    class CHEAT(object):
        target = "start"
        stage = 0

    def cheat_target(label, stage):
        CHEAT.target = label
        CHEAT.stage = stage

    def cheat_apply():
        stage = CHEAT.stage
        for i, flags in enumerate(P1_TALKS):
            for f in flags:
                setattr(store, f, i < stage)
        loop = stage >= 6
        store.in_loop = loop
        for i, flags in enumerate(P2_STEPS):
            for f in flags:
                setattr(store, f, loop and (i < stage - 5))
        if loop:
            renpy.show_screen("loop_overlay")
        else:
            renpy.hide_screen("loop_overlay")

    def cheat_set(names, value=True):
        for n in names:
            setattr(store, n, value)
        renpy.notify(_("Done."))

    def cheat_all_clues():
        cheat_set([cid for cid, _t, _x in CLUE_LIST])

    def cheat_talk_part1():
        cheat_set([f for flags in P1_TALKS for f in flags])

    def cheat_talk_part2():
        cheat_set([f for flags in P2_STEPS for f in flags])

    def cheat_unlock_achievements():
        for a in ACHIEVEMENTS:
            achievement.grant(a["id"])
        renpy.notify(_("All achievements unlocked."))

    def cheat_reset_achievements():
        achievement.clear_all()
        renpy.notify(_("Achievements reset."))

    def cheat_unlock_extras():
        persistent.endings_seen = set(k for k, _a, _b, _c, _d, _e in ENDINGS)
        persistent.secrets = set(sid for sid, _n in SECRET_NOTES if sid) | set(["konami", "key_cut"])
        persistent.crew_found = set(c["key"] for c in CREW)
        persistent.mg_won = set(k for k, _n, _s, _r, _w in MINIGAME_LIST)
        renpy.notify(_("Endings, secrets and minigames unlocked."))

    def cheat_reset_extras():
        persistent.endings_seen = set()
        persistent.secrets = set()
        persistent.crew_found = set()
        persistent.mg_won = set()
        persistent.credits_clicked = set()
        persistent.tickets = 0
        persistent.coins = 50
        persistent.golden_found = set()
        persistent.passes = set()
        persistent.passes_off = set()
        persistent.cast_called = set()
        persistent.eric_clicks = 0
        persistent.key_pokes = 0
        renpy.notify(_("Endings, secrets and minigames reset."))

label cheat_warp:
    $ cheat_apply()
    $ renpy.jump(CHEAT.target)


screen cheat_hotkey():
    if cheats_allowed():
        key "K_F9" action ToggleScreen("cheat_menu")

init python:
    config.always_shown_screens.append("cheat_hotkey")

define CHEAT_TABS = [("jump", _("JUMP")), ("flags", _("FLAGS")), ("games", _("MINIGAMES")), ("unlocks", _("UNLOCKS")), ("tools", _("TOOLS"))]

screen cheat_btn(label, act, w=392, sel=False):
    button:
        xsize w
        ysize 52
        padding (18, 0)
        background rbox("#e0521f" if sel else "#1d1d26", 16)
        hover_background rbox("#f06a35" if sel else "#2c2c3a", 16)
        action act
        text label:
            yalign 0.5
            size 19
            color ("#0a0a0e" if sel else "#e8e4dc")
            font GFONT

screen cheat_menu():
    modal True
    zorder 500
    default ct = "jump"

    key "K_ESCAPE" action Hide("cheat_menu")
    key "game_menu" action Hide("cheat_menu")

    add Solid("#000000c8")

    frame:
        align (0.5, 0.5)
        xysize (1320, 860)
        padding (40, 32)
        background rbox("#121218f4", 34)

        vbox:
            spacing 16
            hbox:
                spacing 24
                text _("CHEATS"):
                    size 40
                    color "#ffd700"
                    font GFONT
                if not main_menu:
                    text (_("Part 2") if in_loop else _("Part 1")) + "   " + _("clues: %d / %d") % (len([c for c, _t, _x in CLUE_LIST if getattr(store, c, False)]), len(CLUE_LIST)):
                        yalign 0.7
                        size 18
                        color "#8888a0"
                        font GFONT

            hbox:
                spacing 10
                for tk, tl in CHEAT_TABS:
                    use cheat_btn(tl, SetScreenVariable("ct", tk), w=190, sel=(ct == tk))

            null height 6

            fixed:
                xysize (1240, 600)

                if ct == "jump":
                    hbox:
                        box_wrap True
                        box_wrap_spacing 12
                        xmaximum 1220
                        spacing 12
                        for lab, target, stage in CHEAT_CHAPTERS:
                            if main_menu:
                                use cheat_btn(lab, [Function(cheat_target, target, stage), Start("cheat_warp")])
                            else:
                                use cheat_btn(lab, [Function(cheat_target, target, stage), Hide("cheat_menu"), Jump("cheat_warp")])

                elif ct == "flags":
                    vbox:
                        spacing 12
                        if main_menu:
                            text _("Start a game first to change story flags."):
                                size 20
                                color "#8888a0"
                                font GFONT
                        else:
                            hbox:
                                spacing 12
                                use cheat_btn(_("Give all clues"), Function(cheat_all_clues))
                                use cheat_btn(_("Talk to everyone (Part 1)"), Function(cheat_talk_part1))
                                use cheat_btn(_("Do everything (Part 2)"), Function(cheat_talk_part2))
                            hbox:
                                box_wrap True
                                box_wrap_spacing 12
                                xmaximum 1220
                                spacing 12
                                for fl in ["in_loop", "has_key", "has_maple_sugar", "found_timetable",
                                           "clue_tile_mismatch", "clue_body_moved", "clue_drug_wrapper",
                                           "clue_hidden_tile", "clue_alexander_alibi", "c2_p2_found_body",
                                           "door_c2_open", "door_c4_open"]:
                                    use cheat_btn(fl, ToggleVariable(fl), sel=bool(getattr(store, fl, False)))

                elif ct == "games":
                    vbox:
                        spacing 12
                        hbox:
                            spacing 12
                            use cheat_btn(_("Minigames win themselves"), ToggleField(persistent, "cheat_autowin"), w=604, sel=persistent.cheat_autowin)
                        hbox:
                            box_wrap True
                            box_wrap_spacing 12
                            xmaximum 1220
                            spacing 12
                            for gk, gname, gscr, greset, gwhere in MINIGAME_LIST:
                                use cheat_btn(gname, Function(play_minigame, gscr, greset))

                elif ct == "unlocks":
                    hbox:
                        box_wrap True
                        box_wrap_spacing 12
                        xmaximum 1220
                        spacing 12
                        use cheat_btn(_("Unlock all achievements"), Function(cheat_unlock_achievements), w=604)
                        use cheat_btn(_("Reset achievements"), Function(cheat_reset_achievements), w=604)
                        use cheat_btn(_("Unlock endings, secrets, minigames"), Function(cheat_unlock_extras), w=604)
                        use cheat_btn(_("Reset endings, secrets, minigames"), Function(cheat_reset_extras), w=604)
                        use cheat_btn(_("Give 50 tickets"), Function(give_tickets, 50), w=604)
                        use cheat_btn(_("9999 coins"), SetField(persistent, "coins", 9999), w=604)
                        use cheat_btn(_("Show hotspot outlines"), ToggleField(persistent, "cheat_hotspots"), w=604, sel=persistent.cheat_hotspots)
                        use cheat_btn(_("Instant text"), [Preference("text speed", 0)], w=604)
                        use cheat_btn(_("Normal text speed"), [Preference("text speed", 40)], w=604)

                elif ct == "tools":
                    vbox:
                        spacing 18
                        hbox:
                            box_wrap True
                            box_wrap_spacing 12
                            xmaximum 1220
                            spacing 12
                            use cheat_btn(_("Skip to the next choice"), ([Hide("cheat_menu"), Skip(fast=True, confirm=False)] if not main_menu else None))
                            use cheat_btn(_("Screenshot"), [Hide("cheat_menu"), Screenshot()])
                            use cheat_btn(_("Mouse coordinates"), ToggleField(persistent, "dev_coords"), sel=persistent.dev_coords)
                            use cheat_btn(_("Every gamepass"), Function(dev_all_passes))
                            use cheat_btn(_("Debug game"), Function(play_minigame, "mg_debug", debug_reset))
                            if config.developer:
                                use cheat_btn(_("Reload script"), Function(renpy.reload_script))
                        if not main_menu:
                            vbox:
                                spacing 6
                                for k, v in dev_state_lines():
                                    hbox:
                                        spacing 20
                                        text k:
                                            min_width 200
                                            size 17
                                            color "#8888a0"
                                            font GFONT
                                        text _esc(str(v)):
                                            size 17
                                            color "#e8e4dc"
                                            font "DejaVuSans.ttf"

            hbox:
                xalign 1.0
                use cheat_btn(_("CLOSE  (F9)"), Hide("cheat_menu"), w=220)


screen arcade_list(w):
    if cheats_allowed():
        frame:
            xfill True
            background rbox("#0e1620", 22)
            padding (26, 14)
            fixed:
                xfill True
                ysize 56
                vbox:
                    yalign 0.5
                    spacing 4
                    text _("DEBUG"):
                        size 26
                        color "#61afef"
                        font GFONT
                    text _("CHEAT MENU"):
                        size 16
                        color "#8888a0"
                        font GFONT
                fixed:
                    xalign 1.0
                    yalign 0.5
                    xysize (170, 50)
                    use rbtn(_("PLAY"), Function(play_minigame, "mg_debug", debug_reset), w=170, h=50, r=16, size=22, bg="#14202e", hov="#1f3048", col="#61afef", hcol="#ffffff")
    for idx, (gk, gname, gscr, greset, gwhere) in enumerate(MINIGAME_LIST):
        $ won = gk in persistent.mg_won
        frame:
            xfill True
            background rbox("#17150d" if won else "#101014", 22)
            padding (26, 14)
            at row_pop(min(idx * 0.04, 0.5))
            fixed:
                xfill True
                ysize 56
                vbox:
                    yalign 0.5
                    spacing 4
                    text gname:
                        size 26
                        color ("#ffd700" if won else "#e8e4dc")
                        font GFONT
                    text gwhere + ("   " + _("WON") if won else ""):
                        size 16
                        color "#8888a0"
                        font GFONT
                fixed:
                    xalign 1.0
                    yalign 0.5
                    xysize (170, 50)
                    use rbtn(_("PLAY"), Function(play_minigame, gscr, greset), w=170, h=50, r=16, size=22, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")


init python:
    class ET_CLOCK(object):
        n = 0

    def clock_poke():
        ET_CLOCK.n += 1
        if ET_CLOCK.n >= 4:
            ET_CLOCK.n = 0
            secret_found("timetable", "timetable")
            renpy.show_screen("gift_shop")
        renpy.restart_interaction()

    def clock_color():
        return "#ffffff%02x" % (8 + ET_CLOCK.n * 12)


default persistent.crew_found = set()

define SECRET_ACHIEVEMENTS = [
    {"id": "whole_crew", "title": _("You Will Before the End"), "description": _("Type all four crew names on the main menu."), "hidden": True},
    {"id": "pixel_parade", "title": _("They Always Come Back"), "description": _("Keep clicking the Blackberry logo after it tells you to stop."), "hidden": True},
    {"id": "right_on_time", "title": _("Departure at 4:00"), "description": _("Open the main menu at exactly 4:00."), "hidden": True},
]

define SECRET_NOTES = [
    ("konami", _("\"Every departure on it is printed the same way: 4:00.\"")),
    ("konami", _("\"This goes to the clock, while this goes to the end. This goes to the fake ones and this goes to the friend.\"")),
    ("key_cut", _("\"Sometimes, life gets hard, and a door is presented to escape. But we're too scared to use the key. Don't hesitate.\"")),
    ("crew", _("\"It's okay, you will before the end.\"")),
    ("parade", _("\"He'll come back though. They always come back. Don't they?\"")),
    ("on_time", _("\"Thank you for boarding the Grekhov Express.\"")),
    (None, _("THANKS FOR PLAYING!")),
]

init python:
    import time as _time
    import datetime as _datetime
    import random as _random

    for _sa in SECRET_ACHIEVEMENTS:
        if _sa["id"] not in [x["id"] for x in ACHIEVEMENTS]:
            ACHIEVEMENTS.append(_sa)
            achievement.register(_sa["id"])

    def secret_found(sid, ach=None):
        if sid not in persistent.secrets:
            give_tickets(TICKETS_FOR["secret"])
        persistent.secrets = set(persistent.secrets) | set([sid])
        if ach:
            achievement.grant(ach)

    def secret_notes():
        found = set(persistent.secrets)
        return [note for sid, note in SECRET_NOTES if sid is None or sid in found]

    class _SECRET(object):
        typed = ""
        berry_clicks = 0
        departed = False

    def _crew_reveal(c):
        renpy.show_screen("map_stamp", c["name"].upper(), _random.choice(c["roles"]).upper())
        persistent.crew_found = set(persistent.crew_found) | set([c["key"]])
        if len(persistent.crew_found) >= len(CREW):
            secret_found("crew", "whole_crew")
            renpy.notify(_("\"We've been waiting for you a while.\""))
        else:
            renpy.notify("%d / %d" % (len(persistent.crew_found), len(CREW)))

    def secret_key(tok):
        konami_feed(tok)
        if len(tok) != 1:
            _SECRET.typed = ""
            return
        _SECRET.typed = (_SECRET.typed + tok)[-12:]
        if CHEATS_BUILD and _SECRET.typed.endswith("debug"):
            _SECRET.typed = ""
            toggle_cheats()
            return
        for c in CREW:
            if _SECRET.typed.endswith(c["key"]):
                _SECRET.typed = ""
                _crew_reveal(c)
                return
        if more_secret_word(_SECRET.typed):
            _SECRET.typed = ""

    SECRET_LETTERS = sorted(set("".join(c["key"] for c in CREW)) | set("ba") | set("debug"))

    BERRY_LINES = {
        1: _("You already found the secret. Stop clicking it. Please."),
        4: _("\"Now leave me alone!\""),
        7: _("\"Can yer shut up?\""),
        10: _("\"WATCH OUT.\""),
        13: _("\"Fine.\""),
    }

    def blackberry_click():
        _SECRET.berry_clicks += 1
        n = _SECRET.berry_clicks
        if n in BERRY_LINES:
            renpy.notify(BERRY_LINES[n])
        if n >= 13:
            _SECRET.berry_clicks = 0
            renpy.show_screen("pixel_parade")
            secret_found("parade", "pixel_parade")

    def check_departure():
        if _SECRET.departed:
            return
        now = _datetime.datetime.now()
        if now.hour % 12 == 4 and now.minute == 0:
            _SECRET.departed = True
            renpy.show_screen("map_stamp", "4:00", _("WELCOME ABOARD"))
            secret_found("on_time", "right_on_time")


transform parade_walk(delay=0.0):
    yanchor 1.0
    xanchor 0.5
    ypos 1.0
    yoffset -14
    xpos config.screen_width + 160
    alpha 0.0
    pause delay
    alpha 1.0
    parallel:
        linear 10.0 xpos -160
    parallel:
        block:
            easeout 0.17 yoffset -34
            easein 0.17 yoffset -14
            repeat

screen pixel_parade():
    zorder 90
    for i, px in enumerate(PIXEL_PASSENGERS):
        add px at parade_walk(i * 0.85)
    timer (10.0 + len(PIXEL_PASSENGERS) * 0.85 + 0.5) action Hide("pixel_parade")


define ENDING_VIDEO = "movies/ending_video.webm"

default persistent.ending_video_seen = False
default persistent.credits_clicked = set()
default persistent.cast_called = set()
default persistent.eric_clicks = 0
default window_looks = 0

define MORE_SECRET_ACHIEVEMENTS = [
    {"id": "bond_one", "title": _("You play nice."), "description": _("Fill a passenger's hearts with gifts."), "hidden": False},
    {"id": "bond_all", "title": _("All of us."), "description": _("Fill every passenger's hearts."), "hidden": False},
    {"id": "timetable", "title": _("A little something..."), "description": _("Find the gift shop on the main menu."), "hidden": True},
    {"id": "golden_tickets", "title": _("Uh… uh… yes, the ticket."), "description": _("Find every golden ticket hidden on the train."), "hidden": False},
    {"id": "credits_all", "title": _("Anyone like who?"), "description": _("Click everyone in the credits."), "hidden": True},
    {"id": "cast_call", "title": _("Everyone."), "description": _("Type every passenger's name on the main menu."), "hidden": True},
    {"id": "quiet", "title": _("Way too quiet."), "description": _("Type a certain rapper's name on the main menu."), "hidden": True},
    {"id": "window", "title": _("What a beautiful sight outside!"), "description": _("Look out of the Carriage 2 window five times."), "hidden": True},
]

define MORE_SECRET_NOTES = [
    ("timetable", _("\"Everyone on this train deserves a little something.\"")),
    ("credits_all", _("\"I don't even know anybody on this express.\"")),
    ("cast_call", _("\"I need to find out who was in this carriage. Everyone.\"")),
    ("quiet", _("\"...It's quiet. Way too quiet.\"")),
    ("window", _("\"What a beautiful sight outside! You can see everything from this train!\"")),
    ("halloween", _("\"...I don't think this carriage was ever meant to be found.\"")),
    ("golden", _("\"Uh… uh… yes, the ticket. I think it's somewhere here…\"")),
    ("logo", _("\"Man… This seems familiar…\"")),
    ("slots", _("\"JACKKKPOTTTTTTT! You win $2! Look at that, beginner's luck!\"")),
    ("train", _("\"Wow damn… So… Expensive cabin, huh?\"")),
    ("version", _("\"I'm… back at the start?\"")),
    ("four_hundred", _("\"Thank you for boarding….\"")),
]

define CAST_CALLS = [
    ("louis", "louis neutral", _("I'm gonna look around.")),
    ("dorothy", "dorothy neutral", _("Excuse me sir, tickets please.")),
    ("fedora", "fedora neutral", _("Why Hello There, are you ready for the CALAMITY?")),
    ("eduard", "eduard neutral", _("All the better for me, I reckon…")),
    ("shunyu", "shunyu excited", _("JACKKKPOTTTTTTT!")),
    ("kimmy", "kimmy neutral", _("Yawns… Hello, are you room service?")),
    ("himmel", "himmel neutral", _("W-what do you want, stranger?")),
    ("sebastian", "sebastian neutral", _("May I know your name, sir?")),
    ("misha", "misha neutral", _("You play nice. Not like the others. They always forget the order.")),
    ("agatha", "agatha neutral", _("C'mon, put the bandage on.")),
    ("ichora", "ichora neutral", _("Oh, I know.")),
    ("pattison", "pattison neutral", _("This goes to the clock, while this goes to the end...")),
    ("alexander", "alexander neutral", _("Depends? Are you a narc?")),
]

init python:
    for _sa in MORE_SECRET_ACHIEVEMENTS:
        if _sa["id"] not in [x["id"] for x in ACHIEVEMENTS]:
            ACHIEVEMENTS.append(_sa)
            achievement.register(_sa["id"])

    SECRET_NOTES = SECRET_NOTES[:-1] + MORE_SECRET_NOTES + SECRET_NOTES[-1:]

    SECRET_LETTERS = sorted(set(SECRET_LETTERS) | set("".join(n for n, _i, _l in CAST_CALLS)) | set("kanye") | set("40"))

    def more_secret_word(typed):
        if typed.endswith("400"):
            store.board_times = []
            renpy.show_screen("map_stamp", "4:00", _("GREKHOV EXPRESS"))
            renpy.notify(_("\"Thank you for boarding….\""))
            secret_found("four_hundred")
            return True
        if typed.endswith("kanye"):
            secret_found("quiet", "quiet")
            play_ending_video()
            return True
        for name, img, line in CAST_CALLS:
            if typed.endswith(name):
                cast_call(name, img, line)
                return True
        return False

    def play_ending_video():
        renpy.music.stop(fadeout=0.5)
        renpy.invoke_in_new_context(renpy.movie_cutscene, ENDING_VIDEO)
        persistent.ending_video_seen = True
        if main_menu:
            music_menu()
        renpy.restart_interaction()

    def cast_call(name, img, line):
        renpy.show_screen("cast_peek", img)
        renpy.notify("\"" + line + "\"")
        persistent.cast_called = set(persistent.cast_called) | set([name])
        if len(persistent.cast_called) >= len(CAST_CALLS):
            secret_found("cast_call", "cast_call")

    def credits_click(key):
        persistent.credits_clicked = set(persistent.credits_clicked) | set([key])
        if key == "eric":
            persistent.eric_clicks = (persistent.eric_clicks or 0) + 1
            secret_found("eric_scare")
        if len(persistent.credits_clicked) >= len(CREW):
            secret_found("credits_all", "credits_all")

    class _CREDMUS(object):
        before = None

    def credits_music_on():
        if _MUSIC.place not in ("credits", "credits_tickets", "credits_spotlight"):
            _CREDMUS.before = _MUSIC.place
        menu_music_filter_off()
        st = credits_style_now()
        music_for({"tickets": "credits_tickets", "spotlight": "credits_spotlight"}.get(st, "credits"), fade=1.0)

    def credits_music_off():
        if main_menu:
            menu_music_filter_on()
            music_menu()
        else:
            before = _CREDMUS.before
            _MUSIC.place = None
            if before and persistent.ingame_music:
                music_for(before, fade=1.0)
            else:
                renpy.music.stop(channel="music", fadeout=1.0)

    def check_halloween():
        if getattr(_SECRET, "spooked", False):
            return
        now = _datetime.datetime.now()
        if now.month == 10 and now.day == 31:
            _SECRET.spooked = True
            secret_found("halloween")


transform peek_in:
    xanchor 0.5
    yanchor 1.0
    xpos 1.12
    ypos 1.08
    easein 0.45 xpos 0.86
    pause 2.2
    easeout 0.45 xpos 1.12

screen cast_peek(img):
    zorder 150
    add img at peek_in
    timer 3.2 action Hide("cast_peek")


default logo_glitched = False
default train_gone = False
default train_trips = 0
default version_pokes = 0

init python:
    class _MENU_SECRET(object):
        logo = 0

    def logo_poke():
        _MENU_SECRET.logo += 1
        if _MENU_SECRET.logo >= 3:
            _MENU_SECRET.logo = 0
            store.logo_glitched = True
            renpy.notify(_("\"Man… This seems familiar…\""))
            secret_found("logo")
        renpy.restart_interaction()

    def train_poke():
        if store.train_gone:
            return
        store.train_gone = True
        store.train_trips += 1
        renpy.notify(_("\"Wow damn… So… Expensive cabin, huh?\""))
        secret_found("train")
        renpy.restart_interaction()

    def version_poke():
        store.version_pokes += 1
        if store.version_pokes == 5:
            renpy.notify(_("\"I'm… back at the start?\""))
            secret_found("version")
        renpy.restart_interaction()

transform logo_glitch:
    alpha 1.0
    block:
        linear 0.04 xoffset 8
        linear 0.04 xoffset -6
        alpha 0.6
        linear 0.04 xoffset 0
        alpha 1.0
        pause 0.25
        linear 0.03 xoffset -10
        linear 0.03 xoffset 0
        pause 0.4
        repeat

transform train_leave(trip):
    alpha 1.0
    xoffset 0
    blur 0
    parallel:
        ease 1.4 alpha 0.0
    parallel:
        ease 1.4 xoffset 40 blur 8
    pause 0.6
    xoffset -320
    blur 8
    parallel:
        easein 1.8 xoffset 0
    parallel:
        ease 1.4 alpha 1.0 blur 0

default persistent.golden_found = set()

define GOLDEN_IDS = ["c1", "c2", "c3", "c4", "c5", "c2b", "c3b", "c5b"]
define GOLDEN_COINS = 25

init python:
    def find_golden(gid):
        if gid in persistent.golden_found:
            return
        persistent.golden_found = set(persistent.golden_found) | set([gid])
        n = len(persistent.golden_found)
        give_coins(GOLDEN_COINS)
        give_tickets(1)
        renpy.show_screen("map_stamp", _("GOLDEN TICKET"), "%d / %d" % (n, len(GOLDEN_IDS)))
        if n >= len(GOLDEN_IDS):
            secret_found("golden", "golden_tickets")
            renpy.notify(_("\"Uh… uh… yes, the ticket. I think it's somewhere here…\""))
        renpy.restart_interaction()

transform golden_glint(d=0.0):
    alpha 0.22
    pause d
    block:
        pause 3.2
        ease 0.25 alpha 1.0 zoom 1.25
        ease 0.45 alpha 0.22 zoom 1.0
        repeat

screen golden_ticket(gid, x, y):
    if gid not in persistent.golden_found:
        button:
            pos map_xy(x, y)
            xysize (40, 28)
            padding (0, 0)
            background None
            action Function(find_golden, gid)
            at golden_glint((len(gid) * 0.37) % 2.0)
            add rbox("#c9921a", 5):
                xysize (40, 28)
            add rbox("#ffd76a", 4):
                pos (3, 3)
                xysize (34, 22)
            add Solid("#c9921a"):
                pos (12, 3)
                xysize (2, 22)
