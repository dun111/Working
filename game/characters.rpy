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

    ART_FILES = {"sebastian": "sebastion"}
    # kimmy_neutral.png still has a solid grey background, so it isn't used until it's cut out.
    ART_PENDING = {"kimmy"}

    def own_art(tag):
        if tag in ART_PENDING:
            return None
        path = "images/%s_neutral.png" % ART_FILES.get(tag, tag)
        if renpy.loadable(path):
            return path, renpy.image_size(path)[1]
        return None

    # Characters without their own sprite show nothing rather than a stand-in.
    def portrait(tag, scale=1.0):
        art = own_art(tag)
        if art:
            return sprite(tag, *art, scale=scale)
        return Null()

    MONSTER_TINT = TintMatrix("#ff7a6a") * SaturationMatrix(0.35) * BrightnessMatrix(-0.18)

    def monster(tag, base, scale=1.0):
        art = own_art(base)
        if art:
            path, src_h = art
            return Transform(Transform(_scaled(path, src_h, scale), matrixcolor=MONSTER_TINT),
                             function=IdleAnim(tag))
        return Null()

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


image eduard neutral    = portrait("eduard")
image kimmy neutral     = portrait("kimmy")
image himmel neutral    = portrait("himmel")
image sebastian neutral = portrait("sebastian")
image misha neutral     = portrait("misha", scale=0.72)
image misha stares      = portrait("misha", scale=0.72)
image agatha neutral    = portrait("agatha")
image pattison neutral  = portrait("pattison")
image alexander neutral = portrait("alexander")

image shunyu_monster neutral = At(
    monster("shunyu_monster", "shunyu", scale=1.08),
    monster_shudder, monster_glow)
image himmel_monster neutral = At(
    monster("himmel_monster", "himmel", scale=1.04),
    monster_shudder, monster_glow)
image conductor_monster neutral = At(
    monster("conductor_monster", "dorothy", scale=1.18),
    distortion_warp, monster_glow)


define talk_in = Dissolve(0.35)

transform talk_drift:
    xalign 0.5
    yalign 0.5
    zoom 1.12
    block:
        ease 14.0 xalign (0.5 if persistent.reduce_motion else 0.42) zoom (1.12 if persistent.reduce_motion else 1.16)
        ease 14.0 xalign (0.5 if persistent.reduce_motion else 0.58) zoom 1.12
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
image shunyu_dead = full_cover("images/shunyu_dead.webp")

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
    def _hs_label_cb(name, abnormal=False):
        if name == "part2_start":
            store.hs_done = set()
            store.coin_found = set()
            store.fares_paid = set()
        elif not main_menu and not name.startswith("_"):
            store.hs_done.add(name)

    config.label_callbacks.append(_hs_label_cb)

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
        ease 0.9 zoom (1.0 if persistent.reduce_motion else 1.25)
        ease 0.9 zoom 1.0
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
        ease 0.7 xoffset (0 if persistent.reduce_motion else dx)
        ease 0.7 xoffset 0
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

    def met_ever(flag):
        return _flag(flag) or flag in (persistent.met or set())

    def _remember_met(name, abnormal=False):
        if main_menu:
            return
        new = [m[3] for m in MANIFEST if m[3] and m[3] not in (persistent.met or set()) and _flag(m[3])]
        if new:
            persistent.met = set(persistent.met or set()) | set(new)

    config.label_callbacks.append(_remember_met)

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
define BOND_MAX = 5

# Presents you can send from the People screen: (id, name, coin price).
define PRESENTS = [
    ("tea",       _("Cup of Tea"),    4),
    ("bandages",  _("Bandages"),      4),
    ("flowers",   _("Flowers"),       5),
    ("stamps",    _("Stamps"),        5),
    ("sweets",    _("Sweets"),        6),
    ("notebook",  _("Notebook"),      7),
    ("whiskey",   _("Whiskey"),       8),
    ("toy_train", _("Toy Train"),     8),
    ("charm",     _("Lucky Charm"),   9),
    ("watch",     _("Pocket Watch"), 12),
    ("maple",     _("Maple Sugar"),  12),
]

# Each passenger's favourite present is worth two hearts instead of one.
define FAVOURITE_PRESENT = {
    "Dorothy": "tea",
    "Fedora": "notebook",
    "Eduard": "whiskey",
    "Shunyu": "charm",
    "Kimmy": "flowers",
    "Himmel": "watch",
    "Sebastian": "tea",
    "Misha": "toy_train",
    "Agatha": "bandages",
    "Ichora": "sweets",
    "Pattison": "stamps",
    "Alexander": "maple",
}

