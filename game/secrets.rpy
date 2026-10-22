# Testing tools. Press F9 in game or on the main menu.

default persistent.cheats_on = False
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
        ("flashlight", _("Search in the dark"),        "mg_flashlight",     flashlight_reset, _("Part 2, Carriage 2")),
        ("combo",      _("The luggage lock"),          "mg_combo",          combo_reset,      _("Part 2, Carriage 3")),
        ("pry",        _("Pull up the carpet"),        "mg_pry",            pry_reset,        _("Part 2, Carriage 3")),
        ("survive",    _("Don't let them reach you"),  "mg_survive",        survive_reset,    _("Carriage 6")),
        ("evidence",   _("Present the evidence"),      "mg_evidence",       evidence_reset,   _("Part 2")),
        ("reveal",     _("Reveal"),                    "mg_reveal",         reveal_reset,     _("Carriage 6")),
    ]

    def arcade_play(scr, reset):
        store.mg_required = False
        reset()
        renpy.call_screen(scr)

    def play_minigame(scr, reset):
        renpy.invoke_in_new_context(arcade_play, scr, reset)

    def test_scare(kind):
        renpy.invoke_in_new_context(jumpscare, kind)

init python:
    def cheats_allowed():
        return bool(config.developer or persistent.cheats_on or has_pass("cheats") or has_pass("eric"))

    def toggle_cheats():
        persistent.cheats_on = not persistent.cheats_on
        sfx("win")
        renpy.notify(_("Cheats ON (F9)") if persistent.cheats_on else _("Cheats OFF"))

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
        (_("Empty train (secret)"), "empty_train", 0),
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
        renpy.hide_screen("dark_eyes")
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
            try:
                achievement.grant(a["id"])
            except Exception:
                pass
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
        persistent.empty_train_done = False
        persistent.cast_called = set()
        persistent.eric_clicks = 0
        persistent.key_pokes = 0
        renpy.notify(_("Endings, secrets and minigames reset."))

label cheat_warp:
    $ cheat_apply()
    $ renpy.jump(CHEAT.target)


# SCREENS

screen cheat_hotkey():
    if cheats_allowed():
        key "K_F9" action ToggleScreen("cheat_menu")

init python:
    config.overlay_screens.append("cheat_hotkey")

define CHEAT_TABS = [("jump", _("JUMP")), ("flags", _("FLAGS")), ("scares", _("SCARES")),
                     ("games", _("MINIGAMES")), ("unlocks", _("UNLOCKS"))]

