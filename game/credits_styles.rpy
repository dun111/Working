# ==============================================================================
# DEPARTURE AT 4:00  -  credits_styles.rpy
# The four looks the credits can have (Settings > Display > CREDITS STYLE, or
# the < > in the top-right corner of the credits):
#
#   SCROLL      the game's art drifting behind, roles and names rolling up
#   TICKETS     every member on a ticket card
#   FILM        old film credits: role on the left, name on the right
#   SPOTLIGHT   a black stage: the camera drifts over every carriage and
#               everyone on the train under a spotlight, one name at a time
#
# Every name can be clicked for its surprise (credits_fx.rpy). The people and
# their roles come from CREW in screens.rpy.
# ==============================================================================

define CREDIT_STYLES = [
    ("scroll",     _("SCROLL")),
    ("tickets",    _("TICKETS")),
    ("film",       _("FILM")),
    ("spotlight",  _("SPOTLIGHT")),
]

default persistent.credits_style = "scroll"

init python:
    def credits_style_now():
        s = persistent.credits_style
        return s if s in dict(CREDIT_STYLES) else "scroll"

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
        """Every (role, person) - one line each."""
        out = []
        for roles, people in credit_roles():
            for r in roles:
                for c in people:
                    out.append((r, c))
        return out


# ------------------------------------------------------------------------------
# SCROLL
# ------------------------------------------------------------------------------

screen credits_scroll():
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
# SPOTLIGHT
# A black stage with one spotlight. The camera drifts and zooms over a picture
# (a carriage, the train, or one of the passengers) for SPOT_TIME seconds, then
# the light moves on to the next, while the crew's roles and names fade in
# beside it. Light textures: gui/spotlight.png, gui/spot_hole.png, gui/spot_cone.png
# ------------------------------------------------------------------------------

define SPOT_TIME = 7.0          # seconds on each picture
define SPOT_X = 0.36            # where the light falls (fraction of the screen)
define SPOT_Y = 0.52
define SPOT_RX = 0.85           # the light's half-width and half-height (x screen height)
define SPOT_RY = 1.25

# (picture, "person" or "place"). People stand in the light; places are seen
# through it while the camera moves across them.
define SPOT_SLIDES = [
    ("images/Carriage_1_With_CharacterS.webp", "place"),
    ("images/louis_neutral.png", "person"),
    ("images/dorothy_normal.png", "person"),
    ("images/fedora.png", "person"),
    ("images/Train_BP.webp", "place"),
    ("eduard neutral", "person"),
    ("shunyu neutral", "person"),
    ("images/Kimmy_Idle.png", "person"),
    ("himmel neutral", "person"),
    ("images/bg_carriage_5.webp", "place"),
    ("sebastian neutral", "person"),
    ("misha neutral", "person"),
    ("agatha neutral", "person"),
    ("ichora neutral", "person"),
    ("images/PT2_Carriage_1_With_CharacterS.webp", "place"),
    ("pattison neutral", "person"),
    ("alexander neutral", "person"),
    ("images/dorothy_sad.png", "person"),
    ("conductor_monster neutral", "person"),
]

init python:
    def spot_slide(i):
        img, kind = SPOT_SLIDES[i % len(SPOT_SLIDES)]
        sw, sh = config.screen_width, config.screen_height
        if kind == "person":
            return Transform(img, fit="contain", ysize=int(sh * 0.92))
        return Transform(img, fit="cover", xysize=(int(sw * 1.3), int(sh * 1.3)))

    def spot_credit(i):
        """The crew block shown with picture i (the logo comes first)."""
        blocks = credit_roles() + [([_("Special credits")], [{"key": None, "name": "larp music"}])]
        if i == 0:
            return None
        return blocks[(i - 1) % len(blocks)]

    # each picture gets its own camera move, so it never feels repeated
    SPOT_MOVES = [
        (1.00, 1.18, -60, 60, 30, -20),
        (1.15, 1.02, 70, -50, -20, 20),
        (1.05, 1.25, 0, 0, 60, -40),
        (1.22, 1.05, -80, 40, -30, 10),
    ]

    def spot_move(i):
        return SPOT_MOVES[i % len(SPOT_MOVES)]

# the camera: fade up, drift and zoom, fade down
transform spot_cam(z0, z1, x0, x1, y0, y1, key):
    alpha 0.0
    zoom z0
    xoffset x0
    yoffset y0
    parallel:
        ease 1.0 alpha 1.0
        pause (SPOT_TIME - 2.0)
        ease 1.0 alpha 0.0
    parallel:
        linear SPOT_TIME zoom z1 xoffset x1 yoffset y1