define FAVOURITE_LINES = {
    "Dorothy": "Oh! Proper tea... thank you, sir.",
    "Fedora": "A fresh notebook? Now I can write EVERYTHING down!",
    "Eduard": "Now that's the good stuff. I'll keep it behind the counter.",
    "Shunyu": "A lucky charm?! I can't stop winning now!",
    "Kimmy": "For me, sugar? Well aren't you sweet.",
    "Himmel": "A watch... so I'll know exactly when the next stop is.",
    "Sebastian": "Most kind, sir. I shall brew it properly.",
    "Misha": "A train! A little train, just like this one!",
    "Agatha": "Finally, someone who gets it. Thanks.",
    "Ichora": "Sweets! Hey, you're alright, buddy!",
    "Pattison": "Stamps! Every mailworker's dream.",
    "Alexander": "THE MAPLE SUGAR!!! You absolute legend!!!",
}

default persistent.favourites_found = set()
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
                # Coins are persistent but fares_paid isn't, so rolling back would charge the fare twice.
                renpy.block_rollback()
        elif lab and lab not in store.coin_found:
            store.coin_found = store.coin_found | set([lab])
            give_coins(COIN_FIND)
            renpy.show_screen("coin_toast", COIN_FIND)
            # Without this, rolling back and clicking again gives the same coins over and over.
            renpy.block_rollback()
        return renpy.run(act)

    def bond(name):
        return (persistent.bond or {}).get(name, 0)

    def present_price(pid):
        return dict((p, c) for p, _n, c in PRESENTS).get(pid, 0)

    def present_name(pid):
        return dict((p, n) for p, n, _c in PRESENTS).get(pid, "")

    def favourite_known(name):
        return name in (persistent.favourites_found or set())

    def gift(name, pid):
        price = present_price(pid)
        if bond(name) >= BOND_MAX or (persistent.coins or 0) < price:
            return
        persistent.coins -= price
        fav = FAVOURITE_PRESENT.get(name) == pid
        b = dict(persistent.bond or {})
        b[name] = min(BOND_MAX, bond(name) + (2 if fav else 1))
        persistent.bond = b
        if fav:
            persistent.favourites_found = set(persistent.favourites_found or set()) | set([name])
            renpy.notify("%s: \"%s\"  (FAVOURITE!)" % (name, FAVOURITE_LINES.get(name, "My favourite!")))
        else:
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
                $ fav = FAVOURITE_PRESENT.get(cur["name"])
                text (_("Loves: %s") % (present_name(fav) if favourite_known(cur["name"]) else "???")):
                    size 18
                    color "#e6a817"
                    font GFONT
                text (_("Hearts full. Thanks for the presents!") if hearts >= BOND_MAX else _("Presents are sent from the main menu.")):
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


# ---------- GIFT SHOP: opened by clicking the big 4:00 on the main menu four times ----------

init python:
    def gift_shop_people():
        return [{"img": m[0], "name": m[1], "known": met_ever(m[3])} for m in MANIFEST[1:]]

    def gift_shop_first():
        for i, p in enumerate(gift_shop_people()):
            if p["known"]:
                return i
        return 0

