define SPRITE_H = 960

init -2 python:
    import math

    class IdleAnim(object):
        def __init__(self, tag):
            self.tag = tag

        def __call__(self, trans, st, at):
            if persistent.reduce_motion:
                trans.yzoom = 1.0
                trans.yoffset = 0
                return None
            trans.yzoom = 1.0 + 0.005 * math.sin(st * math.pi / 2.0)
            if TALK.typing == self.tag:
                trans.yoffset = -abs(math.sin(st * 6.0)) * 2.0
            else:
                trans.yoffset = 0
            return 1.0 / 30

    def _scaled(path, src_h, scale):
        return Transform(path, zoom=SPRITE_H * scale / float(src_h))

    def sprite(tag, path, src_h, scale=1.0):
        return Transform(_scaled(path, src_h, scale), function=IdleAnim(tag))

    def flat_color(color):
        r, g, b = Color(color).rgb
        return Matrix([0, 0, 0, r,
                       0, 0, 0, g,
                       0, 0, 0, b,
                       0, 0, 0, 1])

    def silhouette(tag, name, path, src_h, color, scale=1.0, label=True):
        shadow = Transform(_scaled(path, src_h, scale), matrixcolor=flat_color(color))
        if label:
            shadow = Fixed(
                shadow,
                Text(name.upper(), font=GFONT, size=26, color="#ffffff66",
                     xalign=0.5, yalign=0.82),
                fit_first=True)
        return Transform(shadow, function=IdleAnim(tag))

define LOUIS_PNG       = ("images/louis_neutral.png", 1323)
define FEDORA_PNG      = ("images/fedora_neutral.png", 1314)
define DOROTHY_PNG     = ("images/dorothy_neutral.png", 1305)
define DOROTHY_SAD_PNG = ("images/dorothy_sad.png", 1298)
define SHUNYU_PNG      = ("images/shunyu_neutral.png", 1341)
define ICHORA_PNG      = ("images/ichora_neutral.png", 1288)


image louis neutral        = sprite("louis", *LOUIS_PNG)
image louis confused       = sprite("louis", *LOUIS_PNG)
image louis looking_around = sprite("louis", *LOUIS_PNG)

image fedora neutral = sprite("fedora", *FEDORA_PNG)

image dorothy neutral   = sprite("dorothy", *DOROTHY_PNG)
image dorothy happy     = sprite("dorothy", *DOROTHY_PNG)
image dorothy confused  = sprite("dorothy", *DOROTHY_PNG)
image dorothy surprised = sprite("dorothy", *DOROTHY_PNG)
image dorothy sad       = sprite("dorothy", *DOROTHY_SAD_PNG)


image shunyu neutral = sprite("shunyu", *SHUNYU_PNG)
image shunyu excited = sprite("shunyu", *SHUNYU_PNG)

image ichora neutral = sprite("ichora", *ICHORA_PNG)


image eduard neutral    = silhouette("eduard", "Eduard", *LOUIS_PNG, color="#3b2a20")
image kimmy neutral     = silhouette("kimmy", "Kimmy", *DOROTHY_PNG, color="#4a2026")
image himmel neutral    = silhouette("himmel", "Himmel", *LOUIS_PNG, color="#203040")
image sebastian neutral = silhouette("sebastian", "Sebastian", *LOUIS_PNG, color="#202428")
image misha neutral     = silhouette("misha", "Misha", *LOUIS_PNG, color="#2a3a2a", scale=0.72)
image misha stares      = silhouette("misha", "Misha", *LOUIS_PNG, color="#2a3a2a", scale=0.72)
image agatha neutral    = silhouette("agatha", "Agatha", *FEDORA_PNG, color="#2a3438")
image pattison neutral  = silhouette("pattison", "Pattison", *LOUIS_PNG, color="#30283a")
image alexander neutral = silhouette("alexander", "Alexander", *LOUIS_PNG, color="#3a3a1e")

