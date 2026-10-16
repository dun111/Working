# ==============================================================================
# DEPARTURE AT 4:00  -  credits_styles.rpy
# The five looks the credits can have (Settings > Display > CREDITS STYLE, or
# the < > in the top-right corner of the credits):
#
#   GTA         the game's art drifting behind, roles and names rolling up
#   TICKETS     every member on a ticket card
#   FILM        old film credits: role on the left, name on the right
#   TERMINAL    the credits typed out in a console
#   DEPARTURES  the crew on a departure board, a page at a time
#
# Every name can be clicked for its surprise (credits_fx.rpy). The people and
# their roles come from CREW in screens.rpy.
# ==============================================================================

define CREDIT_STYLES = [
    ("gta",        _("GTA")),
    ("tickets",    _("TICKETS")),
    ("film",       _("FILM")),
    ("terminal",   _("TERMINAL")),
    ("departures", _("DEPARTURES")),
]

default persistent.credits_style = "gta"

init python:
    def credits_style_now():
        s = persistent.credits_style
        return s if s in dict(CREDIT_STYLES) else "gta"

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

    def credit_pairs():
        """Every (role, person) - one line each - for the board and the terminal."""
        out = []
        for roles, people in credit_roles():
            for r in roles:
                for c in people:
                    out.append((r, c))
        return out


# ------------------------------------------------------------------------------
# GTA
# ------------------------------------------------------------------------------

screen credits_gta():
    default cred_adj = ui.adjustment()
    add Solid("#000000")
    add ("credits_art_still" if persistent.reduce_motion else "credits_art")
    # dark enough to read over, darkest down the middle
    add Solid("#000000a8")
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)

    # ---- the roll ----
    viewport:
        xalign 0.5
        xsize 1600
        ysize config.screen_height
        yadjustment cred_adj
        mousewheel True
        draggable True

        vbox:
            xsize 1600
            spacing 0

            null height config.screen_height

            add "game_logo_cycle":
                xalign 0.5
                xsize 720
                ysize 440
                fit "contain"

            null height 180

            # psst: every name does something when you click it (credits_fx.rpy)
            for roles, people in credit_roles():
                for role in roles:
                    text role.upper():
                        xalign 0.5
                        size 26
                        color credit_accent()
                        font GFONT
                null height 8
                for c in people:
                    textbutton c["name"]:
                        xalign 0.5
                        padding (20, 0)
                        background None
                        action Function(credits_click, c["key"])
                        text_size 72
                        text_color "#f2ead8"
                        text_hover_color credit_accent()
                        text_font CREDIT_FONT
                        text_outlines [(0, "#00000099", 3, 4)]
                null height 90

            text _("SPECIAL CREDITS"):
                xalign 0.5
                size 26
                color credit_accent()
                font GFONT
            null height 8
            text _("larp music"):
                xalign 0.5
                size 72
                color "#f2ead8"
                font CREDIT_FONT
            null height 200

            text _("THANKS FOR PLAYING!"):
                xalign 0.5
                size 80
                color "#ffffff"
                font CREDIT_FONT
            null height 30
            text _("Version [config.version]   ·   Made with Ren'Py [renpy.version_only]"):
                xalign 0.5
                size 18
                color "#8888a0"
                font GFONT

            null height config.screen_height

    timer 0.03 repeat True action Function(credits_step, cred_adj)


# ------------------------------------------------------------------------------
# TICKETS  (the original credits)
# ------------------------------------------------------------------------------

# the little badge next to each name (what they did)
define CREW_BADGES = {"eric": "</>", "hannah": "✎", "aydin": "www", "ryan": "☕", "hanyu": "♥"}