screen gift_shop():
    modal True
    zorder 300
    key "game_menu" action Hide("gift_shop")

    default sel = gift_shop_first()
    $ people = gift_shop_people()
    $ cur = people[sel]

    add Solid("#000000c8")

    frame:
        align (0.5, 0.5)
        xysize (1560, 900)
        padding (48, 36)
        background rbox("#0c0b09f4", 24)
        at fade_slide_in(0.0, xoff=0)

        vbox:
            spacing 6
            hbox:
                xfill True
                text _("GIFT SHOP"):
                    size 40
                    color "#ffd76a"
                    font CREDIT_FONT
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 10
                    add circ_coin(26):
                        yalign 0.5
                    text (_("%d COINS") % (persistent.coins or 0)):
                        yalign 0.5
                        size 22
                        color "#ffd76a"
                        font GFONT
            add Solid("#c9a24a55"):
                ysize 2
            null height 12

            hbox:
                spacing 36

                # passengers
                vbox:
                    spacing 6
                    xsize 380
                    for i, p in enumerate(people):
                        $ h = bond(p["name"]) if p["known"] else 0
                        button:
                            xsize 380
                            ysize 50
                            padding (18, 0)
                            background rbox(("#2a2312" if i == sel else "#14141a"), 14)
                            hover_background rbox("#3a3018", 14)
                            action (SetScreenVariable("sel", i) if p["known"] else None)
                            hbox:
                                xfill True
                                yalign 0.5
                                text (p["name"] if p["known"] else "???"):
                                    yalign 0.5
                                    size 20
                                    color (("#ffd700" if i == sel else "#e8e4dc") if p["known"] else "#4a4a58")
                                    font GFONT
                                if p["known"]:
                                    text ("♥" * h + "♡" * (BOND_MAX - h)):
                                        xalign 1.0
                                        yalign 0.5
                                        size 18
                                        color "#e0521f"
                                        font "DejaVuSans.ttf"

                # chosen passenger
                if cur["known"]:
                    $ hearts = bond(cur["name"])
                    $ fav = FAVOURITE_PRESENT.get(cur["name"])
                    fixed:
                        xsize 1060
                        ysize 720
                        add Transform(cur["img"], fit="contain", xysize=(400, 700)):
                            xalign 1.0
                            yalign 1.0
                        vbox:
                            spacing 12
                            xmaximum 620
                            text cur["name"]:
                                size 46
                                color "#ffffff"
                                font GFONT
                            text ("♥" * hearts + "♡" * (BOND_MAX - hearts)):
                                size 34
                                color "#e0521f"
                                font "DejaVuSans.ttf"
                            text (_("Loves: %s") % (present_name(fav) if favourite_known(cur["name"]) else "???")):
                                size 20
                                color "#e6a817"
                                font GFONT
                            null height 8
                            if hearts < BOND_MAX:
                                text _("Pick a present. Their favourite fills two hearts."):
                                    size 16
                                    color "#8888a0"
                                    font GFONT
                                vpgrid:
                                    cols 3
                                    spacing 10
                                    for pid, pname, price in PRESENTS:
                                        $ can = (persistent.coins or 0) >= price
                                        $ known_fav = favourite_known(cur["name"]) and pid == fav
                                        use rbtn("%s  ·  %d" % (pname, price), (Function(gift, cur["name"], pid) if can else None), w=196, h=50, r=14, size=15, bg=("#5a3a14" if known_fav else "#3e2814"), hov="#6a4a1c", col="#ffd76a", hcol="#ffffff")
                            else:
                                text _("Hearts full. Thanks for the presents!"):
                                    size 18
                                    color "#8888a0"
                                    font GFONT
                else:
                    text _("Meet someone on the train first."):
                        yalign 0.3
                        size 22
                        color "#8888a0"
                        font GFONT

        textbutton _("CLOSE"):
            xalign 1.0
            yalign 1.0
            padding (26, 10)
            background rbox("#1a1814", 12)
            hover_background rbox("#2a2620", 12)
            text_size 18
            text_color "#c9c0b0"
            text_hover_color "#ffffff"
            text_font GFONT
            action Hide("gift_shop")


# ---------- LOOK OUTSIDE: a zoomed view of one of Carriage 1's windows ----------

# One window of the Carriage 1 art, frame included (pixel art, so it's scaled with sharp pixels).
define WINDOW_VIEW_CROP = (830, 225, 260, 190)

image window_view_day = Transform("images/bg_carriage_1.webp", crop=WINDOW_VIEW_CROP, zoom=4.0, nearest=True)
image window_view_night = Transform("images/bg_carriage_1.webp", crop=WINDOW_VIEW_CROP, zoom=4.0, nearest=True,
                                    matrixcolor=TintMatrix("#3a4a8a") * SaturationMatrix(0.25) * BrightnessMatrix(-0.45))

transform window_zoom_in:
    alpha 0.0
    zoom (1.0 if persistent.reduce_motion else 0.55)
    easein 0.45 alpha 1.0 zoom 1.0

screen window_view(dark=False):
    add Solid("#000000c8") at window_zoom_in
    add ("window_view_night" if dark else "window_view_day"):
        xalign 0.5
        ycenter 0.4
        at window_zoom_in


# ---------- FULL-SCREEN POP: zooms in to fill the screen, gone after 2 seconds ----------

define POP_SECS = 2.0

transform pop_fill:
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    alpha 0.0
    zoom (1.0 if persistent.reduce_motion else 0.2)
    easein 0.3 alpha 1.0 zoom 1.0
    pause (POP_SECS - 0.6)
    easeout 0.3 alpha 0.0

transform pop_back:
    alpha 0.0
    ease 0.2 alpha 1.0
    pause (POP_SECS - 0.5)
    ease 0.3 alpha 0.0

# The tile art has a lot of transparent space around it; crop to the tile itself.
define TILE_CLOSEUP = Transform("images/clue_hidden_tile.webp", crop=(68, 304, 1317, 837))

screen fullscreen_pop(img, cover=False):
    zorder 350
    $ sw, sh = config.screen_width, config.screen_height
    button:
        xysize (sw, sh)
        padding (0, 0)
        background None
        action Hide("fullscreen_pop")
        add Solid("#000000e6") at pop_back
        add Transform(img, fit=("cover" if cover else "contain"), xysize=(sw, sh)) at pop_fill
    timer POP_SECS action Hide("fullscreen_pop")