image shunyu_monster neutral = At(
    silhouette("shunyu_monster", "", *SHUNYU_PNG, color="#2a0c18", scale=1.08, label=False),
    monster_shudder, monster_glow)
image himmel_monster neutral = At(
    silhouette("himmel_monster", "", *LOUIS_PNG, color="#0c1e24", scale=1.04, label=False),
    monster_shudder, monster_glow)
image conductor_monster neutral = At(
    silhouette("conductor_monster", "", *DOROTHY_PNG, color="#1a0606", scale=1.18, label=False),
    distortion_warp, monster_glow)


define talk_in = Dissolve(0.35)

transform talk_drift:
    xalign 0.5
    yalign 0.5
    zoom 1.12
    block:
        ease anim_t(14.0) xalign 0.42 zoom 1.16
        ease anim_t(14.0) xalign 0.58 zoom 1.12
        repeat

init python:
    def talk_backdrop(path):
        normal = Fixed(At(full_cover(path), talk_drift), Solid("#0a0a0e66"))
        looped = Fixed(
            At(full_cover(path, matrixcolor=TintMatrix("#ff6a5a") * SaturationMatrix(0.5)), talk_drift),
            Solid("#1a000088"))
        return ConditionSwitch("in_loop", looped, "True", normal)

image talk_bg = talk_backdrop("images/bg_first_class.webp")
image talk_bar = talk_backdrop("images/bg_bar.webp")
image talk_sleeper = talk_backdrop("images/bg_sleeper.webp")

image talk to fedora    = "talk_bg"
image talk to eduard    = "talk_bar"
image talk to shunyu    = "talk_bar"
image talk to kimmy     = "talk_sleeper"
image talk to himmel    = "talk_sleeper"
image talk to sebastian = "talk_sleeper"
image talk to misha     = "talk_sleeper"
image talk to agatha    = "talk_bg"
image talk to ichora    = "talk_bg"
image talk to pattison  = "talk_bg"
image talk to alexander = "talk_bg"
image engine room       = "bg carriage_4"


image lights_dying:
    Solid("#000000")
    alpha 0.0
    linear 0.05 alpha 0.85
    linear 0.08 alpha 0.1
    pause 0.15
    linear 0.04 alpha 0.9
    linear 0.10 alpha 0.3
    pause 0.25
    linear 0.03 alpha 0.95
    linear 0.06 alpha 0.5
    pause 0.1
    linear 0.4 alpha 1.0

image door_light:
    Solid("#cfe3ff")
    alpha 0.0
    ease 1.2 alpha 0.35
    ease 1.6 alpha 0.12



transform clue_card_in:
    yoffset -40
    alpha 0.0
    easein anim_t(0.35) yoffset 0 alpha 1.0
    pause 2.6
    easeout anim_t(0.4) yoffset -30 alpha 0.0

screen clue_popup(kind, title, desc=""):
    zorder 120
    frame:
        xalign 0.5
        ypos 190
        padding (4, 4)
        background rbox("#e6a817", 14)
        at clue_card_in
        frame:
            padding (54, 20)
            background rbox("#17150de8", 12)
            vbox:
                spacing 6
                text kind:
                    xalign 0.5
                    size 18
                    color "#e6a817"
                    font GFONT
                text title:
                    xalign 0.5
                    size 38
                    color "#ffd700"
                    font GFONT
                    at gold_glow
                if desc:
                    text desc:
                        xalign 0.5
                        text_align 0.5
                        xmaximum 820
                        size 18
                        color "#e8e4dc"
                        font GFONT
    timer 3.4 action Hide("clue_popup")

init python:
    def _clue_text(var):
        for cid, title, text in CLUE_LIST:
            if cid == var:
                return title, text
        return None, ""

    def found_clue(var):
        already = bool(getattr(store, var, False))
        setattr(store, var, True)
        if already:
            return
        title, text = _clue_text(var)
        renpy.show_screen("clue_popup", _("NEW CLUE  (press J)"), title or var, text)

    def got_item(name, desc=""):
        renpy.show_screen("clue_popup", _("GOT ITEM"), name, desc)


