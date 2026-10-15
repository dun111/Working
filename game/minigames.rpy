# ==============================================================================
# DEPARTURE AT 4:00  -  minigames.rpy
# Every minigame happens inside its carriage instead of a pop-up box.
#
#   A  lock       Carriage 1 cupboard   turn the key when it lines up
#   B  glass      Carriage 2 floor      sweep up the shards
#   C  mahjong    Carriage 2 table      mahjong solitaire with Shunyu
#   D  blocks     Carriage 3 rug        repeat Misha's pattern
#   E  engine     Carriage 4            keep the gauge in the green
#   F  mail       Carriage 5 desk       sort letters into pigeonholes
#
# Each one returns "win" or "lose" to the script (call screen mg_...).
# Layouts use the 1920x1080 design area, centred on any screen (display.rpy).
# ==============================================================================

init python:
    import math as _mgmath

    def _ring_points(cx, cy, radius, angles):
        """(angle, x, y) for marks placed round a dial; 0 degrees is straight up."""
        pts = []
        for a in angles:
            r = _mgmath.radians(a)
            pts.append((a, cx + radius * _mgmath.sin(r), cy - radius * _mgmath.cos(r)))
        return pts


# ------------------------------------------------------------------------------
# SHARED SCENE
# ------------------------------------------------------------------------------

transform mg_npc(x=0.86):
    xanchor 0.5
    xpos x
    yanchor 1.0
    ypos 1.0
    yoffset 40
    zoom 0.94
    alpha 0.0
    ease 0.4 alpha 0.9

transform mg_hud_in:
    alpha 0.0
    yoffset -16
    easein 0.3 alpha 1.0 yoffset 0

transform mg_pop:
    alpha 0.0
    zoom 0.92
    easein 0.25 alpha 1.0 zoom 1.0

# the carriage behind, the character watching, the game in the middle
screen mg_scene(title, hint="", bg="black", who=None, who_x=0.86, skippable=True):
    modal True
    zorder 300

    add bg
    add Solid("#0000004a")
    if who:
        add who at mg_npc(who_x)
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)
        alpha 0.75

    fixed:
        pos (MAP_X0, MAP_Y0)
        xysize (DESIGN_W, DESIGN_H)
        transclude

    # cheat: every minigame wins itself
    if persistent.cheat_autowin:
        timer 0.05 action Return("win")

    frame:
        pos (40, 36)
        padding (26, 16)
        background rbox("#0a0a0ecc", 22)
        at mg_hud_in
        vbox:
            spacing 4
            text title:
                size 28
                color "#ffd700"
                font GFONT
            if hint:
                text hint:
                    size 16
                    color "#c9c9d8"
                    font GFONT
                    xmaximum 760

    if skippable and persistent.mg_skip_allowed:
        fixed:
            xalign 0.98
            yalign 0.97
            xsize 160
            ysize 48
            use rbtn(_("SKIP"), Return("win"), w=160, h=48, r=14, size=20)

# counters in the top-right corner
screen mg_stats(items):
    frame:
        xalign 1.0
        xoffset -40
        ypos 36
        padding (24, 14)
        background rbox("#0a0a0ecc", 22)
        at mg_hud_in
        hbox:
            spacing 30
            for t in items:
                text t:
                    size 20
                    color "#e8e4dc"
                    font GFONT

