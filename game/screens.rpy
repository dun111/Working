init offset = -1

# ==============================================================================
# FONTS & GLOBAL STYLES
# ==============================================================================

style default:
    font "gui/Graduate-Regular.ttf"

style button:
    padding (10, 6)

style button_text:
    font "gui/Graduate-Regular.ttf"
    size 90
    color "#8888a0"
    hover_color "#ffffff"
    selected_color "#ffd700"
    insensitive_color "#444455"

style slider:
    ysize 22
    left_bar Solid("#e6a817")
    right_bar Solid("#222233")
    thumb Solid("#ffffff", xsize=10, ysize=22)

style say_window is default
style say_label is default
style say_dialogue is default

image pill_mask = Frame("images/pill_mask.png", 30, 30, 30, 30)

init python:
    def C(name, tag=None, **kwargs):
        return Character(name, **kwargs)

init python:
    config.overlay_screens.append("quick_menu")

# ==============================================================================
# SHARED LAYOUT CONSTANTS
# ==============================================================================

define gui.sidebar_width = 450
define gui.sidebar_margin = 28
define gui.sidebar_padding = 35
define gui.sidebar_content_width = gui.sidebar_width - (gui.sidebar_padding * 2)


# ==============================================================================
# SHARED TRANSFORMS (ANIMATIONS)
# ==============================================================================

transform key_entrance_and_sway:
    xanchor 0.5
    yanchor 0.0
    alpha 0.0
    xoffset 30
    rotate 0
    pause 0.6
    ease 0.5 alpha 1.0 xoffset 0
    block:
        ease 1.4 rotate 10
        ease 1.4 rotate -10
        repeat

transform boot_logo_anim:
    xalign 0.5
    yalign 0.5
    alpha 0.0
    zoom 0.9
    ease 1.0 alpha 1.0 zoom 1.0
    pause 1.5
    ease 0.8 alpha 0.0

transform fade_slide_in(delay=0.0, xoff=-40, final_xoff=0):
    alpha 0.0
    xoffset xoff
    pause delay
    ease 0.5 alpha 1.0 xoffset final_xoff

transform fade_in(delay=0.0):
    alpha 0.0
    pause delay
    ease 0.6 alpha 1.0

transform credits_scroll(duration=18.0, travel=1400):
    yoffset travel
    linear duration yoffset -travel
    repeat

transform loading_pulse:
    alpha 0.4
    linear 0.6 alpha 1.0
    linear 0.6 alpha 0.4
    repeat

transform notify_anim:
    alpha 0.0 yoffset 20
    ease 0.25 alpha 1.0 yoffset 0
    pause 2.5
    ease 0.5 alpha 0.0

transform confirm_pop:
    alpha 0.0 zoom 0.9
    ease 0.3 alpha 1.0 zoom 1.0

transform train_shake:
    xoffset 0
    yoffset 0
    block:
        linear 0.06 xoffset -2 yoffset 2
        linear 0.06 xoffset 2 yoffset -2
        linear 0.06 xoffset -2 yoffset 1
        linear 0.06 xoffset 2 yoffset 2
        linear 0.06 xoffset -1 yoffset -2
        linear 0.06 xoffset -1 yoffset 0
        repeat 15
    pause 8.0
    repeat

transform button_hover_anim:
    zoom 1.0
    on hover:
        ease 0.15 zoom 1.04
    on idle:
        ease 0.15 zoom 1.0
    on selected_hover:
        ease 0.15 zoom 1.04
    on selected_idle:
        ease 0.15 zoom 1.0

transform blackberry_click_pulse:
    zoom 1.0
    ease 0.15 zoom 1.3
    ease 0.25 zoom 1.0

transform qm_shown:
    alpha 0.0
    ease 0.25 alpha 1.0

transform qm_hidden:
    alpha 1.0
    ease 0.25 alpha 0.0

transform speaker_focus(xalign=0.7):
    xanchor 0.5
    xalign xalign
    yalign 1.0
    yoffset 40
    zoom 1.0
    alpha 1.0
    linear 0.3 zoom 1.08 alpha 1.0

transform speaker_background(xalign=0.3):
    xanchor 0.5
    xalign xalign
    yalign 1.0
    yoffset 40
    zoom 1.0
    alpha 0.55
    linear 0.3 zoom 0.94 alpha 0.55
# ==============================================================================
# GLOBAL TRANSITIONS
# ==============================================================================

define config.enter_transition = Dissolve(0.25)
define config.exit_transition = Dissolve(0.2)
define config.intra_transition = Dissolve(0.2)
define config.window_show_transition = Dissolve(0.2)
define config.window_hide_transition = Dissolve(0.2)


# ==============================================================================
# MENU MUSIC (filtered/boosted theme while on menu screens)
# ==============================================================================

init python:
    import renpy.audio.filter as af

define audio.menu_theme = "gui/main_menu.mp3"

init python:
    def _menu_music_filter():
        boosted_echo = af.Sequence([
            af.Multiply(1.6),
            af.Comb(delay=0.3, multiplier=0.35, wet=True),
        ])
        renpy.music.set_audio_filter("music", boosted_echo, replace=True)
        renpy.music.play(audio.menu_theme, channel="music", fadein=1.5, loop=True)

    def _menu_music_stop():
        renpy.music.set_audio_filter("music", None)
        renpy.music.stop(channel="music", fadeout=1.0)


# ==============================================================================
# BLACKBERRY LOGO EASTER EGG
# ==============================================================================

default found_blackberry_secret = False