define HS_CHECKED = "#7a7a88"
define HS_NUDGE = 20.0

default hs_done = set()

init python:
    def hs_checked(act):
        lab = getattr(act, "label", None)
        return bool(lab) and lab in store.hs_done

init 3 python:
    _old_label_cb_hs = config.label_callback

    def _hs_label_cb(name, abnormal=False):
        if name == "part2_start":
            store.hs_done = set()
            store.coin_found = set()
            store.fares_paid = set()
        elif not main_menu and not name.startswith("_"):
            store.hs_done.add(name)
        if _old_label_cb_hs:
            _old_label_cb_hs(name, abnormal)

    config.label_callback = _hs_label_cb

define HS_STYLE = {
    "talk": ("#e0521f", _("TALK")),
    "look": ("#e6a817", _("LOOK")),
    "door": ("#7fc8a9", _("NEXT CARRIAGE")),
    "back": ("#8888a0", _("BACK")),
    "decide": ("#a8281a", _("ACCUSE")),
}

define PIXEL_SHEET = "images/pixel_sprites.webp"
define PIXEL_CROPS = [
    (141, 45, 96, 134), (301, 51, 96, 128), (429, 38, 102, 141),
    (141, 198, 96, 154), (301, 218, 96, 128), (429, 205, 102, 141),
    (141, 378, 96, 121), (301, 384, 96, 141), (429, 371, 102, 154),
]
init python:
    PIXEL_PASSENGERS = [Transform(PIXEL_SHEET, crop=c, zoom=1.2, nearest=True) for c in PIXEL_CROPS]

transform hs_pulse:
    transform_anchor True
    rotate 45
    zoom 1.0
    block:
        ease anim_t(0.9) zoom 1.25
        ease anim_t(0.9) zoom 1.0
        repeat

transform hs_ring:
    transform_anchor True
    rotate 45
    alpha 0.0
    zoom 1.0
    block:
        alpha (0.0 if persistent.reduce_motion else 0.7)
        zoom 1.0
        linear 1.4 alpha 0.0 zoom 2.6
        pause 0.4
        repeat

transform hs_quiet:
    transform_anchor True
    rotate 45
    alpha 0.75

transform hs_nudge:
    transform_anchor True
    rotate 45
    alpha 0.0
    zoom 1.0
    pause HS_NUDGE
    block:
        ease 0.7 alpha (0.0 if persistent.reduce_motion else 0.45) zoom 1.8
        ease 0.7 alpha 0.0 zoom 1.0
        pause 0.3
        repeat

transform hs_in(delay=0.0):
    alpha 0.0
    pause anim_t(delay)
    ease anim_t(0.3) alpha 1.0

define DOOR_RIGHT = (1820, 340, 100, 400)
define DOOR_LEFT = (0, 340, 100, 400)

transform door_nudge(dx):
    xoffset 0
    block:
        ease anim_t(0.7) xoffset dx
        ease anim_t(0.7) xoffset 0
        repeat

transform hs_tag_always:
    alpha 1.0

transform hs_tag_hover:
    on idle:
        easeout anim_t(0.15) alpha 0.0
    on hover, selected_hover:
        easein anim_t(0.12) alpha 1.0

