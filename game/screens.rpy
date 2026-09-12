init offset = -1

# ------------------------------------------------------------------------------
# Global Styles & Selected State Colors
# ------------------------------------------------------------------------------

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

screen pref_toggle(label, action, selected=False):
    frame:
        xsize 190
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
                size 22
                color ("#ffffff" if selected else "#8888a0")
                hover_color "#ffd700"
                font "gui/RiotCityRevolts-m2nPj.ttf"

style say_window is default
style say_label is default
style say_dialogue is default

image pill_mask = Frame("images/pill_mask.png", 30, 30, 30, 30)

default quick_menu_hover = False

init python:
    import renpy.audio.filter as af

define audio.menu_theme = "gui/main_menu.mp3"

init python:
    def _menu_music_filter():
        # Multiply boosts the raw signal (gain), then Comb adds the echo on top of the boosted signal
        boosted_echo = af.Sequence([
            af.Multiply(1.6),
            af.Comb(delay=0.3, multiplier=0.35, wet=True),
        ])
        renpy.music.set_audio_filter("music", boosted_echo, replace=True)
        renpy.music.play(audio.menu_theme, channel="music", fadein=1.5, loop=True)

    def _menu_music_stop():
        renpy.music.set_audio_filter("music", None)
        renpy.music.stop(channel="music", fadeout=1.0)

# ------------------------------------------------------------------------------
# Achievements
# ------------------------------------------------------------------------------

# Each entry needs a unique "id" (used to register with the achievement module).
# "hidden" achievements show "???" until unlocked. "stat_max" is optional —
# only add it for achievements you want to track progress toward (e.g. 3/10).

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
        "title": _("???"),
        "description": _("A secret achievement. Unlock it to reveal its name."),
        "hidden": True,
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
    use game_menu(_("ACHIEVEMENTS"), back_action=(ShowMenu("main_menu") if main_menu else Return()), scrollable=False):
        vbox:
            spacing 14
            for ach in ACHIEVEMENTS:
                $ unlocked = achievement.has(ach["id"])
                $ locked_and_hidden = ach.get("hidden", False) and not unlocked

                frame:
                    xfill True
                    background Solid("#101014cc" if unlocked else "#10101466")
                    padding (20, 16)

                    hbox:
                        spacing 20

                        # Icon — uses real art if you add it, otherwise a plain color block
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
                            xfill True

                            text (("???" if locked_and_hidden else ach["title"])):
                                size 24
                                color ("#ffd700" if unlocked else "#8888a0")
                                font "gui/Graduate-Regular.ttf"

                            text (("A hidden achievement." if locked_and_hidden else ach["description"])):
                                size 18
                                color ("#ffffff" if unlocked else "#666677")

                            if "stat_max" in ach and not unlocked and not ach.get("hidden", False):
                                $ progress = achievement.get_progress(ach["id"])
                                bar:
                                    value progress
                                    range ach["stat_max"]
                                    style "slider"
                                    xsize 300
                                    ysize 14
                                text "[progress]/[ach['stat_max']]":
                                    size 14
                                    color "#8888a0"

init python:
    def _set_qm_hover(value):
        store.quick_menu_hover = value

transform qm_shown:
    alpha 0.0
    ease 0.25 alpha 1.0

transform qm_hidden:
    alpha 1.0
    ease 0.25 alpha 0.0

# ------------------------------------------------------------------------------
# Animations & Backgrounds
# ------------------------------------------------------------------------------

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

transform fade_slide_in(delay=0.0, xoff=-40):
    alpha 0.0
    xoffset xoff
    pause delay
    ease 0.5 alpha 1.0 xoffset 0

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

define config.enter_transition = Dissolve(0.25)
define config.exit_transition = Dissolve(0.2)
define config.intra_transition = Dissolve(0.2)
define config.window_show_transition = Dissolve(0.2)
define config.window_hide_transition = Dissolve(0.2)

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

define gui.sidebar_width = 450
define gui.sidebar_margin = 28
define gui.sidebar_padding = 35
define gui.sidebar_content_width = gui.sidebar_width - (gui.sidebar_padding * 2)