screen cheat_btn(label, act, w=360, sel=False):
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
                    use cheat_btn(tl, SetScreenVariable("ct", tk), w=210, sel=(ct == tk))

            null height 6

            fixed:
                xysize (1240, 600)

                if ct == "jump":
                    hbox:
                        box_wrap True
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
                                xmaximum 1220
                                spacing 12
                                for fl in ["in_loop", "has_key", "has_maple_sugar", "found_timetable",
                                           "clue_tile_mismatch", "clue_body_moved", "clue_drug_wrapper",
                                           "clue_hidden_tile", "clue_alexander_alibi", "c2_p2_found_body",
                                           "door_c2_open", "door_c4_open"]:
                                    use cheat_btn(fl, ToggleVariable(fl), sel=bool(getattr(store, fl, False)))

                elif ct == "scares":
                    vbox:
                        spacing 12
                        if not persistent.jumpscares:
                            text _("Jumpscares are turned off in Settings > Accessibility."):
                                size 20
                                color "#e0521f"
                                font GFONT
                        hbox:
                            box_wrap True
                            xmaximum 1220
                            spacing 12
                            for kind in ["passenger", "conductor", "flicker", "crawler", "claws", "glitch", "window", "eyes"]:
                                use cheat_btn(kind.upper(), Function(test_scare, kind))
                            use cheat_btn(_("SHADOW FLASH"), Function(shadow_flash))
                            use cheat_btn(_("DO OR DIE"), Function(renpy.invoke_in_new_context, ticket_flash))

                elif ct == "games":
                    vbox:
                        spacing 12
                        hbox:
                            spacing 12
                            use cheat_btn(_("Minigames win themselves"), ToggleField(persistent, "cheat_autowin"), w=420, sel=persistent.cheat_autowin)
                        hbox:
                            box_wrap True
                            xmaximum 1220
                            spacing 12
                            for gk, gname, gscr, greset, gwhere in MINIGAME_LIST:
                                use cheat_btn(gname, Function(play_minigame, gscr, greset))

                elif ct == "unlocks":
                    hbox:
                        box_wrap True
                        xmaximum 1220
                        spacing 12
                        use cheat_btn(_("Unlock all achievements"), Function(cheat_unlock_achievements), w=560)
                        use cheat_btn(_("Reset achievements"), Function(cheat_reset_achievements), w=560)
                        use cheat_btn(_("Unlock endings, secrets, minigames"), Function(cheat_unlock_extras), w=560)
                        use cheat_btn(_("Reset endings, secrets, minigames"), Function(cheat_reset_extras), w=560)
                        use cheat_btn(_("Give 50 tickets"), Function(give_tickets, 50), w=560)
                        use cheat_btn(_("9999 coins"), SetField(persistent, "coins", 9999), w=560)
                        use cheat_btn(_("Show hotspot outlines"), ToggleField(persistent, "cheat_hotspots"), w=560, sel=persistent.cheat_hotspots)
                        use cheat_btn(_("Jumpscares"), ToggleField(persistent, "jumpscares"), w=560, sel=persistent.jumpscares)
                        use cheat_btn(_("Instant text"), [Preference("text speed", 0)], w=560)
                        use cheat_btn(_("Normal text speed"), [Preference("text speed", 40)], w=560)

            hbox:
                xalign 1.0
                use cheat_btn(_("CLOSE  (F9)"), Hide("cheat_menu"), w=220)


# EXTRAS > ARCADE

screen arcade_list(w):
    if has_pass("eric"):
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
                    text _("ERIC PASS"):
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


default persistent.empty_train_done = False

define lv = C("???", plate="#1a0a0a", creepy=True)

default et_c1_gone = False
default et_room_door = 0
default et_rooms_open = []
default et_wrong = 0
default et_door_xy = (1500, 300)
default et_shades = []
default et_step = 0
default et_watching = False
default et_push = 0