screen hs(rect, act, label="", kind="look", delay=0.0):
    $ hx, hy, hw, hh = rect
    $ hcol, hkind = HS_STYLE.get(kind, HS_STYLE["look"])
    $ checked = kind not in ("door", "back") and hs_checked(act)
    if kind not in ("door", "back"):
        $ hs_register(act)
    if checked:
        $ hcol = HS_CHECKED
    button:
        pos map_xy(hx, hy)
        xysize map_wh(hw, hh)
        action Function(hs_press, act, kind)
        background (rbox("#ff00ff40", 6) if persistent.cheat_hotspots else None)
        hover_background rbox(hcol + "26", 22)
        alt (hkind + " " + label)
        at hs_in(delay)

        $ on_head = (kind == "talk") and map_xy(hx, hy)[1] > 110
        $ edge = kind in ("door", "back")
        fixed:
            fit_first False
            xysize map_wh(hw, hh)

            if edge:
                text ("›" if kind == "door" else "‹"):
                    xalign 0.5
                    yalign 0.5
                    yoffset -10
                    size 84
                    font "DejaVuSans.ttf"
                    idle_color hcol
                    hover_color "#ffffff"
                    at door_nudge(10 if kind == "door" else -10)

            if not edge and checked:
                add Solid(hcol):
                    xysize (12, 12)
                    xalign 0.5
                    yalign (0.0 if on_head else 0.5)
                    yoffset (-14 if on_head else 0)
                    at hs_quiet
            elif not edge:
                add Solid(hcol):
                    xysize (30, 30)
                    xalign 0.5
                    yalign (0.0 if on_head else 0.5)
                    yoffset (-23 if on_head else 0)
                    at hs_nudge
                add Solid(hcol):
                    xysize (20, 20)
                    xalign 0.5
                    yalign (0.0 if on_head else 0.5)
                    yoffset (-18 if on_head else 0)
                    at hs_ring
                add Solid(hcol):
                    xysize (14, 14)
                    xalign 0.5
                    yalign (0.0 if on_head else 0.5)
                    yoffset (-15 if on_head else 0)
                    at hs_pulse

            frame:
                at (hs_tag_hover if persistent.hotspot_labels == "hover" else hs_tag_always)
                xalign ((1.0 if kind == "door" else 0.0) if edge else 0.5)
                xoffset ((-8 if kind == "door" else 8) if edge else 0)
                yalign (0.0 if on_head else 0.5)
                yoffset (-58 if on_head else (58 if edge else 34))
                padding (10, 3)
                idle_background rbox("#0a0a0ed8", 10)
                hover_background rbox(hcol, 10)
                hbox:
                    spacing 7
                    text hkind:
                        yalign 0.5
                        layout "nobreak"
                        size 11
                        font GFONT
                        idle_color hcol
                        hover_color "#0a0a0e"
                    if label:
                        text label:
                            yalign 0.5
                            layout "nobreak"
                            size 15
                            font GFONT
                            idle_color "#e8e4dc"
                            hover_color "#0a0a0e"


