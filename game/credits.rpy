define CREDIT_FONT = "gui/Telegraphem.otf"

init python:
    def _esc(t):
        return t.replace("[", "[[").replace("{", "{{")

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
    (["label carriage_6:", "    scene black", "    $ renpy.notify(\"Carriage 6\"", "    u \"Not me. Him.\""],
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
        renpy.restart_interaction()

    def debug_tick():
        if store.dbg_result is not None:
            return
        store.dbg_t -= 0.1
        if store.dbg_t <= 0:
            store.dbg_t = 0
            store.dbg_result = "lose"
        renpy.restart_interaction()

screen mg_debug():
    use mg_scene(_("DEBUG"), _("Click the broken line."), "black", skippable=False, reward=False):
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




# The music credits follow the radio's own song list.
init 1 python:
    CREDIT_MUSIC = [(SONGS[k][1], SONGS[k][2]) for k in SONG_ORDER if k in SONGS]

init python:
    def credit_people():
        return [m[1] for m in MANIFEST] + ["The Passenger", "The Gentleman", "The Conductor"]

    def credit_sections():
        # (heading, [(line, small note)], whether the lines can be clicked)
        places = []
        for t in MAP_TITLES.values():
            line = "%s - %s" % (t[0], t[1])
            if line not in places:
                places.append(line)
        places += ["CARRIAGE 6"]
        return [
            (_("The passengers"), [(n, "") for n in credit_people()], True),
            (_("The carriages"), [(n, "") for n in places], False),
            (_("Endings"), [("Wrong Guess", "Ending 1"), ("Partial Truth", "Ending 2"), ("The True Line", "Ending 3")], False),
            (_("Clues"), [(c[1], "") for c in CLUE_LIST], False),
            (_("Minigames"), [(g[1], "") for g in MINIGAME_LIST], False),
            (_("The 4:00 Casino"), [(g[1], "") for g in CASINO_GAMES], False),
            (_("Achievements"), [(x["title"], "") for x in ACHIEVEMENTS], False),
            (_("Gamepasses"), [(g[1], "") for g in shown_passes()], False),
            (_("Radio stations"), [(n, RADIO_FREQ.get(k, "")) for k, n in RADIO_STATIONS], False),
            (_("Music"), CREDIT_MUSIC, False),
            (_("Fonts"), [("Graduate", ""), ("Telegraphem", ""), ("Reggae One", ""), ("DejaVu Sans", "")], False),
            (_("Made with"), [("Ren'Py", renpy.version_only)], False),
            (_("Special thanks"), [("Mr Kromo", "")], False),
            (_("Special credits"), [("larp music", "")], False),
        ]


define CRED_BG = "#08080c"
define CRED_PANEL = "#121218"
define CRED_ACCENT = "#e0521f"
define CRED_GOLD = "#e6a817"
define CRED_TEXT = "#f2ead8"
define CRED_MUTED = "#8888a0"

# Behind the credits: a faint, blurred first-class carriage.
image cred_backdrop = Fixed(
    Solid(CRED_BG),
    Transform("images/bg_first_class.webp", fit="cover", xysize=(config.screen_width, config.screen_height), blur=28, alpha=0.2),
    Solid("#08080c55"))

# ---------- SPOTLIGHT: one picture and one credit at a time ----------

define SPOT_TIME = 6.0

define SPOT_SLIDES = [
    # Pictures follow the story: each carriage's art next to the people you meet there.
    "images/bg_carriage_1_passengers.webp",
    "louis neutral",
    "dorothy neutral",
    "images/bg_first_class_clear.webp",
    "fedora neutral",
    "images/train_blueprint.webp",
    "images/bg_bar.webp",
    "eduard neutral",
    "images/bg_bar_cart.webp",
    "shunyu neutral",
    "images/shunyu_jackpot.webp",
    "images/bg_sleeper.webp",
    "kimmy neutral",
    "himmel neutral",
    "images/bg_sleeper_cart.webp",
    "images/bg_cabin_kimmy.webp",
    "sebastian neutral",
    "misha neutral",
    "images/bg_cabin_misha.webp",
    "images/cg_agatha_gloves.webp",
    "agatha neutral",
    "ichora neutral",
    "images/bg_staff_cart.webp",
    "images/bg_mail_cart.webp",
    "pattison neutral",
    "alexander neutral",
    "images/bg_mail_room.webp",
    "images/bg_mail_room_part2.webp",
    "images/bg_carriage_1_passengers_part2.webp",
    "dorothy sad",
    "images/bg_bar_cart_part2_crowd.webp",
    "images/clue_wrong_tile.webp",
    "images/clue_drink.webp",
    "images/bg_sleeper_cart_part2.webp",
    "images/clue_hidden_tile.webp",
    "images/clue_alibi.webp",
    "images/bg_first_class.webp",
    "images/key.webp",
    "images/bg_carriage_6.webp",
    "shunyu_monster neutral",
    "himmel_monster neutral",
    "conductor_monster neutral",
    "images/bg_carriage_1_passengers.webp",
    "images/logo_studio_full.webp",
]

init python:
    _SPOT_PICS = []

    def spot_pictures():
        # Built once: drops any character whose sprite isn't there, so no slide is ever empty.
        if not _SPOT_PICS:
            for img in SPOT_SLIDES:
                if img.startswith("images/"):
                    if renpy.loadable(img):
                        _SPOT_PICS.append((img, False))
                elif renpy.render(renpy.displayable(img), 1920, 1200, 0, 0).get_size() != (0, 0):
                    _SPOT_PICS.append((img, True))
        return _SPOT_PICS

    def spot_picture(i):
        pics = spot_pictures()
        img, person = pics[(i - 1) % len(pics)]
        if person:
            return Transform(img, fit="contain", xysize=(860, int(config.screen_height * 0.9))), True
        # Pictures are cropped to their art (the maps have see-through bands) and framed.
        return Transform(autocrop_image(img), fit="contain", xysize=(800, 560)), False

    def spot_blocks():
        blocks = []
        for heading, lines, click in credit_sections():
            chunks = [lines[k:k + 4] for k in range(0, len(lines), 4)]
            for n, chunk in enumerate(chunks):
                blocks.append({"heading": heading, "part": n + 1, "parts": len(chunks), "lines": chunk, "click": click})
        return blocks

    def spot_credit(i):
        if i == 0:
            return None
        blocks = spot_blocks()
        return blocks[(i - 1) % len(blocks)]

transform spot_show(dur):
    alpha 0.0
    ease 0.7 alpha 1.0
    pause max(0.1, dur - 1.4)
    ease 0.7 alpha 0.0

transform spot_rise(dur):
    yoffset 24
    easein 0.9 yoffset 0
    pause max(0.1, dur - 0.9)

transform spot_progress(dur):
    xzoom 0.0
    linear dur xzoom 1.0

screen credits_spotlight():
    default slide = 0
    $ block = spot_credit(slide)

    for k index k in [slide]:
        timer SPOT_TIME action SetLocalVariable("slide", slide + 1)

    add "cred_backdrop"

    if block is None:
        for k index k in [slide]:
            vbox:
                align (0.5, 0.48)
                spacing 22
                at spot_show(SPOT_TIME)
                add Transform("images/logo_game_yellow.webp", fit="contain", xysize=(760, 460)):
                    xalign 0.5
                add Solid(CRED_ACCENT, xsize=120, ysize=3):
                    xalign 0.5
                text _("A BLACKBERRY STUDIOS GAME"):
                    xalign 0.5
                    size 22
                    color CRED_MUTED
                    font GFONT
    else:
        $ pic, person = spot_picture(slide)
        $ longest = max(len(ln) for ln, _sub in block["lines"])
        $ nsz = 76 if longest <= 12 else max(34, int(76 * 12 / longest))
        for k index k in [slide]:
            fixed:
                at spot_show(SPOT_TIME)

                if person:
                    add Transform(_glow(CRED_ACCENT, 820, 820, 2.2), alpha=0.35):
                        xcenter 0.3
                        ycenter 0.55
                    add pic:
                        xcenter 0.3
                        yalign 1.0
                else:
                    frame:
                        xcenter 0.3
                        yalign 0.5
                        padding (8, 8)
                        background rbox(CRED_GOLD, 16)
                        at spot_rise(SPOT_TIME)
                        frame:
                            padding (0, 0)
                            background Solid("#0a0a0e")
                            add pic

                vbox:
                    xpos 0.6
                    yalign 0.5
                    xmaximum int(config.screen_width * 0.36)
                    spacing 12
                    at spot_rise(SPOT_TIME)
                    hbox:
                        spacing 18
                        text _esc(block["heading"].upper()):
                            yalign 1.0
                            size 24
                            color CRED_GOLD
                            font GFONT
                        if block["parts"] > 1:
                            text ("%d / %d" % (block["part"], block["parts"])):
                                yalign 1.0
                                size 18
                                color CRED_MUTED
                                font GFONT
                    add Solid(CRED_ACCENT, xsize=80, ysize=3)
                    null height 10
                    for ln, sub in block["lines"]:
                        vbox:
                            spacing 0
                            textbutton _esc(ln):
                                padding (0, 0)
                                background None
                                text_size nsz
                                text_color CRED_TEXT
                                text_hover_color (CRED_ACCENT if block["click"] else CRED_TEXT)
                                text_font CREDIT_FONT
                                action (Function(credits_click, ln) if block["click"] else None)
                            if sub:
                                text _esc(sub):
                                    size 20
                                    color CRED_GOLD
                                    font GFONT

            # How long until the next credit.
            add Solid(CRED_ACCENT):
                xpos 0
                ypos (config.screen_height - 4)
                xsize config.screen_width
                ysize 4
                at spot_progress(SPOT_TIME)