init 1 python:
    ET_SHADE = Fixed(
        Transform("images/louis_neutral.png", matrixcolor=flat_color("#030103"), zoom=0.53, yzoom=1.11),
        At(_eye(188, 137, 22, 8), Transform()),
        At(_eye(244, 137, 22, 8), Transform()),
        xysize=(394, 780))
    ET_PALE = ET_SHADE

    def et_vision(h=480, alpha=0.75):
        return Transform(ET_PALE, fit="contain", ysize=h, alpha=min(1.0, alpha + 0.15))

    def et_shade(h=480):
        return Transform(ET_SHADE, fit="contain", ysize=h)

    def et_scare(hold=0.7):
        if persistent.jumpscares:
            sfx("sting")
            renpy.invoke_in_new_context(renpy.call_screen, "et_lunge", hold)

    def et_flash():
        if persistent.jumpscares:
            renpy.show_screen("et_edge", renpy.random.choice((0.06, 0.12, 0.88, 0.94)))

    class ETDark(renpy.Displayable):

        def __init__(self, **kwargs):
            super(ETDark, self).__init__(**kwargs)
            self.hole = Transform("gui/flashlight.png", alpha=1.0)
            self.black = Solid("#000000fa")

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            x, y = ET_LIGHT.pos
            hs = 400
            hx, hy = int(x - hs // 2), int(y - hs // 2)

            for px, py, w, h in [(0, 0, width, hy), (0, hy + hs, width, height - hy - hs),
                                 (0, hy, hx, hs), (hx + hs, hy, width - hx - hs, hs)]:
                if w > 0 and h > 0:
                    rv.blit(renpy.render(self.black, w, h, st, at), (px, py))
            rv.blit(renpy.render(self.hole, hs, hs, st, at), (hx, hy))
            return rv

        def event(self, ev, x, y, st):
            if (x, y) != ET_LIGHT.pos:
                ET_LIGHT.pos = (x, y)
                renpy.redraw(self, 0)
            return None

        # Ren'Py calls this
        def visit(self):
            return [self.hole]

    class ET_LIGHT(object):
        pos = (-9999, -9999)

    ET_DARK = ETDark()

    class ET_CLOCK(object):
        n = 0

    def clock_poke():
        ET_CLOCK.n += 1
        sfx("lock_click")
        if ET_CLOCK.n >= 4:
            ET_CLOCK.n = 0
            renpy.music.stop(fadeout=1.0)
            Start("empty_train")()
        renpy.restart_interaction()

    def clock_color():
        return "#ffffff%02x" % (8 + ET_CLOCK.n * 12)

    def et_c4_setup():
        store.et_door_xy = (renpy.random.choice([220, 1500]), 280)
        spots = [(renpy.random.randint(200, 1700), renpy.random.randint(260, 640)) for _i in range(7)]
        store.et_shades = [[x, y, 0.0] for x, y in spots if abs(x - store.et_door_xy[0] - 75) > 260]
        ET_LIGHT.pos = (-9999, -9999)

    def et_c4_tick():
        mx, my = ET_LIGHT.pos
        keep = []
        caught = False
        for x, y, t in store.et_shades:
            sx, sy = map_xy(x + 90, y + 120)
            if (mx - sx) ** 2 + (my - sy) ** 2 <= 170 ** 2:
                t += 0.1
            else:
                t = max(0.0, t - 0.05)
            if t >= 0.8 and not caught:
                caught = True
            else:
                keep.append([x, y, t])
        store.et_shades = keep
        if caught:
            et_scare(0.6)
        renpy.restart_interaction()

    ET_STEPS = 8

    def et_c5_tick():
        if not store.et_watching:
            store.et_step += 1
            if store.et_step >= ET_STEPS:
                return "caught"
        renpy.restart_interaction()

    def et_c5_push():
        store.et_push += 1
        sfx("thud")
        if store.et_push >= 4:
            return "door"
        renpy.restart_interaction()


# LOOK AND FEEL

image et c1 = Transform("bg carriage_1_empty", matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.32) * TintMatrix("#a8b4c4"))
image et c2 = Solid("#0d0b10")
image et c3 = Solid("#0b0d10")
image et c4 = Solid("#0a0b09")
image et c5 = Transform("bg carriage_5", matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.42) * TintMatrix("#a8b4c4"))

transform et_jitter:
    block:
        xoffset 0
        pause 1.1
        linear 0.04 xoffset 4
        linear 0.04 xoffset -3
        linear 0.04 xoffset 0
        pause 0.6
        alpha 0.55
        pause 0.06
        alpha 0.8
        pause 1.7
        repeat

transform et_vanish:
    on show:
        alpha 0.0
        linear 0.6 alpha 1.0
    on hide:
        linear 0.12 alpha 0.0

transform et_lights_soft:
    alpha 0.0
    block:
        pause 4.0
        linear 2.0 alpha 0.4
        linear 2.5 alpha 0.0
        pause 3.0
        repeat

transform et_lights:
    alpha 0.0
    block:
        pause 2.3
        alpha 0.6
        pause 0.05
        alpha 0.0
        pause 0.1
        alpha 0.75
        pause 0.08
        alpha 0.0
        pause 4.1
        linear 1.2 alpha 0.35
        linear 1.6 alpha 0.0
        pause 3.0
        repeat