define MANIFEST = [
    ("louis neutral", "Louis", "\"I was tryna go home…\"", None, [
        (None, "\"Huh, I don't remember how I got here…\""),
        ("in_loop", "\"Man… This seems familiar…\""),
        ("in_loop", "\"I'm… back at the start?\""),
    ]),
    ("dorothy neutral", "Dorothy", "\"Excuse me sir, tickets please.\"", None, [
        (None, "\"I'm not paid enough for this\""),
        ("c2_p2_found_body", "\"R-right. Right! Stay here, don't- don't touch anything else.\""),
    ]),
    ("fedora neutral", "Fedora", "\"I CAN'T WAIT to interview the conductor!\"", "c1_talked_fedora", [
        (None, "\"I boarded this train to speak to the conductor after we arrive in Grekhov\""),
        ("in_loop", "\"I CAN'T WAIT to interview the KILLER.\""),
        ("c2_p2_found_body", "\"I told you to watch out.\""),
    ]),
    ("eduard neutral", "Eduard", "\"I'm Eduard, your bartender.\"", "c2_talked_eduard", [
        (None, "\"That mahjong monster almost got me out of whiskey!\""),
        ("c2_p2_reinterviewed_eduard", "\"I don't leave this counter during service, ask anyone.\""),
        ("clue_tile_mismatch", "\"That's not even from his hand.\""),
    ]),
    ("shunyu neutral", "Shunyu", "\"Playing Mahjong! Doncha just love winning!\"", "c2_talked_shunyu", [
        (None, "\"Yes! I can't stop winning!\""),
        ("c5_talked_alexander", "\"there's this guy that keeps winning money from gambling, yet still hasn't paid for his last portion.\""),
        ("c2_p2_found_body", "There's a jagged shard of glass buried in his side"),
    ]),
    ("kimmy neutral", "Kimmy", "\"My family has a clock business, so we're quite well off.\"", "c3_talked_kimmy", [
        (None, "\"I wanted to make it a trip so I could spend more time with my darling, Himmel.\""),
        ("kimmy_reinterviewed", "\"He said it was for his nerves.\""),
    ]),
    ("himmel neutral", "Himmel", "\"W-what do you want, stranger?\"", "c3_talked_himmel", [
        (None, "\"It's to the left! Now leave me alone!\""),
        ("clue_drug_wrapper", "\"Why would Himmel have this?\""),
        ("himmel_reinterviewed", "\"There's always a next stop...\""),
    ]),
    ("sebastian neutral", "Sebastian", "\"the butler for Mr. Popov, the child in this cabin.\"", "c3_talked_sebastian", [
        (None, "\"if any harm or distress befalls the child, you will be prosecuted.\""),
        ("sebastian_reinterviewed", "\"There are moments when a butler must step away.\""),
    ]),
    ("misha neutral", "Misha", "\"the child in this cabin.\"", "c3_talked_misha", [
        (None, "Misha stares, no response."),
        ("clue_hidden_tile", "\"This was under Misha's carpet the whole time.\""),
        ("misha_reinterviewed", "\"They always come back. Don't they?\""),
    ]),
    ("agatha neutral", "Agatha", "\"I deal with bodies, not motives.\"", "c4_talked_agatha", [
        (None, "\"Put the bandaid on and stop wasting my time.\""),
        ("clue_body_moved", "\"He didn't die in this chair. He was moved here after.\""),
        ("c2_p2_reinterviewed_agatha", "\"I was in the staff cabin.\""),
    ]),
    ("ichora neutral", "Ichora", "\"The name's Ichora, I'm the train's engineer.\"", "c4_talked_ichora", [
        (None, "\"We've been waiting for you a while.\""),
        ("has_key", "\"Don't hesitate.\""),
    ]),
    ("pattison neutral", "Pattison", "\"This goes to the clock, while this goes to the end.\"", "c5_talked_pattison", [
        (None, "\"It's okay, you will before the end.\""),
        ("clue_alexander_alibi", "\"I would've heard the door. It creaks something awful.\""),
    ]),
    ("alexander neutral", "Alexander", "\"The banned super maple sugar!!!\"", "c5_talked_alexander", [
        (None, "\"First one is free, next one is 2000 perkels.\""),
        ("alexander_reinterviewed", "\"Two men who owe me money, and one of 'em ends up dead\""),
        ("clue_alexander_alibi", "\"Ask the postman, he's always lurking round here too.\""),
    ]),
]

init python:
    def _flag(name):
        return name is None or bool(getattr(store, name, False))

    def manifest_rows():
        rows = []
        for img, name, role, met, notes in MANIFEST:
            known = _flag(met)
            rows.append({
                "img": img,
                "name": name if known else "???",
                "role": role if known else "",
                "known": known,
                "notes": [n for f, n in notes if _flag(f)] if known else [],
            })
        return rows

transform manifest_portrait(known=True):
    zoom 0.78
    matrixcolor (IdentityMatrix() if known else flat_color("#000000"))

transform manifest_thumb(known=True):
    crop (0, 0, 900, 560)
    zoom 0.15
    matrixcolor (IdentityMatrix() if known else flat_color("#1a1a22"))

define COIN_FIND = 4
define FARE = 8
define GIFT_COST = 5
define BOND_MAX = 5
define FARE_DOORS = ["c1_door_to_carriage_2", "carriage_3_start", "carriage_4_start", "carriage_5_start",
                     "c5_carriage6_door", "part2_chapter_end", "carriage_5_part2_start"]

default coin_found = set()
default fares_paid = set()
default hs_spots = {}
default persistent.bond = {}

