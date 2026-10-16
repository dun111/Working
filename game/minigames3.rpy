# ==============================================================================
# DEPARTURE AT 4:00  -  minigames3.rpy
# More minigames:
#
#   N  evidence  Part 2       present the clue that proves them wrong
#   O  reveal    Carriage 6   wipe the shadow off each monster
#
#   $ evidence_setup("sebastian neutral", "Sebastian", "...line...", "clue_hidden_tile")
#   call play_required("mg_evidence", evidence_reset)
#
#   $ reveal_setup("The Passenger", "shunyu_monster neutral", "shunyu neutral", "Shunyu")
#   call play_required("mg_reveal", reveal_reset)
# ==============================================================================


# ==============================================================================
# N  -  PRESENT THE EVIDENCE
# ==============================================================================
# Someone says something your clues disprove. Pick the right one.

default ev_cfg = ("", "", "", "clue_hidden_tile", "black")   # image, name, line, answer, bg
default ev_result = None
default ev_pick = None

init python:
    def evidence_setup(img, name, line, answer, bg="black"):
        store.ev_cfg = (img, name, line, answer, bg)

    def evidence_reset():
        store.ev_result = None
        store.ev_pick = None

    def evidence_known(cid):
        return bool(getattr(store, cid, False)) or cid == store.ev_cfg[3]

    def evidence_pick(cid):
        if store.ev_result is not None:
            return
        store.ev_pick = cid
        if cid == store.ev_cfg[3]:
            store.ev_result = "win"
            sfx("win")
            mg_record("evidence")
        else:
            store.ev_result = "lose"
            sfx("thud")
        renpy.restart_interaction()

    def evidence_title(cid):
        for c, title, _text in CLUE_LIST:
            if c == cid:
                return title
        return cid

screen mg_evidence():
    $ ev_img, ev_name, ev_line, ev_answer, ev_bg = ev_cfg
    use mg_scene(_("PRESENT THE EVIDENCE"), _("Pick the clue that proves this wrong."), ev_bg, (ev_img or None), 0.86):

        # what they just said
        frame:
            xalign 0.5
            xoffset -150
            ypos 200
            xmaximum 1200
            padding (40, 26)
            background rbox("#0a0a0ee6", 26)
            vbox:
                spacing 8
                if ev_name:
                    text ev_name:
                        size 22
                        color "#e6a817"
                        font GFONT
                text "\"" + ev_line + "\"":
                    size 30
                    color "#e8e4dc"
                    font say_font()

        # the clue cards
        hbox:
            xalign 0.5
            xoffset -150
            ypos 520
            spacing 18
            for cid, title, desc in CLUE_LIST:
                $ known = evidence_known(cid)
                button:
                    xysize (250, 340)
                    padding (18, 18)
                    background rbox(("#2a2312" if known else "#14141a"), 22)
                    hover_background rbox("#4a3a14", 22)
                    action (Function(evidence_pick, cid) if known and ev_result is None else None)
                    at button_hover_anim
                    vbox:
                        spacing 12
                        text (title if known else "???"):
                            size 20
                            color ("#ffd700" if known else "#55556a")
                            font GFONT
                        if known:
                            text desc:
                                size 15
                                color "#e8e4dc"
                                font GFONT

        if ev_result == "win":
            use mg_end(evidence_title(ev_answer), "win")
        elif ev_result == "lose":
            use mg_end(_("WRONG"), "lose")


# ==============================================================================
# O  -  REVEAL  (Carriage 6)
# ==============================================================================
# Each monster is covered by a grid of shadow squares. Move the mouse over a
# square to wipe it away and see who it really was. Every so often it thrashes
# and some of the shadow comes back.

define RV_COLS = 6
define RV_ROWS = 8
define RV_CW = 87             # square size
define RV_CH = 70

default rv_cfg = ("The Conductor", "conductor_monster neutral", "conductor_monster neutral", "The Conductor")
default rv_dark = []          # True = still shadow
default rv_t = 25.0
default rv_thrash = 2.0
default rv_shake = 0
default rv_result = None

init python:
    def reveal_setup(name, monster_img, true_img, true_name):
        """name / monster image (what you fight), true image / name (what's under it)"""
        store.rv_cfg = (name, monster_img, true_img, true_name)

    def reveal_reset():
        store.rv_dark = [True] * (RV_COLS * RV_ROWS)
        store.rv_t = 25.0 / mg_mult()
        store.rv_thrash = 2.0
        store.rv_shake = 0
        store.rv_result = None

    def reveal_amount():
        return store.rv_dark.count(False) / float(len(store.rv_dark))

    def reveal_wipe(i):
        if store.rv_result is not None or not store.rv_dark[i]:
            return
        d = list(store.rv_dark)
        d[i] = False
        store.rv_dark = d
        if reveal_amount() >= 0.9:
            store.rv_result = "win"
            mg_record("reveal")
        renpy.restart_interaction()

    def reveal_tick():
        if store.rv_result is not None:
            return
        dt = 0.05
        # it fights back: a shudder, and the shadow grows back in places
        store.rv_thrash -= dt
        if store.rv_thrash <= 0:
            store.rv_thrash = renpy.random.uniform(1.6, 2.6) / mg_mult()
            store.rv_shake = 10
            sfx("screech")
            d = list(store.rv_dark)
            for i in renpy.random.sample(range(len(d)), [4, 6, 8][persistent.mg_difficulty]):
                d[i] = True
            store.rv_dark = d
        if store.rv_shake:
            store.rv_shake -= 1
        if mg_timed():
            store.rv_t -= dt
            if store.rv_t <= 0:
                store.rv_result = "lose"
        renpy.restart_interaction()

screen mg_reveal():
    $ rv_name, rv_monster, rv_true, rv_true_name = rv_cfg
    use mg_scene(_("REVEAL"), _("Move the mouse over the shadow to wipe it away. It will fight back."), "carriage_6"):
        if rv_result is None:
            timer 0.05 repeat True action Function(reveal_tick)

        $ stats = [rv_name, _("Revealed: %d%%") % int(reveal_amount() * 100)]
        if mg_timed():
            $ stats.append(_("Time: %d") % max(0, rv_t))
        use mg_stats(stats)

        fixed:
            xysize (RV_COLS * RV_CW, RV_ROWS * RV_CH)
            xalign 0.5
            yalign 0.62
            xoffset (((rv_shake % 2) * 2 - 1) * rv_shake * 3)
            # who it really was, underneath
            add rv_true:
                fit "contain"
                xysize (RV_COLS * RV_CW, RV_ROWS * RV_CH)
            # the shadow squares
            grid RV_COLS RV_ROWS:
                for i in range(RV_COLS * RV_ROWS):
                    button:
                        xysize (RV_CW, RV_CH)
                        padding (0, 0)
                        background (Solid("#3a0a10") if rv_dark[i] else None)
                        hover_background (Solid("#5a1018") if rv_dark[i] else None)
                        hovered Function(reveal_wipe, i)
                        action NullAction()

        if rv_result == "win":
            use mg_end(rv_true_name, "win")
        elif rv_result == "lose":
            use mg_end(_("You'll see."), "lose")