init python:
    def blackberry_secret_action():
        if not store.found_blackberry_secret:
            store.found_blackberry_secret = True
            renpy.notify("Ryan is black (berry)")
        else:
            renpy.notify("You already found the secret. Stop clicking it. Please.")

init python:
    import os
    import pygame

    def autocrop_image(path):
        cache_name = "autocrop_" + path.replace("/", "_").replace("\\", "_") + ".png"
        cache_path = os.path.join(config.gamedir, "cache", cache_name)

        if not os.path.exists(cache_path):
            source = renpy.loader.transfn(path)
            surf = pygame.image.load(source).convert_alpha()

            width, height = surf.get_size()
            min_x, min_y = width, height
            max_x, max_y = 0, 0
            found = False

            for x in range(width):
                for y in range(height):
                    if surf.get_at((x, y))[3] > 0:
                        found = True
                        if x < min_x: min_x = x
                        if x > max_x: max_x = x
                        if y < min_y: min_y = y
                        if y > max_y: max_y = y

            if found:
                rect = pygame.Rect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
                cropped = surf.subsurface(rect).copy()
            else:
                cropped = surf

            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            pygame.image.save(cropped, cache_path)

        return "cache/" + cache_name

# ==============================================================================
# CUSTOM USER PREFERENCES (persistent across sessions)
# ==============================================================================

default persistent.screen_shake_enabled = True
default persistent.dialogue_font_size = 28

transform no_shake:
    pass

init python:
    FONT_SIZE_STEPS = [22, 26, 30, 34]

    def cycle_font_size():
        idx = FONT_SIZE_STEPS.index(persistent.dialogue_font_size) if persistent.dialogue_font_size in FONT_SIZE_STEPS else 1
        persistent.dialogue_font_size = FONT_SIZE_STEPS[(idx + 1) % len(FONT_SIZE_STEPS)]


# ==============================================================================
# QUICK MENU AUTO-HIDE STATE
# ==============================================================================

default quick_menu_hover = False

init python:
    def _set_qm_hover(value):
        store.quick_menu_hover = value


# ==============================================================================
# ACHIEVEMENTS
# ==============================================================================

define ACHIEVEMENTS = [
    {
        "id": "first_departure",
        "title": _("First Departure"),
        "description": _("Reach the train station for the first time."),
        "hidden": False,
    },
    {
        "id": "collector",
        "title": _("Collector"),
        "description": _("Find all hidden collectibles."),
        "hidden": False,
        "stat_max": 10,
    },
    {
        "id": "secret_ending",
        "title": _("REDACTED"),
        "description": _("A secret achievement. Unlock it to reveal its name. Confidential."),
        "hidden": True,
    },
        {
        "id": "the_loop_begins",
        "title": _("Here Again?"),
        "description": _("The train reset. Louis remembers."),
        "hidden": False,
    },
    {
        "id": "eyes_in_the_dark",
        "title": _("???"),
        "description": _("Something was watching from beyond the sixth carriage."),
        "hidden": True,
    },
    {
        "id": "closer_to_the_truth",
        "title": _("Closer to the Truth"),
        "description": _("Investigated Shunyu's murder."),
        "hidden": False,
    },
]

init python:
    for _ach in ACHIEVEMENTS:
        if "stat_max" in _ach:
            achievement.register(_ach["id"], stat_max=_ach["stat_max"])
        else:
            achievement.register(_ach["id"])

screen achievements():
    tag menu

    $ back_action = ShowMenu("main_menu") if main_menu else Return()

    add Solid("#0a0a0e")

    text _("ACHIEVEMENTS"):
        xpos 80
        ypos 50
        size 40
        color "#ffffff"
        font "gui/Graduate-Regular.ttf"

    add Solid("#e0521f"):
        xpos 80
        ypos 105
        xsize 160
        ysize 3

    vbox:
        xpos 80
        ypos 140
        xsize (config.screen_width - 160)
        spacing 14

        for ach in ACHIEVEMENTS:
            $ unlocked = achievement.has(ach["id"])
            $ locked_and_hidden = ach.get("hidden", False) and not unlocked

            frame:
                xfill True
                background Solid("#101014")
                padding (20, 16)

                hbox:
                    spacing 20

                    $ icon_path = "images/achievements/%s.png" % ach["id"]

                    if renpy.loadable(icon_path):
                        add icon_path:
                            xsize 64
                            ysize 64
                            alpha (1.0 if unlocked else 0.35)
                    else:
                        add Solid("#e6a817" if unlocked else "#33334a"):
                            xsize 64
                            ysize 64

                    vbox:
                        spacing 4

                        if unlocked:
                            text ("???" if locked_and_hidden else ach["title"]):
                                size 24
                                color "#ffd700"
                                font "gui/Graduate-Regular.ttf"
                        else:
                            text ("???" if locked_and_hidden else ach["title"]):
                                size 24
                                color "#8888a0"
                                font "gui/Graduate-Regular.ttf"

                        if unlocked:
                            text ("A hidden achievement." if locked_and_hidden else ach["description"]):
                                size 18
                                color "#ffffff"
                                font "gui/Graduate-Regular.ttf"
                        else:
                            text ("A hidden achievement." if locked_and_hidden else ach["description"]):
                                size 18
                                color "#666677"
                                font "gui/Graduate-Regular.ttf"

                        if "stat_max" in ach and not unlocked and not ach.get("hidden", False):
                            $ progress = achievement.get_progress(ach["id"])

                            text "[progress]/[ach['stat_max']]":
                                size 14
                                color "#8888a0"

    frame:
        xpos 80
        yalign 0.95
        xsize 160
        ysize 50
        padding (2, 2)
        background Solid("#33334a")

        button:
            xfill True
            yfill True
            background Solid("#101014")
            hover_background Solid("#2a2a35")
            action back_action

            text "BACK":
                align (0.5, 0.5)
                size 24
                color "#8888a0"
                hover_color "#ffd700"
                font "gui/Graduate-Regular.ttf"
