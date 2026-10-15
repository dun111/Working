# ==============================================================================
# DEPARTURE AT 4:00  -  casino.rpy
# SECRET: click DEPARTURES on the main menu's departure board (or the COINS
# counter in the top-right corner). Four games, all played with COINS:
#
#   SLOTS        slots.rpy
#   ROULETTE     bet chips on numbers, colours, odd/even, halves and dozens
#   HORSE RACE   pick a horse, watch the race
#   MAHJONG      the mahjong minigame from Carriage 2, paid per pair
#
#   CASINO_BETS           the chip sizes you can pick (HIGH ROLLER adds more)
#   CASINO_DAILY          free coins once a day
#   $ casino_pay(n)       pay out n coins with the coin-burst celebration
# ==============================================================================

define CASINO_BETS = [5, 10, 25, 50]
define CASINO_BETS_HIGH = [100, 250]       # HIGH ROLLER pass
define CASINO_DAILY = 50                   # doubled by HIGH ROLLER

default persistent.casino_best = 0         # biggest single win
default persistent.casino_daily = ""       # the date the daily bonus was last claimed
default persistent.casino_won = 0          # coins won, all time
default casino_bet = 10

init python:
    import datetime as _dt

    def casino_bets():
        return CASINO_BETS + (CASINO_BETS_HIGH if has_pass("high_roller") else [])

    def casino_take(n):
        """Take a stake. False if you can't afford it."""
        if (persistent.coins or 0) < n:
            renpy.notify(_("Not enough coins."))
            return False
        persistent.coins -= n
        return True

    def casino_pay(n):
        if n <= 0:
            return
        persistent.coins = (persistent.coins or 0) + n
        persistent.casino_won = (persistent.casino_won or 0) + n
        if n > (persistent.casino_best or 0):
            persistent.casino_best = n
        sfx("win")
        renpy.show_screen("casino_burst", n, renpy.random.random())
        renpy.restart_interaction()

    def casino_today():
        return _dt.date.today().isoformat()

    def casino_daily_ready():
        return persistent.casino_daily != casino_today()

    def casino_daily_amount():
        return CASINO_DAILY * (2 if has_pass("high_roller") else 1)

    def casino_claim_daily():
        if casino_daily_ready():
            persistent.casino_daily = casino_today()
            casino_pay(casino_daily_amount())

    def casino_set_bet(n):
        store.casino_bet = n
        renpy.restart_interaction()

    def casino_open():
        # a bet size the player can't use any more (pass, coins) falls back
        if store.casino_bet not in casino_bets():
            store.casino_bet = 10
        renpy.show_screen("casino")
        renpy.restart_interaction()


# ------------------------------------------------------------------------------
# PIECES SHARED BY THE GAMES
# ------------------------------------------------------------------------------

# coins burst out of the middle of the screen
transform coin_fly(dx, dy, d):
    alpha 0.0
    xoffset 0
    yoffset 0
    zoom 0.6
    pause d
    alpha 1.0
    parallel:
        easeout 0.7 xoffset dx
    parallel:
        easeout 0.35 yoffset (dy - 120)
        easein 0.55 yoffset (dy + 260)
    parallel:
        ease 0.9 zoom 1.1
    linear 0.25 alpha 0.0

transform burst_text:
    zoom 0.3
    alpha 0.0
    easein_back 0.35 zoom 1.0 alpha 1.0
    pause 0.9
    easeout 0.4 alpha 0.0 yoffset -60

