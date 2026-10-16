# ==============================================================================
# DEPARTURE AT 4:00  -  casino.rpy
# SECRET: click DEPARTURES on the main menu's departure board (or the COINS
# counter in the top-right corner). Four simple games, all played with COINS:
#
#   SLOTS        slots.rpy
#   ROULETTE     bet on a colour, odd/even, a half, or one number, then spin
#   HORSE RACE   pick a horse, watch the bars race
#   MAHJONG      the mahjong minigame from Carriage 2, paid per pair
#
#   CASINO_BETS           the bet sizes you can pick (HIGH ROLLER adds more)
#   CASINO_DAILY          free coins once a day
#   $ casino_pay(n)       pay out n coins
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
        renpy.show_screen("casino_win", n)
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
        # a bet size the player can't use any more falls back
        if store.casino_bet not in casino_bets():
            store.casino_bet = 10
        renpy.show_screen("casino")
        # casino songs while you're in here (music.rpy)
        menu_music_filter_off()
        music_for("casino", fade=1.0)
        renpy.restart_interaction()

    def casino_close():
        renpy.hide_screen("casino")
        if main_menu:
            menu_music_filter_on()
            music_menu()
        renpy.restart_interaction()


# ------------------------------------------------------------------------------
# PIECES SHARED BY THE GAMES
# ------------------------------------------------------------------------------

transform casino_win_pop:
    alpha 0.0
    yoffset 20
    easein 0.2 alpha 1.0 yoffset 0
    pause 1.0
    easeout 0.4 alpha 0.0

# "+50 COINS" for a moment
screen casino_win(n):
    zorder 450
    frame:
        xalign 0.5
        yalign 0.12
        padding (36, 14)
        background rbox("#14141aee", 20)
        at casino_win_pop
        text (_("+%d COINS") % n):
            size 36
            color "#ffd76a"
            font GFONT
    timer 1.7 action Hide("casino_win")

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

# pick how big each bet is
screen casino_bet_picker(locked=False):
    hbox:
        spacing 10
        text _("BET"):
            yalign 0.5
            size 18
            color "#8888a0"
            font GFONT
        for b in casino_bets():
            use pref_toggle(str(b), (None if locked else Function(casino_set_bet, b)), selected=(casino_bet == b), w=80)

# a title and a one-line explanation, top-left
screen casino_title(title, hint):
    vbox:
        pos (60, 40)
        spacing 6
        text title:
            size 44
            color "#e6a817"
            font GFONT
        text hint:
            size 17
            color "#8888a0"
            font GFONT


# ------------------------------------------------------------------------------
# THE CASINO  (the lobby)
# ------------------------------------------------------------------------------

# (id, name, what it is)
define CASINO_GAMES = [
    ("slots",    _("SLOTS"),      _("Three reels. Match them. Three 4:00s is the jackpot.")),
    ("roulette", _("ROULETTE"),   _("Bet on a colour, odd or even, a half, or one number.")),
    ("horses",   _("HORSE RACE"), _("Pick one of six horses and watch them race.")),
    ("mahjong",  _("MAHJONG"),    _("Clear the table. Every pair pays, a full clear pays big.")),
]

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

screen casino():
    modal True
    zorder 290
    key "game_menu" action Function(casino_close)

    add Solid("#06060ae8")
    use casino_wallet

    frame:
        align (0.5, 0.5)
        xsize 1000
        padding (50, 40)
        background rbox("#121218f4", 30)
        vbox:
            xfill True
            spacing 16
            text _("4:00 CASINO"):
                size 44
                color "#e6a817"
                font GFONT
            text _("Every game pays out in COINS. Trade 100 coins for a ticket in EXTRAS > GAMEPASS."):
                size 16
                color "#8888a0"
                font GFONT
            null height 6

            for gid, gname, gdesc in CASINO_GAMES:
                button:
                    xfill True
                    ysize 84
                    padding (26, 0)
                    background rbox("#1a1a22", 18)
                    hover_background rbox("#26262f", 18)
                    action Function(casino_play, gid)
                    vbox:
                        yalign 0.5
                        spacing 4
                        text gname:
                            size 26
                            color "#f2e6d8"
                            hover_color "#ffd700"
                            font GFONT
                        text gdesc:
                            size 16
                            color "#8888a0"
                            font GFONT
                    text _("PLAY"):
                        xalign 1.0
                        yalign 0.5
                        size 20
                        color "#e6a817"
                        font GFONT

            null height 6
            hbox:
                spacing 20
                if casino_daily_ready():
                    use mg_btn((_("FREE DAILY COINS  +%d") % casino_daily_amount()), Function(casino_claim_daily), w=420, h=60, size=20)
                else:
                    use rbtn(_("DAILY COINS: COME BACK TOMORROW"), None, w=420, h=60, r=20, size=16)
                use rbtn(_("LEAVE"), Function(casino_close), w=180, h=60, r=20, size=22)
            text (_("BIGGEST WIN %d   ·   WON ALL TIME %d") % ((persistent.casino_best or 0), (persistent.casino_won or 0))):
                size 16
                color "#55556a"
                font GFONT


