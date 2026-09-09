# Complete Standard Ren'Py 8 Screens Template

init offset = -1

################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    xalign 0.5
    xmaximum 0.8

style hyperlink_text:
    properties gui.text_properties("hyperlink")
    hover_underline True

style progress_bar:
    ysize gui.progress_bar_size
    base_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    thumb "gui/bar/thumb.png"

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"

style frame:
    padding gui.frame_tile
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)


################################################################################
## In-Game Screens
################################################################################

## Say screen ##################################################################
screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who:
            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

    if use_quick_menu:
        use quick_menu

style window is default
style namebox is default
style say_thought is default
style say_title is default
style say_label is default
style say_dialogue is default

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Frame("gui/textbox.png", gui.textbox_borders, tile=gui.textbox_tile)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ysize gui.namebox_height
    ypos gui.name_ypos
    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile)
    padding gui.namebox_padding

style say_label:
    properties gui.text_properties("name")
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos


## Input screen ################################################################
screen input(prompt):
    style_prefix "input"

    window:
        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default:
    properties gui.text_properties("input_prompt")


## Choice screen ###############################################################
screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

style choice_vbox is vbox:
    xalign 0.5
    ypos 400
    yanchor 0.5
    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


## Quick Menu screen ###########################################################
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu('history')
            textbutton _("Skip") action Skip() alternate Skip(fast=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Save") action ShowMenu('save')
            textbutton _("Q.Save") action QuickSave()
            textbutton _("Q.Load") action QuickLoad()
            textbutton _("Prefs") action ShowMenu('preferences')

define config.quick_menu_checksum = None

style quick_button is default:
    properties gui.button_properties("quick_button")

style quick_button_text is default:
    properties gui.button_text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
screen navigation():
    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5
        spacing gui.navigation_spacing

        if main_menu:
            textbutton _("Start") action Start()
        else:
            textbutton _("History") action ShowMenu("history")
            textbutton _("Save") action ShowMenu("save")

        textbutton _("Load") action ShowMenu("load")
        textbutton _("Preferences") action ShowMenu("preferences")

        if _in_replay:
            textbutton _("End Replay") action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or renpy.variant("web"):
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):
            textbutton _("Quit") action Quit(confirm=not main_menu)

style navigation_button is default:
    properties gui.button_properties("navigation_button")

style navigation_button_text is default:
    properties gui.button_text_properties("navigation_button")


## Main Menu screen ############################################################
screen main_menu():
    tag menu

    style_prefix "main_menu"

    add gui.main_menu_background

    frame:
        style "main_menu_frame"

    use navigation

    if gui.show_name:
        vbox:
            style "main_menu_title"

            text "[config.name!t]":
                style "main_menu_title_text"

            text "[config.version!t]":
                style "main_menu_version_text"

style main_menu_frame is empty:
    xsize 420
    yfill True
    background "gui/overlay/main_menu.png"

style main_menu_title is default:
    xpos gui.main_menu_title_xpos
    ypos gui.main_menu_title_ypos

style main_menu_title_text is default:
    properties gui.text_properties("title")

style main_menu_version_text is default:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
screen game_menu(title, scroll=None, yinitial=0.0):
    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:
            use navigation

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":
                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transframe True
                            use expression title
                elif scroll == "vpgrid":
                    vpgrid:
                        cols 1
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        use expression title
                else:
                    use expression title

    label title

    if main_menu:
        key "game_menu" action Start()

style game_menu_outer_frame is empty:
    bottom_padding 45
    top_padding 180
    left_padding 300
    right_padding 120
    xfill True
    yfill True

style game_menu_content_frame is empty:
    xfill True
    yfill True

style game_menu_viewport is empty:
    xfill True
    yfill True

style game_menu_side is empty:
    xfill True
    yfill True

style game_menu_label is default:
    xpos 75
    ypos 75

style game_menu_label_text is default:
    properties gui.text_properties("game_menu_label")


## About screen ################################################################
screen about():
    tag menu

    use game_menu(_("About"), scroll="viewport"):
        style_prefix "about"

        vbox:
            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


## Save and Load screens #######################################################
screen save():
    tag menu
    use file_slots(_("Save"))

screen load():
    tag menu
    use file_slots(_("Load"))

screen file_slots(title):
    default page_name_value = FilePageNameInputValue()

    use game_menu(title):
        fixed:
            order_reverse True

            button:
                style "page_label"
                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                xalign 0.5
                yalign 0.5
                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1
                    button:
                        action FileAction(slot)

                        has vbox

                        add FileToml(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            xalign 0.5

                        text FilePageTitle(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            hbox:
                style_prefix "page"
                xalign 0.5
                yalign 1.0
                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()
                if config.has_autosave:
                    textbutton _("A") action FilePage("auto")
                if config.has_quicksave:
                    textbutton _("Q") action FilePage("quick")

                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()

style page_label is default:
    xpadding 75
    ypadding 5

style page_label_text is default:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style slot_button is default:
    properties gui.button_properties("slot_button")

style slot_button_text is default:
    properties gui.button_text_properties("slot_button")

style slot_name_text is default:
    properties gui.text_properties("slot_name")


## Preferences screen ##########################################################
screen preferences():
    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):
        vbox:
            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):
                    vbox:
                        style_option "pref"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_option "pref"
                    label _("Rollback Side")
                    textbutton _("Disable") action Preference("rollback side", "disable")
                    textbutton _("Left") action Preference("rollback side", "left")
                    textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    style_option "pref"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

            null height (45)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:
                    label _("Text Speed")
                    bar value Preference("text speed")

                    label _("Auto-Forward Time")
                    bar value Preference("auto-forward time")

                vbox:
                    if config.has_music:
                        label _("Music Volume")
                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:
                        label _("Sound Volume")
                        hbox:
                            bar value Preference("sound volume")
                            if config.has_voice:
                                textbutton _("Test") action Play("sound", config.sample_sound)

                    if config.has_voice:
                        label _("Voice Volume")
                        hbox:
                            bar value Preference("voice volume")
                            textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height 15
                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"