# ==============================================================================
# BACKGROUNDS
# ==============================================================================

image main_menu_bg_rotation:
    Solid("#1a1a24")
    pause 4.0
    Solid("#241a20") with dissolve
    pause 4.0
    Solid("#1a2420") with dissolve
    pause 4.0
    repeat

image game_logo_cycle:
    "images/Game_Logo_Red.webp" with dissolve
    pause 3.0
    "images/Game_Logo_Yellow.webp" with dissolve
    pause 10.0
    repeat


# ==============================================================================
# LOADING SCREEN
# ==============================================================================

screen loading():
    zorder 200
    add Solid("#0a0a0e")
    frame:
        xalign 0.5
        yalign 0.5
        background None
        vbox:
            xalign 0.5
            spacing 16
            text _("LOADING"):
                xalign 0.5
                size 36
                color "#e0521f"
                font "gui/Telegraphem.otf"
                at loading_pulse
            add Solid("#e0521f"):
                xsize 240
                ysize 3
                xalign 0.5


# ==============================================================================
# BOOT / SPLASHSCREEN
# ==============================================================================

label splashscreen:
    scene black
    with Pause(0.3)

    if renpy.loadable("images/Blackberry_Studios_Full.webp"):
        show expression "images/Blackberry_Studios_Full.webp" as boot_logo at boot_logo_anim
        pause 3.3
        hide boot_logo
    else:
        show text "{size=50}BLACKBERRY STUDIOS{/size}" at boot_logo_anim
        pause 3.3
        hide text

    scene black
    with Pause(0.3)

    return


# ==============================================================================
# MAIN MENU SCREEN
# ==============================================================================

screen main_menu():
    tag menu
    on "show" action Function(_menu_music_filter)
    on "hide" action Function(_menu_music_stop)

    fixed:
        at (train_shake if persistent.screen_shake_enabled else no_shake)

        # Key
        fixed:
            xpos 0.94
            ypos -0.30
            xsize 560
            ysize 770
            xanchor 0.5
            yanchor 0.0
            at key_entrance_and_sway

            if renpy.loadable("images/Key.webp"):
                add "images/Key.webp":
                    xsize 560
                    ysize 770
                    fit "contain"
                    align (0.5, 0.5)
                    xoffset -21.6
                    yoffset -24.3
            else:
                text "KEY":
                    size 160

        # Hook — smaller, sits deeper in the hole, slides/fades in with the key
        fixed:
            xpos 0.94
            ypos -0.30
            xsize 560
            ysize 770
            xanchor 0.5
            yanchor 0.0
            at fade_slide_in(delay=0.6, xoff=40)

            add "images/Key_Hook.webp":
                xsize 200
                ysize 110
                fit "contain"
                align (0.5, 0.5)
                xoffset -25.9
                yoffset 64.4
                matrixcolor TintMatrix("#ae5400")

        # Floating glass sidebar card
        fixed:
            xpos gui.sidebar_margin
            ypos gui.sidebar_margin
            xsize gui.sidebar_width
            ysize (config.screen_height - gui.sidebar_margin * 2)

            add Solid("#000000aa"):
                xsize gui.sidebar_width
                ysize (config.screen_height - gui.sidebar_margin * 2)
                xoffset 6
                yoffset 12
                blur 22

            frame:
                xfill True
                yfill True
                background Solid("#14141aa8")
                padding (0, 0)
                clipping True

                add Solid("#ffffff22"):
                    xsize gui.sidebar_width
                    ysize 2
                    yalign 0.0

                vbox:
                    xpos gui.sidebar_padding
                    ypos 40
                    xsize gui.sidebar_content_width
                    yfill True
                    spacing 50

                    add "game_logo_cycle":
                        xsize gui.sidebar_content_width
                        ysize 260
                        fit "contain"
                        at fade_slide_in(0.1)

                    frame:
                        xsize gui.sidebar_content_width
                        ysize 60
                        background Solid("#e0521f")
                        padding (2, 2)
                        at fade_slide_in(0.3)

                        button:
                            xfill True
                            yfill True
                            background Solid("#00000000")
                            hover_background Solid("#00000033")
                            action Start()
                            text "PLAY":
                                align (0.5, 0.5)
                                size 32
                                color "#0a0a0e"
                                hover_color "#ffffff"
                                font "gui/Graduate-Regular.ttf"
                                at button_hover_anim

                    viewport:
                        xsize gui.sidebar_content_width
                        yfill True
                        mousewheel True
                        vbox:
                            xsize gui.sidebar_content_width
                            spacing 14

                            button:
                                xsize gui.sidebar_content_width
                                ysize 46
                                background Solid("#00000000")
                                hover_background Solid("#ffffff11")
                                action ShowMenu("preferences")
                                at button_hover_anim
                                text "SETTINGS" align (0.0, 0.5) xoffset 4 size 24 color "#8888a0" hover_color "#ffd700" font "gui/Graduate-Regular.ttf"

                            button:
                                xsize gui.sidebar_content_width
                                ysize 46
                                background Solid("#00000000")
                                hover_background Solid("#ffffff11")
                                action ShowMenu("about")
                                at button_hover_anim
                                text "CREDITS" align (0.0, 0.5) xoffset 4 size 24 color "#8888a0" hover_color "#ffd700" font "gui/Graduate-Regular.ttf"

                            button:
                                xsize gui.sidebar_content_width
                                ysize 46
                                background Solid("#00000000")
                                hover_background Solid("#ffffff11")
                                action ShowMenu("achievements")
                                at button_hover_anim
                                text "ACHIEVEMENTS" align (0.0, 0.5) xoffset 4 size 24 color "#8888a0" hover_color "#ffd700" font "gui/Graduate-Regular.ttf"

                            if renpy.variant("pc"):
                                button:
                                    xsize gui.sidebar_content_width
                                    ysize 46
                                    background Solid("#00000000")
                                    hover_background Solid("#ffffff11")
                                    action Quit(confirm=True)
                                    at button_hover_anim
                                    text "QUIT" align (0.0, 0.5) xoffset 4 size 24 color "#8888a0" hover_color "#ffd700" font "gui/Graduate-Regular.ttf"

                frame:
                    xpos 0
                    yalign 1.0
                    yoffset 60
                    xysize (380, 380)
                    background None
                    padding (0, 0)
                    clipping True
                    at fade_slide_in(0.7, xoff=-60)
                    add "images/Train_BP.webp":
                        xysize (380, 380)
                        fit "contain"
                        align (0.0, 1.0)
                        xoffset -30
                        rotate -12

    if renpy.loadable("images/Blackberry_Studios.webp"):
        $ blackberry_cropped = autocrop_image("images/Blackberry_Studios.webp")
        button:
            xalign 1.0
            yalign 1.0
            xoffset 30
            yoffset -30
            xsize 180
            ysize 90
            background None
            action Function(blackberry_secret_action)
            at fade_slide_in(0.9, xoff=70, final_xoff=30)

            add blackberry_cropped:
                xsize 180
                ysize 90
                fit "contain"
                rotate -18
                at button_hover_anim
    else:
        text "Blackberry":
            size 40
            xalign 1.0
            yalign 1.0
            xoffset -20
            yoffset -20
            at fade_slide_in(0.9, xoff=60, final_xoff=-20)

