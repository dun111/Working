# ==============================================================================
# DEPARTURE AT 4:00  -  cheats.rpy
# Testing tools. Press F9 in game or on the main menu.
#
# Always on when the game runs from the Ren'Py SDK (config.developer). In a
# built copy, type "debug" on the main menu to switch them on (or off).
#
#   JUMP       go to any chapter, with the story state set up for it
#   FLAGS      flip story flags, hand out clues
#   SCARES     fire any jumpscare
#   MINIGAMES  play any minigame, or make them all win themselves
#   UNLOCKS    achievements, endings, secrets, hotspot outlines
# ==============================================================================

default persistent.cheats_on = False
default persistent.cheat_autowin = False
default persistent.cheat_hotspots = False

init 1 python:
    # every minigame: (key, name, screen, reset function, where it is)
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
        """Play one minigame on its own (EXTRAS > ARCADE, or the cheat menu)."""
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

    # ----------------------------------------------------------------- chapters
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

    # (button, label to jump to, stage)  stage: how much of the story is done
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
        """Set up the story as if everything before CHEAT.stage had been played."""
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

    # ------------------------------------------------------------------ unlocks
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


# ------------------------------------------------------------------------------
# SCREENS
# ------------------------------------------------------------------------------

# F9 opens the menu (in game this rides along as an overlay screen)
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


# ------------------------------------------------------------------------------
# EXTRAS > ARCADE
# ------------------------------------------------------------------------------

screen arcade_list(w):
    # ERIC PASS: Eric's DEBUG game (credits_fx.rpy)
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