style pref_label is default:
    top_margin 15
    bottom_margin 3

style pref_label_text is default:
    properties gui.text_properties("pref_label")

style pref_button is default:
    properties gui.button_properties("pref_button")

style pref_button_text is default:
    properties gui.button_text_properties("pref_button")

style slider_label is pref_label
style slider_label_text is pref_label_text

style slider_slider is default:
    xsize 345

style slider_button is default:
    properties gui.button_properties("slider_button")
    yalign 0.5

style slider_button_text is default:
    properties gui.button_text_properties("slider_button")

style mute_all_button is default:
    xalign 0.5


## History screen ##############################################################
screen history():
    tag menu

    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):
        style_prefix "history"

        for h in _history_list:
            window:
                has fixed:
                    yfit True

                if h.who:
                    label h.who:
                        style "history_name"
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    style "history_text"

        if not _history_list:
            label _("The backlogging history is empty.")

style history_window is empty:
    xfill True
    ysize gui.history_height

style history_name is default:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    xsize gui.history_name_width
    properties gui.text_properties("history_name")

style history_text is default:
    xpos gui.history_text_xpos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    properties gui.text_properties("history_text")


## Help screen #################################################################
screen help():
    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):
        style_prefix "help"

        vbox:
            spacing 225

            hbox:
                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")
                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help

screen keyboard_help():
    grid 2 7:
        style_prefix "help"
        spacing 15

        text _("Enter")
        text _("Advances dialogue and activates the interface.")

        text _("Space")
        text _("Advances dialogue without selecting choices.")

        text _("Arrow Keys")
        text _("Navigate the interface.")

        text _("Escape")
        text _("Accesses the game menu.")

        text _("Ctrl")
        text _("Skips dialogue while held down.")

        text _("Tab")
        text _("Toggles dialogue skipping.")

        text _("Page Up / Page Down")
        text _("Rolls back or forwards in dialogue.")

screen mouse_help():
    grid 2 4:
        style_prefix "help"
        spacing 15

        text _("Left Click")
        text _("Advances dialogue and activates the interface.")

        text _("Middle Click")
        text _("Hides the interface.")

        text _("Right Click")
        text _("Accesses the game menu.")

        text _("Mouse Wheel Up / Down")
        text _("Rolls back or forwards in dialogue.")

screen gamepad_help():
    grid 2 4:
        style_prefix "help"
        spacing 15

        text _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

        text _("Left Trigger\nLeft Shoulder")
        text _("Rolls back in dialogue.")

        text _("Right Shoulder")
        text _("Rolls forward in dialogue.")

        text _("Start / Select")
        text _("Accesses the game menu.")

style help_button is default:
    properties gui.button_properties("help_button")

style help_button_text is default:
    properties gui.button_text_properties("help_button")

style help_label is default:
    properties gui.text_properties("help_label")

style help_text is default:
    properties gui.text_properties("help_text")


################################################################################
## Special Overlay Screens
################################################################################

## Confirm screen ##############################################################
screen confirm(message, yes_action, no_action):
    modal True
    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    key "game_menu" action no_action

style confirm_frame is default:
    background Frame("gui/confirm_frame.png", gui.confirm_frame_borders, tile=gui.confirm_frame_tile)
    padding gui.confirm_frame_padding
    xalign 0.5
    yalign 0.5

style confirm_prompt is default:
    xalign 0.5

style confirm_prompt_text is default:
    properties gui.text_properties("confirm_prompt")
    text_align 0.5

style confirm_button is default:
    properties gui.button_properties("confirm_button")

style confirm_button_text is default:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
screen skip_indicator():
    zorder 100
    style_prefix "skip"

    frame:
        hbox:
            spacing 9
            text _("Skipping")
            text "..." at delayed_blur(0.25, 1.0)

style skip_frame is default:
    xpos gui.skip_xpos
    ypos gui.skip_ypos
    padding gui.skip_frame_padding
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.skip_frame_tile)

style skip_text is default:
    properties gui.text_properties("skip")

transform delayed_blur(delay, duration):
    alpha 0.0
    pause delay
    linear duration alpha 1.0


## Notify screen ###############################################################
screen notify(message):
    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!t]"

    timer 3.25 action Hide('notify')

transform notify_appear:
    on show:
        alpha 0.0
        linear 0.25 alpha 1.0
    on hide:
        linear 0.5 alpha 0.0

style notify_frame is default:
    xpos gui.notify_xpos
    ypos gui.notify_ypos
    padding gui.notify_frame_padding
    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.notify_frame_tile)

style notify_text is default:
    properties gui.text_properties("notify")


## NVL display screen ##########################################################
screen nvl(dialogue, items=None):
    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        if gui.nvl_height:
            vpgrid:
                cols 1
                yinitial 1.0
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                for d in dialogue:
                    window:
                        id d.window_id
                        has hbox:
                            spacing 15

                        if d.who is not None:
                            text d.who id "who"
                        text d.what id "what"
        else:
            for d in dialogue:
                window:
                    id d.window_id
                    has hbox:
                        spacing 15

                    if d.who is not None:
                        text d.who id "who"
                    text d.what id "what"

        for i in items:
            textbutton i.caption:
                action i.action
                style "nvl_button"

    if use_quick_menu:
        use quick_menu

style nvl_window is default:
    xfill True
    yfill True
    background "gui/nvl.png"
    padding gui.nvl_borders.padding