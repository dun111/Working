init offset = -1

# ------------------------------------------------------------------------------
# Global Styles & Selected State Colors
# ------------------------------------------------------------------------------

style default:
    font "gui/Telegraphem.otf"

style button:
    padding (10, 6)

style button_text:
    font "gui/Telegraphem.otf"
    size 35
    color "#8888a0"
    hover_color "#ffffff"
    selected_color "#ffd700"
    insensitive_color "#444455"

style slider:
    ysize 22
    left_bar Solid("#40a0ff")
    right_bar Solid("#222233")
    thumb Solid("#ffffff", xsize=10, ysize=22)

style say_window is default
style say_label is default
style say_dialogue is default

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

transform moving_key_anim:
    xoffset 0
    ease 2.0 xoffset 15
    ease 2.0 xoffset -15
    ease 2.0 xoffset 0
    repeat

# ------------------------------------------------------------------------------
# Main Menu Screen
# ------------------------------------------------------------------------------

screen main_menu():
    tag menu
    # 1. Right Side Background Rotation
    add "main_menu_bg_rotation"
    # 2. Right Side Moving Key Graphic
    if renpy.loadable("gui/key_graphic.png"):
        add "gui/key_graphic.png":
            xpos 0.85
            yalign 0.3
            at moving_key_anim
    else:
        text "🔑":
            size 60
            xpos 0.85
            yalign 0.3
            at moving_key_anim

    # Bottom Right Decoration
    if renpy.loadable("gui/corner_deco.png"):
        add "gui/corner_deco.png":
            xpos 0.95
            yalign 0.95
    else:
        text "Blackberry":
            size 40
            xpos 0.95
            yalign 0.95

    # 3. Left Sidebar Background Frame
    frame:
        xsize 350
        yfill True
        background Solid("#101014ee")
        vbox:
            xpos 35
            ypos 50
            spacing 25
            # Game Logo Placeholder
            frame:
                xsize 280
                ysize 150
                background Solid("#222233")
                text "GAME LOGO\nPLACEHOLDER" align (0.5, 0.5) text_align 0.5 size 20 color "#8888a0"
            # Play Button (Boxed like the sketch)
            button:
                xsize 280
                ysize 65
                background Solid("#333344")
                hover_background Solid("#444455")
                action Start()
                text "PLAY" align (0.5, 0.5) size 32 color "#ffffff" hover_color "#ffd700" font "gui/Telegraphem.otf"
            # Sub-menu buttons (Settings, Credits, Quit)
            vbox:
                spacing 10
                textbutton _("Settings"):
                    text_size 28
                    action ShowMenu("preferences")
                textbutton _("Credits"):
                    text_size 28
                    action ShowMenu("about")
                if renpy.variant("pc"):
                    textbutton _("Quit"):
                        text_size 28
                        action Quit(confirm=True)
        # Train Image Placeholder (Bottom)
        frame:
            xpos 35
            yalign 0.92
            xsize 280
            ysize 180
            background Solid("#222233")
            text "TRAIN IMAGE\nPLACEHOLDER" align (0.5, 0.5) text_align 0.5 size 20 color "#8888a0"
# 4. Vertical Divider (2 lines)
    hbox:
        xpos 350
        yfill True
        spacing 4
        add Solid("#ffffff44"):
            xsize 2
            ysize 1.0
        add Solid("#ffffff44"):
            xsize 2
            ysize 1.0
# ------------------------------------------------------------------------------
# Dialogue & Interface Screens
# ------------------------------------------------------------------------------

screen say(who, what):
    window:
        id "window"
        xalign 0.5
        yalign 1.0
        xfill True
        ysize 220
        if who:
            text who:
                id "who"
                xpos 0.05
                ypos 20
                xsize 0.9
                size 28
                bold True
        text what:
            id "what"
            xpos 0.05
            xsize 0.9
            ypos 70
            size 26
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
        hbox:
            xpos 0.05
            yalign 1.0
            spacing 8
            textbutton _("Back"):
                action Rollback()
            textbutton _("History"):
                action ShowMenu("history")
            textbutton _("Skip"):
                action Skip()
            textbutton _("Auto"):
                action Preference("auto-forward", "toggle")
            textbutton _("Save"):
                action ShowMenu("save")
            textbutton _("Q.Save"):
                action QuickSave()
            textbutton _("Q.Load"):
                action QuickLoad()
            textbutton _("Prefs"):
                action ShowMenu("preferences")

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
# Generic Game Menu Wrapper
# ------------------------------------------------------------------------------

screen game_menu(title, back_action=None):
    tag menu

    # If no explicit back_action was passed, compute the default.
    $ back_action = back_action if back_action is not None else (ShowMenu("main_menu") if main_menu else Return())

    key "game_menu" action back_action

    frame:
        xfill True
        yfill True
        background None
        padding (80, 60)
        vbox:
            spacing 25
            text title:
                size 40
                bold True
                color "#ffffff"
            transclude
            null height 20
            textbutton _("BACK"):
                text_size 28
                action back_action


