# ==============================================================================
# DEPARTURE AT 4:00  -  minigames2.rpy
# Minigames the story waits on. Lose and you try again.
#
#   G  ticket      start              shell game with your ticket
#   H  door        carriage doors     press LEFT, RIGHT, LEFT, RIGHT to open it
#   I  flashlight  crime scene        shine the light on squares to find the evidence
#   J  combo       Himmel's luggage   crack the 3-digit lock
#   K  pry         Misha's carpet     pull it up without tearing it
#   L  survive     Carriage 6         click the shadows before they reach you
#
#   call play_required("mg_door", door_reset)   - loops until the player wins
# ==============================================================================

default mg_required = False

label play_required(scr, reset):
    $ renpy.block_rollback()
    $ mg_required = True
    while True:
        $ reset()
        call screen expression scr
        if _return == "win":
            $ mg_required = False
            return


# ==============================================================================
# G  -  FIND YOUR TICKET
# ==============================================================================
# You see which card is the ticket, the cards swap around, then you pick one.

define TK_X = [190, 510, 830]         # where the three cards sit (inside the box)

default tk_slot = [0, 1, 2]           # card i sits in slot tk_slot[i]
default tk_ticket = 0
default tk_phase = "show"
default tk_swaps = 6
default tk_result = None

init python:
    def ticket_reset():
        store.tk_slot = [0, 1, 2]
        store.tk_ticket = renpy.random.randint(0, 2)
        store.tk_phase = "show"
        store.tk_swaps = [5, 7, 10][persistent.mg_difficulty]
        store.tk_result = None

    def ticket_begin():
        store.tk_phase = "shuffle"
        renpy.restart_interaction()

    def ticket_swap():
        if store.tk_phase != "shuffle":
            return
        a, b = renpy.random.sample([0, 1, 2], 2)
        s = list(store.tk_slot)
        s[a], s[b] = s[b], s[a]
        store.tk_slot = s
        store.tk_swaps -= 1
        if store.tk_swaps <= 0:
            store.tk_phase = "pick"
        renpy.restart_interaction()

    def ticket_pick(i):
        if store.tk_phase != "pick":
            return
        store.tk_phase = "done"
        if i == store.tk_ticket:
            store.tk_result = "win"
            mg_record("ticket")
        else:
            store.tk_result = "lose"
        renpy.restart_interaction()

# cards glide to their new spot whenever they're swapped
transform tk_slide(x):
    ease 0.3 xcenter x

screen mg_ticket():
    use mg_scene(_("FIND YOUR TICKET"), _("Watch the ticket, then click the card it ends up under."), "Train station", "dorothy neutral", 0.88):
        if tk_phase == "show":
            timer 1.6 action Function(ticket_begin)
        elif tk_phase == "shuffle":
            timer (0.42 / mg_mult()) repeat True action Function(ticket_swap)

        use mg_stats([(_("WATCH") if tk_phase in ("show", "shuffle") else _("PICK ONE"))])

        use mg_box(1100, 500):
            for i in range(3):
                $ face_up = tk_phase in ("show", "done")
                button:
                    padding (0, 0)
                    yalign 0.5
                    xysize (220, 320)
                    background rbox(("#efe3c4" if face_up else "#7a1f12"), 18)
                    hover_background rbox(("#efe3c4" if face_up else "#a02a18"), 18)
                    action Function(ticket_pick, i)
                    at tk_slide(TK_X[tk_slot[i]])
                    text ("4:00" if (face_up and i == tk_ticket) else ("" if face_up else "?")):
                        align (0.5, 0.5)
                        size 72
                        color ("#7a1f12" if face_up else "#efe3c4")
                        font GFONT

        if tk_result == "win":
            use mg_end(_("yes, the ticket."), "win")
        elif tk_result == "lose":
            use mg_end(_("Are you fine… sir?"), "lose")