# ==============================================================================
# DIALOGUE (SAY) SCREEN
# ==============================================================================

screen say(who, what):
    window:
        id "window"
        xalign 0.5
        yalign 1.0
        xsize config.screen_width
        ysize 310                      # was 260 — now includes the quick menu strip (260 + 50)
        background Solid("#0a0a0eee")

        add Solid("#e0521f"):
            xsize config.screen_width
            ysize 2
            yalign 0.0

        if who:
            add AlphaMask(
                Solid("#8a4a22", xsize=260, ysize=44),
                Transform("pill_mask", size=(260, 44))
            ):
                xpos 40
                ypos 44

            text who:
                id "who"
                xpos 170
                xanchor 0.5
                ypos 66
                yanchor 0.5
                size (persistent.dialogue_font_size - 2)
                bold True
                color "#f2e6d8"
                font "gui/Graduate-Regular.ttf"

        text what:
            id "what"
            xpos 40
            xsize 0.85
            ypos 112
            size persistent.dialogue_font_size
            color "#e8e4dc"
            font "gui/Graduate-Regular.ttf"
            line_spacing 10

# ==============================================================================
# INPUT / CHOICE SCREENS
# ==============================================================================

screen input(prompt):
    window:
        xalign 0.5
        yalign 0.5
        xsize 900
        vbox:
            spacing 15
            text prompt
            input:
                id "input"

screen choice(items):
    vbox:
        xalign 0.5
        yalign 1.0
        yoffset -340
        spacing 18

        for i in items:
            frame:
                xalign 0.5
                xsize 760
                ysize 82
                padding (3, 3)
                background Solid("#33334a")
                at button_hover_anim

                button:
                    xfill True
                    yfill True
                    background Solid("#14141aee")
                    hover_background Solid("#2a2a35")
                    action i.action

                    text i.caption:
                        align (0.5, 0.5)
                        size 32
                        color "#c9c9d8"
                        hover_color "#ffd700"
                        selected_color "#ffd700"
                        font "gui/Graduate-Regular.ttf"


# ==============================================================================
# QUICK MENU (auto-hides unless hovering the bottom edge)
# ==============================================================================

default quick_menu = True

screen quick_menu():
    zorder 100
    if quick_menu:

        mousearea:
            area (0, config.screen_height - 50, config.screen_width, 50)
            hovered Function(_set_qm_hover, True)
            unhovered Function(_set_qm_hover, False)

        hbox:
            xpos 40
            yalign 1.0
            yoffset -14
            spacing 8
            at (qm_shown if quick_menu_hover else qm_hidden)
            for label, act in [
                (_("Home"), MainMenu(confirm=True)),
                (_("Back"), Rollback()),
                (_("History"), ShowMenu("history")),
                (_("Skip"), Skip()),
                (_("Auto"), Preference("auto-forward", "toggle")),
                (_("Save"), ShowMenu("save")),
                (_("Q.Save"), QuickSave()),
                (_("Q.Load"), QuickLoad()),
                (_("Prefs"), ShowMenu("preferences")),
            ]:
                fixed:
                    xsize 96
                    ysize 34
                    button:
                        xfill True
                        yfill True
                        background AlphaMask(
                            Solid("#00000000", xsize=96, ysize=34),
                            Transform("pill_mask", size=(96, 34))
                        )
                        hover_background AlphaMask(
                            Solid("#ffffff18", xsize=96, ysize=34),
                            Transform("pill_mask", size=(96, 34))
                        )
                        action act
                        at button_hover_anim
                        text label:
                            align (0.5, 0.5)
                            size 17
                            color "#8888a0"
                            hover_color "#ffd700"
                            selected_color "#ffd700"
                            font "gui/Graduate-Regular.ttf"