# ------------------------------------------------------------------------------
# Shared layout constants (keep sidebar / divider / content math in one place)
# ------------------------------------------------------------------------------

define gui.sidebar_width = 450
define gui.sidebar_padding = 35
define gui.sidebar_content_width = gui.sidebar_width - (gui.sidebar_padding * 2)

# ------------------------------------------------------------------------------
# Main Menu Screen
# ------------------------------------------------------------------------------
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

screen main_menu():
    tag menu
    on "show" action Function(_menu_music_filter)
    on "hide" action Function(_menu_music_stop)

    fixed:
        at train_shake

        # 2. Right Side Moving Key Graphic
        if renpy.loadable("images/Key.webp"):
            add "images/Key.webp":
                xsize 560
                ysize 770
                fit "contain"
                xpos 0.90
                ypos -0.24
                at key_entrance_and_sway
        else:
            text "KEY":
                size 160
                xpos 0.90
                ypos -0.24
                at key_entrance_and_sway

        # 3. Floating glass sidebar card
        fixed:
            xpos gui.sidebar_margin
            ypos gui.sidebar_margin
            xsize gui.sidebar_width
            ysize (config.screen_height - gui.sidebar_margin * 2)

            # Soft blurred drop shadow, offset slightly behind the card
            add Solid("#000000aa"):
                xsize gui.sidebar_width
                ysize (config.screen_height - gui.sidebar_margin * 2)
                xoffset 6
                yoffset 12
                blur 22

            # Frosted glass panel
            frame:
                xfill True
                yfill True
                background Solid("#14141aa8")
                padding (0, 0)
                clipping True

                # Thin light highlight along the top edge, like glass catching light
                add Solid("#ffffff22"):
                    xsize gui.sidebar_width
                    ysize 2
                    yalign 0.0

                vbox:
                    xpos gui.sidebar_padding
                    ypos 40
                    xsize gui.sidebar_content_width
                    spacing 20

                    # Game Logo - cycles through color variants
                    add "game_logo_cycle":
                        xsize gui.sidebar_content_width
                        ysize 260
                        fit "contain"
                        at fade_slide_in(0.1)

                    # Play Button — solid accent fill, the primary action
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

                    # Sub-menu buttons — flat, quiet, secondary
                    vbox:
                        xsize gui.sidebar_content_width
                        spacing 4

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

                # Train — clipped box, slides in from the left
                frame:
                    xpos 0
                    yalign 0.98
                    xysize (380, 380)
                    background None
                    padding (0, 0)
                    clipping True
                    at fade_slide_in(0.7, xoff=-60)

                    add "images/Train_BP.webp":
                        xysize (380, 380)
                        fit "contain"
                        align (0.05, 1.0)
                        rotate -12

    # 5. Blackberry Logo (bottom-right corner of the window)
    if renpy.loadable("images/Blackberry_Studios.webp"):
        add "images/Blackberry_Studios.webp":
            xalign 0.99
            yalign 0.96
            xsize 200
            ysize 95
            fit "contain"
            rotate -18
            at fade_slide_in(0.9, xoff=40)
    else:
        text "Blackberry":
            size 40
            xalign 0.99
            yalign 0.96
            at fade_slide_in(0.9, xoff=40)
#-------------------------------------------------------------------------------
# Dialogue & Interface Screens
# ------------------------------------------------------------------------------

screen say(who, what):
    window:
        id "window"
        xalign 0.5
        yalign 1.0
        xfill True
        ysize 260
        background None

        # Soft gradient blend into the scene above (stacked fading solids)
        add Solid("#0a0a0e00"):
            xsize 2560
            ysize 40
            yalign 0.0
        add Solid("#0a0a0e55"):
            xsize 2560
            ysize 30
            yoffset 40
        add Solid("#0a0a0ecc"):
            xsize 2560
            ysize 190
            yoffset 70

        # Top accent line, sits right at the gradient/solid seam
        add Solid("#e0521f"):
            xsize 2560
            ysize 2
            yoffset 70

        if who:
            # Name tag, boxed pill instead of bare text
            add AlphaMask(
                Solid("#e0521f", xsize=260, ysize=44),
                Transform("pill_mask", size=(260, 44))
            ):
                xpos 40
                ypos 92

            text who:
                id "who"
                xpos 170
                xanchor 0.5
                ypos 105
                size 26
                bold True
                color "#0a0a0e"
                font "gui/Telegraphem.otf"

        text what:
            id "what"
            xpos 40
            xsize 0.9
            ypos 148
            size 27
            color "#ffffff"
            font "gui/Telegraphem.otf"
            line_spacing 5

    if quick_menu:
        use quick_menu

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
        xpos 0.05
        yalign 0.7
        spacing 10
        for i in items:
            textbutton i.caption:
                action i.action

