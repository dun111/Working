# ==============================================================================
# DEPARTURE AT 4:00  -  slots.rpy
# SECRET: click DEPARTURES on the main menu's departure board.
# A slot machine that pays out COINS.
#
#   a spin costs your BET (casino.rpy, CASINO_BETS)
#   three the same pays BET x the symbol's number, two the same pays BET x SLOT_PAIR
#   three 4:00s is the jackpot
#   when the first two reels match, the last one spins a little longer
#
# Coins can be traded for tickets in EXTRAS > GAMEPASS (COINS_PER_TICKET).
#   $ give_coins(50)        hand out coins from anywhere
# ==============================================================================

default persistent.coins = 50

define SLOT_BET = 5            # the smallest bet
define SLOT_PAIR = 2            # two the same pays your bet x this
define COINS_PER_TICKET = 100

# symbol: (how often it comes up, three-of-a-kind pays your bet x this)
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
default slot_tease = False      # first two match: the last reel is taking its time

init python:
    class _SLOT(object):
        t = 0.0
        stops = [1.0, 1.5, 2.0]
        final = ["4:00", "4:00", "4:00"]
        refilled = False

    def circ_coin(d):
        return Fixed(
            Transform("gui/round/r256.png", xysize=(d, d), matrixcolor=TintMatrix("#c9921a")),
            At(Transform("gui/round/r256.png", xysize=(d - 6, d - 6), matrixcolor=TintMatrix("#ffd76a")),
               Transform(pos=(3, 3))),
            xysize=(d, d))

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
        # two the same: hold the last reel back for suspense
        _SLOT.stops = [1.0, 1.5, (3.0 if _SLOT.final[0] == _SLOT.final[1] else 2.0)]
        store.slot_tease = False
        store.slot_spinning = [True, True, True]
        store.slot_msg = ""
        store.slot_win = 0
        sfx("ui_click")
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
                    sfx("thud")
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
        else:
            sfx("lose")
        if a == b == c == "4:00":
            store.slot_msg = _("JACKKKPOTTTTTTT!")
            secret_found("slots_jackpot")
        elif win:
            store.slot_msg = _("+%d COINS") % win
        else:
            store.slot_msg = _("No luck.")
        secret_found("slots")

    def slot_refill():
        """Broke? Once per session the machine spots you a few coins."""
        if not _SLOT.refilled and (persistent.coins or 0) < store.casino_bet:
            _SLOT.refilled = True
            give_coins(20)
            store.slot_msg = _("+20 COINS")

    def coins_to_ticket():
        if (persistent.coins or 0) >= COINS_PER_TICKET:
            persistent.coins -= COINS_PER_TICKET
            give_tickets(1)
            renpy.restart_interaction()


# ------------------------------------------------------------------------------
# THE MACHINE
# ------------------------------------------------------------------------------

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

# the frame round the reels glows gold on a jackpot
transform slot_glow:
    alpha 0.0
    block:
        ease 0.3 alpha 1.0
        ease 0.3 alpha 0.3
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
            # header: the machine's name and your coins
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

            # the three reels
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

            # result
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

            # bet size and win streak
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

            # buttons
            hbox:
                xalign 0.5
                spacing 24
                use mg_btn((_("SPIN  (%d COINS)") % casino_bet), Function(slot_spin), w=320, h=70, size=26)
                if (persistent.coins or 0) < casino_bet and not any(slot_spinning):
                    use rbtn(_("SPOT ME 20"), Function(slot_refill), w=240, h=70, r=22, size=22)
                use rbtn(_("CLOSE"), Hide("slot_machine"), w=180, h=70, r=22, size=22)

            # what pays
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