default et_level = 1

transform grain_jitter:
    block:
        choice:
            xoffset -24
            yoffset -12
        choice:
            xoffset 18
            yoffset 14
        choice:
            xoffset -8
            yoffset 20
        choice:
            xoffset 26
            yoffset -16
        pause 0.05
        repeat

transform et_heartbeat(rest):
    alpha 0.0
    block:
        ease 0.09 alpha 0.55
        ease 0.22 alpha 0.12
        ease 0.09 alpha 0.42
        ease 0.45 alpha 0.0
        pause rest
        repeat

transform et_breathe:
    xalign 0.5
    yalign 0.5
    zoom 1.0
    block:
        ease 3.2 zoom 1.035 rotate 0.25
        ease 3.2 zoom 1.0 rotate -0.2
        repeat

screen et_atmos():
    zorder 40
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)
    if not persistent.reduce_motion:
        add Transform("gui/vignette.png", matrixcolor=TintMatrix("#ff1a10")):
            xysize (config.screen_width, config.screen_height)
            at et_heartbeat(max(0.15, 1.5 - et_level * 0.24))
        add Transform("gui/grain.png", xysize=(config.screen_width + 60, config.screen_height + 40), alpha=0.11):
            pos (-30, -20)
            at grain_jitter
    add Solid("#000000") at (et_lights_soft if persistent.reduce_flashes else et_lights)
    timer max(2.5, 8.0 - et_level) repeat True action Function(et_flash)

transform cut_static:
    alpha 0.9
    linear 0.35 alpha 0.0

transform cut_glimpse:
    xalign 0.5
    yalign 1.0
    alpha 0.0
    pause 0.12
    alpha 0.9
    pause 0.07
    alpha 0.0

screen et_cut():
    zorder 280
    add Solid("#000000")
    add Transform("gui/grain.png", xysize=(config.screen_width, config.screen_height)) at cut_static
    if persistent.jumpscares:
        add Transform(ET_SHADE, fit="contain", ysize=int(config.screen_height * 1.1)) at cut_glimpse

label et_hard_cut:
    show screen et_cut
    $ renpy.pause(0.45, hard=True)
    hide screen et_cut
    return

screen et_finale():
    zorder 300
    add Solid("#000000")
    fixed:
        xysize (1, 1)
        at es_eyes_far
        add _eye(-46, 0, 46, 16)
        add _eye(46, 0, 46, 16)
    add SCARE_FACES["passenger"] at es_lunge
    add Solid("#6a0000") at es_red
    for k, (y, dx) in enumerate([(0.18, 60), (0.41, -90), (0.57, 120), (0.76, -70), (0.9, 40)]):
        add Solid("#000000"):
            xysize (config.screen_width, 40 + k * 9)
            at es_band(y, dx, k * 0.04)

transform crowd_step(near):
    xalign 0.5
    yalign 1.0
    ease 0.18 zoom (1.0 + near * 0.28)

transform et_rush:
    xanchor 0.5
    yanchor 0.15
    xpos 0.5
    ypos 0.5
    zoom 0.4
    alpha 0.0
    linear 0.06 alpha 1.0
    easein 0.22 zoom 2.6
    block:
        linear 0.03 xoffset 12
        linear 0.03 xoffset -12
        repeat

screen et_lunge(hold=0.7):
    zorder 300
    modal True
    add Solid("#000000")
    add Transform(ET_SHADE, fit="contain", ysize=900) at et_rush
    timer hold action Return()

transform et_edge_blip:
    alpha 0.0
    linear 0.03 alpha 0.8
    pause 0.1
    linear 0.03 alpha 0.0
    pause 0.06
    linear 0.02 alpha 0.5
    linear 0.15 alpha 0.0