# ------------------------------------------------------------------------------
# ROULETTE  -  a number flickers and stops, like a departure board
# ------------------------------------------------------------------------------

define RL_RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
define RL_SPIN = 2.4         # seconds the number flickers

# (key, label) - each pays 2x; a single number pays 36x
define RL_BETS = [
    ("red", _("RED")), ("black", _("BLACK")),
    ("odd", _("ODD")), ("even", _("EVEN")),
    ("low", _("1-18")), ("high", _("19-36")),
]

default rl_bets = {}
default rl_spinning = False
default rl_show = 0          # the number on the display
default rl_result = None
default rl_t = 0.0
default rl_pick = 17         # the number for a ONE NUMBER bet
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
        }.get(key, False)

    def rl_pays(key):
        return 36 if isinstance(key, int) else 2

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
        store.rl_msg = ""
        sfx("ui_click")
        renpy.restart_interaction()

    def rl_pick_step(d):
        store.rl_pick = (store.rl_pick + d) % 37
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
        store.rl_result = renpy.random.randint(0, 36)
        store.rl_t = 0.0
        store.rl_spinning = True
        store.rl_msg = ""
        sfx("ui_click")
        renpy.restart_interaction()

    def rl_tick():
        if not store.rl_spinning:
            return
        store.rl_t += 0.08
        if store.rl_t >= RL_SPIN:
            rl_land()
        else:
            store.rl_show = renpy.random.randint(0, 36)
        renpy.restart_interaction()

    def rl_land():
        n = store.rl_result
        store.rl_spinning = False
        store.rl_show = n
        won = sum(amt * rl_pays(key) for key, amt in store.rl_bets.items() if rl_wins(key, n))
        staked = sum(store.rl_bets.values())
        store.rl_history = ([n] + list(store.rl_history))[:12]
        if won:
            store.rl_msg = (_("%d - YOU WIN %d") % (n, won))
            casino_pay(won)
        else:
            store.rl_msg = (_("%d - YOU LOSE %d") % (n, staked))
            sfx("lose")
        store.rl_bets = {}

    def rl_label(key, lab):
        amt = store.rl_bets.get(key, 0)
        return ("%s  (%d)" % (lab, amt)) if amt else lab

screen roulette():
    modal True
    zorder 310
    key "game_menu" action Hide("roulette")
    if rl_spinning:
        timer 0.08 repeat True action Function(rl_tick)

    add Solid("#0a0a0ef4")
    use casino_wallet
    use casino_title(_("ROULETTE"), _("Click a bet as many times as you like (one BET each click), then SPIN. Numbers 0 to 36."))

    frame:
        align (0.5, 0.55)
        xsize 1100
        padding (50, 40)
        background rbox("#121218f4", 30)
        vbox:
            xfill True
            spacing 24

            # the number
            hbox:
                xalign 0.5
                spacing 40
                frame:
                    xysize (220, 200)
                    background rbox(rl_color(rl_show), 26)
                    text str(rl_show):
                        align (0.5, 0.5)
                        size 110
                        color "#f4ecd6"
                        font GFONT
                vbox:
                    yalign 0.5
                    spacing 10
                    text (rl_msg or (_("SPINNING...") if rl_spinning else _("PLACE YOUR BETS"))):
                        size 30
                        color ("#ffd700" if "WIN" in rl_msg else ("#e0521f" if rl_msg else "#e8e4dc"))
                        font GFONT
                    text (_("ON THE TABLE  %d") % sum(rl_bets.values())):
                        size 20
                        color "#ffd76a"
                        font GFONT
                    hbox:
                        spacing 10
                        for hn in rl_history:
                            text str(hn):
                                size 18
                                color ("#ff6b5a" if hn in RL_RED else ("#6dffa5" if hn == 0 else "#a8a4b4"))
                                font GFONT

            # the bets
            hbox:
                xalign 0.5
                spacing 12
                for key, lab in RL_BETS:
                    use rbtn(rl_label(key, lab), Function(rl_place, key), w=150, h=56, r=16, size=18, sel=(key in rl_bets))
            hbox:
                xalign 0.5
                spacing 12
                text _("ONE NUMBER (pays 36x):"):
                    yalign 0.5
                    size 18
                    color "#8888a0"
                    font GFONT
                use rbtn("-", Function(rl_pick_step, -1), w=56, h=56, r=16, size=24)
                text str(rl_pick):
                    yalign 0.5
                    min_width 60
                    text_align 0.5
                    size 30
                    color "#e8e4dc"
                    font GFONT
                use rbtn("+", Function(rl_pick_step, 1), w=56, h=56, r=16, size=24)
                use rbtn(rl_label(rl_pick, _("BET ON IT")), Function(rl_place, rl_pick), w=220, h=56, r=16, size=18, sel=(rl_pick in rl_bets))
            text _("Colours, odd/even and halves pay 2x. 0 loses them all."):
                xalign 0.5
                size 15
                color "#55556a"
                font GFONT

            use casino_bet_picker(rl_spinning)
            hbox:
                spacing 20
                use mg_btn(_("SPIN"), (Function(rl_spin) if (rl_bets and not rl_spinning) else None), w=240, h=64, size=26)
                use rbtn(_("CLEAR BETS"), (Function(rl_clear) if (rl_bets and not rl_spinning) else None), w=220, h=64, r=20, size=20)
                use rbtn(_("BACK"), (Hide("roulette") if not rl_spinning else None), w=160, h=64, r=20, size=20)