# the light itself sways a little, like someone is holding it
transform spot_sway:
    xoffset 0
    yoffset 0
    block:
        ease 3.1 xoffset 26 yoffset -10
        ease 2.7 xoffset -18 yoffset 8
        ease 3.4 xoffset 8 yoffset 14
        ease 2.9 xoffset 0 yoffset 0
        repeat

transform spot_text_in(key):
    alpha 0.0
    xoffset 30
    pause 1.2
    easein 0.8 alpha 1.0 xoffset 0
    pause (SPOT_TIME - 3.0)
    easeout 0.8 alpha 0.0

transform spot_flicker:
    alpha 0.9
    block:
        linear 0.12 alpha 1.0
        linear 0.18 alpha 0.92
        linear 0.10 alpha 0.98
        repeat

screen credits_spotlight():
    default slide = 0
    # SetLocalVariable: this screen is "use"d by about, so it has its own scope
    timer SPOT_TIME repeat True action SetLocalVariable("slide", slide + 1)
    $ sw, sh = config.screen_width, config.screen_height
    $ z0, z1, x0, x1, y0, y1 = spot_move(slide)
    $ kind = SPOT_SLIDES[slide % len(SPOT_SLIDES)][1]

    add Solid("#000000")

    # ---- what's under the light, with the camera moving over it
    fixed:
        at (spot_sway if not persistent.reduce_motion else Transform())
        # "index k": a new picture is a new displayable, so its camera move
        # starts from the beginning instead of carrying on from the last one
        for k index k in [slide]:
            add spot_slide(k):
                xcenter SPOT_X
                yanchor (1.0 if kind == "person" else 0.5)
                ypos (1.04 if kind == "person" else SPOT_Y)
                at spot_cam(z0, (z1 if not persistent.reduce_motion else z0), x0, (x1 if not persistent.reduce_motion else x0), y0, (y1 if not persistent.reduce_motion else y0), k)

        # the dark all around the light: a tall oval of light, black beyond
        add "gui/spot_hole.png":
            xysize (int(sh * SPOT_RX * 2), int(sh * SPOT_RY * 2))
            xcenter SPOT_X
            ycenter SPOT_Y
        # black past every edge too, so nothing peeks out while the light sways
        add Solid("#000000"):
            pos (-100, -100)
            xysize (max(0, int(sw * SPOT_X - sh * SPOT_RX) + 102), sh + 200)
        add Solid("#000000"):
            pos (int(sw * SPOT_X + sh * SPOT_RX) - 2, -100)
            xysize (max(0, sw - int(sw * SPOT_X + sh * SPOT_RX) + 102), sh + 200)
        add Solid("#000000"):
            pos (-100, -100)
            xysize (sw + 200, max(0, int(sh * SPOT_Y - sh * SPOT_RY) + 102))
        add Solid("#000000"):
            pos (-100, sh - 2)
            xysize (sw + 200, 102)

        # warm light on the floor of the stage, and the beam from above
        add Transform("gui/spotlight.png", alpha=0.10, xysize=(int(sh * 1.1), int(sh * 1.1))):
            xcenter SPOT_X
            ycenter SPOT_Y
        add Transform("gui/spot_cone.png", xysize=(int(sh * 1.0), int(sh * 1.25))):
            xcenter SPOT_X
            yanchor 1.0
            ypos (SPOT_Y + 0.2)
            at spot_flicker

    # dust drifting through the beam
    if not persistent.reduce_motion:
        for ex, esz, edur, edelay, esway in MENU_EMBERS[:14]:
            add Solid("#fff4dc88"):
                xpos (SPOT_X - 0.12 + ex * 0.24)
                xsize max(2, esz - 2)
                ysize max(2, esz - 2)
                at ember(edur * 1.4, edelay, esway // 2)

    # ---- the credit beside the light
    $ block = spot_credit(slide)
    for k index k in [slide]:
      vbox:
        xpos 0.62
        yalign 0.5
        xsize int(sw * 0.33)
        spacing 6
        at spot_text_in(k)
        if block is None:
            add Transform("images/Game_Logo_Yellow.webp", fit="contain", xysize=(620, 400))
            null height 10
            text _("A BLACKBERRY STUDIOS GAME"):
                size 22
                color "#8a8a8a"
                font GFONT
        else:
            $ roles, people = block
            for role in roles:
                text role.upper():
                    size 22
                    color credit_accent()
                    font GFONT
            null height 10
            for c in people:
                textbutton c["name"]:
                    padding (0, 0)
                    background None
                    action (Function(credits_click, c["key"]) if c.get("key") else None)
                    text_size 86
                    text_color "#f2ead8"
                    text_hover_color credit_accent()
                    text_font CREDIT_FONT