define GIFT_LINES = {
    "Dorothy": ["...Oh...", "Are you fine… sir?", "Excuse me sir, tickets please."],
    "Fedora": ["Why Hello There! Whaddaya need?", "Now THAT'S a headline.", "Everything's a story if you wait long enough."],
    "Eduard": ["All the better for me, I reckon…", "Me?? I- I never even left the counter."],
    "Shunyu": ["JACKKKPOTTTTTTT!", "Yes! I can't stop winning!", "Playing Mahjong! Doncha just love winning!"],
    "Kimmy": ["Yawns… Hello, are you room service?", "Yeah, it's kinda obvious, matchstick.", "Don't worry Sugar, he's not dangerous… I think."],
    "Himmel": ["Of course!", "W-what do you want, stranger?", "It's to the left! Now leave me alone!"],
    "Sebastian": ["May I know your name, sir?", "It is a warning. For your own sake."],
    "Misha": ["...Oh.", "...Why would you say that?"],
    "Agatha": ["What, need help too?", "Actual infants…", "C'mon, put the bandage on."],
    "Ichora": ["Here ya go!", "Hey! I've been waiting for ya, buddy!", "Oh, I know."],
    "Pattison": ["Hello Sir, you another mailworker?", "It's okay, you will before the end.", "That's what I said, isn't it?"],
    "Alexander": ["The banned super maple sugar!!!", "Hahahaha… this stuff is so gooddddd….", "Depends? Are you a narc?"],
}

init python:
    def hs_register(act):
        lab = getattr(act, "label", None)
        if lab and lab not in store.hs_spots.get(DEV.label, ()):
            spots = dict(store.hs_spots)
            spots[DEV.label] = set(spots.get(DEV.label, ())) | set([lab])
            store.hs_spots = spots

    def fare_waived():
        return all(s in store.coin_found for s in store.hs_spots.get(DEV.label, ()))

    def hs_press(act, kind):
        lab = getattr(act, "label", None)
        if kind in ("door", "back"):
            if lab in FARE_DOORS and lab not in store.fares_paid:
                if (persistent.coins or 0) >= FARE:
                    persistent.coins -= FARE
                    renpy.show_screen("coin_toast", -FARE)
                elif not fare_waived():
                    renpy.notify(_("The door costs %d coins. Look around for more.") % FARE)
                    return
                store.fares_paid = store.fares_paid | set([lab])
        elif lab and lab not in store.coin_found:
            store.coin_found = store.coin_found | set([lab])
            give_coins(COIN_FIND)
            renpy.show_screen("coin_toast", COIN_FIND)
        return renpy.run(act)

    def bond(name):
        return (persistent.bond or {}).get(name, 0)

    def gift(name):
        if bond(name) >= BOND_MAX or (persistent.coins or 0) < GIFT_COST:
            return
        persistent.coins -= GIFT_COST
        b = dict(persistent.bond or {})
        b[name] = bond(name) + 1
        persistent.bond = b
        renpy.notify("%s: \"%s\"" % (name, renpy.random.choice(GIFT_LINES.get(name, ["..."]))))
        if b[name] == BOND_MAX:
            give_tickets(TICKETS_FOR["secret"])
            achievement.grant("bond_one")
            if all(b.get(m[1], 0) >= BOND_MAX for m in MANIFEST[1:]):
                achievement.grant("bond_all")
        renpy.restart_interaction()

define TOAST_BOTTOM = config.screen_height - 18 - 290 - 14

screen coin_toast(n):
    zorder 400
    frame:
        xpos 28
        yanchor 1.0
        ypos TOAST_BOTTOM
        padding (24, 12)
        background rbox("#14141aee", 18)
        at ticket_pop
        hbox:
            spacing 12
            add circ_coin(22):
                yalign 0.5
            text (("+%d COINS" if n > 0 else "%d COINS") % n):
                size 22
                color ("#ffd76a" if n > 0 else "#e0521f")
                font GFONT
    timer 2.0 action Hide("coin_toast")