# one ticket card in the credits: number stub, name, every role they took on
screen crew_card(ci, c):
    $ card_h = max(150, 96 + 34 * len(c["roles"]))
    hbox:
        frame:
            xsize 150
            ysize card_h
            background rbox(credit_accent(), 26)
            text ("%02d" % (ci + 1)):
                align (0.5, 0.5)
                size 54
                color "#0a0a0e"
                font GFONT

        # perforation dots
        vbox:
            xsize 24
            yalign 0.5
            spacing 10
            for _d in range(max(6, len(c["roles"]) + 3)):
                add rbox("#33334a", 4):
                    xalign 0.5
                    xsize 8
                    ysize 8

        vbox:
            yalign 0.5
            spacing 4
            xoffset 14
            hbox:
                spacing 18
                text c["name"]:
                    size 60
                    color "#f2ead8"
                    hover_color credit_accent()
                    font CREDIT_FONT
                    outlines [(0, "#00000080", 2, 3)]
                if c["key"] in CREW_BADGES:
                    frame:
                        yalign 0.6
                        padding (12, 4)
                        background rbox("#22222c", 10)
                        text CREW_BADGES[c["key"]]:
                            size 22
                            color "#8888a0"
                            hover_color "#e8e4dc"
                            font "DejaVuSans.ttf"
            null height 4
            for role in c["roles"]:
                hbox:
                    spacing 12
                    add rbox(credit_accent(), 2):
                        xysize (8, 8)
                        yalign 0.5
                    text role:
                        size 22
                        color "#e6a817"
                        font GFONT

# credits: cards slide in one after another, lean out when you point at them,
# and the logo floats
transform card_in(d):
    alpha 0.0
    xoffset 260
    pause d
    easein 0.6 alpha 1.0 xoffset 0

transform card_hover:
    on idle:
        ease 0.25 xoffset 0 zoom 1.0
    on hover:
        ease 0.25 xoffset -18 zoom 1.01



screen credits_tickets():
    default cred_adj = ui.adjustment()
    add Solid("#08080c")

    if persistent.menu_fx and not persistent.reduce_motion:
        for sy, sdur, sdelay, slen in MENU_STREAKS:
            add Solid("#ffffff10", xsize=slen, ysize=2):
                ypos sy
                at streak(sdur, sdelay)

    # ---- left title panel ----
    frame:
        xpos 80
        ypos 70
        xsize 560
        ysize 830
        padding (2, 2)
        background rbox("#ffffff1e", 40)
        at fade_slide_in(0.0, xoff=-50)

        frame:
            xfill True
            yfill True
            padding (40, 40)
            background rbox("#14141aee", 38)

            vbox:
                spacing 26
                xfill True

                text _("CREDITS"):
                    xalign 0.5
                    size 54
                    color "#ffffff"
                    font GFONT

                add rbox("#e0521f", 2):
                    xalign 0.5
                    xsize 160
                    ysize 6

                add "game_logo_cycle":
                    xsize 440
                    ysize 260
                    fit "contain"
                    xalign 0.5
                    at logo_float

                fixed:
                    xfill True
                    ysize 22
                    use menu_tagline

                null height 10

                text _("Version [config.version]"):
                    xalign 0.5
                    size 20
                    color "#e6a817"
                    font GFONT

                text _("Made with Ren'Py [renpy.version_only]"):
                    xalign 0.5
                    size 16
                    color "#8888a0"
                    font GFONT

    # ---- scrolling ticket cards ----
    viewport:
        xpos 720
        ypos 70
        xsize (config.screen_width - 800)
        ysize 830
        yadjustment cred_adj
        mousewheel True
        draggable True

        vbox:
            xsize (config.screen_width - 820)
            spacing 22

            null height 760

            for ci, c in enumerate(CREW):
                # psst: everyone's card does something when you click it (credits_fx.rpy)
                frame:
                    xfill True
                    padding (0, 0)
                    background None
                    at card_in(0.3 + ci * 0.15)
                    button:
                        xfill True
                        padding (0, 0)
                        background rbox("#14141a", 26)
                        hover_background rbox("#1d1820", 26)
                        action Function(credits_click, c["key"])
                        at card_hover
                        use crew_card(ci, c)

            frame:
                xfill True
                background rbox("#14141a", 26)
                padding (40, 34)
                vbox:
                    spacing 10
                    xalign 0.5
                    text _("SPECIAL CREDITS"):
                        xalign 0.5
                        size 20
                        color "#e6a817"
                        font GFONT
                    text _("larp music"):
                        xalign 0.5
                        size 44
                        color "#ffffff"
                        font GFONT

            text _("THANKS FOR PLAYING!"):
                xalign 0.5
                size 64
                italic True
                color "#8888a0"
                font GFONT

            null height 760

    timer 0.03 repeat True action Function(credits_step, cred_adj)


# ------------------------------------------------------------------------------
# FILM
# ------------------------------------------------------------------------------

transform film_flicker:
    alpha 0.05
    block:
        linear 0.08 alpha 0.09
        linear 0.11 alpha 0.04
        linear 0.07 alpha 0.07
        repeat