screen casino_burst(n, seed):
    zorder 450
    $ rnd = renpy.random.Random(int(seed * 100000))
    $ many = min(28, 8 + n // 10)
    fixed:
        xpos 0.5
        ypos 0.45
        xysize (0, 0)
        for k in range(many):
            add circ_coin(rnd.randint(22, 40)):
                at coin_fly(rnd.randint(-520, 520), rnd.randint(-260, 60), rnd.random() * 0.25)
    text ("+%d" % n):
        xalign 0.5
        yalign 0.42
        size (90 if n >= 100 else 64)
        color "#ffd76a"
        outlines [(4, "#3a2208", 0, 0)]
        font CREDIT_FONT
        at burst_text
    timer 1.9 action Hide("casino_burst")

# coins in the top corner of every casino screen
screen casino_wallet():
    frame:
        xalign 1.0
        xoffset -40
        ypos 34
        padding (22, 10)
        background rbox("#0c0c10e8", 16)
        hbox:
            spacing 12
            add circ_coin(26):
                yalign 0.5
            text (_("COINS  %d") % (persistent.coins or 0)):
                yalign 0.5
                size 24
                color "#ffd76a"
                font GFONT

# pick how big each chip / stake is
screen casino_bet_picker(locked=False):
    hbox:
        spacing 10
        text _("BET"):
            yalign 0.5
            size 18
            color "#8888a0"
            font GFONT
        for b in casino_bets():
            $ on = (casino_bet == b)
            button:
                xysize (76, 46)
                padding (0, 0)
                background rbox(("#e6a817" if on else "#1a1a22"), 23)
                hover_background rbox(("#ffd76a" if on else "#2a2a35"), 23)
                action (None if locked else Function(casino_set_bet, b))
                text str(b):
                    align (0.5, 0.5)
                    size 20
                    color ("#1a1206" if on else ("#55556a" if (persistent.coins or 0) < b else "#e8e4dc"))
                    font GFONT


# ------------------------------------------------------------------------------
# THE CASINO  (the lobby)
# ------------------------------------------------------------------------------

# (id, name, what it is, symbol, colour)
define CASINO_GAMES = [
    ("slots",    _("SLOTS"),      _("Three reels. Match them. Three 4:00s is the jackpot."), "7",  "#e6a817"),
    ("roulette", _("ROULETTE"),   _("Put chips on the table, spin the wheel. A single number pays 36x."), "0", "#c0392b"),
    ("horses",   _("HORSE RACE"), _("Six horses, six prices. Pick one and watch it run."), "♞", "#2e8b57"),
    ("mahjong",  _("MAHJONG"),    _("Clear the table. Every pair pays, a full clear pays big."), "中", "#3a6fd8"),
]

transform casino_card_in(d):
    alpha 0.0
    yoffset 40
    pause d
    easein 0.35 alpha 1.0 yoffset 0

transform casino_card_hover:
    on idle:
        ease 0.15 yoffset 0 zoom 1.0
    on hover:
        ease 0.15 yoffset -10 zoom 1.03

init python:
    def casino_play(gid):
        if gid == "slots":
            renpy.show_screen("slot_machine")
        elif gid == "roulette":
            roulette_open()
        elif gid == "horses":
            horses_open()
        elif gid == "mahjong":
            won = renpy.invoke_in_new_context(casino_mahjong)
            if won:
                casino_pay(won)
            elif won == 0:
                renpy.notify(_("No pairs, no coins."))
        renpy.restart_interaction()

screen casino_icon(sym, col, size):
    if sym == "中":
        text sym:
            align (0.5, 0.5)
            size size
            color col
            font MJ_FONT
    else:
        text sym:
            align (0.5, 0.5)
            size size
            color col
            font ("DejaVuSans.ttf" if sym == "♞" else CREDIT_FONT)

screen casino():
    modal True
    zorder 290
    key "game_menu" action Hide("casino")

    add Solid("#06060ae8")
    use casino_wallet

    fixed:
        pos (MAP_X0, MAP_Y0)
        xysize (DESIGN_W, DESIGN_H)

        vbox:
            xalign 0.5
            ypos 80
            spacing 6
            text _("4:00 CASINO"):
                xalign 0.5
                size 72
                color "#e6a817"
                font CREDIT_FONT
                at fade_slide_in(0.0)
            text _("Every game pays out in COINS. Trade 100 coins for a ticket in EXTRAS > GAMEPASS."):
                xalign 0.5
                size 18
                color "#8888a0"
                font GFONT
                at fade_slide_in(0.1)

        # the four tables
        hbox:
            xalign 0.5
            ypos 270
            spacing 30
            for k, (gid, gname, gdesc, gsym, gcol) in enumerate(CASINO_GAMES):
                button:
                    xysize (400, 470)
                    padding (0, 0)
                    background rbox("#121218", 30)
                    hover_background rbox("#1b1b24", 30)
                    action Function(casino_play, gid)
                    at casino_card_in(0.1 + k * 0.08), casino_card_hover
                    # the felt with the game's symbol
                    add rbox(gcol + "33", 26):
                        pos (14, 14)
                        xysize (372, 230)
                    fixed:
                        pos (14, 14)
                        xysize (372, 230)
                        use casino_icon(gsym, gcol, 150)
                    vbox:
                        pos (34, 268)
                        xsize 332
                        spacing 10
                        text gname:
                            size 34
                            color "#f2e6d8"
                            font GFONT
                        text gdesc:
                            size 17
                            color "#8888a0"
                            font GFONT
                    text _("PLAY  ›"):
                        xpos 34
                        yalign 0.94
                        size 22
                        color gcol
                        hover_color "#ffffff"
                        font GFONT

        # daily coins, records, leave
        hbox:
            xalign 0.5
            ypos 790
            spacing 26
            if casino_daily_ready():
                use rbtn((_("FREE DAILY COINS  +%d") % casino_daily_amount()), Function(casino_claim_daily), w=380, h=64, r=20, size=21, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")
            else:
                use rbtn(_("DAILY COINS: COME BACK TOMORROW"), None, w=380, h=64, r=20, size=17)
            use rbtn(_("LEAVE"), Hide("casino"), w=180, h=64, r=20, size=22)

        hbox:
            xalign 0.5
            ypos 880
            spacing 50
            text (_("BIGGEST WIN  %d") % (persistent.casino_best or 0)):
                size 18
                color "#55556a"
                font GFONT
            text (_("WON ALL TIME  %d") % (persistent.casino_won or 0)):
                size 18
                color "#55556a"
                font GFONT
            if has_pass("high_roller"):
                text _("HIGH ROLLER"):
                    size 18
                    color "#ffd700"
                    font GFONT


# ------------------------------------------------------------------------------
# ROULETTE
# ------------------------------------------------------------------------------

# the real order of the numbers round a single-zero wheel
define RL_WHEEL = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
                   5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
define RL_RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
define RL_R = 250            # wheel radius
define RL_SPIN = 4.6         # seconds the wheel spins

# (key, label, pays x, wins on)
define RL_OUTSIDE = [
    ("low",   _("1-18"),  2), ("even", _("EVEN"), 2), ("red",  _("RED"), 2),
    ("black", _("BLACK"), 2), ("odd",  _("ODD"),  2), ("high", _("19-36"), 2),
]
define RL_DOZENS = [("d1", _("1st 12"), 3), ("d2", _("2nd 12"), 3), ("d3", _("3rd 12"), 3)]

default rl_bets = {}
default rl_spinning = False
default rl_angle = 0.0
default rl_target = 0.0
default rl_ball = 0.0
default rl_spin_id = 0
default rl_result = None
default rl_msg = ""
default rl_history = []

init python:
    def rl_color(n):
        if n == 0:
            return "#1f7a3a"
        return "#b0201a" if n in RL_RED else "#141418"

    def rl_wins(key, n):
        if isinstance(key, int):
            return key == n
        if n == 0:
            return False
        return {
            "red": n in RL_RED, "black": n not in RL_RED,
            "odd": n % 2 == 1, "even": n % 2 == 0,
            "low": n <= 18, "high": n >= 19,
            "d1": n <= 12, "d2": 13 <= n <= 24, "d3": n >= 25,
        }.get(key, False)

    def rl_pays(key):
        if isinstance(key, int):
            return 36
        return 3 if key in ("d1", "d2", "d3") else 2

    def roulette_open():
        store.rl_bets = {}
        store.rl_result = None
        store.rl_msg = ""
        renpy.show_screen("roulette")

    def rl_place(key):
        if store.rl_spinning:
            return
        if not casino_take(store.casino_bet):
            return
        b = dict(store.rl_bets)
        b[key] = b.get(key, 0) + store.casino_bet
        store.rl_bets = b
        store.rl_result = None
        store.rl_msg = ""
        sfx("ui_click")
        renpy.restart_interaction()

    def rl_clear():
        if store.rl_spinning:
            return
        persistent.coins = (persistent.coins or 0) + sum(store.rl_bets.values())
        store.rl_bets = {}
        renpy.restart_interaction()

    def rl_spin():
        if store.rl_spinning or not store.rl_bets:
            return
        n = renpy.random.choice(RL_WHEEL)
        k = RL_WHEEL.index(n)
        step = 360.0 / len(RL_WHEEL)
        # the wheel turns clockwise until pocket k sits under the marker at the top
        start = store.rl_angle % 360.0
        store.rl_target = start + 360.0 * 4 + ((-k * step - start) % 360.0)
        store.rl_angle = start
        store.rl_result = n
        store.rl_spinning = True
        store.rl_spin_id += 1
        store.rl_msg = ""
        sfx("ui_click")
        renpy.restart_interaction()

    def rl_land():
        n = store.rl_result
        store.rl_spinning = False
        store.rl_angle = store.rl_target
        won = sum(amt * rl_pays(key) for key, amt in store.rl_bets.items() if rl_wins(key, n))
        staked = sum(store.rl_bets.values())
        store.rl_history = ([n] + list(store.rl_history))[:12]
        if won:
            store.rl_msg = (_("%d!  YOU WIN %d") % (n, won))
            casino_pay(won)
        else:
            store.rl_msg = (_("%d.  YOU LOSE %d") % (n, staked))
            sfx("lose")
        store.rl_bets = {}
        renpy.restart_interaction()

    # the wheel is built once: pockets round the edge, numbers on them
    def _rl_wheel():
        R = RL_R
        kids = [Transform("gui/round/r256.png", xysize=(2 * R, 2 * R), matrixcolor=TintMatrix("#5a3418")),
                At(Transform("gui/round/r256.png", xysize=(2 * R - 24, 2 * R - 24), matrixcolor=TintMatrix("#2a160a")),
                   Transform(xcenter=R, ycenter=R))]
        step = 360.0 / len(RL_WHEEL)
        import math
        for k, n in enumerate(RL_WHEEL):
            a = math.radians(k * step)
            r = R - 44
            pocket = Fixed(
                Transform(rbox(rl_color(n), 6), xysize=(40, 56)),
                Text(str(n), size=20, color="#f4ecd6", font=GFONT, xalign=0.5, ypos=6),
                xysize=(40, 56))
            kids.append(At(pocket, Transform(rotate=k * step, rotate_pad=False, transform_anchor=True,
                                              anchor=(0.5, 0.5),
                                              # whole pixels: a float position would mean "fraction of the screen"
                                              xcenter=int(R + r * math.sin(a)), ycenter=int(R - r * math.cos(a)))))
        # the hub in the middle
        kids.append(At(Transform("gui/round/r256.png", xysize=(2 * R - 170, 2 * R - 170), matrixcolor=TintMatrix("#1d5236")),
                       Transform(xcenter=R, ycenter=R)))
        kids.append(At(Transform("gui/round/r256.png", xysize=(90, 90), matrixcolor=TintMatrix("#c9921a")),
                       Transform(xcenter=R, ycenter=R)))
        return Fixed(*kids, xysize=(2 * R, 2 * R))

    RL_WHEEL_D = _rl_wheel()

    def _rl_ball_track():
        R = RL_R
        return Fixed(At(Transform("gui/round/r256.png", xysize=(22, 22), matrixcolor=TintMatrix("#ffffff")),
                        Transform(xcenter=R, ycenter=40)),
                     xysize=(2 * R, 2 * R))

    RL_BALL_D = _rl_ball_track()

transform rl_wheel_spin(a0, a1, sid):
    rotate a0
    easeout_cubic RL_SPIN rotate a1

transform rl_wheel_still(a):
    rotate a

# the ball runs the other way, slows, and drops into the top pocket
transform rl_ball_spin(sid):
    rotate 0
    easeout_quart RL_SPIN rotate -1440

transform rl_cell_hover:
    on idle:
        ease 0.1 zoom 1.0
    on hover:
        ease 0.1 zoom 1.06

transform rl_msg_pop:
    zoom 0.7
    alpha 0.0
    easein_back 0.3 zoom 1.0 alpha 1.0

# one place to put chips: a number, colour, half...
screen rl_cell(key, label, w, h, bg, size=22):
    $ amt = rl_bets.get(key, 0)
    button:
        xysize (w, h)
        padding (0, 0)
        background rbox(bg, 8)
        hover_background rbox("#e6a817", 8)
        action Function(rl_place, key)
        at rl_cell_hover
        text label:
            align (0.5, 0.5)
            size size
            color "#f4ecd6"
            hover_color "#1a1206"
            font GFONT
        if amt:
            fixed:
                xysize (34, 34)
                align (1.0, 0.0)
                offset (8, -8)
                add circ_coin(34)
                text str(amt):
                    align (0.5, 0.5)
                    size (13 if amt < 100 else 11)
                    color "#3a2208"
                    font GFONT

screen roulette():
    modal True
    zorder 310
    key "game_menu" action Hide("roulette")

    add Solid("#0b130ef4")
    use casino_wallet

    if rl_spinning:
        timer RL_SPIN action Function(rl_land)

    fixed:
        pos (MAP_X0, MAP_Y0)
        xysize (DESIGN_W, DESIGN_H)

        text _("ROULETTE"):
            pos (60, 40)
            size 54
            color "#e6a817"
            font CREDIT_FONT
        text _("Click the table to put chips down (one BET each click), then SPIN."):
            pos (62, 112)
            size 17
            color "#8888a0"
            font GFONT

        # ---- the wheel
        fixed:
            pos (70, 220)
            xysize (2 * RL_R, 2 * RL_R)
            add RL_WHEEL_D:
                align (0.5, 0.5)
                at (rl_wheel_spin(rl_angle, rl_target, rl_spin_id) if rl_spinning else rl_wheel_still(rl_angle))
            if rl_spinning:
                add RL_BALL_D:
                    align (0.5, 0.5)
                    at rl_ball_spin(rl_spin_id)
            elif rl_result is not None:
                add RL_BALL_D:
                    align (0.5, 0.5)
            # the marker at the top
            add Transform(rbox("#ffd76a", 4), xysize=(14, 34)):
                xalign 0.5
                ypos -22

        # the last numbers
        hbox:
            pos (70, 770)
            spacing 6
            for hn in rl_history:
                frame:
                    xysize (40, 40)
                    padding (0, 0)
                    background rbox(rl_color(hn), 10)
                    text str(hn):
                        align (0.5, 0.5)
                        size 16
                        color "#f4ecd6"
                        font GFONT

        # result
        if rl_msg:
            text rl_msg:
                xpos 320
                xanchor 0.5
                ypos 840
                size 34
                color ("#ffd700" if "WIN" in rl_msg else "#e0521f")
                font CREDIT_FONT
                at rl_msg_pop

        # ---- the table
        fixed:
            pos (680, 220)
            xysize (1180, 560)
            add rbox("#1d5236", 26):
                xysize (1180, 560)
            # 0, then the numbers in three rows of twelve, like a real table
            fixed:
                pos (30, 30)
                use rl_cell(0, "0", 70, 222, rl_color(0), 26)
            for n in range(1, 37):
                $ col = (n - 1) // 3
                $ row = 2 - (n - 1) % 3
                fixed:
                    pos (110 + col * 86, 30 + row * 76)
                    xysize (80, 70)
                    use rl_cell(n, str(n), 80, 70, rl_color(n))
            # dozens
            for k, (key, lab, pays) in enumerate(RL_DOZENS):
                fixed:
                    pos (110 + k * 344, 268)
                    xysize (338, 66)
                    use rl_cell(key, lab, 338, 66, "#174630")
            # halves, colours, odd / even
            for k, (key, lab, pays) in enumerate(RL_OUTSIDE):
                fixed:
                    pos (110 + k * 172, 346)
                    xysize (166, 66)
                    use rl_cell(key, lab, 166, 66, ("#b0201a" if key == "red" else ("#141418" if key == "black" else "#174630")))
            text _("Number pays 36x   ·   Dozen pays 3x   ·   Everything else pays 2x   ·   0 loses every outside bet"):
                pos (110, 440)
                size 16
                color "#9fc7b0"
                font GFONT
            text (_("ON THE TABLE  %d") % sum(rl_bets.values())):
                pos (110, 480)
                size 22
                color "#ffd76a"
                font GFONT

        # ---- controls
        hbox:
            pos (680, 820)
            spacing 22
            use casino_bet_picker(rl_spinning)
        hbox:
            pos (680, 900)
            spacing 20
            use mg_btn(_("SPIN"), (Function(rl_spin) if (rl_bets and not rl_spinning) else None), w=260, h=70, size=28)
            use rbtn(_("CLEAR CHIPS"), (Function(rl_clear) if (rl_bets and not rl_spinning) else None), w=240, h=70, r=22, size=22)
            use rbtn(_("BACK"), (Hide("roulette") if not rl_spinning else None), w=180, h=70, r=22, size=22)


# ------------------------------------------------------------------------------
# HORSE RACE
# ------------------------------------------------------------------------------

define HR_COLORS = ["#e0521f", "#3a6fd8", "#2e8b57", "#c9a21a", "#9b4fd0", "#d8d8e0"]
define HR_TRACK = 1260        # how far they run (pixels)
define HR_TICK = 0.05

default hr_power = []         # each horse's hidden strength this race
default hr_odds = []          # what each one pays
default hr_pos = []
default hr_pick = None
default hr_stake = 0
default hr_running = False
default hr_winner = None
default hr_order = []
default hr_msg = ""
default hr_race = 0

init python:
    def horses_new_race():
        n = len(HR_COLORS)
        power = [renpy.random.uniform(0.75, 1.25) for _i in range(n)]
        total = sum(power)
        odds = []
        for p in power:
            o = total / p * 0.88
            odds.append(max(1.5, round(o * 2) / 2.0))
        store.hr_power = power
        store.hr_odds = odds
        store.hr_pos = [0.0] * n
        store.hr_pick = None
        store.hr_stake = 0
        store.hr_running = False
        store.hr_winner = None
        store.hr_order = []
        store.hr_msg = ""
        store.hr_race += 1

    def horses_open():
        horses_new_race()
        renpy.show_screen("horses")

    def hr_choose(i):
        if not store.hr_running and store.hr_winner is None:
            store.hr_pick = i
            renpy.restart_interaction()

    def hr_start():
        if store.hr_running or store.hr_pick is None or store.hr_winner is not None:
            return
        if not casino_take(store.casino_bet):
            return
        store.hr_stake = store.casino_bet
        store.hr_running = True
        sfx("ui_click")
        renpy.restart_interaction()

    def hr_tick():
        if not store.hr_running:
            return
        pos = list(store.hr_pos)
        rnd = renpy.random
        for i, p in enumerate(store.hr_power):
            if pos[i] >= HR_TRACK:
                continue
            # steady pace + bursts and stumbles, so anything can happen
            surge = rnd.uniform(0.4, 1.7)
            pos[i] = min(HR_TRACK, pos[i] + 13.0 * p * surge)
            if pos[i] >= HR_TRACK and i not in store.hr_order:
                store.hr_order = store.hr_order + [i]
        store.hr_pos = pos
        if store.hr_order and store.hr_winner is None:
            store.hr_winner = store.hr_order[0]
        if all(x >= HR_TRACK for x in pos):
            hr_finish()
        renpy.restart_interaction()

    def hr_finish():
        store.hr_running = False
        w = store.hr_winner
        if w == store.hr_pick:
            win = int(store.hr_stake * store.hr_odds[w])
            store.hr_msg = (_("NO.%d WINS!  +%d") % (w + 1, win))
            casino_pay(win)
        else:
            store.hr_msg = (_("NO.%d WINS.  YOUR HORSE CAME %s") % (w + 1, hr_place(store.hr_pick)))
            sfx("lose")

    def hr_place(i):
        k = store.hr_order.index(i) + 1 if i in store.hr_order else len(HR_COLORS)
        return {1: _("1ST"), 2: _("2ND"), 3: _("3RD")}.get(k, _("%dTH") % k)

    def hr_leader():
        if not store.hr_pos:
            return None
        return max(range(len(store.hr_pos)), key=lambda i: store.hr_pos[i])

    # the chess knight faces left, so it's flipped to run towards the finish
    HR_HORSE = Transform(Text("♞", font="DejaVuSans.ttf", size=88, color="#f4ecd6"), xzoom=-1)

transform hr_gallop(i, running):
    yoffset 0
    rotate 0
    block:
        ease (0.16 + i * 0.01) yoffset -9 rotate -4
        ease (0.16 + i * 0.01) yoffset 0 rotate 2
        repeat

transform hr_still:
    yoffset 0
    rotate 0

screen horses():
    modal True
    zorder 310
    key "game_menu" action Hide("horses")
    if hr_running:
        timer HR_TICK repeat True action Function(hr_tick)

    add Solid("#0e120af4")
    use casino_wallet

    fixed:
        pos (MAP_X0, MAP_Y0)
        xysize (DESIGN_W, DESIGN_H)

        text _("HORSE RACE"):
            pos (60, 40)
            size 54
            color "#e6a817"
            font CREDIT_FONT
        text _("Pick a horse, set your BET and press START. Lower prices win more often, higher prices pay more."):
            pos (62, 112)
            size 17
            color "#8888a0"
            font GFONT

        # ---- the track
        fixed:
            pos (60, 170)
            xysize (1800, 600)
            add rbox("#5a4022", 26):
                xysize (1800, 600)
            add rbox("#3e6b2a", 22):
                pos (10, 10)
                xysize (1780, 580)
            # the finish line
            for k in range(24):
                add Solid(("#f4ecd6" if k % 2 == 0 else "#141418")):
                    pos (160 + HR_TRACK + 90, 14 + k * 24)
                    xysize (16, 24)
                add Solid(("#141418" if k % 2 == 0 else "#f4ecd6")):
                    pos (176 + HR_TRACK + 90, 14 + k * 24)
                    xysize (16, 24)
            for i, hcol in enumerate(HR_COLORS):
                $ ly = 18 + i * 95
                # lane, gate and price
                add Solid("#ffffff22"):
                    pos (20, ly + 92)
                    xysize (1760, 2)
                button:
                    pos (24, ly + 8)
                    xysize (140, 78)
                    padding (0, 0)
                    background rbox((hcol if hr_pick == i else "#0a0a0eaa"), 14)
                    hover_background rbox(hcol + "aa", 14)
                    action Function(hr_choose, i)
                    vbox:
                        align (0.5, 0.5)
                        spacing 0
                        text (_("NO.%d") % (i + 1)):
                            xalign 0.5
                            size 22
                            color ("#0a0a0e" if hr_pick == i else hcol)
                            font GFONT
                        text ("x%s" % (("%g" % hr_odds[i]) if hr_odds else "-")):
                            xalign 0.5
                            size 18
                            color ("#0a0a0e" if hr_pick == i else "#e8e4dc")
                            font GFONT
                # the horse and its jockey's colours
                fixed:
                    pos (170 + int(hr_pos[i] if hr_pos else 0), ly)
                    xysize (100, 90)
                    at (hr_gallop(i, hr_race) if hr_running else hr_still)
                    add HR_HORSE:
                        align (0.5, 1.0)
                    add rbox(hcol, 8):
                        xysize (30, 22)
                        pos (34, 30)
                    text str(i + 1):
                        pos (42, 30)
                        size 16
                        color "#0a0a0e"
                        font GFONT

        # live order / result
        if hr_running:
            $ lead = hr_leader()
            text (_("IN FRONT:  NO.%d") % (lead + 1)):
                pos (60, 800)
                size 30
                color HR_COLORS[lead]
                font GFONT
        elif hr_msg:
            text hr_msg:
                pos (60, 800)
                size 34
                color ("#ffd700" if "+" in hr_msg else "#e0521f")
                font CREDIT_FONT
                at rl_msg_pop
        elif hr_pick is not None:
            text (_("YOUR HORSE:  NO.%d  PAYS x%g") % (hr_pick + 1, hr_odds[hr_pick])):
                pos (60, 800)
                size 28
                color HR_COLORS[hr_pick]
                font GFONT
        else:
            text _("Click a horse's number to back it."):
                pos (60, 800)
                size 24
                color "#8888a0"
                font GFONT

        hbox:
            pos (60, 880)
            spacing 22
            use casino_bet_picker(hr_running)
            null width 30
            if hr_winner is not None and not hr_running:
                use mg_btn(_("NEXT RACE"), Function(horses_new_race), w=260, h=60, size=24)
            else:
                use mg_btn(_("START"), (Function(hr_start) if (hr_pick is not None and not hr_running) else None), w=260, h=60, size=26)
            use rbtn(_("BACK"), (Hide("horses") if not hr_running else None), w=180, h=60, r=20, size=22)


# ------------------------------------------------------------------------------
# MAHJONG  (the Carriage 2 minigame, for coins)
# ------------------------------------------------------------------------------

define CASINO_MJ_FEE = 20         # to sit down
define CASINO_MJ_PAIR = 3         # paid for every pair
define CASINO_MJ_CLEAR = 150      # bonus for clearing the whole table

default mj_casino = False

init python:
    def casino_mahjong():
        """Plays one table. Returns the coins won (None if you couldn't pay to sit)."""
        if not casino_take(CASINO_MJ_FEE):
            return None
        mahjong_reset()
        store.mj_casino = True
        try:
            renpy.call_screen("mahjong_minigame")
        finally:
            store.mj_casino = False
        pairs = store.mj_gone.count(True) // 2
        return pairs * CASINO_MJ_PAIR + (CASINO_MJ_CLEAR if all(store.mj_gone) else 0)