screen et_edge(x):
    zorder 46
    add Transform(ET_SHADE, fit="contain", ysize=1000):
        xanchor 0.5
        xpos x
        yanchor 1.0
        ypos 1.05
        at et_edge_blip
    timer 0.5 action Hide("et_edge")


# THE CARRIAGES

screen et_c1():
    add "et c1"
    fixed:
        pos map_xy(0, 0)
        xysize (DESIGN_W, DESIGN_H)
        at Transform(zoom=MAP_K)
        showif not et_c1_gone:
            button:
                pos (1250, 330)
                xysize (200, 420)
                padding (0, 0)
                background None
                action NullAction()
                hovered SetVariable("et_c1_gone", True)
                at et_vanish
                add et_vision(420, 0.7) at et_jitter
    use hs(DOOR_RIGHT, Return("door"), "Carriage 2", "door")

screen et_c2():
    add "et c2"
    use hs(DOOR_RIGHT, Return("door"), "Carriage 3", "door")

screen et_c3():
    add "et c3"
    for i in range(4):
        $ rx = 200 + i * 400
        if i in et_rooms_open:
            fixed:
                pos map_xy(rx, 240)
                xysize (300, 560)
                at Transform(zoom=MAP_K)
                add rbox("#020102", 14)
                if i != et_room_door:
                    add et_shade(500):
                        xalign 0.5
                        yalign 1.0
                        at et_jitter
        else:
            fixed:
                pos map_xy(rx, 240)
                xysize (300, 560)
                at Transform(zoom=MAP_K)
                add rbox("#1b1920", 14)
                add rbox("#232129", 10):
                    pos (20, 20)
                    xysize (260, 230)
                add rbox("#232129", 10):
                    pos (20, 290)
                    xysize (260, 250)
                add rbox("#5a4a2a", 8):
                    pos (250, 270)
                    xysize (16, 16)
                add Solid("#000000"):
                    xpos 296
                    xysize (4, 560)
            use hs((rx, 240, 300, 560), Return(i), "Room", "look", i * 0.05)

screen et_c4():
    add "et c4"
    timer 0.1 repeat True action Function(et_c4_tick)
    fixed:
        pos map_xy(0, 0)
        xysize (DESIGN_W, DESIGN_H)
        at Transform(zoom=MAP_K)
        for x, y, t in et_shades:
            add et_shade(480):
                pos (x, y)
                at et_jitter
    use hs((et_door_xy[0], et_door_xy[1], 150, 420), Return("door"), "Carriage 5", "door")
    add ET_DARK:
        xysize (config.screen_width, config.screen_height)

transform et_closeness_shake(amount):
    block:
        linear 0.05 xoffset amount
        linear 0.05 xoffset (-amount)
        repeat

screen et_c5():
    add "et c5"
    timer 0.5 repeat True action Function(et_c5_tick)
    add Solid("#5a0000"):
        xysize (config.screen_width, config.screen_height)
        alpha (et_step / float(ET_STEPS) * 0.45)
    fixed:
        pos map_xy(0, 0)
        xysize (DESIGN_W, DESIGN_H)
        at Transform(zoom=MAP_K)
        $ z = 0.45 + et_step * 0.16
        button:
            xcenter 760
            yanchor 1.0
            ypos 1040
            xysize (int(260 * z), int(560 * z))
            padding (0, 0)
            background None
            action NullAction()
            hovered SetVariable("et_watching", True)
            unhovered SetVariable("et_watching", False)
            add et_vision(int(560 * z), 0.8):
                xalign 0.5
                yalign 1.0
                at et_jitter, et_closeness_shake(et_step * 2)
    use hs(DOOR_RIGHT, Function(et_c5_push), "Carriage 6", "door")

default et_near = 0