screen mg_continue(result):
    # a game the story is waiting on can't be lost: it offers another go
    $ again = (result == "lose" and mg_required)
    hbox:
        xalign 0.5
        use rbtn((_("TRY AGAIN") if again else _("CONTINUE")), Return(result), w=260, h=58, r=22, size=24, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")

# the result card in the middle of the scene
screen mg_end(msg, result):
    add Solid("#0000006a")
    frame:
        align (0.5, 0.5)
        padding (64, 36)
        background rbox("#0a0a0ee6", 30)
        at mg_pop
        vbox:
            spacing 24
            text msg:
                xalign 0.5
                size 40
                color ("#ffd700" if result == "win" else "#e0521f")
                font GFONT
            use mg_continue(result)


# ---- simple pieces used by the newer minigames (minigames2.rpy / minigames3.rpy)

# the dark box in the middle that a game sits in
screen mg_box(w=1100, h=620):
    frame:
        xalign 0.5
        yalign 0.58
        xysize (w, h)
        padding (40, 36)
        background rbox("#0a0a0ee0", 30)
        fixed:
            transclude

# a plain bar:  use mg_meter(how_full, out_of)
screen mg_meter(v, vmax, w=600, h=26, col="#6dffa5"):
    fixed:
        xysize (w, h)
        add rbox("#ffffff22", h // 2)
        add rbox(col, h // 2):
            xsize max(h, min(w, int(w * v / float(vmax))))

# a big orange button
screen mg_btn(label, act, w=260, h=70, size=26):
    use rbtn(label, act, w=w, h=h, r=22, size=size, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")

style mg_big is text:
    xalign 0.5
    size 40
    color "#e8e4dc"
    font GFONT

style mg_small is text:
    xalign 0.5
    size 22
    color "#8888a0"
    font GFONT


# ==============================================================================
# A  -  THE LOCK  (Carriage 1 cupboard)
# ==============================================================================
# The key sits in the keyhole and swings back and forth. Turn it while it's
# inside the green marks on the dial to set a pin. 3 pins opens it, 3 slips
# and the lock jams.

define LP_SWING = 70          # how far the key swings each way (degrees)
define LP_CX = 960            # keyhole centre (design area)
define LP_CY = 520

default lp_pos = 0.0
default lp_dir = 1
default lp_pins = 0
default lp_fails = 0
default lp_zone = 0.4
default lp_w = 0.2
default lp_speed = 0.9
default lp_result = None

init python:
    # the key from the main menu, standing in the keyhole by the tip of its blade
    LP_KEY = Transform(Transform("images/Key.webp", crop=KEY_CROP), zoom=0.3)
    LP_KEY_TIP = (307.0 / KEY_CROP[2], 0.97)
    LP_TICKS = _ring_points(LP_CX, LP_CY, 150, range(-LP_SWING, LP_SWING + 1, 7))

    def lp_angle(pos):
        return (pos - 0.5) * 2 * LP_SWING

    def lockpick_reset():
        m = mg_mult()
        store.lp_pos = 0.0
        store.lp_dir = 1
        store.lp_pins = 0
        store.lp_fails = 0
        store.lp_result = None
        store.lp_w = 0.2 / m
        store.lp_speed = 0.9 * m
        store.lp_zone = renpy.random.uniform(0.15, 0.85 - store.lp_w)

    def lockpick_tick():
        if store.lp_result is not None:
            return
        store.lp_pos += store.lp_dir * store.lp_speed * 0.025
        if store.lp_pos >= 1.0:
            store.lp_pos = 1.0
            store.lp_dir = -1
        elif store.lp_pos <= 0.0:
            store.lp_pos = 0.0
            store.lp_dir = 1
        renpy.restart_interaction()

    def lockpick_turn():
        if store.lp_result is not None:
            return
        if store.lp_zone <= store.lp_pos <= store.lp_zone + store.lp_w:
            store.lp_pins += 1
            if store.lp_pins >= 3:
                store.lp_result = "win"
                mg_record("lockpick", "tumbler_talent")
            else:
                sfx("lock_click")
                store.lp_w = max(0.07, store.lp_w * 0.9)
                store.lp_speed *= 1.12
                store.lp_zone = renpy.random.uniform(0.1, 0.9 - store.lp_w)
        else:
            store.lp_fails += 1
            if store.lp_fails >= 3:
                store.lp_result = "lose"
                sfx("lose")
            else:
                sfx("lock_snap")
        renpy.restart_interaction()

transform lp_key_turn(start=0.0):
    rotate start
    ease 0.5 rotate 90

screen mg_lockpick():
    use mg_scene(_("PICK THE LOCK"), _("Turn the key (TURN or SPACE) while it's inside the green marks. Set 3 pins. 3 slips and it jams."), "bg carriage_1"):
        if lp_result is None:
            timer 0.025 repeat True action Function(lockpick_tick)
            key "K_SPACE" action Function(lockpick_turn)

        use mg_stats([_("Pins: %d / 3") % lp_pins, _("Slips: %d / 3") % lp_fails])

        # the cupboard door
        add rbox("#2e1a0e", 40):
            pos (548, 118)
            xysize (824, 884)
        add rbox("#4a2c18", 36):
            pos (560, 130)
            xysize (800, 860)
        add rbox("#55331d", 24):
            pos (600, 170)
            xysize (720, 300)
        add rbox("#55331d", 24):
            pos (600, 690)
            xysize (720, 260)

        # brass lock plate, keyhole, pins
        add rbox("#7a5518", 50):
            pos (LP_CX - 180, 330)
            xysize (360, 460)
        add rbox("#c08f34", 46):
            pos (LP_CX - 170, 340)
            xysize (340, 440)
        for i in range(3):
            add rbox("#ffd76a" if i < lp_pins else "#6a5228", 10):
                pos (LP_CX - 70 + i * 60 - 13, (382 if i < lp_pins else 400))
                xysize (26, 60)
        # dial marks round the keyhole (on the plate): green where the key will turn
        $ z0 = lp_angle(lp_zone)
        $ z1 = lp_angle(lp_zone + lp_w)
        for a, tx, ty in LP_TICKS:
            add rbox("#6dffa5" if z0 <= a <= z1 else "#5a3d14", 3):
                xysize (6, 24)
                anchor (0.5, 0.5)
                pos (int(tx), int(ty))
                transform_anchor True
                rotate a

        add rbox("#140c05", 26):
            pos (LP_CX - 26, LP_CY - 26)
            xysize (52, 52)
        add rbox("#140c05", 8):
            pos (LP_CX - 11, LP_CY)
            xysize (22, 74)

        # the key
        if lp_result == "win":
            add LP_KEY:
                anchor LP_KEY_TIP
                pos (LP_CX, LP_CY)
                transform_anchor True
                at lp_key_turn(lp_angle(lp_pos))
        else:
            add LP_KEY:
                anchor LP_KEY_TIP
                pos (LP_CX, LP_CY)
                transform_anchor True
                rotate lp_angle(lp_pos)

        if lp_result is None:
            fixed:
                pos (LP_CX - 130, 860)
                xysize (260, 64)
                use rbtn(_("TURN"), Function(lockpick_turn), w=260, h=64, r=22, size=28, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")
        elif lp_result == "win":
            use mg_end(_("CLICK!"), "win")
        else:
            use mg_end(_("The lock jams."), "lose")


# ==============================================================================
# B  -  SWEEP THE GLASS  (Carriage 2 floor)
# ==============================================================================

define SH_COUNT = 6

default sh_pos = []
default sh_got = [False] * 6
default sh_time = 30
default sh_result = None

init python:
    def shards_reset():
        store.sh_pos = [(renpy.random.randint(300, 1540), renpy.random.randint(680, 930),
                         renpy.random.randint(-70, 70), renpy.random.randint(64, 116))
                        for _i in range(SH_COUNT)]
        store.sh_got = [False] * SH_COUNT
        store.sh_time = int(30 / mg_mult())
        store.sh_result = None

    def shards_pick(i):
        if store.sh_result is not None:
            return
        store.sh_got[i] = True
        if all(store.sh_got):
            store.sh_result = "win"
            mg_record("shards", "sharp_eyes")
        renpy.restart_interaction()

    def shards_tick():
        if store.sh_result is not None or not mg_timed():
            return
        store.sh_time -= 1
        if store.sh_time <= 0:
            store.sh_time = 0
            store.sh_result = "lose"
        renpy.restart_interaction()

transform shard_glint(delay=0.0):
    alpha 0.75
    pause delay
    block:
        ease 0.9 alpha 1.0
        ease 0.9 alpha 0.7
        repeat

screen mg_shards():
    use mg_scene(_("SWEEP UP THE GLASS"), _("Click every shard on the floor before time runs out."), "bg carriage_2", "eduard neutral", 0.88):
        if sh_result is None and mg_timed():
            timer 1.0 repeat True action Function(shards_tick)

        $ stats = [_("Shards left: %d") % sh_got.count(False)]
        if mg_timed():
            $ stats.append(_("Time: %d") % sh_time)
        use mg_stats(stats)

        # floorboards
        add rbox("#2a1a10", 30):
            pos (240, 640)
            xysize (1440, 340)
        for i in range(5):
            add Solid("#1a100a"):
                pos (260, 700 + i * 60)
                xysize (1400, 3)

        for i, sp in enumerate(sh_pos):
            if not sh_got[i]:
                button:
                    pos (sp[0], sp[1])
                    xysize (sp[3], sp[3] // 3 + 8)
                    background rbox("#bfe6f2b0", 6)
                    hover_background rbox("#ffffff", 6)
                    action Function(shards_pick, i)
                    at tilt(sp[2]), shard_glint(i * 0.3)
                    add Solid("#ffffffcc"):
                        xysize (sp[3] // 2, 2)
                        pos (6, 4)

        if sh_result == "win":
            use mg_end(_("All swept up."), "win")
        elif sh_result == "lose":
            use mg_end(_("Out of time!"), "lose")


# ==============================================================================
# C  -  MAHJONG  (Carriage 2, Shunyu's table)
# ==============================================================================
# Mahjong solitaire: 36 tiles in three layers. Click two matching tiles that
# are free (nothing on top of them, and open on the left or right) to take
# them off the table. Clear it to win. Every deal is solvable.

define MJ_FONT = "gui/ReggaeOne-Regular.ttf"
define MJ_TW = 78               # tile size as drawn
define MJ_TH = 100
define MJ_ZOOM = 1.25           # tiles are shown this much bigger
define MJ_X0 = 594              # top-left of the bottom layer (design area)
define MJ_Y0 = 290
define MJ_LIFT = 10             # how far each layer is raised

# (column, row, layer)
define MJ_LAYOUT = (
    [(c, r, 0) for r in range(4) for c in range(6)] +
    [(c, r, 1) for r in (1, 2) for c in (1, 2, 3, 4)] +
    [(c, r, 2) for r in (1, 2) for c in (2, 3)]
)

default mj_face = []
default mj_gone = []
default mj_sel = None
default mj_result = None
default mj_time_left = 120
default mj_end_msg = ""

init python:
    MJ_NUMS = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
    MJ_WINDS = {"E": "東", "S": "南", "W": "西", "N": "北"}
    MJ_KINDS = (["c%d" % n for n in range(1, 10)] + ["d%d" % n for n in range(1, 10)] +
                ["b%d" % n for n in range(1, 10)] + ["wE", "wS", "wW", "wN"] + ["dR", "dG", "dW"])

    _MJ_FW, _MJ_FH = MJ_TW - 6, MJ_TH - 6
    _MJ_BLUE, _MJ_RED, _MJ_GREEN = "#1f4fa0", "#b0201a", "#1f7a3a"

    def _at(d, fx, fy):
        return At(d, Transform(xcenter=int(fx * _MJ_FW), ycenter=int(fy * _MJ_FH)))

    def _mj_dot(col, d):
        return Fixed(rbox(col, d // 2 + 1), At(rbox("#f4ecd6", d // 4 + 1), Transform(xcenter=d // 2, ycenter=d // 2, xysize=(d // 2, d // 2))),
                     At(rbox(col, d // 8 + 1), Transform(xcenter=d // 2, ycenter=d // 2, xysize=(d // 4, d // 4))),
                     xysize=(d, d))

    def _mj_stick(col, h):
        return Fixed(rbox(col, 4), At(Solid("#f4ecd6aa"), Transform(xcenter=4, ycenter=h // 2, xysize=(2, h - 6))),
                     xysize=(9, h))

    DOT_SPOTS = {
        1: ([(.5, .5)], 46), 2: ([(.5, .27), (.5, .73)], 30), 3: ([(.25, .2), (.5, .5), (.75, .8)], 24),
        4: ([(.3, .28), (.7, .28), (.3, .72), (.7, .72)], 26),
        5: ([(.3, .25), (.7, .25), (.5, .5), (.3, .75), (.7, .75)], 22),
        6: ([(x, y) for y in (.2, .5, .8) for x in (.3, .7)], 22),
        7: ([(.22, .14), (.5, .26), (.78, .38)] + [(x, y) for y in (.62, .86) for x in (.3, .7)], 18),
        8: ([(x, y) for y in (.14, .38, .62, .86) for x in (.3, .7)], 18),
        9: ([(x, y) for y in (.2, .5, .8) for x in (.2, .5, .8)], 18),
    }
    BAM_SPOTS = {
        2: [(.5, .3), (.5, .7)], 3: [(.5, .3), (.3, .7), (.7, .7)],
        4: [(.3, .3), (.7, .3), (.3, .7), (.7, .7)],
        5: [(.3, .3), (.7, .3), (.5, .5), (.3, .7), (.7, .7)],
        6: [(x, y) for y in (.3, .7) for x in (.25, .5, .75)],
        7: [(.5, .16)] + [(x, y) for y in (.5, .82) for x in (.25, .5, .75)],
        8: [(x, y) for y in (.3, .7) for x in (.2, .4, .6, .8)],
        9: [(x, y) for y in (.2, .5, .8) for x in (.25, .5, .75)],
    }

    def _mj_face(kind):
        suit, val = kind[0], kind[1:]
        kids = []
        if suit == "c":
            n = int(val)
            kids += [_at(Text(MJ_NUMS[n - 1], font=MJ_FONT, size=32, color="#1a1a1a"), .5, .27),
                     _at(Text("萬", font=MJ_FONT, size=32, color=_MJ_RED), .5, .73)]
        elif suit == "w":
            kids.append(_at(Text(MJ_WINDS[val], font=MJ_FONT, size=48, color="#1a1a1a"), .5, .5))
        elif kind == "dR":
            kids.append(_at(Text("中", font=MJ_FONT, size=52, color=_MJ_RED), .5, .5))
        elif kind == "dG":
            kids.append(_at(Text("發", font=MJ_FONT, size=48, color=_MJ_GREEN), .5, .5))
        elif kind == "dW":
            kids += [_at(Transform(rbox(_MJ_BLUE, 6), xysize=(50, 72)), .5, .5),
                     _at(Transform(rbox("#f4ecd6", 4), xysize=(40, 62)), .5, .5)]
        elif suit == "d":
            n = int(val)
            spots, size = DOT_SPOTS[n]
            cols = [_MJ_BLUE, _MJ_RED, _MJ_GREEN]
            for i, (fx, fy) in enumerate(spots):
                col = _MJ_RED if n == 1 else cols[(i + n) % 3]
                kids.append(_at(_mj_dot(col, size), fx, fy))
        elif kind == "b1":
            kids += [_at(_mj_stick(_MJ_GREEN, 58), .5, .56), _at(_mj_dot(_MJ_RED, 18), .5, .18)]
        else:
            n = int(val)
            spots = BAM_SPOTS[n]
            h = 22 if len(set(y for _x, y in spots)) >= 3 else 28
            for i, (fx, fy) in enumerate(spots):
                red = (n == 5 and i == 2) or (n == 7 and i == 0) or (n == 9 and i % 3 == 1)
                kids.append(_at(_mj_stick(_MJ_RED if red else _MJ_GREEN, h), fx, fy))
        return Fixed(*kids, xysize=(_MJ_FW, _MJ_FH))

    def _mj_tile(kind):
        return Fixed(
            At(Transform(rbox("#a8946a", 10), xysize=(MJ_TW, MJ_TH)), Transform(xpos=6, ypos=7)),
            Transform(rbox("#f4ecd6", 10), xysize=(MJ_TW, MJ_TH)),
            At(_mj_face(kind), Transform(xpos=3, ypos=3)),
            xysize=(MJ_TW + 6, MJ_TH + 7))

    # one picture per kind, built once
    MJ_TILE = dict((k, Transform(_mj_tile(k), zoom=MJ_ZOOM)) for k in MJ_KINDS)
    MJ_W, MJ_H = int(MJ_TW * MJ_ZOOM), int(MJ_TH * MJ_ZOOM)

    def mj_xy(i):
        c, r, l = MJ_LAYOUT[i]
        return (MJ_X0 + int(c * (MJ_TW + 2) * MJ_ZOOM) - l * MJ_LIFT,
                MJ_Y0 + int(r * (MJ_TH + 4) * MJ_ZOOM) - l * MJ_LIFT)

    def mj_free(i, gone=None):
        gone = store.mj_gone if gone is None else gone
        c, r, l = MJ_LAYOUT[i]
        left = right = False
        for j, (c2, r2, l2) in enumerate(MJ_LAYOUT):
            if j == i or gone[j]:
                continue
            if l2 == l + 1 and abs(c2 - c) < 1 and abs(r2 - r) < 1:
                return False
            if l2 == l and r2 == r:
                if c2 == c - 1:
                    left = True
                elif c2 == c + 1:
                    right = True
        return not (left and right)

    def mahjong_reset():
        """Deal by taking pairs off a full table in a legal order, so it's always solvable."""
        n = len(MJ_LAYOUT)
        kinds = renpy.random.sample(MJ_KINDS, n // 2)
        faces = None
        for _try in range(200):
            gone = [False] * n
            faces = [None] * n
            for k in kinds:
                free = [i for i in range(n) if not gone[i] and mj_free(i, gone)]
                if len(free) < 2:
                    faces = None
                    break
                a, b = renpy.random.sample(free, 2)
                faces[a] = faces[b] = k
                gone[a] = gone[b] = True
            if faces:
                break
        store.mj_face = faces
        store.mj_gone = [False] * n
        store.mj_sel = None
        store.mj_result = None
        store.mj_end_msg = ""
        store.mj_time_left = [180, 130, 95][persistent.mg_difficulty]

    def mj_moves_left():
        seen = set()
        for i in range(len(MJ_LAYOUT)):
            if not store.mj_gone[i] and mj_free(i):
                if store.mj_face[i] in seen:
                    return True
                seen.add(store.mj_face[i])
        return False

    def mahjong_pick(i):
        if store.mj_result is not None or store.mj_gone[i] or not mj_free(i):
            return
        s = store.mj_sel
        if s is None or s == i:
            store.mj_sel = None if s == i else i
        elif store.mj_face[s] == store.mj_face[i]:
            store.mj_gone[s] = store.mj_gone[i] = True
            store.mj_sel = None
            sfx("ui_click")
            if all(store.mj_gone):
                store.mj_result = "win"
                store.mj_end_msg = _("Table cleared!")
                if not mj_casino:
                    mg_record("mahjong", "high_roller_win")
            elif not mj_moves_left():
                store.mj_result = "lose"
                store.mj_end_msg = _("No more matches.")
        else:
            store.mj_sel = i
        renpy.restart_interaction()

    def mahjong_tick():
        if store.mj_result is not None or not mg_timed():
            return
        store.mj_time_left -= 1
        if store.mj_time_left <= 0:
            store.mj_time_left = 0
            store.mj_result = "lose"
            store.mj_end_msg = _("Out of time!")
        renpy.restart_interaction()

screen mahjong_minigame():
    use mg_scene(_("MAHJONG"), _("Match two free tiles with the same face. A tile is free if nothing is on it and one side is open."), "bg carriage_2", "shunyu neutral", 0.9, skippable=False):
        if mj_result is None and mg_timed():
            timer 1.0 repeat True action Function(mahjong_tick)

        $ stats = [_("Pairs left: %d") % (mj_gone.count(False) // 2)]
        if mj_casino:
            $ stats.append(_("Coins: +%d") % ((mj_gone.count(True) // 2) * CASINO_MJ_PAIR))
        if mg_timed():
            $ stats.append(_("Time: %d") % mj_time_left)
        use mg_stats(stats)

        # the table
        add rbox("#3e2412", 48):
            pos (440, 190)
            xysize (900, 700)
        add rbox("#1d5236", 40):
            pos (462, 212)
            xysize (856, 656)

        # tiles, bottom layer first
        for layer in range(3):
            for i, (c, r, l) in enumerate(MJ_LAYOUT):
                if l == layer and not mj_gone[i]:
                    $ tx, ty = mj_xy(i)
                    $ free = mj_free(i)
                    button:
                        pos (tx, ty)
                        xysize (MJ_W + 8, MJ_H + 9)
                        padding (0, 0)
                        background None
                        action (Function(mahjong_pick, i) if free else None)
                        add MJ_TILE[mj_face[i]]
                        if mj_sel == i:
                            add rbox("#e6a81788", 12):
                                xysize (MJ_W, MJ_H)
                        elif not free:
                            add rbox("#0000002e", 12):
                                xysize (MJ_W, MJ_H)

        if mj_result is None:
            fixed:
                pos (790, 960)
                xysize (200, 50)
                use rbtn(_("WALK AWAY"), Return("lose"), w=200, h=50, r=14, size=22)
        else:
            use mg_end(mj_end_msg, mj_result)


# ==============================================================================
# D  -  MISHA'S BLOCKS  (Carriage 3 rug)
# ==============================================================================

define MS_COLORS = ["#a83a2e", "#2c6a9c", "#2c8a4f", "#c9a21a"]
define MS_LIT    = ["#ff8a7a", "#7fcaff", "#7dffb0", "#fff08a"]
define MS_LETTERS = ["A", "B", "C", "D"]
define MS_ROUNDS = 4

default ms_seq = []
default ms_round = 1
default ms_step = -1
default ms_lit_i = None
default ms_phase = "show"
default ms_idx = 0
default ms_strikes = 0
default ms_result = None

init python:
    def blocks_reset():
        store.ms_seq = [renpy.random.randint(0, 3) for _i in range(MS_ROUNDS + 1)]
        store.ms_round = 1
        store.ms_step = -1
        store.ms_lit_i = None
        store.ms_phase = "show"
        store.ms_idx = 0
        store.ms_strikes = 0
        store.ms_result = None

    def blocks_show_step():
        if store.ms_phase != "show" or store.ms_result is not None:
            return
        n = store.ms_round + 1
        k = store.ms_step
        if k % 2 == 0:
            i = k // 2
            if i >= n:
                store.ms_phase = "input"
                store.ms_idx = 0
                store.ms_lit_i = None
            else:
                store.ms_lit_i = store.ms_seq[i]
        else:
            store.ms_lit_i = None
        store.ms_step += 1
        renpy.restart_interaction()

    def blocks_unlight():
        store.ms_lit_i = None
        renpy.restart_interaction()

    def blocks_pick(i):
        if store.ms_phase != "input" or store.ms_result is not None:
            return
        store.ms_lit_i = i
        n = store.ms_round + 1
        if store.ms_seq[store.ms_idx] == i:
            store.ms_idx += 1
            if store.ms_idx >= n:
                store.ms_round += 1
                if store.ms_round > MS_ROUNDS:
                    store.ms_result = "win"
                    mg_record("blocks", "block_party")
                else:
                    store.ms_phase = "show"
                    store.ms_step = -1
        else:
            store.ms_strikes += 1
            if store.ms_strikes >= [4, 3, 2][persistent.mg_difficulty]:
                store.ms_result = "lose"
            else:
                store.ms_phase = "show"
                store.ms_step = -1
        renpy.restart_interaction()

screen mg_blocks():
    use mg_scene(_("MISHA'S BLOCKS"), _("Watch the order the blocks light up, then click them in the same order."), "bg carriage_3", "misha neutral", 0.86):
        if ms_phase == "show" and ms_result is None:
            timer (0.6 / mg_mult()) repeat True action Function(blocks_show_step)
        if ms_phase == "input" and ms_lit_i is not None:
            timer 0.25 action Function(blocks_unlight)

        $ ms_max = [4, 3, 2][persistent.mg_difficulty]
        use mg_stats([_("Round %d / %d") % (min(ms_round, MS_ROUNDS), MS_ROUNDS),
                      _("Mistakes: %d / %d") % (ms_strikes, ms_max),
                      (_("WATCH") if ms_phase == "show" else _("YOUR TURN"))])

        # the rug
        add rbox("#4a1e1e", 120):
            pos (300, 560)
            xysize (1200, 380)
        add rbox("#6a2c28", 100):
            pos (340, 590)
            xysize (1120, 320)

        for i in range(4):
            $ bx = 420 + i * 260
            $ lit = (ms_lit_i == i)
            if lit:
                add rbox(MS_LIT[i] + "66", 50):
                    pos (bx - 30, 560)
                    xysize (240, 290)
            button:
                pos (bx, 600)
                xysize (180, 220)
                padding (0, 0)
                background None
                action Function(blocks_pick, i)
                at button_hover_anim
                # top face, then the front
                add rbox(MS_LIT[i] if lit else MS_LIT[i] + "aa", 14):
                    xysize (180, 60)
                add rbox(MS_LIT[i] if lit else MS_COLORS[i], 14):
                    ypos 40
                    xysize (180, 180)
                text MS_LETTERS[i]:
                    xalign 0.5
                    ypos 70
                    size 96
                    color "#ffffffcc"
                    font GFONT

        if ms_result == "win":
            use mg_end(_("Misha claps, once."), "win")
        elif ms_result == "lose":
            use mg_end(_("Misha knocks the tower over."), "lose")


# ==============================================================================
# E  -  ENGINE PRESSURE  (Carriage 4, with Ichora the engineer)
# ==============================================================================

define EP_GOAL = 12.0
define EP_CX = 960              # gauge centre (design area)
define EP_CY = 470

default ep_p = 50.0
default ep_drift = 4.0
default ep_ok = 0.0
default ep_t = 35.0
default ep_result = None

init python:
    def ep_angle(p):
        """Pressure 0-100 on a dial from -120 to +120 degrees."""
        return -120 + p * 2.4

    EP_TICKS = [(v,) + _ring_points(EP_CX, EP_CY, 196, [ep_angle(v)])[0] for v in range(0, 101, 5)]

    def engine_reset():
        m = mg_mult()
        store.ep_p = 50.0
        store.ep_drift = 4.0 * m
        store.ep_ok = 0.0
        store.ep_t = 35.0 / m
        store.ep_result = None

    def engine_tick():
        if store.ep_result is not None:
            return
        m = mg_mult()
        if renpy.random.random() < 0.07:
            store.ep_drift = renpy.random.uniform(-9.0, 13.0) * m
        store.ep_p += store.ep_drift * 0.1
        if 38.0 <= store.ep_p <= 64.0:
            store.ep_ok += 0.1
        if mg_timed():
            store.ep_t -= 0.1
        if store.ep_p >= 100.0 or store.ep_p <= 0.0:
            store.ep_p = max(0.0, min(100.0, store.ep_p))
            store.ep_result = "lose"
        elif store.ep_ok >= EP_GOAL:
            store.ep_result = "win"
            mg_record("engine", "full_steam")
        elif mg_timed() and store.ep_t <= 0.0:
            store.ep_result = "lose"
        renpy.restart_interaction()

    def engine_push(amount):
        if store.ep_result is not None:
            return
        store.ep_p = max(0.0, min(100.0, store.ep_p + amount))
        renpy.restart_interaction()

screen mg_engine():
    use mg_scene(_("KEEP STEAM PRESSURE STEADY"), _("Stoke the fire (UP) or vent steam (DOWN). Keep the needle in the green for 12 seconds. Hit 0 or 100 and it's over."), "bg carriage_4", "ichora neutral", 0.88):
        if ep_result is None:
            timer 0.1 repeat True action Function(engine_tick)
            key "K_UP" action Function(engine_push, 9)
            key "K_DOWN" action Function(engine_push, -9)

        $ stats = [_("Stable: %.1f / %d s") % (ep_ok, EP_GOAL)]
        if mg_timed():
            $ stats.append(_("Time: %d") % max(0, ep_t))
        use mg_stats(stats)

        # iron panel and the gauge
        add rbox("#1c1916", 44):
            pos (EP_CX - 430, 160)
            xysize (860, 800)
        add rbox("#7a5a24", 250):
            pos (EP_CX - 250, EP_CY - 250)
            xysize (500, 500)
        add rbox("#e6dcc0", 236):
            pos (EP_CX - 236, EP_CY - 236)
            xysize (472, 472)
        for v, a, tx, ty in EP_TICKS:
            $ major = (v % 25 == 0)
            add rbox("#2fa84f" if 38 <= v <= 64 else ("#c0301a" if (v > 85 or v < 15) else "#2a2420"), 2):
                xysize ((7, 34) if major else (4, 18))
                anchor (0.5, 0.5)
                pos (int(tx), int(ty))
                transform_anchor True
                rotate a
        text "PSI":
            xalign 0.5
            xoffset EP_CX - 960
            ypos EP_CY + 90
            size 26
            color "#2a2420"
            font GFONT
        add Solid("#b0201a"):
            xysize (8, 190)
            anchor (0.5, 0.95)
            pos (EP_CX, EP_CY)
            transform_anchor True
            rotate ep_angle(ep_p)
        add rbox("#1c1916", 22):
            pos (EP_CX - 22, EP_CY - 22)
            xysize (44, 44)

        # how long it's been steady
        add rbox("#0a0a0e", 10):
            pos (EP_CX - 300, 760)
            xysize (600, 20)
        add rbox("#6dffa5", 10):
            pos (EP_CX - 300, 760)
            xysize (max(20, int(600 * min(1.0, ep_ok / EP_GOAL))), 20)

        if ep_result is None:
            fixed:
                pos (EP_CX - 320, 840)
                xysize (300, 70)
                use rbtn(_("VENT  (DOWN)"), Function(engine_push, -9), w=300, h=70, r=22, size=24)
            fixed:
                pos (EP_CX + 20, 840)
                xysize (300, 70)
                use rbtn(_("STOKE  (UP)"), Function(engine_push, 9), w=300, h=70, r=22, size=24, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")
        elif ep_result == "win":
            use mg_end(_("Steady as she goes."), "win")
        else:
            use mg_end(_("The boiler shrieks."), "lose")


# ==============================================================================
# F  -  SORT THE MAIL  (Carriage 5, Pattison's desk)
# ==============================================================================

define ML_LETTERS = [
    ("Pendulum order #44 - rush", "clock"),
    ("Invoice: 800 brass cogs", "clock"),
    ("Clockwork quarterly report", "clock"),
    ("Mainspring parts, fragile", "clock"),
    ("FINAL NOTICE: last stop", "end"),
    ("Terminal arrival timetable", "end"),
    ("\"Open only at the end\"", "end"),
    ("Memorial service invitation", "end"),
    ("Counterfeit ticket stamps", "fake"),
    ("Forged wax seal: OFFICIAL", "fake"),
    ("Fake perkel notes x2000", "fake"),
    ("Return to sender: no such person", "fake"),
    ("Postcard: Wish you were here!", "friend"),
    ("Birthday card for Dorothy", "friend"),
    ("Letter from an old pal", "friend"),
    ("Thank-you note from a friend", "friend"),
]
# (pile, name on the pile, what goes in it)
define ML_BINS = [
    ("clock", _("CLOCK"), _("Clock parts\nand orders")),
    ("end", _("END"), _("The last stop\nand endings")),
    ("fake", _("FAKE"), _("Forged or\ncounterfeit")),
    ("friend", _("FRIEND"), _("Cards and\npersonal letters")),
]

default ml_letters = []
default ml_idx = 0
default ml_ok = 0
default ml_bad = 0
default ml_t = 9.0
default ml_fb = ""
default ml_result = None

init python:
    ML_COUNT = 10

    def mail_allowed():
        return [4, 3, 2][persistent.mg_difficulty]

    def mail_tmax():
        return 9.0 / mg_mult()

    def mail_reset():
        pool = list(ML_LETTERS)
        renpy.random.shuffle(pool)
        store.ml_letters = pool[:ML_COUNT]
        store.ml_idx = 0
        store.ml_ok = 0
        store.ml_bad = 0
        store.ml_t = mail_tmax()
        store.ml_fb = ""
        store.ml_result = None

    def _mail_next():
        store.ml_idx += 1
        store.ml_t = mail_tmax()
        if store.ml_bad > mail_allowed():
            store.ml_result = "lose"
        elif store.ml_idx >= ML_COUNT:
            store.ml_result = "win"
            mg_record("mail", "sorted")

    def mail_pick(bin_name):
        if store.ml_result is not None:
            return
        if store.ml_letters[store.ml_idx][1] == bin_name:
            store.ml_ok += 1
            store.ml_fb = "RIGHT PILE"
        else:
            store.ml_bad += 1
            store.ml_fb = "WRONG PILE"
        _mail_next()
        renpy.restart_interaction()

    def mail_tick():
        if store.ml_result is not None or not mg_timed():
            return
        store.ml_t -= 0.1
        if store.ml_t <= 0:
            store.ml_bad += 1
            store.ml_fb = "TOO SLOW"
            _mail_next()
        renpy.restart_interaction()

transform letter_in:
    on show:
        alpha 0.0
        yoffset 40
        easein 0.25 alpha 1.0 yoffset 0
    on hide:
        linear 0.1 alpha 0.0

screen mg_mail():
    use mg_scene(_("SORT THE MAIL"), _("Read the letter on the desk, then click the pile it belongs in. Each pile says what goes inside.") + "  " + _("\"This goes to the clock, while this goes to the end. This goes to the fake ones and this goes to the friend.\""), "bg carriage_5", "pattison neutral", 0.9):
        if ml_result is None and mg_timed():
            timer 0.1 repeat True action Function(mail_tick)

        $ ml_max = mail_allowed()
        $ stats = [_("Letter %d / %d") % (min(ml_idx + 1, ML_COUNT), ML_COUNT), _("Mistakes: %d / %d") % (ml_bad, ml_max)]
        if mg_timed() and ml_result is None:
            $ stats.append("%.1f" % ml_t)
        use mg_stats(stats)

        # pigeonholes
        for bi, (bkey, blabel, bdesc) in enumerate(ML_BINS):
            $ px = 330 + bi * 300
            button:
                pos (px, 200)
                xysize (260, 260)
                padding (0, 0)
                background rbox("#5a3a1e", 18)
                hover_background rbox("#8a5a2a", 18)
                action Function(mail_pick, bkey)
                sensitive (ml_result is None)
                add rbox("#140d07", 12):
                    pos (16, 16)
                    xysize (228, 170)
                text bdesc:
                    xalign 0.5
                    ycenter 101
                    text_align 0.5
                    size 22
                    color "#e6dcc0"
                    font GFONT
                add rbox("#c9a24a", 8):
                    xalign 0.5
                    ypos 200
                    xysize (170, 40)
                text blabel:
                    xalign 0.5
                    ypos 205
                    size 22
                    color "#2a1f10"
                    font GFONT

        # the desk and the letter on it
        add rbox("#3e2614", 30):
            pos (260, 640)
            xysize (1340, 360)
        for li in range(len(ml_letters)):
            showif li == ml_idx and ml_result is None:
                frame:
                    pos (560, 690)
                    xysize (740, 230)
                    background rbox("#efe3c4", 18)
                    at letter_in
                    add rbox("#b0201a", 6):
                        xalign 1.0
                        xoffset -10
                        ypos 6
                        xysize (54, 66)
                    text ml_letters[li][0]:
                        align (0.5, 0.55)
                        text_align 0.5
                        xmaximum 600
                        size 32
                        color "#2a1f10"
                        font GFONT
        if ml_result is None and ml_fb:
            text ml_fb:
                xalign 0.5
                xoffset -30
                ypos 940
                size 22
                color ("#6dffa5" if ml_fb == "RIGHT PILE" else "#ff7b6b")
                font GFONT

        if ml_result == "win":
            use mg_end(_("Every letter has a home."), "win")
        elif ml_result == "lose":
            use mg_end(_("The mail pile collapses."), "lose")