screen credits_film():
    default cred_adj = ui.adjustment()
    add Solid("#050505")
    add Transform("gui/grain.png", xysize=(config.screen_width, config.screen_height)):
        at (film_flicker if not persistent.reduce_motion else Transform(alpha=0.06))
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)

    viewport:
        xalign 0.5
        xsize 1700
        ysize config.screen_height
        yadjustment cred_adj
        mousewheel True
        draggable True
        vbox:
            xsize 1700
            null height config.screen_height
            text _("A BLACKBERRY STUDIOS GAME"):
                xalign 0.5
                size 26
                color "#9a9a9a"
                font GFONT
            null height 40
            add Transform("images/Game_Logo_Yellow.webp", matrixcolor=SaturationMatrix(0.0)):
                xalign 0.5
                xsize 640
                ysize 400
                fit "contain"
            null height 200
            for roles, people in credit_roles():
                hbox:
                    xalign 0.5
                    spacing 60
                    vbox:
                        xsize 800
                        spacing 6
                        for role in roles:
                            text role:
                                xalign 1.0
                                text_align 1.0
                                size 30
                                color "#a8a8a8"
                                font GFONT
                    vbox:
                        xsize 800
                        spacing 0
                        for c in people:
                            textbutton c["name"]:
                                padding (0, 0)
                                background None
                                action Function(credits_click, c["key"])
                                text_size 46
                                text_color "#ededed"
                                text_hover_color credit_accent()
                                text_font CREDIT_FONT
                null height 70
            null height 120
            hbox:
                xalign 0.5
                spacing 60
                text _("Special credits"):
                    xsize 800
                    text_align 1.0
                    size 30
                    color "#a8a8a8"
                    font GFONT
                text _("larp music"):
                    xsize 800
                    size 46
                    color "#ededed"
                    font CREDIT_FONT
            null height 260
            text _("THE END"):
                xalign 0.5
                size 90
                color "#ededed"
                font CREDIT_FONT
            null height config.screen_height

    timer 0.03 repeat True action Function(credits_step, cred_adj)


# ------------------------------------------------------------------------------
# TERMINAL
# ------------------------------------------------------------------------------

define TERM_KEEP = 22        # how many lines fit on the screen

init python:
    def term_lines():
        """(prompt, text, person or None) for every line the console prints."""
        lines = [("$", "./credits --all", None), ("", _("loading crew... ok"), None), ("", "", None)]
        for roles, people in credit_roles():
            for r in roles:
                lines.append(("", "[[ %s ]" % r.upper(), None))    # [[ = a plain "["
            for c in people:
                lines.append(("", "    > ", c))
            lines.append(("", "", None))
        lines += [("", _("[[ SPECIAL CREDITS ]"), None), ("", "    > larp music", None), ("", "", None),
                  ("", _("THANKS FOR PLAYING!"), None), ("$", "", None)]
        return lines

    def term_tick(n, total):
        # print the next line; after a pause at the end, start again
        return (n + 1) if n < total + 12 else 0

transform term_cursor:
    alpha 1.0
    pause 0.5
    alpha 0.0
    pause 0.5
    repeat

screen credits_terminal():
    default shown = 0
    $ lines = term_lines()
    # SetLocalVariable: this screen is "use"d by about, so it has its own scope
    timer 0.32 repeat True action SetLocalVariable("shown", term_tick(shown, len(lines)))

    add Solid("#0c0c0c")
    frame:
        align (0.5, 0.5)
        xysize (1700, 900)
        padding (0, 0)
        background rbox("#0c0c0c", 12)
        # the title bar
        add rbox("#2b2b2e", 12):
            xysize (1700, 46)
        add Solid("#2b2b2e"):
            ypos 32
            xysize (1700, 14)
        hbox:
            xpos 20
            ypos 15
            spacing 10
            for dot in ("#ff5f57", "#febc2e", "#28c840"):
                add rbox(dot, 8):
                    xysize (16, 16)
        text "credits":
            xalign 0.5
            ypos 12
            size 18
            color "#9a9aa0"
            font "DejaVuSans.ttf"
        vbox:
            xpos 40
            ypos 70
            spacing 4
            $ first = max(0, min(shown, len(lines)) - TERM_KEEP)
            for prompt, line, who in lines[first:min(shown, len(lines))]:
                hbox:
                    spacing 12
                    if prompt:
                        text prompt:
                            size 24
                            color "#28c840"
                            font "DejaVuSans.ttf"
                    text line:
                        size 24
                        color ("#e6a817" if line.startswith("[") else "#d8d8d8")
                        font "DejaVuSans.ttf"
                    if who:
                        textbutton who["name"]:
                            padding (0, 0)
                            background None
                            action Function(credits_click, who["key"])
                            text_size 24
                            text_color "#ffffff"
                            text_hover_color "#28c840"
                            text_font "DejaVuSans.ttf"
            text "_":
                size 24
                color "#d8d8d8"
                font "DejaVuSans.ttf"
                at term_cursor