screen et_c6_crowd():
    zorder 5
    fixed:
        xysize (config.screen_width, config.screen_height)
        at crowd_step(et_near)
        fixed:
            pos map_xy(0, 0)
            xysize (DESIGN_W, DESIGN_H)
            at Transform(zoom=MAP_K)
            for i, (x, h) in enumerate([(80, 620), (300, 520), (480, 440), (620, 380),
                                        (1180, 380), (1320, 440), (1500, 520), (1720, 620)]):
                add et_shade(h):
                    xcenter x
                    yanchor 1.0
                    ypos 1080
                    at et_jitter


# THE STORY

label empty_train:
    $ in_secret_game = True
    $ renpy.block_rollback()
    stop music fadeout 2.0
    hide screen loop_overlay
    hide screen dark_eyes
    $ in_loop = False
    $ et_c1_gone = False
    $ et_rooms_open = []
    $ et_wrong = 0
    $ et_step = 0
    $ et_push = 0
    $ et_near = 0
    $ et_level = 1
    scene black
    pause 2.0
    "{i}Louis wakes up violently to the sound of train tracks.{/i}"
    "{i}He opens his eyes.{/i}"
    scene et c1 with Dissolve(2.5)
    if not persistent.reduce_motion:
        show layer master at et_breathe
    show screen et_atmos
    "{whisper}{i}No one is there.{/i}{/whisper}"
    l "{tremble}...It's quiet. Way too quiet.{/tremble}"

    call screen et_c1
    call et_hard_cut from _call_et_hard_cut

    $ et_level = 2
    scene et c2
    "{i}Louis enters. The lights feel dimmer, creepier than before.{/i}"
    show expression et_vision(560, 0.8) as vision:
        xalign 0.5
        yalign 1.0
        et_jitter
    with Dissolve(1.5)
    lv "{glitch}...It's quiet. Way too quiet.{/glitch}"
    l "{tremble}H-hello?? Who said that…{/tremble}"
    hide vision
    with Dissolve(0.08)
    "{whisper}{i}No one is there.{/i}{/whisper}"
    call screen et_c2
    call et_hard_cut from _call_et_hard_cut_1

    $ et_level = 3
    scene et c3
    "{i}The sleeper cabin is colder than before. The four rooms all sit slightly ajar, as if something moved through recently and didn't bother closing doors behind it.{/i}"
    $ et_room_door = renpy.random.randint(0, 3)
label et_c3_loop:
    call screen et_c3
    $ et_rooms_open = et_rooms_open + [_return]
    if _return == et_room_door:
        call et_hard_cut from _call_et_hard_cut_2
        jump et_c4_start
    $ et_wrong += 1
    if et_wrong == 1:
        u "{glitch}Be careful, young one. Do you really wanna do that?{/glitch}"
    elif et_wrong == 2:
        $ et_scare()
    else:
        mi "{wave}He'll come back though. They always come back. Don't they?{/wave}"
    jump et_c3_loop

label et_c4_start:
    $ et_level = 4
    scene et c4
    "{whisper}Huh… It's dark..{/whisper}"
    $ et_c4_setup()
    call screen et_c4
    call et_hard_cut from _call_et_hard_cut_3