# ==============================================================================
# IN-GAME NAVIGATION (used by Ren'Py's default escape menu, if triggered)
# ==============================================================================

screen navigation():
    vbox:
        xpos 0.05
        yalign 0.5
        spacing 12
        if main_menu:
            textbutton _("Play"):
                action Start()
        else:
            textbutton _("History"):
                action ShowMenu("history")
            textbutton _("Save"):
                action ShowMenu("save")
        textbutton _("Load"):
            action ShowMenu("load")
        textbutton _("Preferences"):
            action ShowMenu("preferences")
        if _in_replay:
            textbutton _("End Replay"):
                action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _("Main Menu"):
                action MainMenu()
        textbutton _("About"):
            action ShowMenu("about")
        if renpy.variant("pc") or renpy.variant("web"):
            textbutton _("Help"):
                action ShowMenu("help")
        if renpy.variant("pc"):
            textbutton _("Quit"):
                action Quit(confirm=not main_menu)

# ==============================================================================
# SHARED "MENU" CHROME (title bar + back button + dim overlay)
# ==============================================================================

screen game_menu_header(title):
    text title:
        size 40
        color "#ffffff"
        font "gui/Graduate-Regular.ttf"
        at fade_in(0.1)
    add Solid("#e0521f"):
        xsize 160
        ysize 3

screen game_menu_back(back_action):
    frame:
        xpos 80
        yalign 0.95
        xsize 160
        ysize 50
        padding (2, 2)
        background Solid("#33334a")
        at fade_in(0.3)
        button:
            xfill True
            yfill True
            background Solid("#101014")
            hover_background Solid("#2a2a35")
            action back_action
            text "BACK" align (0.5, 0.5) size 24 color "#8888a0" hover_color "#ffd700" font "gui/Graduate-Regular.ttf"

screen game_menu_overlay():
    add Solid("#0a0a0eee"):
        xsize config.screen_width
        ysize config.screen_height


# ==============================================================================
# PREFERENCES
# ==============================================================================

screen pref_toggle(label, action, selected=False):
    frame:
        xsize 200
        ysize 44
        padding (2, 2)
        background Solid("#e6a817" if selected else "#33334a")
        button:
            xfill True
            yfill True
            background Solid("#1a1a24" if selected else "#101014")
            hover_background Solid("#2a2a35")
            action action
            text label:
                align (0.5, 0.5)
                size 18
                color ("#ffffff" if selected else "#8888a0")
                hover_color "#ffd700"
                font "gui/Graduate-Regular.ttf"

screen preferences():
    tag menu

    $ back_action = ShowMenu("main_menu") if main_menu else Return()

    add Solid("#0a0a0e")

    text _("PREFERENCES"):
        xpos 80
        ypos 50
        size 40
        color "#ffffff"
        font "gui/Graduate-Regular.ttf"

    add Solid("#e0521f"):
        xpos 80
        ypos 105
        xsize 160
        ysize 3

    hbox:
        xpos 80
        ypos 140
        spacing 60

        # ---------------- LEFT COLUMN ----------------
        vbox:
            spacing 20
            xsize 700

            frame:
                background Solid("#101014")
                padding (24, 20)
                xfill True

                vbox:
                    spacing 10

                    text _("DISPLAY"):
                        size 18
                        color "#e6a817"
                        font "gui/Graduate-Regular.ttf"

                    hbox:
                        spacing 12

                        use pref_toggle(
                            _("WINDOW"),
                            Preference("display", "window"),
                            selected=(_preferences.fullscreen == False)
                        )

                        use pref_toggle(
                            _("FULLSCREEN"),
                            Preference("display", "fullscreen"),
                            selected=(_preferences.fullscreen == True)
                        )

            frame:
                background Solid("#101014")
                padding (24, 20)
                xfill True

                vbox:
                    spacing 10

                    text _("SKIP"):
                        size 18
                        color "#e6a817"
                        font "gui/Graduate-Regular.ttf"

                    hbox:
                        spacing 12

                        use pref_toggle(
                            _("SEEN TEXT"),
                            Preference("skip", "seen"),
                            selected=(_preferences.skip_unseen == False)
                        )

                        use pref_toggle(
                            _("ALL TEXT"),
                            Preference("skip", "all"),
                            selected=(_preferences.skip_unseen == True)
                        )

            frame:
                background Solid("#101014")
                padding (24, 20)
                xfill True

                vbox:
                    spacing 10

                    text _("AFTER CHOICES"):
                        size 18
                        color "#e6a817"
                        font "gui/Graduate-Regular.ttf"

                    hbox:
                        spacing 12

                        use pref_toggle(
                            _("STOP SKIPPING"),
                            Preference("after choices", "stop"),
                            selected=(_preferences.skip_after_choices == False)
                        )

                        use pref_toggle(
                            _("KEEP SKIPPING"),
                            Preference("after choices", "skip"),
                            selected=(_preferences.skip_after_choices == True)
                        )

            frame:
                background Solid("#101014")
                padding (24, 20)
                xfill True

                vbox:
                    spacing 10

                    text _("MORE OPTIONS"):
                        size 18
                        color "#e6a817"
                        font "gui/Graduate-Regular.ttf"

                    text _("SCREEN SHAKE / RUMBLE"):
                        size 14
                        color "#8888a0"
                        font "gui/Graduate-Regular.ttf"

                    hbox:
                        spacing 12

                        use pref_toggle(
                            _("ON"),
                            SetField(persistent, "screen_shake_enabled", True),
                            selected=persistent.screen_shake_enabled
                        )

                        use pref_toggle(
                            _("OFF"),
                            SetField(persistent, "screen_shake_enabled", False),
                            selected=not persistent.screen_shake_enabled
                        )

                    text _("DIALOGUE FONT SIZE"):
                        size 14
                        color "#8888a0"
                        font "gui/Graduate-Regular.ttf"

                    textbutton "[persistent.dialogue_font_size]px":
                        action Function(cycle_font_size)
                        text_size 18

        # ---------------- RIGHT COLUMN ----------------
        vbox:
            spacing 20
            xsize 700

            frame:
                background Solid("#101014")
                padding (24, 20)
                xfill True

                vbox:
                    spacing 12

                    text _("TEXT SPEED"):
                        size 18
                        color "#e6a817"
                        font "gui/Graduate-Regular.ttf"

                    bar:
                        style "slider"
                        value Preference("text speed")
                        xsize 380

                    text _("AUTO-FORWARD SPEED"):
                        size 18
                        color "#e6a817"
                        font "gui/Graduate-Regular.ttf"

                    bar:
                        style "slider"
                        value Preference("auto-forward time")
                        xsize 380

                    text _("MUSIC VOLUME"):
                        size 18
                        color "#e6a817"
                        font "gui/Graduate-Regular.ttf"

                    bar:
                        style "slider"
                        value Preference("music volume")
                        xsize 380

                    text _("SOUND VOLUME"):
                        size 18
                        color "#e6a817"
                        font "gui/Graduate-Regular.ttf"

                    bar:
                        style "slider"
                        value Preference("sound volume")
                        xsize 380

                    text _("VOICE VOLUME"):
                        size 18
                        color "#e6a817"
                        font "gui/Graduate-Regular.ttf"

                    bar:
                        style "slider"
                        value Preference("voice volume")
                        xsize 380

                    use pref_toggle(
                        _("MUTE ALL AUDIO"),
                        Preference("all mute", "toggle"),
                        selected=False
                    )

    frame:
        xpos 80
        yalign 0.95
        xsize 160
        ysize 50
        padding (2, 2)
        background Solid("#33334a")

        button:
            xfill True
            yfill True
            background Solid("#101014")
            hover_background Solid("#2a2a35")
            action back_action

            text "BACK":
                align (0.5, 0.5)
                size 24
                color "#8888a0"
                hover_color "#ffd700"
                font "gui/Graduate-Regular.ttf"


