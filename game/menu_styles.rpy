# ==============================================================================
# DEPARTURE AT 4:00  -  menu_styles.rpy
# Extra main menu layouts (Settings > Display > MAIN MENU STYLE). Each one is
# a screen called mm_<id> and gets the same list of options:
#   rows = [(label, action, primary), ...]   (primary = the highlighted one)
# The carriage behind, the key and the secrets stay the same in every style.
# ==============================================================================

# (id, name, what it looks like). The order the setting steps through them.
define MENU_STYLES = [
    ("new",       _("BOARD"),     _("The cinematic menu: the logo, the train and the departure board down the left.")),
    ("classic",   _("CLASSIC"),   _("The rounded sidebar.")),
    ("minimal",   _("MINIMAL"),   _("Just the logo and a clean list, in one column on the left.")),
    ("panel",     _("PANEL"),     _("A dark glass panel down the right side.")),
    ("cinema",    _("CINEMA"),    _("Black bars top and bottom, the logo big in the middle, the options along the bottom.")),
    ("ticket",    _("TICKET"),    _("The menu printed on a train ticket.")),
    ("neon",      _("NEON"),      _("A glowing neon sign in the dark, one tube flickering.")),
    ("poster",    _("POSTER"),    _("An old travel poster, sun rays behind the train.")),
    ("window",    _("WINDOW"),    _("The night rushing past a carriage window, the menu on a brass plate.")),
    ("centered",  _("CENTERED"),  _("THEME PACK: the logo and the menu down the middle.")),
]

# the styles drawn by the screens in this file
define MENU_EXTRA = ("minimal", "panel", "cinema", "ticket", "neon", "poster", "window")

init python:
    def menu_styles_usable():
        return [m for m in MENU_STYLES if m[0] not in THEME_MENUS or has_pass("themes")]

    def menu_style_step(d):
        ids = [m[0] for m in menu_styles_usable()]
        cur = menu_style_now()
        k = ids.index(cur) if cur in ids else 0
        persistent.menu_style = ids[(k + d) % len(ids)]
        renpy.restart_interaction()

    def menu_style_info():
        for sid, name, desc in MENU_STYLES:
            if sid == menu_style_now():
                return name, desc
        return MENU_STYLES[0][1], MENU_STYLES[0][2]

    def menu_hides_key():
        """The PANEL style needs the right side of the screen."""
        return menu_style_now() == "panel"

transform mm_lift:
    on idle:
        ease 0.15 yoffset 0
    on hover:
        ease 0.15 yoffset -4

transform mm_in(d=0.0):
    alpha 0.0
    yoffset 16
    pause d
    easein 0.35 alpha 1.0 yoffset 0

# the logo (psst: click it three times), any size
screen mm_logo(w):
    button:
        xysize (w, int(w * 808 / 1239.0))
        padding (0, 0)
        background None
        action Function(logo_poke)
        if logo_glitched:
            add Transform("images/Game_Logo_Purple.webp", fit="contain", xysize=(w, int(w * 808 / 1239.0))) at logo_glitch
        else:
            add "game_logo_rumble":
                xysize (w, int(w * 808 / 1239.0))
                fit "contain"

# what the option you're pointing at does
screen mm_help(col="#e6a817", dim="#55556a", size=16, xa=0.0, w=900, font=None):
    text (GetTooltip() or _("Point at an option to see what it does.")):
        xalign xa
        xmaximum w
        text_align xa
        size size
        color (col if GetTooltip() else dim)
        font (font or GFONT)

# the secret way into the casino, in every style
screen mm_departures(col="#55556a", size=16):
    textbutton _("DEPARTURES"):
        padding (0, 4)
        background None
        text_size size
        text_color col
        text_hover_color "#e6a817"
        text_font CREDIT_FONT
        action Function(casino_open)


# ------------------------------------------------------------------------------
# MINIMAL
# ------------------------------------------------------------------------------