screen coin_hud():
    zorder 41
    if not main_menu and active_map_any():
        frame:
            xpos 30
            ypos 18
            padding (16, 8)
            background rbox("#0a0806b0", 10)
            hbox:
                spacing 10
                add circ_coin(18):
                    yalign 0.5
                text ("%d" % (persistent.coins or 0)):
                    yalign 0.5
                    size 20
                    color "#ffd76a"
                    font GFONT

init python:
    def active_map_any():
        return any(renpy.get_screen(n) for n in MAP_TITLES)

    config.overlay_screens.append("coin_hud")

screen manifest():
    tag menu
    modal True

    default sel = 0

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    $ rows = manifest_rows()
    $ known_n = len([r for r in rows if r["known"]])
    $ cur = rows[sel]

    add Solid("#0a0a0e")
    use game_menu_nav

    text _("PASSENGER MANIFEST"):
        xpos 80
        ypos 50
        size 40
        color "#ffffff"
        font GFONT
        at fade_in(0.1)

    add rbox("#e0521f", 2):
        xpos 80
        ypos 105
        xsize 160
        ysize 6
        at underline_in

    text "[known_n] / [len(rows)] MET":
        xpos 80
        ypos 125
        size 20
        color "#e6a817"
        font GFONT

    $ grid_rows = (len(rows) + 1) // 2
    grid 2 grid_rows:
        xpos 80
        ypos 180
        spacing 8

        for idx, r in enumerate(rows):
            button:
                xsize 380
                ysize 100
                padding (12, 8)
                background rbox("#1d1a12" if idx == sel else "#101014", 18)
                hover_background rbox("#2a2a35", 18)
                action SetScreenVariable("sel", idx)
                at row_pop(min(idx * 0.03, 0.4))

                hbox:
                    spacing 14
                    fixed:
                        xysize (80, 84)
                        add r["img"]:
                            xalign 0.5
                            ypos 0
                            at manifest_thumb(r["known"])
                    vbox:
                        yalign 0.5
                        spacing 4
                        text r["name"]:
                            size 22
                            font GFONT
                            color ("#ffd700" if idx == sel else ("#e8e4dc" if r["known"] else "#55556a"))
                        text r["role"]:
                            size 14
                            font GFONT
                            color "#8888a0"
                            xmaximum 250

        if len(rows) % 2:
            null

    frame:
        xpos 880
        ypos 180
        xsize (config.screen_width - 960)
        ysize 760
        padding (36, 28)
        background rbox("#101014", 22)

        add cur["img"]:
            xalign 1.0
            yalign 1.0
            xoffset 20
            yoffset 30
            alpha 0.9
            at manifest_portrait(cur["known"])

        vbox:
            spacing 10
            xmaximum 560
            text cur["name"]:
                size 44
                color "#ffffff"
                font GFONT
            text cur["role"]:
                size 20
                color "#e6a817"
                font GFONT
            if cur["known"] and sel > 0:
                $ hearts = bond(cur["name"])
                hbox:
                    spacing 16
                    text ("♥" * hearts + "♡" * (BOND_MAX - hearts)):
                        yalign 0.5
                        size 30
                        color "#e0521f"
                        font "DejaVuSans.ttf"
                    if hearts < BOND_MAX:
                        use rbtn((_("GIFT %d COINS") % GIFT_COST), (Function(gift, cur["name"]) if (persistent.coins or 0) >= GIFT_COST else None), w=220, h=46, r=14, size=18, bg="#3e2814", hov="#5a3a1c", col="#ffd76a", hcol="#ffffff")
                text (_("You have %d coins") % (persistent.coins or 0)):
                    size 16
                    color "#8888a0"
                    font GFONT
            null height 16
            if cur["known"]:
                for n in cur["notes"]:
                    hbox:
                        spacing 12
                        add rbox("#e0521f", 2):
                            xysize (6, 6)
                            yoffset 11
                        text n:
                            size 20
                            color "#e8e4dc"
                            font say_font()
                            xmaximum 520
            else:
                text _("\"I don't even know anybody on this express.\""):
                    size 20
                    color "#55556a"
                    font GFONT

    use game_menu_back(back_action)
