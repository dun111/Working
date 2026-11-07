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


define CREDIT_STYLES = [
    ("spotlight",  _("SPOTLIGHT")),
    ("tickets",    _("TICKETS")),
]


define CREDIT_MUSIC = [
    ("Grekhov Theme", "Departure at 4:00"),
    ("Carriage 1", "Departure at 4:00"),
    ("Let's All Do the Conga", "Colin Sheen"),
    ("Rendezvous (Instrumental)", "Carriages 2 and 3"),
    ("Part 2 Carriage 3", "Departure at 4:00"),
    ("Carriage 4", "Departure at 4:00"),
    ("Carriage 5", "Departure at 4:00"),
    ("Flower In A Hurricane", "Justice ft. Tame Impala, SZA, King Gizzard & the Lizard Wizard"),
]

init python:
    def credits_style_now():
        s = persistent.credits_style
        return s if s in dict(CREDIT_STYLES) else "spotlight"

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
        passengers = [m[1] for m in MANIFEST] + ["The Passenger", "The Gentleman", "The Conductor"]
        places = []
        for t in MAP_TITLES.values():
            line = "%s - %s" % (t[0], t[1])
            if line not in places:
                places.append(line)
        places += ["CARRIAGE 6"]
        return [
            (_("The passengers"), [(n, "") for n in passengers]),
            (_("The carriages"), [(n, "") for n in places]),
            (_("Endings"), [("Wrong Guess", "Ending 1"), ("Partial Truth", "Ending 2"), ("The True Line", "Ending 3")]),
            (_("Clues"), [(c[1], "") for c in CLUE_LIST]),
            (_("Minigames"), [(g[1], "") for g in MINIGAME_LIST]),
            (_("The 4:00 Casino"), [(g[1], "") for g in CASINO_GAMES]),
            (_("Achievements"), [(x["title"], "") for x in ACHIEVEMENTS]),
            (_("Gamepasses"), [(g[1], "") for g in shown_passes()]),
            (_("Radio stations"), [(n, RADIO_FREQ.get(k, "")) for k, n in RADIO_STATIONS]),
            (_("Music"), CREDIT_MUSIC),
            (_("Fonts"), [("Graduate", ""), ("Telegraphem", ""), ("Reggae One", ""), ("DejaVu Sans", "")]),
            (_("Made with"), [("Ren'Py", renpy.version_only)]),
            (_("Special thanks"), [("Mr Kromo", "")]),
        ]


define CREW_BADGES = {"eric": "</>", "hannah": "✎", "aydin": "www", "ryan": "☕"}

define CRED_BG = "#08080c"
define CRED_PANEL = "#121218"
define CRED_ACCENT = "#e0521f"
define CRED_GOLD = "#e6a817"
define CRED_TEXT = "#f2ead8"
define CRED_MUTED = "#8888a0"

init python:
    def credits_roll(adj, state):
        # Hold still for the first 3 seconds so the crew can be read, then roll.
        state["ticks"] += 1
        if state["ticks"] > 100:
            credits_step(adj)

transform cred_fade(d=0.0):
    alpha 0.0
    pause d
    ease 0.5 alpha 1.0


# ---------- TICKETS: a scrolling list of plain cards ----------

screen crew_card(c):
    button:
        xfill True
        padding (40, 28)
        background rbox(CRED_PANEL, 22)
        hover_background rbox("#191920", 22)
        action Function(credits_click, c["key"])
        vbox:
            spacing 14
            hbox:
                spacing 16
                text c["name"]:
                    size 56
                    color CRED_TEXT
                    hover_color CRED_ACCENT
                    font CREDIT_FONT
                if c["key"] in CREW_BADGES:
                    frame:
                        yalign 0.5
                        padding (10, 3)
                        background rbox("#22222c", 8)
                        text CREW_BADGES[c["key"]]:
                            size 18
                            color CRED_MUTED
                            font "DejaVuSans.ttf"
            add Solid(CRED_ACCENT, xsize=60, ysize=3)
            text "\u00a0\u00a0·   ".join(c["roles"]):
                size 20
                color CRED_GOLD
                font GFONT
                line_spacing 6

screen cred_section(heading, lines):
    frame:
        xfill True
        padding (40, 28)
        background rbox(CRED_PANEL, 22)
        vbox:
            spacing 10
            xfill True
            text heading.upper():
                xalign 0.5
                size 18
                color CRED_GOLD
                font GFONT
            null height 2
            for ln, sub in lines:
                text _esc((ln + "   ·   " + sub) if sub else ln):
                    xalign 0.5
                    text_align 0.5
                    size 26
                    color CRED_TEXT
                    font GFONT

define CRED_TOP = 70
define CRED_H = config.screen_height - 230