# ==============================================================================
# SAVE / LOAD
# ==============================================================================

screen save():
    tag menu
    use file_slots(_("Save"))

screen load():
    tag menu
    use file_slots(_("Load"))

screen file_slots(title):
    default page = 1

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    use game_menu_overlay

    frame:
        xsize config.screen_width
        ysize config.screen_height
        background None
        padding (80, 60)
        at fade_slide_in(0.0, xoff=-30)

        vbox:
            xsize (config.screen_width - 160)
            spacing 20

            use game_menu_header(title)

            viewport:
                xsize (config.screen_width - 160)
                ysize (config.screen_height - 260)
                mousewheel True
                draggable True
                scrollbars "vertical"

                vbox:
                    spacing 10
                    for slot in range(1, 9):
                        $ slot_index = slot + (page - 1) * 8
                        button:
                            xsize 700
                            action FileAction(slot_index)
                            $ slot_name = FileSlotName(slot_index)
                            if slot_name:
                                text slot_name
                            else:
                                text _("Empty Slot")
                    hbox:
                        spacing 10
                        textbutton _("<"):
                            action SetScreenVariable("page", max(1, page - 1))
                        textbutton _("Page [page]"):
                            action NullAction()
                        textbutton _(">"):
                            action SetScreenVariable("page", page + 1)

    use game_menu_back(back_action)


# ==============================================================================
# HISTORY
# ==============================================================================

screen history():
    tag menu

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    use game_menu_overlay

    frame:
        xsize config.screen_width
        ysize config.screen_height
        background None
        padding (80, 60)
        at fade_slide_in(0.0, xoff=-30)

        vbox:
            xsize (config.screen_width - 160)
            spacing 20

            use game_menu_header(_("History"))

            viewport:
                xsize (config.screen_width - 160)
                ysize (config.screen_height - 260)
                mousewheel True
                draggable True
                scrollbars "vertical"
                vbox:
                    spacing 18
                    for h in _history_list:
                        vbox:
                            spacing 4
                            if h.who:
                                text h.who:
                                    bold True
                                    size 24
                                    color "#ffd700"
                                    font "gui/Graduate-Regular.ttf"
                            text h.what:
                                size 24
                                color "#ffffff"
                    if not _history_list:
                        text _("The backlog is empty."):
                            color "#8888a0"

    use game_menu_back(back_action)



# ==============================================================================
# CREDITS
# ==============================================================================

