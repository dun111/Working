define CASINO_BETS = [5, 10, 25, 50]
define CASINO_BETS_HIGH = [100, 250]
define CASINO_DAILY = 50

default persistent.casino_best = 0
default persistent.casino_daily = ""
default persistent.casino_won = 0
default casino_bet = 10

init python:
    import datetime as _dt

    def casino_bets():
        return CASINO_BETS + (CASINO_BETS_HIGH if has_pass("high_roller") else [])

    def casino_take(n):
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
        if store.casino_bet not in casino_bets():
            store.casino_bet = 10
        renpy.show_screen("casino")
        menu_music_filter_off()
        music_for("casino", fade=1.0)
        renpy.restart_interaction()

    def casino_close():
        renpy.hide_screen("casino")
        if main_menu:
            menu_music_filter_on()
            music_menu()
        renpy.restart_interaction()


transform casino_win_pop:
    alpha 0.0
    yoffset 20
    easein 0.2 alpha 1.0 yoffset 0
    pause 1.0
    easeout 0.4 alpha 0.0

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


define CASINO_GAMES = [
    ("slots",    _("SLOTS"),      _("Match three. Three 4:00s is the jackpot.")),
    ("roulette", _("ROULETTE"),   _("Bet on a colour, odd or even, a half, or one number.")),
    ("horses",   _("HORSE RACE"), _("Pick one of six horses and watch them race.")),
    ("mahjong",  _("MAHJONG"),    _("Every pair pays. Clear the table for a big win.")),
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
            text _("You win coins here. 100 coins buys a ticket in EXTRAS > GAMEPASS."):
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


define RL_RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
define RL_SPIN = 2.4

define RL_BETS = [
    ("red", _("RED")), ("black", _("BLACK")),
    ("odd", _("ODD")), ("even", _("EVEN")),
    ("low", _("1-18")), ("high", _("19-36")),
]

default rl_bets = {}
default rl_spinning = False
default rl_show = 0
default rl_result = None
default rl_t = 0.0
default rl_pick = 17
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
    use casino_title(_("ROULETTE"), _("Click bets to place them, then SPIN."))

    frame:
        align (0.5, 0.55)
        xsize 1100
        padding (50, 40)
        background rbox("#121218f4", 30)
        vbox:
            xfill True
            spacing 24

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
            text _("Colours, odd/even and halves pay 2x. 0 loses."):
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


define HR_COLORS = ["#e0521f", "#3a6fd8", "#2e8b57", "#c9a21a", "#9b4fd0", "#d8d8e0"]
define HR_TRACK = 1000
define HR_TICK = 0.05

default hr_power = []
default hr_odds = []
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
        renpy.restart_interaction()

    def hr_tick():
        if not store.hr_running:
            return
        pos = list(store.hr_pos)
        for i, p in enumerate(store.hr_power):
            if pos[i] >= HR_TRACK:
                continue
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
    use casino_title(_("HORSE RACE"), _("Pick a horse and press START. Low odds win more often, high odds pay more."))

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


define CASINO_MJ_FEE = 20
define CASINO_MJ_PAIR = 3
define CASINO_MJ_CLEAR = 150

default mj_casino = False

init python:
    def casino_mahjong():
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


default persistent.coins = 50

define SLOT_PAIR = 2
define COINS_PER_TICKET = 100

define SLOT_SYMBOLS = [
    ("4:00", 1, 100),
    ("7", 2, 40),
    ("$", 3, 20),
    ("中", 4, 12),
    ("♦", 5, 8),
    ("♣", 5, 6),
]

default slot_reels = ["4:00", "7", "$"]
default slot_spinning = [False, False, False]
default slot_msg = ""
default slot_win = 0
default slot_stake = 0
default slot_streak = 0
default slot_tease = False

init python:
    class _SLOT(object):
        t = 0.0
        stops = [1.0, 1.5, 2.0]
        final = ["4:00", "4:00", "4:00"]
        refilled = False

    def circ_coin(d):
        return Text("●", size=d, color="#ffd76a", font="DejaVuSans.ttf")

    def give_coins(n):
        persistent.coins = (persistent.coins or 0) + n
        renpy.restart_interaction()

    def _slot_pick():
        bag = []
        for sym, weight, _pay in SLOT_SYMBOLS:
            bag += [sym] * weight
        return renpy.random.choice(bag)

    def slot_pay(sym):
        for s, _w, pay in SLOT_SYMBOLS:
            if s == sym:
                return pay
        return 0

    def slot_spin():
        if any(store.slot_spinning):
            return
        bet = store.casino_bet
        if (persistent.coins or 0) < bet:
            store.slot_msg = _("Not enough coins.")
            renpy.restart_interaction()
            return
        persistent.coins -= bet
        store.slot_stake = bet
        _SLOT.t = 0.0
        _SLOT.final = [_slot_pick() for _i in range(3)]
        _SLOT.stops = [1.0, 1.5, (3.0 if _SLOT.final[0] == _SLOT.final[1] else 2.0)]
        store.slot_tease = False
        store.slot_spinning = [True, True, True]
        store.slot_msg = ""
        store.slot_win = 0
        renpy.restart_interaction()

    def slot_tick():
        if not any(store.slot_spinning):
            return
        _SLOT.t += 0.07
        reels = list(store.slot_reels)
        spin = list(store.slot_spinning)
        for i in range(3):
            if spin[i]:
                if _SLOT.t >= _SLOT.stops[i]:
                    spin[i] = False
                    reels[i] = _SLOT.final[i]
                    if i == 1 and reels[0] == reels[1]:
                        store.slot_tease = True
                else:
                    reels[i] = _slot_pick()
        store.slot_reels = reels
        store.slot_spinning = spin
        if not any(spin):
            _slot_payout()
        renpy.restart_interaction()

    def _slot_payout():
        a, b, c = store.slot_reels
        store.slot_tease = False
        win = 0
        if a == b == c:
            win = slot_pay(a) * store.slot_stake
        elif a == b or b == c or a == c:
            win = SLOT_PAIR * store.slot_stake
        store.slot_win = win
        store.slot_streak = (store.slot_streak + 1) if win else 0
        if win:
            casino_pay(win)
        if a == b == c == "4:00":
            store.slot_msg = _("JACKKKPOTTTTTTT!")
            secret_found("slots_jackpot")
        elif win:
            store.slot_msg = _("+%d COINS") % win
        else:
            store.slot_msg = _("No luck.")
        secret_found("slots")

    def slot_refill():
        if not _SLOT.refilled and (persistent.coins or 0) < store.casino_bet:
            _SLOT.refilled = True
            give_coins(20)
            store.slot_msg = _("+20 COINS")

    def coins_to_ticket():
        if (persistent.coins or 0) >= COINS_PER_TICKET:
            persistent.coins -= COINS_PER_TICKET
            give_tickets(1)
            renpy.restart_interaction()


transform slot_in:
    alpha 0.0
    zoom 0.9
    easein_back 0.35 alpha 1.0 zoom 1.0

transform reel_flip(key):
    yzoom 0.2
    ease 0.06 yzoom 1.0

transform slot_win_pop:
    zoom 0.6
    alpha 0.0
    easein_back 0.3 zoom 1.0 alpha 1.0

screen slot_symbol(sym, size):
    if sym == "中":
        text sym:
            align (0.5, 0.5)
            size size
            color "#d83a2a"
            font MJ_FONT
    elif sym in ("♦", "♣"):
        text sym:
            align (0.5, 0.5)
            size size
            color ("#d83a2a" if sym == "♦" else "#e8e4dc")
            font "DejaVuSans.ttf"
    else:
        text sym:
            align (0.5, 0.5)
            size (int(size * 0.8) if sym == "4:00" else size)
            color ("#ffd76a" if sym in ("4:00", "7") else "#6dffa5")
            font CREDIT_FONT

transform slot_tease_pulse:
    alpha 0.4
    block:
        ease 0.25 alpha 1.0
        ease 0.25 alpha 0.4
        repeat

screen slot_machine():
    modal True
    zorder 310
    key "game_menu" action Hide("slot_machine")
    if any(slot_spinning):
        timer 0.07 repeat True action Function(slot_tick)

    add Solid("#000000c8")

    frame:
        align (0.5, 0.5)
        xysize (1180, 720)
        padding (40, 30)
        background rbox("#121218f4", 30)
        at slot_in
        vbox:
            xfill True
            spacing 18
            hbox:
                xfill True
                text _("4:00 SLOTS"):
                    size 40
                    color "#e6a817"
                    font CREDIT_FONT
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 12
                    add circ_coin(28):
                        yalign 0.5
                    text (_("COINS  %d") % (persistent.coins or 0)):
                        yalign 0.5
                        size 28
                        color "#ffd76a"
                        font GFONT

            frame:
                xalign 0.5
                padding (24, 20)
                background rbox(("#3a2a08" if (slot_reels[0] == slot_reels[1] == slot_reels[2] and not any(slot_spinning) and slot_win) else "#0a0a0e"), 24)
                hbox:
                    spacing 22
                    for i in range(3):
                        frame:
                            xysize (240, 220)
                            padding (0, 0)
                            background rbox(("#1a1a22" if slot_spinning[i] else "#22222c"), 18)
                            fixed:
                                at reel_flip((i, slot_reels[i], slot_spinning[i]))
                                use slot_symbol(slot_reels[i], 130)

            fixed:
                ysize 56
                if slot_tease:
                    text _("ONE MORE..."):
                        align (0.5, 0.5)
                        size 40
                        color "#ffd76a"
                        font CREDIT_FONT
                        at slot_tease_pulse
                elif slot_msg:
                    text slot_msg:
                        align (0.5, 0.5)
                        size 40
                        color ("#ffd700" if slot_win else "#8888a0")
                        font CREDIT_FONT
                        at slot_win_pop

            hbox:
                xalign 0.5
                spacing 40
                use casino_bet_picker(any(slot_spinning))
                if slot_streak >= 2:
                    text (_("WIN STREAK x%d") % slot_streak):
                        yalign 0.5
                        size 22
                        color "#6dffa5"
                        font GFONT

            hbox:
                xalign 0.5
                spacing 24
                use mg_btn((_("SPIN  (%d COINS)") % casino_bet), Function(slot_spin), w=320, h=70, size=26)
                if (persistent.coins or 0) < casino_bet and not any(slot_spinning):
                    use rbtn(_("SPOT ME 20"), Function(slot_refill), w=240, h=70, r=22, size=22)
                use rbtn(_("CLOSE"), Hide("slot_machine"), w=180, h=70, r=22, size=22)

            hbox:
                xalign 0.5
                spacing 26
                for sym, _w, pay in SLOT_SYMBOLS:
                    hbox:
                        spacing 8
                        fixed:
                            xysize (64, 36)
                            use slot_symbol(sym, 26)
                        text ("x%d" % pay):
                            yalign 0.5
                            layout "nobreak"
                            size 15
                            color "#8888a0"
                            font GFONT
                text (_("PAIR x%d") % SLOT_PAIR):
                    yalign 0.5
                    layout "nobreak"
                    size 15
                    color "#8888a0"
                    font GFONT
