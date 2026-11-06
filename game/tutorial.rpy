# How to play: a page-by-page guide to the whole game.
# Shown once at the start of the first new game, and any time from HOW TO PLAY
# (main menu, the in-game menu bar, or F1). Edit the pages freely.

default persistent.tutorial_seen = False

init python:
    def tutorial_pages():
        return [
            (_("WELCOME ABOARD"), [
                _("You're Louis. You wake up on the Grekhov Express with no idea how you got here."),
                _("Walk the train carriage by carriage, talk to the passengers and staff, and piece together what's going on."),
                _("Reach the end of Carriage 5 and the journey starts over. This time, someone has been murdered."),
            ]),
            (_("READING THE STORY"), [
                _("Click, or press Space or Enter, for the next line."),
                _("Hold Ctrl to fast-forward, or press Tab to keep skipping. Scroll up, or open the Logbook, to read earlier lines."),
                _("Point at the bottom of the screen for the quick menu: Back, Logbook (earlier lines), Skip, Let It Roll (auto), Save and more."),
            ]),
            (_("EXPLORING A CARRIAGE"), [
                _("Each carriage is a map. The glowing diamonds are things you can click: LOOK at objects, TALK to people."),
                _("The line at the bottom of the map tells you what to do next."),
                _("The arrows at the left and right edges are the doors to the next and previous carriage."),
            ]),
            (_("COINS AND DOORS"), [
                _("The first time you look at something, you find %d coins.") % COIN_FIND,
                _("Each door to the next carriage costs %d coins. If you can't pay, look around more. A door is free once you've checked everything in the carriage.") % FARE,
                _("Each carriage also hides a golden ticket worth %d coins. Keep your eyes open.") % GOLDEN_COINS,
            ]),
            (_("CLUES AND PASSENGERS"), [
                _("Some conversations and choices give you clues. Press J any time to open the clue journal."),
                _("Press M to see the passengers you've met and what they've told you."),
                _("Talk to everyone. People say more once they know more."),
            ]),
            (_("MINIGAMES"), [
                _("Some moments are minigames: mahjong, picking locks, sorting mail, keeping the engine's steam steady and more."),
                _("The instructions are in the top-left corner. If you fail, just try again. Each win pays %d coins.") % MG_COIN_REWARD,
                _("Settings has the difficulty, timers on or off, and a SKIP button if you'd rather skip them. Replay them any time in EXTRAS > ARCADE."),
            ]),
            (_("THE LOOP"), [
                _("After Carriage 5 the train starts again, but things have changed."),
                _("Go back through the carriages, question everyone again, and look for what's different."),
                _("When someone lies to you, present the clue that proves them wrong."),
            ]),
            (_("NAMING THE KILLER"), [
                _("At the end you accuse someone. Choose carefully: a wrong guess ends badly."),
                _("There are three endings. The more of the truth you've found, the better the ending you can reach."),
                _("Missed something? Replay any chapter from EXTRAS > CHAPTERS."),
            ]),
            (_("SAVING"), [
                _("The game auto-saves whenever you enter a new carriage (you can turn this off in Settings)."),
                _("F5 quick-saves and F8 quick-loads. Use SAVE and LOAD in the menu for more slots."),
                _("Hardcore mode (Settings > Gameplay) gives you a time limit for the whole journey."),
            ]),
            (_("REWARDS AND EXTRAS"), [
                _("Achievements, minigames, secrets and endings earn tickets. Spend them on Gamepasses in EXTRAS > GAMEPASS."),
                _("Trade %d coins for a ticket, and try your luck in the casino on the main menu (free coins every day).") % COINS_PER_TICKET,
                _("The RADIO tab plays the soundtrack. And the main menu rewards curiosity: try clicking things, especially the big 4:00."),
            ]),
        ]

    def tutorial_done():
        persistent.tutorial_seen = True
        renpy.save_persistent()


transform tutorial_page_in:
    alpha 0.0
    xoffset (0 if persistent.reduce_motion else 30)
    easein 0.25 alpha 1.0 xoffset 0


# The guide itself; `closing` is what CLOSE / SKIP / Esc does.
screen tutorial_book(closing, first=False):
    default page = 0
    $ pages = tutorial_pages()
    $ title, lines = pages[page]
    $ last = page == len(pages) - 1

    key "K_RIGHT" action (SetLocalVariable("page", page + 1) if not last else NullAction())
    key "K_LEFT" action (SetLocalVariable("page", page - 1) if page > 0 else NullAction())

    frame:
        align (0.5, 0.5)
        xysize (1240, 700)
        padding (60, 48)
        background rbox("#0c0b09f4", 24)

        vbox:
            spacing 10
            hbox:
                xfill True
                text _("HOW TO PLAY"):
                    size 22
                    color "#c9a24a"
                    font CREDIT_FONT
                text ("%d / %d" % (page + 1, len(pages))):
                    xalign 1.0
                    size 20
                    color "#6a6050"
                    font GFONT
            add Solid("#c9a24a55"):
                ysize 2
            null height 18

            for k in [page]:
                vbox:
                    spacing 22
                    at tutorial_page_in
                    text title:
                        size 52
                        color "#ffd76a"
                        font CREDIT_FONT
                    for ln in lines:
                        hbox:
                            spacing 18
                            add rbox("#e0521f", 3):
                                xysize (10, 10)
                                yoffset 14
                            text ln:
                                size 26
                                color "#e8e4dc"
                                font say_font()
                                xmaximum 1060
                                line_spacing 6

        # page dots
        hbox:
            xalign 0.5
            yalign 1.0
            yoffset -10
            spacing 10
            for i in range(len(pages)):
                add rbox(("#ffd76a" if i == page else "#3a3630"), 6):
                    xysize (12, 12)

        hbox:
            xalign 1.0
            yalign 1.0
            spacing 12
            if page > 0:
                use rbtn(_("BACK"), SetLocalVariable("page", page - 1), w=140, h=52, r=16, size=20)
            if not last:
                use rbtn(_("NEXT"), SetLocalVariable("page", page + 1), w=160, h=52, r=16, size=20, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")
            else:
                use rbtn((_("START PLAYING") if first else _("DONE")), closing, w=(240 if first else 160), h=52, r=16, size=20, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")

        if first and not last:
            textbutton _("SKIP TUTORIAL"):
                xalign 0.0
                yalign 1.0
                padding (0, 14)
                background None
                text_size 18
                text_color "#8888a0"
                text_hover_color "#ffffff"
                text_font GFONT
                action closing


# Shown once, at the start of the first new game.
screen tutorial_first():
    modal True
    zorder 250
    key "game_menu" action [Function(tutorial_done), Return()]
    add Solid("#000000d0")
    use tutorial_book([Function(tutorial_done), Return()], first=True)


# HOW TO PLAY from the menus (and F1).
screen help():
    tag menu
    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action
    add Solid("#0a0a0e")
    use game_menu_nav
    use tutorial_book([Function(tutorial_done), back_action])
    use game_menu_back(back_action)