screen about():
    tag menu
    key "game_menu" action (ShowMenu("main_menu") if main_menu else Return())

    frame:
        xfill True
        yfill True
        background Solid("#0a0a0e")

        text _("CREDITS"):
            xalign 0.5
            ypos 50
            size 56
            color "#ffffff"
            font "gui/RiotCityRevolts-m2nPj.ttf"

        frame:
            xalign 0.5
            ypos 130
            xsize 1400
            ysize 720
            background None
            padding (0, 0)
            clipping True

            vbox:
                xalign 0.5
                spacing 50
                at credits_scroll(duration=60.0, travel=760)

                vbox:
                    xalign 0.5
                    spacing 6
                    text (config.name if config.name else "Game Title"):
                        xalign 0.5
                        size 80
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Version [config.version]"):
                        xalign 0.5
                        size 40
                        color "#8888a0"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Made with Ren'Py [renpy.version_only]."):
                        xalign 0.5
                        size 40
                        color "#8888a0"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                vbox:
                    xalign 0.5
                    spacing 4
                    text _("DIRECTION & DESIGN"):
                        xalign 0.5
                        size 58
                        color "#e0521f"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Eric Zheng"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                vbox:
                    xalign 0.5
                    spacing 4
                    text _("Game UI & Programming"):
                        xalign 0.5
                        size 58
                        color "#e0521f"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Eric Zheng"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                vbox:
                    xalign 0.5
                    spacing 4
                    text _("Financial and Budget Director"):
                        xalign 0.5
                        size 58
                        color "#e0521f"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Eric Zheng"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                vbox:
                    xalign 0.5
                    spacing 4
                    text _("R&D and Technical Support"):
                        xalign 0.5
                        size 58
                        color "#e0521f"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Eric Zheng"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                vbox:
                    xalign 0.5
                    spacing 4
                    text _("Visual Effects and Animation"):
                        xalign 0.5
                        size 58
                        color "#e0521f"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Eric Zheng"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                vbox:
                    xalign 0.5
                    spacing 4
                    text _("PROGRAMMING"):
                        xalign 0.5
                        size 58
                        color "#e0521f"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Ryan"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                vbox:
                    xalign 0.5
                    spacing 4
                    text _("Lead Graphic Designers"):
                        xalign 0.5
                        size 58
                        color "#e0521f"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Hannah"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Aydin"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                vbox:
                    xalign 0.5
                    spacing 4
                    text _("Story & Writing"):
                        xalign 0.5
                        size 58
                        color "#e0521f"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Hannah"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                vbox:
                    xalign 0.5
                    spacing 4
                    text _("Character Design"):
                        xalign 0.5
                        size 58
                        color "#e0521f"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Hannah"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Aydin"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                vbox:
                    xalign 0.5
                    spacing 4
                    text _("Map Design"):
                        xalign 0.5
                        size 58
                        color "#e0521f"
                        font "gui/RiotCityRevolts-m2nPj.ttf"
                    text _("Aydin"):
                        xalign 0.5
                        size 50
                        color "#ffffff"
                        font "gui/RiotCityRevolts-m2nPj.ttf"

                text _("THANKS FOR PLAYING!"):
                    xalign 0.5
                    size 100
                    italic True
                    color "#8888a0"
                    font "gui/RiotCityRevolts-m2nPj.ttf"
        frame:
            xpos 80
            yalign 0.95
            xsize 160
            ysize 50
            padding (2, 2)
            background Solid("#33334a")
            at fade_in(0.3)
            button:
                xfill True
                yfill True
                background Solid("#101014")
                hover_background Solid("#2a2a35")
                action (ShowMenu("main_menu") if main_menu else Return())
                text "BACK" align (0.5, 0.5) size 24 color "#8888a0" hover_color "#ffd700" font "gui/Graduate-Regular.ttf"

# ==============================================================================
# MAHJONG MINIGAME
# ------------------------------------------------------------------------------
# This is the ONLY definition of `mahjong_minigame` now. script.rpy used to
# define a second, different screen under the same name — a same-named
# screen defined later in file-load order (script.rpy sorts after
# screen.rpy) silently wins in Ren'Py, so that duplicate was quietly
# shadowing this one entirely; it's been removed from script.rpy. The
# calling code in script.rpy (c2_shunyu_dialogue) was checking `if _return:`
# which happened to work for a bare True/False return, but this screen
# returns the strings "win"/"lose" via Return(...) — both of which are
# truthy — so that check has been fixed to `if _return == "win":`.
# ==============================================================================

screen mahjong_minigame():
    modal True
    zorder 300

    add Solid("#00000099"):
        xsize 1920
        ysize 1080

    if mj_result is None:
        timer 1.0 repeat True action Function(mahjong_tick)

    if mj_lock:
        timer 0.9 action Function(mahjong_hide_mismatch)

    fixed:
        xalign 0.5
        yalign 0.5

        add Solid("#000000aa"):
            xsize 640
            ysize 560
            xalign 0.5
            yalign 0.5
            xoffset 8
            yoffset 12
            blur 24

        frame:
            xalign 0.5
            yalign 0.5
            background Solid("#14141aee")
            padding (40, 30)

            vbox:
                spacing 16
                xalign 0.5

                text "MAHJONG — MATCH THE TILES":
                    xalign 0.5
                    size 30
                    color "#ffd700"
                    font "gui/Graduate-Regular.ttf"

                hbox:
                    xalign 0.5
                    spacing 30
                    text "Moves left: [mj_moves_left]":
                        size 22
                        color "#8888a0"
                        font "gui/Graduate-Regular.ttf"
                    text "Time: [mj_time_left]":
                        size 22
                        color "#8888a0"
                        font "gui/Graduate-Regular.ttf"

                grid 4 3:
                    xalign 0.5
                    spacing 10
                    for i in range(12):
                        button:
                            xsize 90
                            ysize 90
                            background (Solid("#e0521f") if mj_matched[i] else (Solid("#33334a") if mj_revealed[i] else Solid("#101014")))
                            action Function(mahjong_pick, i)
                            at button_hover_anim
                            text (mj_tiles[i] if (mj_revealed[i] or mj_matched[i]) else "?"):
                                align (0.5, 0.5)
                                size 40
                                color "#ffffff"
                                font "gui/Graduate-Regular.ttf"

                if mj_result == "win":
                    text "You matched them all!":
                        xalign 0.5
                        size 26
                        color "#ffd700"
                        font "gui/Graduate-Regular.ttf"
                    textbutton "Continue":
                        xalign 0.5
                        action Return("win")
                        text_font "gui/Graduate-Regular.ttf"
                elif mj_result == "lose":
                    text "Out of moves or time!":
                        xalign 0.5
                        size 26
                        color "#e0521f"
                        font "gui/Graduate-Regular.ttf"
                    textbutton "Continue":
                        xalign 0.5
                        action Return("lose")
                        text_font "gui/Graduate-Regular.ttf"

    frame:
        xalign 0.5
        yalign 0.97
        xsize 160
        ysize 50
        padding (2, 2)
        background Solid("#33334a")
        button:
            xfill True
            yfill True
            background Solid("#101014")
            hover_background Solid("#2a2a35")
            action (ShowMenu("main_menu") if main_menu else Return())
            text "BACK" align (0.5, 0.5) size 24 color "#8888a0" hover_color "#ffd700" font "gui/Graduate-Regular.ttf"