# ------------------------------------------------------------------------------
# Preferences & Submenus
# ------------------------------------------------------------------------------

screen preferences():
    tag menu
    use game_menu(_("PREFERENCES"), back_action=(ShowMenu("main_menu") if main_menu else Return())):
        hbox:
            spacing 80
            # Left Column
            vbox:
                spacing 20
                xsize 420
                vbox:
                    spacing 6
                    text _("DISPLAY"):
                        size 18
                        color "#8888a0"
                    hbox:
                        spacing 15
                        textbutton _("WINDOW"):
                            action Preference("display", "window")
                        textbutton _("FULLSCREEN"):
                            action Preference("display", "fullscreen")
                vbox:
                    spacing 6
                    text _("SKIP"):
                        size 18
                        color "#8888a0"
                    hbox:
                        spacing 15
                        textbutton _("SEEN TEXT"):
                            action Preference("skip", "seen")
                        textbutton _("ALL TEXT"):
                            action Preference("skip", "all")
                vbox:
                    spacing 6
                    text _("AFTER CHOICES"):
                        size 18
                        color "#8888a0"
                    hbox:
                        spacing 15
                        textbutton _("STOP SKIPPING"):
                            action Preference("after choices", "stop")
                        textbutton _("KEEP SKIPPING"):
                            action Preference("after choices", "skip")
                vbox:
                    spacing 6
                    text _("TEXT SPEED"):
                        size 18
                        color "#8888a0"
                    bar:
                        style "slider"
                        value Preference("text speed")
                        xsize 380
                vbox:
                    spacing 6
                    text _("AUTO-FORWARD SPEED"):
                        size 18
                        color "#8888a0"
                    bar:
                        style "slider"
                        value Preference("auto-forward time")
                        bar_invert True
                        xsize 380
            # Right Column
            vbox:
                spacing 20
                xsize 420
                vbox:
                    spacing 6
                    hbox:
                        text _("MUSIC VOLUME"):
                            size 18
                            color "#8888a0"
                        null width 20
                        textbutton _("MUTE"):
                            action Preference("music mute", "toggle")
                    bar:
                        style "slider"
                        value Preference("music volume")
                        xsize 380
                vbox:
                    spacing 6
                    hbox:
                        text _("SOUND VOLUME"):
                            size 18
                            color "#8888a0"
                        null width 20
                        textbutton _("MUTE"):
                            action Preference("sound mute", "toggle")
                    bar:
                        style "slider"
                        value Preference("sound volume")
                        xsize 380
                vbox:
                    spacing 6
                    hbox:
                        text _("VOICE VOLUME"):
                            size 18
                            color "#8888a0"
                        null width 20
                        textbutton _("MUTE"):
                            action Preference("voice mute", "toggle")
                    bar:
                        style "slider"
                        value Preference("voice volume")
                        xsize 380
                vbox:
                    spacing 6
                    textbutton _("MUTE ALL AUDIO"):
                        action Preference("all mute", "toggle")

screen save():
    use file_slots(_("Save"))

screen load():
    use file_slots(_("Load"))

screen file_slots(title):
    default page = 1
    use game_menu(title, back_action=(ShowMenu("main_menu") if main_menu else Return())):
        vbox:
            spacing 10
            for slot in range(1, 9):
                button:
                    xsize 700
                    action FileAction(slot + (page - 1) * 8)
                    text FileSlotName(slot + (page - 1) * 8, empty=_("Empty Slot"))
            hbox:
                spacing 10
                textbutton _("<"):
                    action SetScreenVariable("page", max(1, page - 1))
                textbutton _("Page [page]"):
                    action NullAction()
                textbutton _(">"):
                    action SetScreenVariable("page", page + 1)

screen history():
    use game_menu(_("History"), back_action=(ShowMenu("main_menu") if main_menu else Return())):
        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            vbox:
                spacing 20
                for h in _history_list:
                    vbox:
                        spacing 5
                        if h.who:
                            text h.who:
                                bold True
                        text h.what
                if not _history_list:
                    text _("The backlog is empty.")

screen about():
    use game_menu(_("Credits"), back_action=Return()):
        vbox:
            spacing 15
            text (config.name if config.name else "Game Title")
            text _("Version [config.version]")
            text _("Made with Ren'Py [renpy.version_only].")
            text _("Developed by Eric Zheng with love and dedication, Ryan with nothing, Hannah with art and Aydin with art")


screen help():
    use game_menu(_("Help"), back_action=(ShowMenu("main_menu") if main_menu else Return())):
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
    frame:
        xalign 0.5
        yalign 0.5
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