label et_c5_start:
    $ et_level = 5
    $ et_step = 0
    $ et_push = 0
    $ et_watching = False
    scene et c5
    u "{glitch}Not yet! Try to see the truth before you see the future.{/glitch}"
    call screen et_c5
    if _return == "caught":
        $ et_scare(1.0)
        u "{glitch}You'll see.{/glitch}"
        jump et_c5_start
    call et_hard_cut from _call_et_hard_cut_4

    $ et_level = 6
    scene carriage_6 with fade
    show carriage_6_fog
    show screen et_c6_crowd
    "{i}You step through. The temperature drops.{/i}"
    show screen dark_eyes(((0.18, 0.22, 0.0), (0.82, 0.26, 0.4), (0.3, 0.55, 0.9), (0.7, 0.6, 1.3), (0.5, 0.15, 1.8)))
    l "{tremble}...It's so quiet. Why is it so quiet.{/tremble}"
    $ et_near = 1
    $ renpy.pause(0.6, hard=True)
    "{i}Two pairs of eyes glint in the blackness, watching.{/i}"
    $ et_near = 2
    $ renpy.pause(0.6, hard=True)
    l "{shake}What do you want from me?{/shake}"
    u "{glitch}Not me. Him.{/glitch}"
    hide screen dark_eyes
    show black as lights_out
    with Dissolve(0.15)
    $ renpy.pause(0.5, hard=True)
    hide lights_out
    show expression et_vision(900, 0.9) as vision:
        xalign 0.5
        yalign 1.0
        yoffset 120
        et_jitter
    with Dissolve(1.2)
    lv "{glitch}Man… This seems familiar…{/glitch}"
    lv "{glitch}“Here again?”{/glitch}"
    if persistent.jumpscares:
        show screen et_finale
        $ renpy.pause(ES_DARK + ES_HOLD, hard=True)
        hide screen et_finale
    hide screen et_c6_crowd
    hide screen et_atmos
    show layer master
    scene black
    "{i}Louis is hit with the darkness.{/i}"
    pause 2.5
    "{i}Louis wakes up violently to the sound of train tracks.{/i}"
    l "{tremble}I'm… back at the start?{/tremble}"
    call et_hard_cut from _call_et_hard_cut_5

    $ persistent.empty_train_done = True
    $ secret_found("empty_train", "empty_train")
    $ MainMenu(confirm=False)()
    return


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
            try:
                achievement.grant(ach)
            except Exception:
                pass

    def secret_notes():
        found = set(persistent.secrets)
        return [note for sid, note in SECRET_NOTES if sid is None or sid in found]

    class _SECRET(object):
        typed = ""
        berry_clicks = 0
        departed = False

    def _crew_reveal(c):
        sfx("win")
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
        if _SECRET.typed.endswith("debug"):
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

    def blackberry_click():
        _SECRET.berry_clicks += 1
        n = _SECRET.berry_clicks
        if n in BERRY_LINES:
            renpy.notify(BERRY_LINES[n])
        if n >= 13:
            _SECRET.berry_clicks = 0
            sfx("win")
            renpy.show_screen("pixel_parade")
            secret_found("parade", "pixel_parade")

    def check_departure():
        if _SECRET.departed:
            return
        now = _datetime.datetime.now()
        if now.hour % 12 == 4 and now.minute == 0:
            _SECRET.departed = True
            sfx("win")
            renpy.show_screen("map_stamp", "4:00", _("WELCOME ABOARD"))
            secret_found("on_time", "right_on_time")


# HEARTS

# PIXEL PARADE  (the pixel passengers, see PIXEL_CROPS in characters.rpy)

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

define CREDITS_CORNER_TEXT = {
    "eric": "PLACEHOLDER",
    "hannah": "PLACEHOLDER",
    "aydin": "PLACEHOLDER",
    "ryan": "PLACEHOLDER",
}

default persistent.ending_video_seen = False
default persistent.credits_clicked = set()
default persistent.cast_called = set()
default persistent.eric_clicks = 0
default window_looks = 0

define MORE_SECRET_ACHIEVEMENTS = [
    {"id": "empty_train", "title": _("Not me. Him."), "description": _("Ride the empty train to the end."), "hidden": True},
    {"id": "golden_tickets", "title": _("Uh… uh… yes, the ticket."), "description": _("Find every golden ticket hidden on the train."), "hidden": False},
    {"id": "credits_all", "title": _("Anyone like who?"), "description": _("Click everyone in the credits."), "hidden": True},
    {"id": "cast_call", "title": _("Everyone."), "description": _("Type every passenger's name on the main menu."), "hidden": True},
    {"id": "quiet", "title": _("Way too quiet."), "description": _("Type a certain rapper's name on the main menu."), "hidden": True},
    {"id": "window", "title": _("What a beautiful sight outside!"), "description": _("Look out of the Carriage 2 window five times."), "hidden": True},
]