# ==============================================================================
# HELP
# ==============================================================================

screen help():
    tag menu

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    use game_menu_overlay

    frame:
        xsize config.screen_width
        ysize config.screen_height
        background None
        padding (80, 60)
        at fade_slide_in(0.0, xoff=-30)

        vbox:
            xsize (config.screen_width - 160)
            spacing 20

            use game_menu_header(_("Help"))

            vbox:
                spacing 10
                text _("Keyboard Controls")
                text _("Enter / Space: Advance dialogue")
                text _("Escape: Toggle Game Menu")
                text _("Ctrl: Fast Forward while held")
                text _("Tab: Toggle Skipping")

    use game_menu_back(back_action)


# ==============================================================================
# CONFIRM / NOTIFY / SKIP INDICATOR
# ==============================================================================

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200

    add Solid("#00000099"):
        xsize 1920
        ysize 1080

    frame:
        xalign 0.5
        yalign 0.5
        xsize 820
        background Solid("#14141aee")
        padding (50, 40)
        at confirm_pop

        vbox:
            xfill True
            spacing 34

            text message:
                xalign 0.5
                text_align 0.5
                size 34
                color "#f2e6d8"
                font "gui/Graduate-Regular.ttf"

            hbox:
                xalign 0.5
                spacing 24

                frame:
                    xsize 200
                    ysize 66
                    padding (3, 3)
                    background Solid("#33334a")
                    at button_hover_anim
                    button:
                        xfill True
                        yfill True
                        background Solid("#8a4a22")
                        hover_background Solid("#b8631f")
                        action yes_action
                        text _("Yes"):
                            align (0.5, 0.5)
                            size 28
                            color "#f2e6d8"
                            hover_color "#ffffff"
                            font "gui/Graduate-Regular.ttf"

                frame:
                    xsize 200
                    ysize 66
                    padding (3, 3)
                    background Solid("#33334a")
                    at button_hover_anim
                    button:
                        xfill True
                        yfill True
                        background Solid("#101014")
                        hover_background Solid("#2a2a35")
                        action no_action
                        text _("No"):
                            align (0.5, 0.5)
                            size 28
                            color "#8888a0"
                            hover_color "#ffd700"
                            font "gui/Graduate-Regular.ttf"

    key "game_menu":
        action no_action

    key "game_menu":
        action no_action

screen notify(message):
    zorder 100
    frame:
        xalign 0.99
        yalign 0.93
        xoffset -240
        background Solid("#101014cc")
        padding (14, 10)
        at notify_anim
        text message:
            size 20
            color "#ffffff"
            font "gui/Graduate-Regular.ttf"
    timer 3.25:
        action Hide("notify")

screen skip_indicator():
    zorder 100
    frame:
        xpos 0.05
        yalign 0.1
        at fade_in(0.0)
        text _("Skipping...")


# ==============================================================================
# NVL MODE
# ==============================================================================

# screen nvl(dialogue, items=None):
#     window:
#         xfill True
#         yfill True
#         background Solid("#0a0a0ef2")

#         add Solid("#b8631f"):
#             xsize config.screen_width
#             ysize 2
#             yalign 0.0
#             yoffset 90

#         viewport:
#             id "nvl_viewport"
#             xpos scaled(90)
#             ypos 110
#             xsize (config.screen_width - scaled(180))
#             ysize (config.screen_height - 220)
#             mousewheel True
#             draggable True
#             yinitial 1.0

#             vbox:
#                 spacing scaled(24)

#                 for d in dialogue[-8:]:
#                     window:
#                         id d.window_id

#                         vbox:
#                             spacing scaled(6)

#                             if d.who:
#                                 text d.who:
#                                     id "who"
#                                     size scaled(persistent.dialogue_font_size + 2)
#                                     bold True
#                                     color "#ffd700"
#                                     font "gui/Graduate-Regular.ttf"

#                             text d.what:
#                                 id "what"
#                                 size scaled(persistent.dialogue_font_size)
#                                 color "#e8e4dc"
#                                 font "gui/Graduate-Regular.ttf"
#                                 line_spacing scaled(10)

#                 if items:
#                     vbox:
#                         spacing scaled(10)
#                         for i in items:
#                             textbutton i.caption:
#                                 action i.action
#                                 text_font "gui/Graduate-Regular.ttf"
#                                 text_color "#8888a0"
#                                 text_hover_color "#ffd700"

#     if quick_menu:
#         use quick_menu