default quick_menu = True

screen quick_menu():
    zorder 100
    if quick_menu:

        # Invisible zone along the bottom edge — hovering here reveals the bar
        mousearea:
            area (0, config.screen_height - 90, config.screen_width, 90)
            hovered Function(_set_qm_hover, True)
            unhovered Function(_set_qm_hover, False)

        hbox:
            xpos 40
            yalign 1.0
            yoffset -10
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
                            font "gui/Telegraphem.otf"

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

# ------------------------------------------------------------------------------
# Shared "menu" wrapper - every screen that uses this MUST declare its own
# "tag menu" (a tag inside a transcluded/used screen does NOT propagate to the
# screen that calls "use" - that was the bug causing menus to stack instead of
# replacing each other).
# ------------------------------------------------------------------------------

screen game_menu(title, back_action=None, scrollable=True):

    $ back_action = back_action if back_action is not None else (ShowMenu("main_menu") if main_menu else Return())

    key "game_menu" action back_action

    add Solid("#0a0a0eee")

    frame:
        xfill True
        yfill True
        background None
        padding (80, 60)
        at fade_slide_in(0.0, xoff=-30)

        vbox:
            xfill True
            yfill True
            spacing 20

            text title:
                size 40
                color "#ffffff"
                font "gui/Graduate-Regular.ttf"
                at fade_in(0.1)
            add Solid("#e0521f"):
                xsize 160
                ysize 3

            if scrollable:
                viewport:
                    xfill True
                    yfill True
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    vbox:
                        xfill True
                        spacing 10
                        transclude
            else:
                vbox:
                    xfill True
                    spacing 10
                    transclude

            null height 20

            frame:
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

# ------------------------------------------------------------------------------
# Preferences & Submenus
# ------------------------------------------------------------------------------

screen preferences():
    tag menu
    use game_menu(_("PREFERENCES"), back_action=(ShowMenu("main_menu") if main_menu else Return()), scrollable=False):
        hbox:
            spacing 60

            # Left Column
            vbox:
                spacing 26
                xsize 460

                frame:
                    background Solid("#101014cc")
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
                            use pref_toggle(_("WINDOW"), Preference("display", "window"), selected=(_preferences.fullscreen == False))
                            use pref_toggle(_("FULLSCREEN"), Preference("display", "fullscreen"), selected=(_preferences.fullscreen == True))

                frame:
                    background Solid("#101014cc")
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
                            use pref_toggle(_("SEEN TEXT"), Preference("skip", "seen"), selected=(_preferences.skip_unseen == False))
                            use pref_toggle(_("ALL TEXT"), Preference("skip", "all"), selected=(_preferences.skip_unseen == True))

                frame:
                    background Solid("#101014cc")
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
                            use pref_toggle(_("STOP SKIPPING"), Preference("after choices", "stop"), selected=(_preferences.skip_after_choices == False))
                            use pref_toggle(_("KEEP SKIPPING"), Preference("after choices", "skip"), selected=(_preferences.skip_after_choices == True))

                frame:
                    background Solid("#101014cc")
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
                        null height 6
                        text _("AUTO-FORWARD SPEED"):
                            size 18
                            color "#e6a817"
                            font "gui/Graduate-Regular.ttf"
                        bar:
                            style "slider"
                            value Preference("auto-forward time")
                            bar_invert True
                            xsize 380

            # Right Column
            vbox:
                spacing 26
                xsize 420

                frame:
                    background Solid("#101014cc")
                    padding (24, 20)
                    xfill True
                    vbox:
                        spacing 22

                        vbox:
                            spacing 8
                            hbox:
                                xfill True
                                text _("MUSIC VOLUME"):
                                    size 18
                                    color "#e6a817"
                                    font "gui/Graduate-Regular.ttf"
                                text _("  MUTE"):
                                    size 16
                                    color "#8888a0"
                                    hover_color "#ffd700"
                            bar:
                                style "slider"
                                value Preference("music volume")
                                xsize 380

                        vbox:
                            spacing 8
                            hbox:
                                xfill True
                                text _("SOUND VOLUME"):
                                    size 18
                                    color "#e6a817"
                                    font "gui/Graduate-Regular.ttf"
                            bar:
                                style "slider"
                                value Preference("sound volume")
                                xsize 380

                        vbox:
                            spacing 8
                            hbox:
                                xfill True
                                text _("VOICE VOLUME"):
                                    size 18
                                    color "#e6a817"
                                    font "gui/Graduate-Regular.ttf"
                            bar:
                                style "slider"
                                value Preference("voice volume")
                                xsize 380
                        use pref_toggle(_("MUTE ALL AUDIO"), Preference("all mute", "toggle"), selected=False)