# ------------------------------------------------------------------------------
# HORSE RACE  -  six bars race to the end
# ------------------------------------------------------------------------------

define HR_COLORS = ["#e0521f", "#3a6fd8", "#2e8b57", "#c9a21a", "#9b4fd0", "#d8d8e0"]
define HR_TRACK = 1000        # how far they run
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

init python:
    def horses_new_race():
        n = len(HR_COLORS)
        power = [renpy.random.uniform(0.75, 1.25) for _i in range(n)]
        total = sum(power)
        store.hr_power = power
        store.hr_odds = [max(1.5, round(total / p * 0.88 * 2) / 2.0) for p in power]
        store.hr_pos = [0.0] * n
        store.hr_pick = None
        store.hr_stake = 0
        store.hr_running = False
        store.hr_winner = None
        store.hr_order = []
        store.hr_msg = ""

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
        for i, p in enumerate(store.hr_power):
            if pos[i] >= HR_TRACK:
                continue
            # steady pace + bursts and stumbles, so anything can happen
            pos[i] = min(HR_TRACK, pos[i] + 10.0 * p * renpy.random.uniform(0.4, 1.7))
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
            store.hr_msg = (_("NO.%d WINS. YOURS CAME %s") % (w + 1, hr_place(store.hr_pick)))
            sfx("lose")

    def hr_place(i):
        k = store.hr_order.index(i) + 1 if i in store.hr_order else len(HR_COLORS)
        return {1: _("1ST"), 2: _("2ND"), 3: _("3RD")}.get(k, _("%dTH") % k)

    def hr_status():
        if store.hr_msg:
            return store.hr_msg
        if store.hr_pick is not None:
            return _("YOUR HORSE: NO.%d") % (store.hr_pick + 1)
        return _("Click a horse to back it.")

screen horses():
    modal True
    zorder 310
    key "game_menu" action Hide("horses")
    if hr_running:
        timer HR_TICK repeat True action Function(hr_tick)

    add Solid("#0a0a0ef4")
    use casino_wallet
    use casino_title(_("HORSE RACE"), _("Pick a horse, set your BET, press START. A low price wins more often, a high price pays more."))

    frame:
        align (0.5, 0.55)
        xsize 1300
        padding (50, 40)
        background rbox("#121218f4", 30)
        vbox:
            xfill True
            spacing 14
            for i, hcol in enumerate(HR_COLORS):
                hbox:
                    spacing 20
                    use rbtn((_("NO.%d   x%g") % (i + 1, hr_odds[i])), Function(hr_choose, i), w=220, h=50, r=16, size=18, sel=(hr_pick == i))
                    fixed:
                        yalign 0.5
                        xysize (860, 26)
                        use mg_meter(hr_pos[i], HR_TRACK, w=860, h=26, col=hcol)
                    if i in hr_order:
                        text hr_place(i):
                            yalign 0.5
                            size 18
                            color ("#ffd700" if hr_order.index(i) == 0 else "#8888a0")
                            font GFONT

            null height 8
            text hr_status():
                size 28
                color (("#ffd700" if "+" in hr_msg else "#e0521f") if hr_msg else "#e8e4dc")
                font GFONT

            use casino_bet_picker(hr_running)
            hbox:
                spacing 20
                if hr_winner is not None and not hr_running:
                    use mg_btn(_("NEXT RACE"), Function(horses_new_race), w=240, h=64, size=24)
                else:
                    use mg_btn(_("START"), (Function(hr_start) if (hr_pick is not None and not hr_running) else None), w=240, h=64, size=26)
                use rbtn(_("BACK"), (Hide("horses") if not hr_running else None), w=160, h=64, r=20, size=20)


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
