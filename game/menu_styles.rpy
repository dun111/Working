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
    ("centered",  _("CENTERED"),  _("THEME PACK: the logo and the menu down the middle.")),
]

# the styles drawn by the screens in this file
define MENU_EXTRA = ("minimal", "panel", "cinema", "ticket")

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