# ==============================================================================
# H  -  OPEN THE DOOR  (valve wheel between carriages)
# ==============================================================================
# Press LEFT then RIGHT then LEFT... Each swap turns the wheel a bit. It slips
# back if you stop.

default dr_prog = 0.0
default dr_last = None
default dr_t = 10.0
default dr_result = None
default dr_bg = "bg carriage_1"

init python:
    def door_reset(bg=None):
        store.dr_prog = 0.0
        store.dr_last = None
        store.dr_t = 10.0
        store.dr_result = None
        if bg:
            store.dr_bg = bg

    def door_push(side):
        if store.dr_result is not None:
            return
        if side != store.dr_last:
            store.dr_prog = min(100.0, store.dr_prog + 6.0 / mg_mult())
            store.dr_last = side
        if store.dr_prog >= 100.0:
            store.dr_result = "win"
            mg_record("door")
        renpy.restart_interaction()

    def door_tick():
        if store.dr_result is not None:
            return
        store.dr_prog = max(0.0, store.dr_prog - 1.1 * mg_mult())
        if mg_timed():
            store.dr_t -= 0.1
            if store.dr_t <= 0:
                store.dr_result = "lose"
        renpy.restart_interaction()

screen mg_door():
    use mg_scene(_("OPEN THE DOOR"), _("Alternate LEFT and RIGHT (arrow keys, A/D or the buttons) to turn the wheel before it slips back."), dr_bg):
        if dr_result is None:
            timer 0.1 repeat True action Function(door_tick)
            key "K_LEFT" action Function(door_push, "L")
            key "K_a" action Function(door_push, "L")
            key "K_RIGHT" action Function(door_push, "R")
            key "K_d" action Function(door_push, "R")

        $ stats = [_("Open: %d%%") % dr_prog]
        if mg_timed():
            $ stats.append(_("Time: %d") % max(0, dr_t))
        use mg_stats(stats)

        use mg_box(900, 440):
            vbox:
                xalign 0.5
                spacing 40
                text ("%d%%" % dr_prog):
                    xalign 0.5
                    size 120
                    color "#ffd700"
                    font GFONT
                hbox:
                    xalign 0.5
                    use mg_meter(dr_prog, 100, w=700)
                if dr_result is None:
                    hbox:
                        xalign 0.5
                        spacing 40
                        use mg_btn(_("LEFT"), Function(door_push, "L"), w=240)
                        use mg_btn(_("RIGHT"), Function(door_push, "R"), w=240)

        if dr_result == "win":
            use mg_end(_("OPEN"), "win")
        elif dr_result == "lose":
            use mg_end(_("LOCKED"), "lose")


# ==============================================================================
# I  -  SEARCH IN THE DARK  (crime scene)
# ==============================================================================
# A grid of dark squares. Click one to shine your light on it. Three of them
# hide the evidence. One hides something else. The battery doesn't last.

define FL_COLS = 6
define FL_ROWS = 3
define FL_ITEMS = [_("TILE"), _("GLASS"), _("BLOOD")]

default fl_items = {}           # square number -> what's there
default fl_ghost = 0            # the square with the thing in it
default fl_lit = []             # squares you've already looked at
default fl_battery = 12
default fl_t = 40.0
default fl_result = None