screen mm_minimal(rows):
    add Solid("#00000050")
    # one column on the left: logo, tagline, options and help all share its centre
    vbox:
        xpos 120
        yalign 0.5
        xsize 560
        spacing 0
        hbox:
            xalign 0.5
            at mm_in(0.1)
            use mm_logo(520)
        fixed:
            xsize 560
            ysize 34
            use menu_tagline(0.5, 18)
        null height 40
        for i, (lab, act, primary) in enumerate(rows):
            textbutton lab:
                xalign 0.5
                padding (0, 4)
                background None
                action act
                tooltip MENU_HELP.get(lab, "")
                text_size (46 if primary else 32)
                text_color ("#e0521f" if primary else "#cfcac0")
                text_hover_color ("#ff7a3d" if primary else "#ffffff")
                text_font GFONT
                at mm_in(0.25 + i * 0.04), mm_lift
        null height 18
        use mm_help(xa=0.5, w=560)
        null height 6
        hbox:
            xalign 0.5
            spacing 30
            use mm_departures
            text "v[config.version]":
                yalign 0.5
                size 14
                color "#44445a"
                font GFONT


# ------------------------------------------------------------------------------
# PANEL
# ------------------------------------------------------------------------------

screen mm_panel(rows):
    frame:
        xalign 1.0
        yfill True
        xsize 640
        padding (56, 120, 56, 50)
        background Solid("#08080ce6")
        at mm_in(0.0)
        add Solid("#e0521f"):
            xpos -60
            xysize (4, config.screen_height)
        vbox:
            xfill True
            yalign 0.5
            spacing 8
            hbox:
                xalign 0.5
                use mm_logo(380)
            fixed:
                xfill True
                ysize 30
                use menu_tagline(0.5, 18)
            null height 18
            for i, (lab, act, primary) in enumerate(rows):
                button:
                    xfill True
                    ysize (64 if primary else 50)
                    padding (26, 0)
                    background rbox(("#e0521f" if primary else "#16161c"), 16)
                    hover_background rbox(("#ff7a3d" if primary else "#26262f"), 16)
                    action act
                    tooltip MENU_HELP.get(lab, "")
                    at mm_in(0.2 + i * 0.04), mm_lift
                    text lab:
                        yalign 0.5
                        size (30 if primary else 22)
                        color ("#0a0a0e" if primary else "#e8e4dc")
                        hover_color ("#0a0a0e" if primary else "#ffd76a")
                        font GFONT
            null height 12
            use mm_help(w=520)
            null height 6
            hbox:
                xfill True
                use mm_departures
                text "v[config.version]":
                    xalign 1.0
                    yalign 0.5
                    size 14
                    color "#44445a"
                    font GFONT


# ------------------------------------------------------------------------------
# CINEMA
# ------------------------------------------------------------------------------

define CINEMA_BAR = 170