define MORE_SECRET_NOTES = [
    ("empty_train", _("\"Not me. Him.\"")),
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
    ("idle", _("\"Two pairs of eyes glint in the blackness, watching.\"")),
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
            sfx("win")
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
        if renpy.loadable(ENDING_VIDEO):
            renpy.music.stop(fadeout=0.5)
            renpy.invoke_in_new_context(renpy.movie_cutscene, ENDING_VIDEO)
            persistent.ending_video_seen = True
            if main_menu:
                music_menu()
            renpy.restart_interaction()

    def cast_call(name, img, line):
        sfx("ui_click")
        renpy.show_screen("cast_peek", img)
        renpy.notify("\"" + line + "\"")
        persistent.cast_called = set(persistent.cast_called) | set([name])
        if len(persistent.cast_called) >= len(CAST_CALLS):
            secret_found("cast_call", "cast_call")

    def credits_click(key):
        persistent.credits_clicked = set(persistent.credits_clicked) | set([key])
        c = [x for x in CREW if x["key"] == key][0]
        if key == "eric":
            persistent.eric_clicks = (persistent.eric_clicks or 0) + 1
            sfx("win")
            renpy.show_screen("eric_surprise")
            renpy.notify(CREDITS_CORNER_TEXT["eric"])
        elif key == "hannah":
            sfx("win")
            renpy.show_screen("hannah_surprise")
            renpy.notify(CREDITS_CORNER_TEXT["hannah"])
        elif key == "aydin":
            sfx("win")
            renpy.show_screen("aydin_surprise")
            renpy.notify(CREDITS_CORNER_TEXT["aydin"])
        elif key == "ryan":
            sfx("win")
            renpy.show_screen("ryan_surprise")
            renpy.notify(CREDITS_CORNER_TEXT["ryan"])
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
            renpy.invoke_in_new_context(jumpscare, "eyes")


# A PASSENGER PEEKS IN  (type their name on the main menu)

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
default idle_walk = False
default version_pokes = 0

init python:
    class _MENU_SECRET(object):
        logo = 0

    def logo_poke():
        _MENU_SECRET.logo += 1
        if _MENU_SECRET.logo >= 3:
            _MENU_SECRET.logo = 0
            store.logo_glitched = True
            sfx("static")
            renpy.notify(_("\"Man… This seems familiar…\""))
            secret_found("logo")
        renpy.restart_interaction()

    def train_poke():
        if store.train_gone:
            return
        store.train_gone = True
        store.train_trips += 1
        sfx("win")
        renpy.notify(_("\"Wow damn… So… Expensive cabin, huh?\""))
        secret_found("train")
        renpy.restart_interaction()

    def version_poke():
        store.version_pokes += 1
        if store.version_pokes == 5:
            renpy.notify(_("\"I'm… back at the start?\""))
            secret_found("version")
        renpy.restart_interaction()

    def idle_watch():
        if persistent.jumpscares and not store.idle_walk:
            store.idle_walk = True
            secret_found("idle")
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

transform idle_walker:
    xanchor 0.5
    yanchor 1.0
    ypos 1.12
    xpos -0.1
    alpha 0.0
    parallel:
        ease 2.0 alpha 0.55
    parallel:
        linear 26.0 xpos 1.1
    parallel:
        block:
            ease 0.6 yoffset -8
            ease 0.6 yoffset 0
            repeat


default persistent.golden_found = set()

define GOLDEN_IDS = ["c1", "c2", "c3", "c4", "c5", "c2b", "c3b", "c5b"]
define GOLDEN_COINS = 25

init python:
    def find_golden(gid):
        if gid in persistent.golden_found:
            return
        persistent.golden_found = set(persistent.golden_found) | set([gid])
        n = len(persistent.golden_found)
        sfx("win")
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