init python:
    def fl_battery_max():
        return [14, 11, 8][persistent.mg_difficulty] + pass_bonus("extra_life", 4)

    def flashlight_reset():
        spots = renpy.random.sample(range(FL_COLS * FL_ROWS), len(FL_ITEMS) + 1)
        store.fl_items = dict(zip(spots[:-1], FL_ITEMS))
        store.fl_ghost = spots[-1]
        store.fl_lit = []
        store.fl_battery = fl_battery_max()
        store.fl_t = 40.0 / mg_mult()
        store.fl_result = None

    def fl_found():
        return len([i for i in store.fl_lit if i in store.fl_items])

    def flashlight_click(i):
        if store.fl_result is not None or i in store.fl_lit:
            return
        store.fl_lit = store.fl_lit + [i]
        store.fl_battery -= 1
        sfx("ui_click")
        if i == store.fl_ghost:
            renpy.invoke_in_new_context(jumpscare, "passenger", 0.6)
        if fl_found() == len(FL_ITEMS):
            store.fl_result = "win"
            mg_record("flashlight")
        elif store.fl_battery <= 0:
            store.fl_result = "lose"
        renpy.restart_interaction()

    def flashlight_tick():
        if store.fl_result is not None or not mg_timed():
            return
        store.fl_t -= 0.1
        if store.fl_t <= 0:
            store.fl_result = "lose"
        renpy.restart_interaction()

screen mg_flashlight():
    use mg_scene(_("SEARCH IN THE DARK"), _("Click a square to shine your light on it. Find the mahjong tile, the glass and the blood before the battery dies."), "bg carriage_2"):
        if fl_result is None and mg_timed():
            timer 0.1 repeat True action Function(flashlight_tick)

        $ stats = [_("Found: %d / %d") % (fl_found(), len(FL_ITEMS)), _("Battery: %d") % fl_battery]
        if mg_timed():
            $ stats.append(_("Time: %d") % max(0, fl_t))
        use mg_stats(stats)

        use mg_box(1200, 620):
            grid FL_COLS FL_ROWS:
                align (0.5, 0.5)
                spacing 16
                for i in range(FL_COLS * FL_ROWS):
                    $ lit = i in fl_lit
                    button:
                        padding (0, 0)
                        xysize (170, 160)
                        background rbox(("#3a3428" if lit else "#050507"), 16)
                        hover_background rbox(("#3a3428" if lit else "#1a1a22"), 16)
                        action Function(flashlight_click, i)
                        if lit:
                            text (fl_items.get(i, "") if i != fl_ghost else "?"):
                                align (0.5, 0.5)
                                size 30
                                color ("#ff3d3d" if i == fl_ghost else "#ffd76a")
                                font GFONT

        if fl_result == "win":
            use mg_end(_("Ooh, I thought this was blood for a second…"), "win")
        elif fl_result == "lose":
            use mg_end(_("Huh… It's dark.."), "lose")


# ==============================================================================
# J  -  THE LUGGAGE LOCK  (3-digit combination)
# ==============================================================================
# The code is 4-0-0. If you opened the cupboard in Carriage 1 you saw it.

define CB_CODE = [4, 0, 0]

default cb_digits = [0, 0, 0]
default cb_tries = 0
default cb_fb = ""
default cb_result = None
default found_timetable = False

init python:
    def combo_reset():
        store.cb_digits = [renpy.random.randint(1, 9), renpy.random.randint(1, 9), renpy.random.randint(1, 9)]
        store.cb_tries = 0
        store.cb_fb = ""
        store.cb_result = None

    def combo_max():
        return [12, 9, 6][persistent.mg_difficulty] + pass_bonus("extra_life", 3)

    def combo_spin(i, step):
        if store.cb_result is not None:
            return
        d = list(store.cb_digits)
        d[i] = (d[i] + step) % 10
        store.cb_digits = d
        sfx("ui_click")
        renpy.restart_interaction()

    def combo_try():
        if store.cb_result is not None:
            return
        store.cb_tries += 1
        right = sum(1 for a, b in zip(store.cb_digits, CB_CODE) if a == b)
        store.cb_fb = "%d / 3" % right
        if right == 3:
            store.cb_result = "win"
            mg_record("combo")
        elif store.cb_tries >= combo_max():
            store.cb_result = "lose"
        renpy.restart_interaction()