screen mm_cinema(rows):
    add Solid("#00000060")
    # the letterbox
    add Solid("#000000"):
        xysize (config.screen_width, CINEMA_BAR)
        at mm_in(0.0)
    add Solid("#000000"):
        yalign 1.0
        xysize (config.screen_width, CINEMA_BAR)
        at mm_in(0.0)

    vbox:
        xalign 0.5
        yalign 0.42
        at mm_in(0.15)
        use mm_logo(760)
        fixed:
            xsize 760
            ysize 34
            use menu_tagline(0.5, 22)

    fixed:
        xalign 0.5
        yalign 1.0
        yoffset -(CINEMA_BAR + 16)
        xysize (config.screen_width, 30)
        use mm_help(xa=0.5, w=config.screen_width - 200)

    hbox:
        xalign 0.5
        yalign 1.0
        yoffset -(CINEMA_BAR // 2 - 24)
        spacing 54
        for i, (lab, act, primary) in enumerate(rows):
            textbutton lab:
                padding (0, 4)
                background None
                action act
                tooltip MENU_HELP.get(lab, "")
                text_size (30 if primary else 24)
                text_color ("#e0521f" if primary else "#cfcac0")
                text_hover_color ("#ff7a3d" if primary else "#ffffff")
                text_font GFONT
                at mm_in(0.3 + i * 0.04), mm_lift
        use mm_departures(size=20)


# ------------------------------------------------------------------------------
# TICKET
# ------------------------------------------------------------------------------

define TICKET_W = 1180
define TICKET_H = 700

screen mm_ticket(rows):
    add Solid("#00000060")
    fixed:
        xpos 140
        yalign 0.5
        xysize (TICKET_W, TICKET_H)
        at mm_in(0.1)
        # the paper, with a shadow
        add rbox("#00000088", 30):
            pos (14, 18)
            xysize (TICKET_W, TICKET_H)
        add rbox("#efe3c4", 30):
            xysize (TICKET_W, TICKET_H)
        # the stub, torn along the dots
        for k in range(26):
            add Solid("#9a8a66"):
                pos (300, 26 + k * 26)
                xysize (3, 12)
        text "4:00":
            xcenter 150
            ycenter TICKET_H // 2
            size 110
            color "#b0201a"
            font CREDIT_FONT
            at Transform(rotate=-90)
        text "GREKHOV EXPRESS":
            xcenter 150
            ypos TICKET_H - 60
            size 16
            color "#7a6a4a"
            font GFONT
        # the ticket itself
        vbox:
            xpos 350
            ypos 40
            xsize TICKET_W - 400
            spacing 6
            hbox:
                xfill True
                use mm_logo(330)
                vbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 4
                    text _("DEPARTS"):
                        xalign 1.0
                        size 16
                        color "#7a6a4a"
                        font GFONT
                    text "4:00":
                        xalign 1.0
                        size 64
                        color "#2a1f10"
                        font CREDIT_FONT
            add Solid("#2a1f1033"):
                xysize (TICKET_W - 400, 2)
            null height 10
            text _("DESTINATION"):
                size 16
                color "#7a6a4a"
                font GFONT
            # two columns of destinations
            $ half = (len(rows) + 1) // 2
            hbox:
                spacing 60
                for col in (rows[:half], rows[half:]):
                    vbox:
                        xsize 360
                        spacing 8
                        for lab, act, primary in col:
                            textbutton lab:
                                padding (0, 4)
                                background None
                                action act
                                tooltip MENU_HELP.get(lab, "")
                                text_size (36 if primary else 28)
                                text_color ("#b0201a" if primary else "#2a1f10")
                                text_hover_color "#e0521f"
                                text_font GFONT
                                at mm_lift
            null height 10
            add Solid("#2a1f1033"):
                xysize (TICKET_W - 400, 2)
            null height 6
            hbox:
                xfill True
                use mm_help(col="#7a1f12", dim="#7a6a4a", size=16, w=TICKET_W - 600)
                hbox:
                    xalign 1.0
                    use mm_departures(col="#7a6a4a")


# ------------------------------------------------------------------------------
# NEON
# ------------------------------------------------------------------------------

define NEON_PINK = "#ff3df0"
define NEON_BLUE = "#3df2ff"

# a neon tube: lit, with the odd stutter
transform neon_hum:
    alpha 1.0
    block:
        pause 3.7
        linear 0.04 alpha 0.55
        linear 0.04 alpha 1.0
        pause 5.1
        linear 0.03 alpha 0.7
        linear 0.05 alpha 1.0
        repeat

# the one tube that's on its way out
transform neon_broken:
    alpha 1.0
    block:
        pause 1.6
        alpha 0.2
        pause 0.08
        alpha 1.0
        pause 0.12
        alpha 0.25
        pause 0.3
        alpha 1.0
        pause 2.4
        repeat

screen neon_logo(w):
    fixed:
        xysize (w, int(w * 808 / 1239.0))
        # the logo lit up pink (the sign's black inside hides the picture's own dark background)
        add Transform("images/Game_Logo_Yellow.webp", fit="contain", xysize=(w, int(w * 808 / 1239.0)),
                      matrixcolor=TintMatrix("#ffb0f4"))

screen mm_neon(rows):
    add Solid("#05030ad0")
    $ last = len(rows) - 1
    fixed:
        xpos 160
        yalign 0.5
        xysize (900, 960)
        # the sign's border: a glowing pink tube
        for blur_r, a in ((26, 0.7), (0, 1.0)):
            add Transform(rbox(NEON_PINK, 40), xysize=(900, 960), blur=blur_r, alpha=a)
            add Transform(rbox("#000000", 37), xysize=(892, 952), pos=(4, 4))
        vbox:
            xalign 0.5
            ypos 40
            spacing 2
            hbox:
                xalign 0.5
                at neon_hum
                button:
                    padding (0, 0)
                    background None
                    action Function(logo_poke)
                    use neon_logo(420)
            fixed:
                xsize 800
                ysize 34
                use menu_tagline(0.5, 18)
            null height 14
            for i, (lab, act, primary) in enumerate(rows):
                textbutton lab:
                    xalign 0.5
                    padding (20, 0)
                    background None
                    action act
                    tooltip MENU_HELP.get(lab, "")
                    text_size (46 if primary else 30)
                    text_color (NEON_PINK if primary else NEON_BLUE)
                    text_hover_color "#ffffff"
                    text_font GFONT
                    text_outlines [(10, (NEON_PINK if primary else NEON_BLUE) + "30", 0, 0), (4, (NEON_PINK if primary else NEON_BLUE) + "70", 0, 0)]
                    at mm_in(0.25 + i * 0.05), (neon_broken if i == last else neon_hum)
            null height 16
            use mm_help(col=NEON_BLUE, dim="#4a4a6a", xa=0.5, w=820)
            hbox:
                xalign 0.5
                use mm_departures(col="#4a4a6a")


# ------------------------------------------------------------------------------
# POSTER
# ------------------------------------------------------------------------------

define POSTER_W = 780
define POSTER_H = 1000
define POSTER_ART_H = 380       # the sun-and-train picture at the top
define POSTER_INK = "#2a1d14"
define POSTER_RED = "#b0301e"

# the sun rays behind the train turn very slowly
transform poster_turn:
    rotate 0
    linear 240.0 rotate 360
    repeat

init python:
    def poster_rays(r):
        """Sun rays round a point: a fan of long thin wedges."""
        kids = []
        for k in range(18):
            kids.append(At(Solid(("#e8b35a" if k % 2 == 0 else "#f3d08a"), xysize=(int(r * 0.36), r)),
                           Transform(anchor=(0.5, 1.0), pos=(r, r), rotate=k * 20, transform_anchor=True)))
        return Fixed(*kids, xysize=(2 * r, 2 * r))

screen mm_poster(rows):
    add Solid("#00000060")
    $ half = (len(rows) + 1) // 2
    fixed:
        xpos 200
        yalign 0.5
        xysize (POSTER_W, POSTER_H)
        at mm_in(0.1)
        # the paper, with a shadow and a printed border
        add rbox("#00000080", 10):
            pos (16, 20)
            xysize (POSTER_W, POSTER_H)
        add rbox("#f1e3c4", 10):
            xysize (POSTER_W, POSTER_H)
        add rbox(POSTER_INK, 6):
            pos (22, 22)
            xysize (POSTER_W - 44, POSTER_H - 44)
        add rbox("#f1e3c4", 4):
            pos (28, 28)
            xysize (POSTER_W - 56, POSTER_H - 56)

        # the sun, its rays, and the train in front of it
        fixed:
            pos (40, 40)
            xysize (POSTER_W - 80, POSTER_ART_H)
            add rbox("#e8b35a", 4):
                xysize (POSTER_W - 80, POSTER_ART_H)
            add poster_rays(360):
                xcenter (POSTER_W - 80) // 2
                ycenter POSTER_ART_H
                at (poster_turn if not persistent.reduce_motion else Transform())
            # cover the rays that spill past the picture
            add Solid("#f1e3c4"):
                ypos POSTER_ART_H
                xysize (POSTER_W - 80, 400)
            add Transform("images/Train_BP.webp", fit="contain", xysize=(POSTER_W - 160, 280), matrixcolor=TintMatrix(POSTER_INK)):
                xalign 0.5
                yalign 1.0
        add Solid("#f1e3c4"):
            pos (0, 0)
            xysize (40, POSTER_H)
        add Solid("#f1e3c4"):
            pos (POSTER_W - 40, 0)
            xysize (40, POSTER_H)
        add Solid("#f1e3c4"):
            pos (0, 0)
            xysize (POSTER_W, 40)

        # title and the destinations
        vbox:
            xpos 60
            ypos POSTER_ART_H + 52
            xsize POSTER_W - 120
            spacing 4
            hbox:
                xalign 0.5
                use mm_logo(250)
            fixed:
                xsize POSTER_W - 120
                ysize 30
                use menu_tagline(0.5, 16)
            null height 10
            hbox:
                xalign 0.5
                spacing 50
                for col in (rows[:half], rows[half:]):
                    vbox:
                        spacing 4
                        for lab, act, primary in col:
                            textbutton lab:
                                padding (0, 2)
                                background None
                                action act
                                tooltip MENU_HELP.get(lab, "")
                                text_size (30 if primary else 23)
                                text_color (POSTER_RED if primary else POSTER_INK)
                                text_hover_color POSTER_RED
                                text_font GFONT
                                at mm_lift
        # the band along the bottom
        frame:
            pos (28, POSTER_H - 92)
            xysize (POSTER_W - 56, 64)
            padding (24, 0)
            background Solid(POSTER_INK)
            use mm_help(col="#f3d08a", dim="#a89070", size=15, w=POSTER_W - 300)
            hbox:
                xalign 1.0
                yalign 0.5
                use mm_departures(col="#f3d08a", size=16)


# ------------------------------------------------------------------------------
# WINDOW
# ------------------------------------------------------------------------------

define WIN_W = 1240
define WIN_H = 600

# things outside the window rush past (near ones faster than far ones)
transform win_pass(speed, delay):
    xpos 1.05
    pause delay
    block:
        xpos 1.05
        linear speed xpos -0.15
        repeat

transform win_glass:
    alpha 0.08
    block:
        ease 4.0 alpha 0.14
        ease 4.0 alpha 0.08
        repeat

screen mm_window(rows):
    add Solid("#0a0604e8")
    vbox:
        xalign 0.42
        yalign 0.5
        spacing 26
        at mm_in(0.1)

        # the window: a wooden frame, the night outside
        fixed:
            xysize (WIN_W + 48, WIN_H + 48)
            add rbox("#3a2312", 36):
                xysize (WIN_W + 48, WIN_H + 48)
            add rbox("#5e3a1e", 32):
                pos (8, 8)
                xysize (WIN_W + 32, WIN_H + 32)
            viewport:
                pos (24, 24)
                xysize (WIN_W, WIN_H)
                fixed:
                    xysize (WIN_W, WIN_H)
                    # the sky, darker at the top
                    add Solid("#0b1024")
                    add Solid("#16203c"):
                        ypos WIN_H // 2
                        xysize (WIN_W, WIN_H // 2)
                    add Transform("gui/round/r256.png", xysize=(90, 90), matrixcolor=TintMatrix("#f4ecd0")):
                        pos (WIN_W - 240, 70)
                    # far hills, slow
                    if not persistent.reduce_motion:
                        for k in range(3):
                            add rbox("#0d1428", 60):
                                xysize (520, 200)
                                ypos WIN_H - 210
                                at win_pass(26.0, k * 8.7)
                        # town lights far away
                        for k in range(10):
                            add Solid("#ffcf70"):
                                xysize (4, 4)
                                ypos WIN_H - 170 + (k * 37) % 60
                                at win_pass(18.0, k * 1.9)
                        # telegraph poles, fast
                        for k in range(3):
                            add Solid("#05060c"):
                                xysize (16, WIN_H)
                                at win_pass(1.6, k * 0.53)
                    # the ground racing by
                    add Solid("#07080e"):
                        ypos WIN_H - 70
                        xysize (WIN_W, 70)
                    # a faint reflection on the glass
                    add Solid("#ffffff"):
                        xysize (WIN_W, WIN_H)
                        at win_glass
            # the frame's middle bar and the logo in the corner of the glass
            add Solid("#5e3a1e"):
                pos (24, WIN_H // 2 + 14)
                xysize (WIN_W, 20)
            hbox:
                pos (60, 50)
                use mm_logo(330)

        # the brass plate with the destinations
        frame:
            xalign 0.5
            xsize WIN_W + 48
            padding (34, 18)
            background rbox("#a9823c", 20)
            vbox:
                spacing 10
                hbox:
                    xalign 0.5
                    spacing 34
                    for i, (lab, act, primary) in enumerate(rows):
                        textbutton lab:
                            padding (0, 2)
                            background None
                            action act
                            tooltip MENU_HELP.get(lab, "")
                            text_size (30 if primary else 22)
                            text_color ("#3a1206" if primary else "#2a1a08")
                            text_hover_color "#fff4d0"
                            text_font GFONT
                            at mm_in(0.3 + i * 0.04), mm_lift
                hbox:
                    xfill True
                    use mm_help(col="#3a1206", dim="#5e4418", size=15, w=WIN_W - 200)
                    hbox:
                        xalign 1.0
                        use mm_departures(col="#5e4418", size=16)