screen credits_tickets():
    default cred_adj = ui.adjustment()
    default cred_roll = {"ticks": 0}
    add Solid(CRED_BG)

    frame:
        xpos 80
        ypos CRED_TOP
        xsize 520
        ysize CRED_H
        padding (40, 48)
        background rbox(CRED_PANEL, 30)
        at cred_fade(0.0)
        vbox:
            xfill True
            spacing 22
            text _("CREDITS"):
                xalign 0.5
                size 48
                color "#ffffff"
                font GFONT
            add Solid(CRED_ACCENT, xsize=120, ysize=3):
                xalign 0.5
            null height 10
            add "game_logo_cycle":
                xsize 420
                ysize 250
                fit "contain"
                xalign 0.5
            null height 10
            text _("Version [config.version]"):
                xalign 0.5
                size 20
                color CRED_GOLD
                font GFONT
            text _("Made with Ren'Py [renpy.version_only]"):
                xalign 0.5
                size 16
                color CRED_MUTED
                font GFONT

    viewport:
        xpos 680
        ypos CRED_TOP
        xsize (config.screen_width - 760)
        ysize CRED_H
        yadjustment cred_adj
        mousewheel True
        draggable True
        at cred_fade(0.2)

        vbox:
            xsize (config.screen_width - 760)
            spacing 18

            text _("THE CREW"):
                size 18
                color CRED_GOLD
                font GFONT

            for c in CREW:
                use crew_card(c)

            null height 20

            for heading, lines in credit_sections():
                use cred_section(heading, lines)

            use cred_section(_("Special credits"), [("larp music", "")])

            null height 40
            text _("THANKS FOR PLAYING!"):
                xalign 0.5
                size 48
                color CRED_MUTED
                font GFONT
            null height CRED_H

    timer 0.03 repeat True action Function(credits_roll, cred_adj, cred_roll)


# ---------- SPOTLIGHT: one picture and one credit at a time ----------

define SPOT_TIME = 6.0

define SPOT_SLIDES = [
    "images/bg_carriage_1_passengers.webp",
    "louis neutral",
    "dorothy neutral",
    "fedora neutral",
    "images/train_blueprint.webp",
    "eduard neutral",
    "shunyu neutral",
    "kimmy neutral",
    "images/bg_mail_cart.webp",
    "himmel neutral",
    "sebastian neutral",
    "misha neutral",
    "agatha neutral",
    "ichora neutral",
    "images/bg_carriage_1_passengers_part2.webp",
    "pattison neutral",
    "alexander neutral",
    "dorothy sad",
    "images/bg_first_class_clear.webp",
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
        return Transform(img, fit="contain", xysize=(860, 600)), False

    def spot_blocks():
        blocks = list(credit_roles())
        for heading, lines in credit_sections():
            for k in range(0, len(lines), 4):
                blocks.append(([heading], [{"key": None, "name": ln + ("  ·  " + sub if sub else "")}
                                           for ln, sub in lines[k:k + 4]]))
        blocks.append(([_("Special credits")], [{"key": None, "name": "larp music"}]))
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

screen credits_spotlight():
    default slide = 0
    $ block = spot_credit(slide)

    for k index k in [slide]:
        timer SPOT_TIME action SetLocalVariable("slide", slide + 1)

    add Solid("#000000")

    if block is None:
        for k index k in [slide]:
            vbox:
                align (0.5, 0.48)
                spacing 24
                at spot_show(SPOT_TIME)
                add Transform("images/logo_game_yellow.webp", fit="contain", xysize=(760, 460)):
                    xalign 0.5
                text _("A BLACKBERRY STUDIOS GAME"):
                    xalign 0.5
                    size 22
                    color CRED_MUTED
                    font GFONT
    else:
        $ pic, person = spot_picture(slide)
        $ roles, people = block
        for k index k in [slide]:
            fixed:
                at spot_show(SPOT_TIME)

                if person:
                    add pic:
                        xcenter 0.3
                        yalign 1.0
                else:
                    add pic:
                        xcenter 0.3
                        yalign 0.5

                vbox:
                    xpos 0.6
                    yalign 0.5
                    xmaximum int(config.screen_width * 0.36)
                    spacing 12
                    for role in roles:
                        text _esc(role.upper()):
                            size 24
                            color CRED_ACCENT
                            font GFONT
                    add Solid(CRED_ACCENT, xsize=80, ysize=3)
                    null height 8
                    $ longest = max(len(c["name"]) for c in people)
                    $ nsz = 80 if longest <= 12 else max(34, int(80 * 12 / longest))
                    for c in people:
                        textbutton _esc(c["name"]):
                            padding (0, 0)
                            background None
                            text_size nsz
                            text_color CRED_TEXT
                            text_hover_color CRED_ACCENT
                            text_font CREDIT_FONT
                            action (Function(credits_click, c["key"]) if c.get("key") else None)