screen mg_combo():
    $ cb_hint = _("Set the three wheels and press OPEN. It tells you how many wheels are right.")
    if found_timetable:
        $ cb_hint = cb_hint + "  \"" + _("Every departure on it is printed the same way: 4:00.") + "\""
    use mg_scene(_("THE LUGGAGE LOCK"), cb_hint, "bg carriage_3"):
        use mg_stats([_("Tries: %d / %d") % (cb_tries, combo_max()), (_("Right: %s") % cb_fb) if cb_fb else _("Right: ?")])

        use mg_box(700, 560):
            vbox:
                xalign 0.5
                spacing 30
                hbox:
                    xalign 0.5
                    spacing 40
                    for i in range(3):
                        vbox:
                            spacing 14
                            use rbtn("+", Function(combo_spin, i, 1), w=120, h=60, r=18, size=30)
                            text str(cb_digits[i]):
                                xalign 0.5
                                size 110
                                color "#ffd76a"
                                font GFONT
                            use rbtn("-", Function(combo_spin, i, -1), w=120, h=60, r=18, size=30)
                if cb_result is None:
                    hbox:
                        xalign 0.5
                        use mg_btn(_("OPEN"), Function(combo_try))

        if cb_result == "win":
            use mg_end(_("OPEN"), "win")
        elif cb_result == "lose":
            use mg_end(_("LOCKED"), "lose")


# ==============================================================================
# K  -  PULL UP THE CARPET
# ==============================================================================
# Every PULL lifts the carpet but adds tension. Tension goes down by itself
# if you wait. Let it fill up and the carpet tears.

default pr_tension = 0.0
default pr_prog = 0.0
default pr_tears = 0
default pr_result = None

init python:
    def pry_reset():
        store.pr_tension = 0.0
        store.pr_prog = 0.0
        store.pr_tears = 0
        store.pr_result = None

    def pry_tears_max():
        return [4, 3, 2][persistent.mg_difficulty] + pass_bonus("extra_life", 1)

    def pry_pull():
        if store.pr_result is not None:
            return
        store.pr_prog = min(100.0, store.pr_prog + 8.0)
        store.pr_tension += renpy.random.uniform(14.0, 26.0) * mg_mult()
        if store.pr_tension >= 100.0:
            store.pr_tears += 1
            store.pr_tension = 30.0
            store.pr_prog = max(0.0, store.pr_prog - 18.0)
            sfx("thud")
            if store.pr_tears >= pry_tears_max():
                store.pr_result = "lose"
        if store.pr_prog >= 100.0 and store.pr_result is None:
            store.pr_result = "win"
            mg_record("pry")
        renpy.restart_interaction()

    def pry_tick():
        if store.pr_result is not None:
            return
        store.pr_tension = max(0.0, store.pr_tension - 3.0)
        renpy.restart_interaction()

screen mg_pry():
    use mg_scene(_("PULL UP THE CARPET"), _("Click PULL (or SPACE). Wait for the tension to drop, or the carpet tears."), "bg carriage_3", "misha stares", 0.88):
        if pr_result is None:
            timer 0.1 repeat True action Function(pry_tick)
            key "K_SPACE" action Function(pry_pull)

        use mg_stats([_("Pulled: %d%%") % pr_prog, _("Tears: %d / %d") % (pr_tears, pry_tears_max())])

        use mg_box(900, 460):
            vbox:
                xalign 0.5
                spacing 22
                text _("Pulled: %d%%") % pr_prog style "mg_small"
                hbox:
                    xalign 0.5
                    use mg_meter(pr_prog, 100, w=700)
                text _("Tension") style "mg_small"
                hbox:
                    xalign 0.5
                    use mg_meter(pr_tension, 100, w=700, col=("#e0521f" if pr_tension > 70 else "#e6a817"))
                null height 10
                if pr_result is None:
                    hbox:
                        xalign 0.5
                        use mg_btn(_("PULL"), Function(pry_pull))

        if pr_result == "win":
            use mg_end(_("DONE"), "win")
        elif pr_result == "lose":
            use mg_end(_("This again..."), "lose")