screen save():
    tag menu
    use file_slots(_("Save"))

screen load():
    tag menu
    use file_slots(_("Load"))

screen file_slots(title):
    default page = 1
    use game_menu(title, back_action=(ShowMenu("main_menu") if main_menu else Return())):
        vbox:
            spacing 10
            for slot in range(1, 9):
                $ slot_index = slot + (page - 1) * 8
                button:
                    xsize 700
                    action FileAction(slot_index)
                    if FileSlotName(slot_index):
                        text FileSlotName(slot_index)
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

screen history():
    tag menu
    use game_menu(_("History"), back_action=(ShowMenu("main_menu") if main_menu else Return())):
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
                at credits_scroll(duration=40.0, travel=760)

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

                text _("Thank you for playing."):
                    xalign 0.5
                    size 70
                    italic True
                    color "#8888a0"
                    font "gui/RiotCityRevolts-m2nPj.ttf"

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
                text "BACK" align (0.5, 0.5) size 24 color "#8888a0" hover_color "#ffd700" font "gui/RiotCityRevolts-m2nPj.ttf"

screen help():
    tag menu
    use game_menu(_("Help"), back_action=(ShowMenu("main_menu") if main_menu else Return()), scrollable=False):
        vbox:
            spacing 10
            text _("Keyboard Controls")
            text _("Enter / Space: Advance dialogue")
            text _("Escape: Toggle Game Menu")
            text _("Ctrl: Fast Forward while held")
            text _("Tab: Toggle Skipping")

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#00000099"):
        xsize 2560
        ysize 1440
    frame:
        xalign 0.5
        yalign 0.5
        at confirm_pop
        vbox:
            spacing 20
            text message
            hbox:
                xalign 0.5
                spacing 20
                textbutton _("Yes"):
                    action yes_action
                textbutton _("No"):
                    action no_action

    key "game_menu":
        action no_action

screen notify(message):
    zorder 100
    frame:
        xpos 0.05
        yalign 0.2
        at notify_anim
        text message
    timer 3.25:
        action Hide("notify")

screen skip_indicator():
    zorder 100
    frame:
        xpos 0.05
        yalign 0.1
        at fade_in(0.0)
        text _("Skipping...")

screen skip_indicator():
    zorder 100
    frame:
        xpos 0.05
        yalign 0.1
        text _("Skipping...")

screen notify(message):
    zorder 100
    frame:
        xpos 0.05
        yalign 0.2
        text message
    timer 3.25:
        action Hide("notify")

screen nvl(dialogue, items=None):
    window:
        xfill True
        yfill True
        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            vbox:
                spacing 15
                for d in dialogue:
                    window:
                        id d.window_id
                        hbox:
                            spacing 10
                            if d.who:
                                text d.who
                            text d.what
                if items:
                    for i in items:
                        textbutton i.caption:
                            action i.action
    if quick_menu:
        use quick_menu