# ------------------------------------------------------------------------------
# DEPARTURES
# ------------------------------------------------------------------------------

define BOARD_ROWS = 8        # rows on one page of the board
define BOARD_PAGE = 6.0      # seconds a page stays up

init python:
    def board_pages():
        rows = credit_pairs() + [(_("Special credits"), {"key": None, "name": "larp music"})]
        return [rows[i:i + BOARD_ROWS] for i in range(0, len(rows), BOARD_ROWS)]

    def credit_platform(c):
        keys = [m["key"] for m in CREW]
        return str(keys.index(c["key"]) + 1) if c["key"] in keys else "-"

screen credits_departures():
    default page = 0
    $ pages = board_pages()
    timer BOARD_PAGE repeat True action SetLocalVariable("page", (page + 1) % len(pages))

    add "images/1st_carriage_Visualnovel_Background.webp":
        fit "cover"
        xysize (config.screen_width, config.screen_height)
        matrixcolor theme_matrix()
    add Solid("#000000c0")

    frame:
        align (0.5, 0.5)
        xsize 1900
        padding (50, 36)
        background rbox("#0a0a0ef0", 24)
        vbox:
            spacing 0
            hbox:
                xfill True
                text _("DEPARTURES"):
                    size 40
                    color "#e6a817"
                    font CREDIT_FONT
                text (_("CREW  ·  PAGE %d / %d") % (page + 1, len(pages))):
                    xalign 1.0
                    yalign 0.5
                    size 22
                    color "#55556a"
                    font CREDIT_FONT
            null height 14
            hbox:
                text _("TIME"):
                    min_width 170
                    size 16
                    color "#44445a"
                    font GFONT
                text _("NAME"):
                    min_width 420
                    size 16
                    color "#44445a"
                    font GFONT
                text _("ROLE"):
                    min_width 860
                    size 16
                    color "#44445a"
                    font GFONT
                text _("PLATFORM"):
                    min_width 180
                    size 16
                    color "#44445a"
                    font GFONT
                text _("STATUS"):
                    size 16
                    color "#44445a"
                    font GFONT
            null height 8
            add Solid("#2a2a35"):
                xysize (1800, 2)
            for i, (role, c) in enumerate(pages[page % len(pages)]):
                hbox:
                    ysize 74
                    fixed:
                        xysize (170, 74)
                        text "4:00":
                            yalign 0.5
                            size 30
                            color "#ffd76a"
                            font CREDIT_FONT
                            at board_flip(("t", page, i), i * 0.08)
                    fixed:
                        xysize (420, 74)
                        textbutton c["name"].upper():
                            yalign 0.5
                            padding (0, 0)
                            background None
                            action (Function(credits_click, c["key"]) if c["key"] else None)
                            text_size 34
                            text_color "#f2ead8"
                            text_hover_color credit_accent()
                            text_font CREDIT_FONT
                            at board_flip(("n", page, i), 0.04 + i * 0.08)
                    fixed:
                        xysize (860, 74)
                        text role.upper():
                            yalign 0.5
                            size 22
                            color "#cfcac0"
                            font GFONT
                            at board_flip(("r", page, i), 0.08 + i * 0.08)
                    fixed:
                        xysize (180, 74)
                        text credit_platform(c):
                            yalign 0.5
                            size 30
                            color "#e8e4dc"
                            font CREDIT_FONT
                    text (_("BOARDING") if i == 0 else _("ON TIME")):
                        yalign 0.5
                        size 22
                        color ("#e0521f" if i == 0 else "#6dffa5")
                        font CREDIT_FONT
                add Solid("#ffffff0d"):
                    xysize (1800, 1)