# ==============================================================================
# L  -  DON'T LET THEM REACH YOU  (Carriage 6)
# ==============================================================================
# Three doors. A shadow comes down one of them, its bar filling as it gets
# closer. Click that door (or press 1, 2, 3) to send it back. Hold on.

define SV_TIME = 20.0

default sv_lanes = [0.0, 0.0, 0.0]    # how close each door's shadow is (0 = no shadow, 1 = reached you)
default sv_spawn = 0.0
default sv_hp = 3
default sv_t = 20.0
default sv_flash = 0
default sv_result = None

init python:
    def survive_reset():
        store.sv_lanes = [0.0, 0.0, 0.0]
        store.sv_spawn = 0.6
        store.sv_hp = 3 + pass_bonus("extra_life", 1)
        store.sv_t = SV_TIME
        store.sv_flash = 0
        store.sv_result = None

    def survive_tick():
        if store.sv_result is not None:
            return
        dt = 0.05
        lanes = list(store.sv_lanes)
        # a new shadow at an empty door
        store.sv_spawn -= dt
        if store.sv_spawn <= 0:
            store.sv_spawn = [1.5, 1.15, 0.85][persistent.mg_difficulty]
            empty = [i for i in range(3) if lanes[i] == 0.0]
            if empty:
                lanes[renpy.random.choice(empty)] = 0.01
        # shadows get closer
        for i in range(3):
            if lanes[i] > 0.0:
                lanes[i] += dt * 0.28 * mg_mult()
                if lanes[i] >= 1.0:
                    lanes[i] = 0.0
                    store.sv_hp -= 1
                    store.sv_flash = 6
                    sfx("thud")
        store.sv_lanes = lanes
        if store.sv_flash:
            store.sv_flash -= 1
        store.sv_t -= dt
        if store.sv_hp <= 0:
            store.sv_result = "lose"
        elif store.sv_t <= 0:
            store.sv_result = "win"
            mg_record("survive")
        renpy.restart_interaction()

    def survive_banish(i):
        if store.sv_result is not None or store.sv_lanes[i] == 0.0:
            return
        lanes = list(store.sv_lanes)
        lanes[i] = 0.0
        store.sv_lanes = lanes
        sfx("static")
        renpy.restart_interaction()

screen mg_survive():
    use mg_scene(_("DON'T LET THEM REACH YOU"), _("Click each shadow before it reaches you."), "carriage_6"):
        if sv_result is None:
            timer 0.05 repeat True action Function(survive_tick)
            key "K_1" action Function(survive_banish, 0)
            key "K_2" action Function(survive_banish, 1)
            key "K_3" action Function(survive_banish, 2)

        use mg_stats([_("Hold on: %d") % max(0, sv_t), _("Lives: %d") % max(0, sv_hp)])

        use mg_box(1100, 640):
            hbox:
                align (0.5, 0.5)
                spacing 40
                for i in range(3):
                    $ near = sv_lanes[i]
                    button:
                        padding (0, 0)
                        xysize (300, 540)
                        background rbox("#14141a", 20)
                        hover_background rbox("#24242e", 20)
                        action Function(survive_banish, i)
                        # the shadow's bar grows up from the bottom as it gets closer
                        if near > 0.0:
                            add rbox("#8a0000", 20):
                                xsize 300
                                yalign 1.0
                                ysize max(40, int(540 * near))
                        text str(i + 1):
                            xalign 0.5
                            ypos 20
                            size 40
                            color "#55556a"
                            font GFONT

        if sv_flash:
            add Solid("#8a0000"):
                pos (-MAP_X0, -MAP_Y0)
                xysize (config.screen_width, config.screen_height)
                alpha (sv_flash / 10.0)

        if sv_result == "win":
            use mg_end(_("Three questions. Three chances."), "win")
        elif sv_result == "lose":
            use mg_end(_("You'll see."), "lose")
