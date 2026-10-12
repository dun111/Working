init offset = -1

# ==============================================================================
# DEPARTURE AT 4:00  -  screens.rpy
# (minigames, burn transition, map look, EXTRAS menu and secrets are all in
#  this file. Do NOT keep a separate extras.rpy.)
#
# NOTE: references to image files that don't exist in game/images have been
# removed (rb_*.png, vignette.png, noise_*.png, bg carriage 2-4 .webp).
# ==============================================================================

# ==============================================================================
# FONTS & GLOBAL STYLES
# ==============================================================================

# rbox(color, radius) = a flat box tinted to any colour (alpha supported).
# (init -5 so styles below can use it)
init -5 python:
    def rbox(color, r=14):
        return Solid(Color(color))

    # --- shared helpers ------------------------------------------------------
    def anim_t(t):
        """Animation length that collapses to 0 when REDUCE MOTION is on."""
        try:
            return 0.0 if persistent.reduce_motion else t
        except Exception:
            return t

    def hover_lift(px):
        try:
            return 0 if persistent.reduce_motion else px
        except Exception:
            return px

    def sfx(name):
        """Play audio/<name>.wav on the sound channel (follows SOUND VOLUME)."""
        path = "audio/%s.wav" % name
        try:
            if renpy.loadable(path):
                renpy.play(path, channel="sound")
        except Exception:
            pass

    def sfx_sample():
        sfx("ui_click")

    # Achievement icons: first file that exists wins.
    ACH_ICON_UNLOCK = ["images/Achievement_Unlock.webp", "images/achievements/Achievement_Unlock.webp",
                       "gui/Achievement_Unlock.webp", "Achievement_Unlock.webp"]
    ACH_ICON_LOCK = ["images/Achievement_Lock.webp", "images/achievements/Achievement_Lock.webp",
                     "gui/Achievement_Lock.webp", "Achievement_Lock.webp"]

    def ach_default_icon(unlocked):
        for path in (ACH_ICON_UNLOCK if unlocked else ACH_ICON_LOCK):
            try:
                if renpy.loadable(path):
                    return path
            except Exception:
                pass
        return None

define GFONT = "gui/Graduate-Regular.ttf"

style default:
    font "gui/Graduate-Regular.ttf"

style button:
    padding (10, 6)

style button_text:
    font "gui/Graduate-Regular.ttf"
    size 28
    color "#8888a0"
    hover_color "#ffffff"
    selected_color "#ffd700"
    insensitive_color "#444455"

# Settings sliders / scrollbars. These are their own styles so they can't
# clash with the global slider style from gui.rpy.
style pref_bar:
    xsize 560
    ysize 18
    left_bar rbox("#e6a817", 8)
    right_bar rbox("#222233", 8)
    thumb Solid("#ffffff", xsize=10, ysize=18)
    hover_thumb Solid("#ffd700", xsize=10, ysize=18)
    left_gutter 0
    right_gutter 0
    thumb_offset 0

style pref_vbar:
    xsize 14
    bar_vertical True
    top_bar rbox("#222233", 4)
    bottom_bar rbox("#222233", 4)
    thumb Solid("#e6a817", xsize=14, ysize=90)
    hover_thumb Solid("#ffd700", xsize=14, ysize=90)
    top_gutter 0
    bottom_gutter 0
    thumb_offset 0

style say_window is default
style say_label is default
style say_dialogue is default

image pill_mask = Frame("images/pill_mask.png", 30, 30, 30, 30)

init python:
    def C(name, tag=None, **kwargs):
        return Character(name, **kwargs)

    config.overlay_screens.append("quick_menu")
    config.overlay_screens.append("clue_hotkey")

    # Soft UI sounds on every button (they follow SOUND VOLUME)
    try:
        if renpy.loadable("audio/ui_hover.wav"):
            style.default.hover_sound = "audio/ui_hover.wav"
        if renpy.loadable("audio/ui_click.wav"):
            style.default.activate_sound = "audio/ui_click.wav"
            config.sample_sound = "audio/ui_click.wav"
    except Exception:
        pass


# ==============================================================================
# SHARED LAYOUT CONSTANTS
# ==============================================================================

define gui.sidebar_width = 450
define gui.sidebar_margin = 28
define gui.sidebar_padding = 35
define gui.sidebar_content_width = gui.sidebar_width - (gui.sidebar_padding * 2)

define PREF_PANEL_W = 1380

# Key on the main menu.  KEY_SCALE 1.0 = the old size.  1.5 = 50% bigger.
define KEY_SCALE = 1.5
# (kept as an int: a float ypos means "fraction of the container" in Ren'Py)
define KEY_Y = int(-120 * KEY_SCALE)


# ==============================================================================
# TRANSFORMS
# ==============================================================================

transform key_drop:
    transform_anchor True
    anchor (0.5, 0.0)
    yoffset -1400
    rotate 0
    pause 0.4
    ease 1.1 yoffset 0
    block:
        ease 2.2 rotate 5
        ease 2.2 rotate -5
        repeat

# Used instead of key_drop when "Reduce motion" is on
transform key_static:
    anchor (0.5, 0.0)
    yoffset 0

transform menu_bg_drift:
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    zoom 1.06
    ease 25.0 zoom 1.14
    ease 25.0 zoom 1.06
    repeat

transform menu_bg_still:
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    zoom 1.06

transform streak(dur=3.0, delay=0.0):
    alpha 0.0
    xpos 1.05
    pause delay
    block:
        xpos 1.05
        alpha 0.8
        linear dur xpos -0.3
        repeat

# Embers drifting up the main menu
transform ember(dur=9.0, delay=0.0, sway=40):
    alpha 0.0
    ypos 1.05
    pause delay
    block:
        ypos 1.05
        xoffset 0
        alpha 0.0
        parallel:
            linear dur ypos -0.05
        parallel:
            ease dur*0.25 alpha 0.75
            pause dur*0.5
            ease dur*0.25 alpha 0.0
        parallel:
            ease dur*0.5 xoffset sway
            ease dur*0.5 xoffset -sway
        repeat

transform boot_logo_anim:
    xalign 0.5
    yalign 0.5
    alpha 0.0
    zoom 0.9
    ease 1.0 alpha 1.0 zoom 1.0
    pause 1.5
    ease 0.8 alpha 0.0

transform fade_slide_in(delay=0.0, xoff=-40, final_xoff=0):
    alpha 0.0
    xoffset xoff
    pause delay
    ease 0.5 alpha 1.0 xoffset final_xoff

transform fade_in(delay=0.0):
    alpha 0.0
    pause delay
    ease 0.6 alpha 1.0

transform loading_pulse:
    alpha 0.4
    linear 0.6 alpha 1.0
    linear 0.6 alpha 0.4
    repeat

transform notify_anim:
    alpha 0.0 yoffset 20
    ease 0.25 alpha 1.0 yoffset 0
    pause 2.5
    ease 0.5 alpha 0.0

transform confirm_pop:
    alpha 0.0 zoom 0.9
    ease anim_t(0.3) alpha 1.0 zoom 1.0

transform train_shake:
    xoffset 0
    yoffset 0
    block:
        linear 0.06 xoffset -2 yoffset 2
        linear 0.06 xoffset 2 yoffset -2
        linear 0.06 xoffset -2 yoffset 1
        linear 0.06 xoffset 2 yoffset 2
        linear 0.06 xoffset -1 yoffset -2
        linear 0.06 xoffset -1 yoffset 0
        repeat 15
    pause 8.0
    repeat

transform no_shake:
    pass

# Hover = a small lift. Offsets never change layout size, so neighbouring
# buttons no longer jitter.
transform button_hover_anim:
    yoffset 0
    on hover:
        easein anim_t(0.14) yoffset hover_lift(-3)
    on idle:
        easeout anim_t(0.22) yoffset 0
    on selected_hover:
        easein anim_t(0.14) yoffset hover_lift(-3)
    on selected_idle:
        easeout anim_t(0.22) yoffset 0

transform blackberry_click_pulse:
    zoom 1.0
    ease 0.15 zoom 1.3
    ease 0.25 zoom 1.0

transform qm_shown:
    alpha 0.0
    ease 0.25 alpha 1.0

transform qm_hidden:
    alpha 1.0
    ease 0.25 alpha 0.0

transform underline_grow:
    xzoom 0.001
    on hover:
        ease 0.25 xzoom 1.0
    on idle:
        ease 0.2 xzoom 0.001

transform entry_bar:
    transform_anchor True
    yzoom 0.001
    on hover:
        ease 0.22 yzoom 1.0
    on idle:
        ease 0.18 yzoom 0.001

transform underline_in(delay=0.2):
    xzoom 0.001
    pause delay
    ease 0.6 xzoom 1.0

transform fill_grow(delay=0.3):
    xzoom 0.001
    pause delay
    ease 0.9 xzoom 1.0

transform entry_arrow:
    xoffset 0
    on hover:
        ease 0.15 xoffset 8
    on idle:
        ease 0.15 xoffset 0

transform shine_sweep(delay=1.5):
    alpha 0.0
    xpos -90
    pause delay
    block:
        alpha 0.25
        xpos -90
        linear 0.9 xpos 420
        alpha 0.0
        pause 3.5
        repeat

transform nudge_hover:
    xoffset 0
    on hover:
        ease 0.12 xoffset 6
    on idle:
        ease 0.12 xoffset 0

# Choices pop up one after another
transform choice_in(delay=0.0):
    alpha 0.0
    yoffset 26
    pause anim_t(delay)
    easein anim_t(0.3) alpha 1.0 yoffset 0

# Breathing glow for a highlighted thing (name tag / next arrow)
transform soft_pulse:
    alpha 0.45
    ease 0.8 alpha 1.0
    ease 0.8 alpha 0.45
    repeat

transform next_arrow_bob:
    yoffset 0
    block:
        ease 0.5 yoffset 6
        ease 0.5 yoffset 0
        repeat

# Dialogue box slides up whenever the say screen appears
transform say_rise:
    yoffset 40 alpha 0.0
    easein anim_t(0.22) yoffset 0 alpha 1.0

# A heartbeat for Part 2's red tint
transform heartbeat:
    alpha 0.04
    block:
        ease 0.18 alpha 0.14
        ease 0.22 alpha 0.04
        pause 0.12
        ease 0.16 alpha 0.11
        ease 0.5 alpha 0.04
        pause 0.9
        repeat

transform tilt(a=0):
    transform_anchor True
    rotate a

# --- AUTOMATIC SPEAKER FOCUS ---------------------------------------------------
# Script lines like  show louis neutral at speaker_focus(xalign=0.1)  still work
# exactly as before. On top of that, EVERY line of dialogue now re-focuses the
# scene automatically: the speaker's sprite zooms up and brightens, every other
# sprite shrinks and dims. Positions are remembered from your show statements.

transform _sp_focus(xalign=0.7):
    xanchor 0.5
    xalign xalign
    yalign 1.0
    yoffset 40
    linear anim_t(0.3) zoom 1.08 alpha 1.0

transform _sp_bg(xalign=0.3):
    xanchor 0.5
    xalign xalign
    yalign 1.0
    yoffset 40
    linear anim_t(0.3) zoom 0.94 alpha 0.55

# tag -> (xalign, "f" focused / "b" background) for every sprite shown on master
default sprite_info = {}
# is the in-game train rumble currently applied?
default rumble_on = False

init python:
    _STRING_TYPES = (type(u""), type(""))

    # variable used in the script  ->  image tag of that character's sprite
    SPEAKER_TAGS = {
        "d": "dorothy", "l": "louis", "f": "fedora",
        "ed": "eduard", "s": "shunyu", "k": "kimmy",
        "h": "himmel", "seb": "sebastian", "mi": "misha", "a": "agatha",
        "ic": "ichora", "p": "pattison", "al": "alexander",
        "shunyu_monster": "shunyu_monster",
        "himmel_monster": "himmel_monster",
        "conductor_monster": "conductor_monster",
    }

    _sp_pending = {}

    def _make_speaker_transform(base, state):
        def make(xalign=0.5):
            t = base(xalign=xalign)
            _sp_pending["obj"] = t
            _sp_pending["val"] = (float(xalign), state)
            return t
        return make

    # Used all over script.rpy as  "at speaker_focus(xalign=..)"
    speaker_focus = _make_speaker_transform(_sp_focus, "f")
    speaker_background = _make_speaker_transform(_sp_bg, "b")

    # remember where every sprite was placed
    _orig_show = config.show

    def _show_track(name, at_list=[], *args, **kwargs):
        try:
            obj = _sp_pending.get("obj")
            if obj is not None and any(t is obj for t in (at_list or [])):
                if kwargs.get("layer") in (None, "master"):
                    tag = kwargs.get("tag")
                    if not tag:
                        nm = name if isinstance(name, (tuple, list)) else str(name).split()
                        tag = nm[0]
                    info = getattr(store, "sprite_info", None)
                    if info is not None:
                        info[tag] = _sp_pending["val"]
            _sp_pending.clear()
        except Exception:
            pass
        return _orig_show(name, at_list, *args, **kwargs)

    config.show = _show_track

    # re-focus the scene whenever someone starts talking
    def _focus_cb(event, interact=True, **kwargs):
        if event != "begin":
            return
        try:
            apply_rumble()
        except Exception:
            pass
        try:
            who = getattr(store, "_last_say_who", None)
            tag = SPEAKER_TAGS.get(who) if isinstance(who, _STRING_TYPES) else None
            info = getattr(store, "sprite_info", None)
            if not tag or info is None:
                return
            if renpy.get_attributes(tag) is None:
                return      # the speaker has no sprite on screen: leave everyone as is
            for t in list(info.keys()):
                attrs = renpy.get_attributes(t)
                if attrs is None:
                    del info[t]
                    continue
                x, st = info[t]
                want = "f" if t == tag else "b"
                if st == want:
                    continue
                fn = speaker_focus if want == "f" else speaker_background
                tr = fn(xalign=x)
                _sp_pending.clear()
                renpy.show(" ".join((t,) + tuple(attrs)), at_list=[tr])
                info[t] = (x, want)
        except Exception:
            pass

    config.all_character_callbacks = [c for c in config.all_character_callbacks
                                      if getattr(c, "__name__", "") != "_focus_cb"] + [_focus_cb]

# Carriage 6 transforms
transform monster_shudder:
    yoffset 0
    block:
        linear 0.1 yoffset 2
        linear 0.1 yoffset -2
        repeat

transform monster_glow:
    alpha 0.8
    linear 2.0 alpha 1.0
    linear 2.0 alpha 0.8
    repeat

transform distortion_warp:
    zoom 1.0
    block:
        linear 0.3 zoom 1.05
        linear 0.3 zoom 0.95
        repeat

transform carriage_6_ambient:
    alpha 0.0
    linear 3.0 alpha 0.3
    linear 3.0 alpha 0.0
    repeat

# --- settings / achievements animations ---------------------------------------

transform row_pop(delay=0.0):
    alpha 0.0
    yoffset 18
    pause delay
    easein 0.35 alpha 1.0 yoffset 0

# for content inside "showif": slides in on show, slides out on hide
transform tab_page:
    on appear:
        alpha 1.0
        xoffset 0
    on show:
        alpha 0.0
        xoffset 36
        easein 0.32 alpha 1.0 xoffset 0
    on hide:
        easeout 0.16 alpha 0.0 xoffset -28

# same, but the old list vanishes almost instantly (lists differ in height)
transform list_page:
    on appear:
        alpha 1.0
        yoffset 0
    on show:
        alpha 0.0
        yoffset 20
        easein 0.3 alpha 1.0 yoffset 0
    on hide:
        linear 0.01 alpha 0.0

transform tab_ind_in:
    alpha 0.0
    xoffset -10
    easein 0.25 alpha 1.0 xoffset 0

transform gold_glow:
    alpha 0.85
    ease 1.2 alpha 1.0
    ease 1.2 alpha 0.85
    repeat

transform ach_toast_anim:
    xoffset 520
    alpha 0.0
    easein 0.5 xoffset 0 alpha 1.0
    pause 3.8
    easeout 0.5 xoffset 520 alpha 0.0

transform toast_timer:
    xzoom 1.0
    linear 4.3 xzoom 0.0


# ==============================================================================
# IMAGES
# ==============================================================================

image carriage_6 = Solid("#0a0a0e")
image carriage_6_fog = At(Solid("#4a0a0a"), carriage_6_ambient)
image shunyu_monster neutral = Solid("#4a2a4a", xsize=420, ysize=760)
image himmel_monster neutral = Solid("#2a4a4a", xsize=420, ysize=760)
image conductor_monster neutral = Solid("#4a4a2a", xsize=520, ysize=900)

image black = Solid("#000000")
image Train station = Solid("#1a1a24")
image bg carriage_1 = "images/bg_carriage_1.webp"
image bg carriage_5 = "images/bg_carriage_5.webp"

# Placeholder backgrounds: the real bg carriage 2/3/4 .webp files are not in
# the project yet. Replace each Solid with "images/bg_carriage_N.webp" once the
# art is added.
image bg carriage_2 = Solid("#2a2430")
image bg carriage_3 = Solid("#242a30")
image bg carriage_4 = Solid("#2a3024")

image talk to fedora = "bg carriage_1"
image talk to eduard = "bg carriage_2"
image talk to shunyu = "bg carriage_2"
image talk to kimmy = "bg carriage_3"
image talk to himmel = "bg carriage_3"
image talk to sebastian = "bg carriage_3"
image talk to misha = "bg carriage_3"
image talk to agatha = "bg carriage_4"
image talk to ichora = "bg carriage_4"
image engine room = "bg carriage_4"
image talk to pattison = "bg carriage_5"
image talk to alexander = "bg carriage_5"

# Part 2 look: a flat red tint with a pulsing heartbeat wash on top
screen loop_overlay():
    zorder 50
    add Solid("#3a000020")
    add Solid("#ff2a1a") at heartbeat


# ==============================================================================
# GLOBAL TRANSITIONS
# ==============================================================================

define config.enter_transition = Dissolve(0.3)
define config.exit_transition = Dissolve(0.3)
define config.intra_transition = Dissolve(0.25)
define config.window_show_transition = Dissolve(0.2)
define config.window_hide_transition = Dissolve(0.2)
define config.after_load_transition = Dissolve(0.4)
define config.end_game_transition = Dissolve(0.6)
define config.main_game_transition = Dissolve(0.5)
define config.game_main_transition = Dissolve(0.5)
define config.say_attribute_transition = Dissolve(0.2)
define config.say_attribute_transition_layer = "master"


# ==============================================================================
# MENU MUSIC
# ==============================================================================

define audio.menu_theme = "gui/main_menu.mp3"

init python:
    # Only set the menu music if the file is actually in the project
    if renpy.loadable("gui/main_menu.mp3"):
        config.main_menu_music = "gui/main_menu.mp3"

    def menu_music_filter_on():
        if not persistent.menu_echo:
            return
        try:
            import renpy.audio.filter as af
            echo = af.Sequence([
                af.Multiply(1.6),
                af.Comb(delay=0.3, multiplier=0.35, wet=True),
            ])
            renpy.music.set_audio_filter("music", echo, replace=True)
        except Exception:
            pass

    def menu_music_filter_off():
        try:
            renpy.music.set_audio_filter("music", None)
        except Exception:
            pass

label before_main_menu:
    $ menu_music_filter_on()
    return


# ==============================================================================
# BLACKBERRY LOGO EASTER EGG + IMAGE HELPERS
# ==============================================================================

default found_blackberry_secret = False

init python:
    def blackberry_secret_action():
        if not store.found_blackberry_secret:
            store.found_blackberry_secret = True
            renpy.notify("Ryan is black (berry)")
        else:
            renpy.notify("You already found the secret. Stop clicking it. Please.")

    _crop_cache = {}

    def autocrop_info(path):
        if path in _crop_cache:
            return _crop_cache[path]
        info = None
        try:
            surf = renpy.load_surface(path)
            x, y, w, h = surf.get_bounding_rect()
            if w > 0 and h > 0:
                info = (x, y, w, h)
        except Exception:
            info = None
        _crop_cache[path] = info
        return info

    def autocrop_image(path):
        info = autocrop_info(path)
        if info is None:
            return path
        return Transform(path, crop=info)

    # --- main-menu key ---------------------------------------------------------
    # The key HANGS from the end of the string: the hole of its ring is anchored
    # to the string tip.
    #
    # KEY_HOLE_FRAC : how far down the visible key the ring hole is
    # KEY_NUDGE_Y   : NEGATIVE = key moves UP, positive = down (pixels)
    # KEY_NUDGE_X   : NEGATIVE = left, positive = right (pixels)
    # KEY_TRIM      : the png's empty padding in SOURCE pixels (l, t, r, b)
    KEY_HOLE_FRAC = 0.14
    KEY_NUDGE_Y = -285
    KEY_NUDGE_X = 0
    KEY_TRIM = None
    _key_cache = {}

    def _alpha_bbox(surf, min_alpha=60, step=3):
        """Bounding box of every pixel with alpha >= min_alpha (ignores glow)."""
        w, h = surf.get_size()
        get = surf.get_at

        def row_hit(y):
            for x in range(0, w, step):
                if get((x, y))[3] >= min_alpha:
                    return True
            return False

        top = None
        for y in range(0, h, step):
            if row_hit(y):
                top = y
                break
        if top is None:
            return None
        bottom = top
        for y in range(h - 1, top - 1, -step):
            if row_hit(y):
                bottom = y
                break

        def col_hit(x):
            for y in range(top, bottom + 1, step):
                if get((x, y))[3] >= min_alpha:
                    return True
            return False

        left = 0
        for x in range(0, w, step):
            if col_hit(x):
                left = x
                break
        right = w - 1
        for x in range(w - 1, -1, -step):
            if col_hit(x):
                right = x
                break
        return (left, top, right - left + 1, bottom - top + 1)

    def key_visual(path, target_h):
        """Returns (displayable, w, h): padding cropped off, scaled to target_h tall."""
        ck = (path, target_h)
        if ck in _key_cache:
            return _key_cache[ck]
        if not renpy.loadable(path):
            return None, 0, 0

        iw, ih = renpy.image_size(path)
        x, y, cw, ch = 0, 0, iw, ih
        if KEY_TRIM:
            tl, tt, tr, tb = KEY_TRIM
            x, y, cw, ch = tl, tt, iw - tl - tr, ih - tt - tb
        else:
            try:
                surf = renpy.load_surface(path)
                bb = _alpha_bbox(surf, min_alpha=200)
                if bb:
                    x, y, cw, ch = bb
            except Exception:
                pass

        z = float(target_h) / ch
        w_px = int(cw * z)
        h_px = int(ch * z)
        img = Transform(Transform(path, crop=(x, y, cw, ch)), zoom=z)
        out = Fixed(img, xsize=w_px, ysize=h_px)
        _key_cache[ck] = (out, w_px, h_px)
        return _key_cache[ck]

    def latest_save():
        try:
            return renpy.newest_slot()
        except Exception:
            return None

    MENU_STREAKS = [
        (140, 2.4, 0.0, 520),
        (260, 3.4, 0.9, 340),
        (410, 2.0, 0.3, 620),
        (560, 3.0, 1.7, 400),
        (690, 2.2, 0.6, 560),
        (830, 3.6, 1.2, 300),
        (960, 2.6, 2.1, 480),
    ]

    # (x position 0-1, size px, seconds per rise, start delay, sway px)
    import random as _pyrandom
    _er = _pyrandom.Random(11)
    MENU_EMBERS = [(_er.uniform(0.03, 0.97), _er.choice([3, 4, 5, 6]),
                    _er.uniform(7.0, 13.0), _er.uniform(0.0, 8.0),
                    _er.choice([30, 45, 60, 80])) for _ in range(26)]


# ==============================================================================
# USER PREFERENCES (persistent)
# ==============================================================================

default persistent.screen_shake_enabled = True
default persistent.dialogue_font_size = 30
default persistent.dialogue_opacity = 0.93
default persistent.menu_fx = True
default persistent.menu_echo = True
default persistent.reduce_motion = False
default persistent.text_outline = False
default persistent.readable_font = False
default persistent.mg_difficulty = 1
default persistent.mg_timers = True
default persistent.mg_skip_allowed = True
default persistent.autosave_on = True
default persistent.film_transition = True
default persistent.old_map = True
default persistent.ach_toasts = True
default persistent.mg_won = set()

define DIALOGUE_SIZES = [(22, "S"), (26, "M"), (30, "L"), (34, "XL")]

init python:
    FONT_SIZE_STEPS = [22, 26, 30, 34]

    def cycle_font_size():
        cur = persistent.dialogue_font_size
        idx = FONT_SIZE_STEPS.index(cur) if cur in FONT_SIZE_STEPS else 1
        persistent.dialogue_font_size = FONT_SIZE_STEPS[(idx + 1) % len(FONT_SIZE_STEPS)]

    def reset_preferences():
        acts = [
            Preference("text speed", 40),
            Preference("auto-forward time", 15),
            Preference("music volume", 1.0),
            Preference("sound volume", 1.0),
            Preference("voice volume", 1.0),
            Preference("skip", "seen"),
            Preference("after choices", "stop"),
            Preference("all mute", "disable"),
        ]
        for act in acts:
            try:
                renpy.run(act)
            except Exception:
                pass
        persistent.screen_shake_enabled = True
        persistent.dialogue_font_size = 30
        persistent.dialogue_opacity = 0.93
        persistent.menu_fx = True
        persistent.menu_echo = True
        persistent.reduce_motion = False
        persistent.text_outline = False
        persistent.readable_font = False
        persistent.mg_difficulty = 1
        persistent.mg_timers = True
        persistent.mg_skip_allowed = True
        persistent.autosave_on = True
        persistent.film_transition = True
        persistent.old_map = True
        persistent.ach_toasts = True
        persistent.show_objective = True
        renpy.notify("Settings reset to defaults")
        renpy.restart_interaction()

    def vol_pct(mixer):
        try:
            return str(int(round(_preferences.get_volume(mixer) * 100))) + "%"
        except Exception:
            return ""

    def text_speed_label():
        try:
            cps = int(_preferences.text_cps)
            return "INSTANT" if cps <= 0 else str(cps) + " cps"
        except Exception:
            return ""

    def auto_speed_label():
        try:
            return str(int(_preferences.afm_time))
        except Exception:
            return ""

    def opacity_label():
        return str(int(round(persistent.dialogue_opacity * 100))) + "%"

    def say_font():
        return "DejaVuSans.ttf" if persistent.readable_font else "gui/Graduate-Regular.ttf"

    def motion_ok():
        return not persistent.reduce_motion


# ==============================================================================
# QUICK MENU AUTO-HIDE STATE
# ==============================================================================

default quick_menu_hover = False

init python:
    def _set_qm_hover(value):
        store.quick_menu_hover = value


# ==============================================================================
# ACHIEVEMENTS
# ==============================================================================

define ACHIEVEMENTS = [
    {"id": "first_departure", "title": _("First Departure"), "description": _("Reach the train station for the first time."), "hidden": False},
    {"id": "carriage_1_complete", "title": _("First Class"), "description": _("Reach the second carriage."), "hidden": False},
    {"id": "carriage_2_complete", "title": _("A Drink and a Game"), "description": _("Reach the third carriage."), "hidden": False},
    {"id": "high_roller", "title": _("High Roller"), "description": _("Agree to play mahjong with Shunyu."), "hidden": False},
    {"id": "carriage_3_complete", "title": _("Quiet Car"), "description": _("Reach the fourth carriage."), "hidden": False},
    {"id": "key_holder", "title": _("A Way Out"), "description": _("Accept the key from Ichora."), "hidden": False},
    {"id": "carriage_4_complete", "title": _("The Mail Car"), "description": _("Reach the fifth carriage."), "hidden": False},
    {"id": "forbidden_sweetness", "title": _("Forbidden Sweetness"), "description": _("Accept Alexander's maple sugar."), "hidden": False},
    {"id": "carriage_5_complete", "title": _("Beyond the Fifth"), "description": _("Reach the door beyond the fifth carriage."), "hidden": False},
    {"id": "the_loop_begins", "title": _("Here Again?"), "description": _("The train reset. Louis remembers."), "hidden": False},
    {"id": "eyes_in_the_dark", "title": _("???"), "description": _("Something was watching from beyond the sixth carriage."), "hidden": True},
    {"id": "closer_to_the_truth", "title": _("Closer to the Truth"), "description": _("Investigated Shunyu's murder."), "hidden": False},
    {"id": "suspicious_luggage", "title": _("Suspicious Luggage"), "description": _("Found the drug wrapper in Himmel's luggage."), "hidden": False},
    {"id": "alibi_confirmed", "title": _("Alibi Confirmed"), "description": _("Pattison confirmed Alexander's alibi."), "hidden": False},
    {"id": "hidden_evidence", "title": _("Hidden Evidence"), "description": _("Found the missing mahjong tile."), "hidden": False},
    {"id": "true_detective", "title": _("True Detective"), "description": _("Accused the killer with full evidence."), "hidden": False},
    {"id": "wrong_guess", "title": _("Wrong Guess"), "description": _("Accused the wrong person."), "hidden": False},
    {"id": "perfect_understanding", "title": _("Perfect Understanding"), "description": _("Answered all three questions correctly in Carriage 6."), "hidden": False},
    {"id": "partial_truth", "title": _("Partial Truth"), "description": _("Answered some questions correctly in Carriage 6."), "hidden": False},
    {"id": "total_failure", "title": _("Total Failure"), "description": _("Failed all questions in Carriage 6."), "hidden": False},
    # --- minigames ---
    {"id": "tumbler_talent", "title": _("Tumbler Talent"), "description": _("Pick the lock of the Carriage 1 cupboard."), "hidden": False},
    {"id": "sharp_eyes", "title": _("Sharp Eyes"), "description": _("Sweep up the broken glass in Carriage 2."), "hidden": False},
    {"id": "high_roller_win", "title": _("Beginner's Luck"), "description": _("Win a game of mahjong against Shunyu."), "hidden": False},
    {"id": "block_party", "title": _("Block Party"), "description": _("Beat Misha's block game."), "hidden": False},
    {"id": "full_steam", "title": _("Full Steam Ahead"), "description": _("Keep the engine pressure stable."), "hidden": False},
    {"id": "sorted", "title": _("Return to Sender"), "description": _("Help Pattison sort the mail."), "hidden": False},
    {"id": "game_night", "title": _("Game Night"), "description": _("Win every minigame on the train."), "hidden": False, "stat_max": 6},
]

init python:
    for _ach in ACHIEVEMENTS:
        if "stat_max" in _ach:
            achievement.register(_ach["id"], stat_max=_ach["stat_max"])
        else:
            achievement.register(_ach["id"])

    def _ach_unlocked(ach_id):
        try:
            if achievement.has(ach_id):
                return True
        except Exception:
            pass
        try:
            return ach_id in persistent._achievements
        except Exception:
            return False

    def achievement_counts():
        done = 0
        for ach in ACHIEVEMENTS:
            if _ach_unlocked(ach["id"]):
                done += 1
        return done, len(ACHIEVEMENTS)

    def achievement_rows(mode="all"):
        rows = []
        for ach in ACHIEVEMENTS:
            unlocked = _ach_unlocked(ach["id"])
            secret = bool(ach.get("hidden", False)) and not unlocked
            if mode == "unlocked" and not unlocked:
                continue
            if mode == "locked" and unlocked:
                continue

            mx = ach.get("stat_max", 0)
            cur = 0
            if mx:
                try:
                    cur = int(achievement.get_progress(ach["id"]) or 0)
                except Exception:
                    cur = 0
                if unlocked:
                    cur = mx
            frac = (float(cur) / mx) if mx else 0.0

            # per-achievement art wins; otherwise the shared lock / star icons
            icon = "images/achievements/%s.png" % ach["id"]
            if not renpy.loadable(icon):
                icon = ach_default_icon(unlocked)

            rows.append({
                "title": "???" if secret else ach["title"],
                "desc": "A hidden achievement." if secret else ach["description"],
                "unlocked": unlocked,
                "secret": secret,
                "mx": mx,
                "cur": cur,
                "frac": max(0.0, min(1.0, frac)),
                "icon": icon,
            })
        return rows

    # Popup when an achievement is granted. renpy.session is not saved and
    # not rolled back, so this never ends up in a save file.
    def ach_poll():
        try:
            s = renpy.session
            have = set([a["id"] for a in ACHIEVEMENTS if _ach_unlocked(a["id"])])
            seen = s.get("ach_seen")
            if seen is None:
                s["ach_seen"] = have
                s["ach_queue"] = []
                return
            new = have - seen
            if new:
                s["ach_seen"] = have
                for a in ACHIEVEMENTS:
                    if a["id"] in new:
                        s["ach_queue"].append((a["title"], a["description"]))
            q = s.get("ach_queue")
            if q and persistent.ach_toasts and not renpy.get_screen("ach_toast"):
                t, d = q.pop(0)
                renpy.show_screen("ach_toast", t, d)
                renpy.restart_interaction()
            elif q and not persistent.ach_toasts:
                del q[:]
        except Exception:
            pass

    if ach_poll not in config.periodic_callbacks:
        config.periodic_callbacks.append(ach_poll)

    # Live MENU MUSIC ECHO + sound for the achievement banner / map stamp.
    def ui_periodic():
        try:
            s = renpy.session
            if getattr(store, "main_menu", False):
                want = bool(persistent.menu_echo)
                if s.get("echo_state") != want:
                    s["echo_state"] = want
                    if want:
                        menu_music_filter_on()
                    else:
                        menu_music_filter_off()
            else:
                s["echo_state"] = None

            for scr, snd in (("ach_toast", "ach"), ("map_stamp", "stamp")):
                on = bool(renpy.get_screen(scr))
                key = "snd_" + scr
                if on and not s.get(key):
                    sfx(snd)
                s[key] = on
        except Exception:
            pass

    config.periodic_callbacks = [c for c in config.periodic_callbacks
                                 if getattr(c, "__name__", "") != "ui_periodic"] + [ui_periodic]


# ==============================================================================
# SHARED ROUND BUTTON
# ==============================================================================

screen rbtn(label, act, w=200, h=50, r=14, size=22, bg="#101014", hov="#2a2a35", edge="#33334a", col="#8888a0", hcol="#ffd700", sel=False):
    button:
        xsize w
        ysize h
        padding (0, 0)
        background rbox(edge, r)
        hover_background rbox(hcol, r)
        selected_background rbox(edge, r)
        selected_hover_background rbox(hcol, r)
        action act
        selected sel
        at button_hover_anim

        frame:
            margin (2, 2)
            padding (0, 0)
            xfill True
            yfill True
            background rbox(bg, r)
            hover_background rbox(hov, r)
            selected_background rbox(bg, r)
            selected_hover_background rbox(hov, r)
            text label:
                align (0.5, 0.5)
                size size
                color col
                hover_color hcol
                selected_color hcol
                font GFONT


# ==============================================================================
# ACHIEVEMENT POPUP
# ==============================================================================

screen ach_toast(title, desc):
    zorder 400
    $ toast_icon = ach_default_icon(True)
    frame:
        xanchor 1.0
        xpos config.screen_width - 40
        ypos 40
        xsize 500
        padding (2, 2)
        background rbox("#e6a817", 18)
        at ach_toast_anim

        frame:
            xfill True
            padding (20, 16, 20, 20)
            background rbox("#14141aee", 16)

            if toast_icon:
                add toast_icon:
                    xysize (84, 84)
                    fit "contain"
                    xalign 1.0
                    yalign 0.0

            vbox:
                spacing 6
                text _("ACHIEVEMENT UNLOCKED"):
                    size 14
                    color "#e6a817"
                    font GFONT
                text title:
                    size 28
                    color "#ffffff"
                    font GFONT
                    xsize (350 if toast_icon else 450)
                text desc:
                    size 16
                    color "#8888a0"
                    font GFONT
                    xsize (350 if toast_icon else 450)
                null height 6
                add rbox("#e6a817", 2):
                    xsize 456
                    ysize 3
                    at toast_timer
    timer 4.8 action Hide("ach_toast")


# ==============================================================================
# ACHIEVEMENTS SCREEN
# ==============================================================================

screen achievements():
    tag menu
    modal True
    default ach_filter = "all"

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    $ ach_done, ach_total = achievement_counts()
    $ ach_pct = float(ach_done) / max(ach_total, 1)
    $ ach_fill = int(360 * ach_pct)
    $ ach_w = config.screen_width - 200

    add Solid("#0a0a0e")
    use game_menu_nav

    text _("ACHIEVEMENTS"):
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

    vbox:
        xalign 0.95
        ypos 120
        spacing 8
        xsize 360
        at fade_in(0.3)

        text "[ach_done] / [ach_total] UNLOCKED":
            xalign 1.0
            size 20
            color "#e6a817"
            font GFONT

        fixed:
            xsize 360
            ysize 10
            add rbox("#222233", 4):
                xsize 360
                ysize 10
            if ach_fill > 0:
                add rbox("#e6a817", 4):
                    xsize ach_fill
                    ysize 10
                    at fill_grow(0.4)

    hbox:
        xpos 80
        ypos 135
        spacing 10
        for fkey, flabel in [("all", _("ALL")), ("unlocked", _("UNLOCKED")), ("locked", _("LOCKED"))]:
            button:
                padding (22, 10)
                background rbox("#101014", 14)
                hover_background rbox("#1a1a22", 14)
                selected_background rbox("#e0521f", 14)
                selected_hover_background rbox("#f06a35", 14)
                action SetScreenVariable("ach_filter", fkey)
                selected (ach_filter == fkey)
                at button_hover_anim
                text flabel:
                    size 18
                    color "#8888a0"
                    hover_color "#ffd700"
                    selected_color "#0a0a0e"
                    selected_hover_color "#0a0a0e"
                    font GFONT

    viewport:
        id "ach_vp"
        xpos 80
        ypos 200
        xsize ach_w
        ysize (config.screen_height - 360)
        mousewheel True
        draggable True

        vbox:
            xsize ach_w
            for mode in ("all", "unlocked", "locked"):
                showif ach_filter == mode:
                    vbox:
                        xsize ach_w
                        spacing 12
                        at list_page

                        $ ach_list = achievement_rows(mode)

                        if not ach_list:
                            text _("Nothing here yet."):
                                size 22
                                color "#666677"
                                font GFONT

                        for idx, arow in enumerate(ach_list):
                            frame:
                                xfill True
                                background rbox("#17150d" if arow["unlocked"] else "#101014", 22)
                                padding (20, 14)
                                at row_pop(min(idx * 0.04, 0.5))

                                fixed:
                                    xfill True
                                    ysize 64

                                    hbox:
                                        spacing 20
                                        yalign 0.5

                                        fixed:
                                            xsize 64
                                            ysize 64
                                            if arow["icon"]:
                                                add arow["icon"]:
                                                    xysize (64, 64)
                                                    fit "contain"
                                                    alpha (1.0 if arow["unlocked"] else 0.9)
                                            else:
                                                add rbox("#e6a817" if arow["unlocked"] else "#33334a", 15):
                                                    xsize 64
                                                    ysize 64
                                                    if arow["unlocked"]:
                                                        at gold_glow
                                                text ("+" if arow["unlocked"] else "?"):
                                                    align (0.5, 0.5)
                                                    size 34
                                                    color ("#0a0a0e" if arow["unlocked"] else "#8888a0")
                                                    font GFONT

                                        vbox:
                                            spacing 4
                                            yalign 0.5
                                            text arow["title"]:
                                                size 24
                                                color ("#ffd700" if arow["unlocked"] else "#8888a0")
                                                font GFONT
                                            text arow["desc"]:
                                                size 18
                                                color ("#ffffff" if arow["unlocked"] else "#666677")
                                                font GFONT
                                                xsize 1000

                                    vbox:
                                        xalign 1.0
                                        yalign 0.5
                                        spacing 6
                                        if arow["unlocked"]:
                                            text _("UNLOCKED"):
                                                xalign 1.0
                                                size 16
                                                color "#e6a817"
                                                font GFONT
                                        elif arow["mx"]:
                                            text "[arow['cur']] / [arow['mx']]":
                                                xalign 1.0
                                                size 16
                                                color "#8888a0"
                                                font GFONT
                                            fixed:
                                                xsize 220
                                                ysize 8
                                                add rbox("#222233", 4):
                                                    xsize 220
                                                    ysize 8
                                                if arow["frac"] > 0:
                                                    add rbox("#e6a817", 4):
                                                        xsize max(1, int(220 * arow["frac"]))
                                                        ysize 8
                                                        at fill_grow(0.3)
                                        else:
                                            text (_("HIDDEN") if arow["secret"] else _("LOCKED")):
                                                xalign 1.0
                                                size 16
                                                color "#55556a"
                                                font GFONT

    vbar:
        style "pref_vbar"
        value YScrollValue("ach_vp")
        xpos config.screen_width - 96
        ypos 200
        ysize (config.screen_height - 360)

    use game_menu_back(back_action)


# ==============================================================================
# BACKGROUNDS
# ==============================================================================

image main_menu_bg_rotation:
    Solid("#0c0c12")
    pause 6.0
    Solid("#140c10") with Dissolve(3.0)
    pause 6.0
    Solid("#0c1412") with Dissolve(3.0)
    pause 6.0
    Solid("#0c0c12") with Dissolve(3.0)
    repeat

# Game_Logo_Purple.webp also exists in game/images if you want a third colour.
image game_logo_cycle:
    "images/Game_Logo_Red.webp" with dissolve
    pause 3.0
    "images/Game_Logo_Yellow.webp" with dissolve
    pause 10.0
    repeat


# ==============================================================================
# LOADING SCREEN / SPLASH
# ==============================================================================

screen loading():
    zorder 200
    add Solid("#0a0a0e")
    frame:
        xalign 0.5
        yalign 0.5
        background None
        vbox:
            xalign 0.5
            spacing 16
            text _("LOADING"):
                xalign 0.5
                size 36
                color "#e0521f"
                font "gui/Telegraphem.otf"
                at loading_pulse
            add rbox("#e0521f", 2):
                xsize 240
                ysize 6
                xalign 0.5

label splashscreen:
    scene black
    with Pause(0.3)

    if renpy.loadable("images/Blackberry_Studios_Full.webp"):
        show expression "images/Blackberry_Studios_Full.webp" as boot_logo at boot_logo_anim
        pause 3.3
        hide boot_logo
    else:
        show text "{size=50}BLACKBERRY STUDIOS{/size}" at boot_logo_anim
        pause 3.3
        hide text

    scene black
    with Pause(0.3)
    return


# ==============================================================================
# MAIN MENU
# ==============================================================================

screen menu_entry(caption, act, delay=0.0, bright=False):
    button:
        xsize gui.sidebar_content_width
        ysize 50
        background rbox("#00000000", 14)
        hover_background rbox("#ffffff14", 14)
        action act
        at fade_slide_in(delay)

        # accent bar on the left edge (grows from the middle on hover)
        add rbox("#e0521f", 2):
            xsize 4
            ysize 30
            xpos 4
            yalign 0.5
            at entry_bar

        hbox:
            yalign 0.5
            spacing 14
            xoffset 14
            text "›":
                size 24
                color "#e0521f"
                font GFONT
                yalign 0.5
                at entry_arrow
            text caption:
                size 24
                color ("#e8e4dc" if bright else "#8888a0")
                hover_color "#ffd700"
                font GFONT
                yalign 0.5

screen main_menu():
    tag menu

    $ newest_save = latest_save()
    $ fx = persistent.menu_fx and not persistent.reduce_motion
    use secret_listener

    # ---- Atmosphere -----------------------------------------------------------
    add "images/1st_carriage_Visualnovel_Background.webp":
        fit "cover"
        xysize (config.screen_width, config.screen_height)
        at (menu_bg_drift if not persistent.reduce_motion else menu_bg_still)
    add Solid("#08080cb8")

    fixed:
        at (train_shake if (persistent.screen_shake_enabled and not persistent.reduce_motion) else no_shake)

        text "4:00":
            xalign 0.78
            yalign 0.52
            size 520
            color "#ffffff08"
            font GFONT

        if fx:
            for sy, sdur, sdelay, slen in MENU_STREAKS:
                add Solid("#ffffff1c", xsize=slen, ysize=2):
                    ypos sy
                    at streak(sdur, sdelay)

            # embers rising through the carriage
            for ex, esz, edur, edelay, esway in MENU_EMBERS:
                add Solid("#ff8a3cc0"):
                    xpos ex
                    xsize esz
                    ysize esz
                    at ember(edur, edelay, esway)

        # Key swinging from a string - scaled by KEY_SCALE.
        $ key_string_h = int(170 * KEY_SCALE)
        $ key_img, key_w, key_h = key_visual("images/Key.webp", int(520 * KEY_SCALE))
        fixed:
            xpos 0.80
            ypos 0
            xysize (int(340 * KEY_SCALE), int(840 * KEY_SCALE))
            at (key_drop if not persistent.reduce_motion else key_static)

            add Solid("#7a7a88", xsize=3, ysize=key_string_h):
                xalign 0.5

            if key_img is not None:
                button:
                    background None
                    padding (0, 0)
                    xysize (key_w, key_h)
                    xanchor 0.5
                    xpos 0.5
                    yanchor KEY_HOLE_FRAC
                    ypos key_string_h
                    yoffset KEY_NUDGE_Y
                    xoffset KEY_NUDGE_X
                    action Function(key_poke)      # easter egg: poke it
                    add key_img
            else:
                text "KEY":
                    xalign 0.5
                    ypos 200
                    size 120

    # ---- Sidebar card ---------------------------------------------------------
    fixed:
        xpos gui.sidebar_margin
        ypos gui.sidebar_margin
        xsize gui.sidebar_width
        ysize (config.screen_height - gui.sidebar_margin * 2)

        add rbox("#000000aa", 40):
            xsize gui.sidebar_width
            ysize (config.screen_height - gui.sidebar_margin * 2)
            xoffset 6
            yoffset 12
            blur 22

        frame:
            xfill True
            yfill True
            padding (2, 2)
            background rbox("#ffffff22", 40)

            frame:
                xfill True
                yfill True
                background rbox("#14141ab8", 38)
                padding (0, 0)
                clipping True

                if renpy.loadable("images/Train_BP.webp"):
                    frame:
                        xpos 18
                        yalign 1.0
                        yoffset 40
                        xysize (380, 380)
                        background None
                        padding (0, 0)
                        clipping True
                        at fade_slide_in(0.7, xoff=-60)
                        add "images/Train_BP.webp":
                            xysize (380, 380)
                            fit "contain"
                            align (0.0, 1.0)
                            xoffset -30
                            rotate -12
                            alpha 0.3

                vbox:
                    xpos gui.sidebar_padding - 2
                    ypos 40
                    xsize gui.sidebar_content_width
                    spacing 26

                    add "game_logo_cycle":
                        xsize gui.sidebar_content_width
                        ysize 240
                        fit "contain"
                        at fade_slide_in(0.1)

                    text _("A MURDER MYSTERY ON THE GREKHOV EXPRESS"):
                        xalign 0.5
                        text_align 0.5
                        size 14
                        color "#8888a0"
                        font GFONT
                        at fade_slide_in(0.2)

                    frame:
                        xsize gui.sidebar_content_width
                        ysize 64
                        background rbox("#e0521f", 22)
                        padding (2, 2)
                        clipping True
                        at fade_slide_in(0.3)

                        button:
                            xfill True
                            yfill True
                            background None
                            hover_background rbox("#00000033", 20)
                            action Start()

                            add Solid("#ffffff"):
                                xsize 70
                                ysize 40
                                yalign 0.5
                                at shine_sweep

                            text (_("NEW GAME") if newest_save else _("PLAY")):
                                align (0.5, 0.5)
                                size 32
                                color "#0a0a0e"
                                hover_color "#ffffff"
                                font GFONT

                    vbox:
                        xsize gui.sidebar_content_width
                        spacing 8

                        if newest_save:
                            use menu_entry(_("CONTINUE"), Function(renpy.load, newest_save), 0.34, True)
                        use menu_entry(_("LOAD GAME"), ShowMenu("load"), 0.40)
                        use menu_entry(_("SETTINGS"), ShowMenu("preferences"), 0.48)
                        use menu_entry(_("ACHIEVEMENTS"), ShowMenu("achievements"), 0.56)
                        use menu_entry(_("EXTRAS"), ShowMenu("extras_menu"), 0.60)
                        use menu_entry(_("CREDITS"), ShowMenu("about"), 0.64)
                        if renpy.variant("pc"):
                            use menu_entry(_("QUIT"), Quit(confirm=True), 0.72)

                text "v[config.version]":
                    xalign 0.95
                    yalign 0.985
                    size 14
                    color "#55556a"
                    font GFONT

    # ---- Studio logo (easter egg) ----------------------------------------------
    if renpy.loadable("images/Blackberry_Studios.webp"):
        button:
            xalign 1.0
            yalign 1.0
            xoffset 30
            yoffset -30
            xsize 180
            ysize 90
            background None
            action Function(blackberry_secret_action)
            at fade_slide_in(0.9, xoff=70, final_xoff=30)

            add autocrop_image("images/Blackberry_Studios.webp"):
                xsize 180
                ysize 90
                fit "contain"
                rotate -18
                at button_hover_anim
    else:
        text "Blackberry":
            size 40
            xalign 1.0
            yalign 1.0
            xoffset -20
            yoffset -20
            at fade_slide_in(0.9, xoff=60, final_xoff=-20)


# ==============================================================================
# DIALOGUE (SAY) SCREEN
# ==============================================================================

screen say(who, what):
    window:
        id "window"
        xalign 0.5
        yalign 1.0
        xsize config.screen_width
        ysize 310
        background Solid(Color("#0a0a0e").replace_opacity(persistent.dialogue_opacity))
        at say_rise

        add Solid("#e0521f"):
            xsize config.screen_width
            ysize 2
            yalign 0.0

        if who:
            add rbox("#8a4a22", 22):
                xpos 40
                ypos 44
                xsize 260
                ysize 44

            text who:
                id "who"
                xpos 170
                xanchor 0.5
                ypos 66
                yanchor 0.5
                size (persistent.dialogue_font_size - 2)
                bold True
                color "#f2e6d8"
                font GFONT

        text what:
            id "what"
            xpos 40
            xsize 0.85
            ypos 112
            size persistent.dialogue_font_size
            color "#e8e4dc"
            font say_font()
            line_spacing 10
            outlines ([(2, "#000000", 0, 0)] if persistent.text_outline else [])

        # little "next" diamond bottom-right
        add rbox("#e0521f", 2):
            xalign 0.97
            yalign 0.9
            xsize 16
            ysize 16
            rotate 45
            at (soft_pulse, next_arrow_bob)


# ==============================================================================
# INPUT / CHOICE
# ==============================================================================

screen input(prompt):
    window:
        xalign 0.5
        yalign 0.5
        xsize 900
        background rbox("#14141aee", 26)
        padding (40, 30)
        at confirm_pop
        vbox:
            spacing 15
            text prompt
            input:
                id "input"

screen choice(items):
    vbox:
        xalign 0.5
        yalign 1.0
        yoffset -340
        spacing 18

        for idx, i in enumerate(items):
            frame:
                xalign 0.5
                xsize 760
                ysize 82
                padding (3, 3)
                background rbox("#33334a", 26)
                at choice_in(idx * 0.08)

                button:
                    xfill True
                    yfill True
                    background rbox("#14141aee", 24)
                    hover_background rbox("#2a2a35", 24)
                    action i.action
                    at button_hover_anim

                    text i.caption:
                        align (0.5, 0.5)
                        text_align 0.5
                        xsize 700
                        size 30
                        color "#c9c9d8"
                        hover_color "#ffd700"
                        selected_color "#ffd700"
                        font say_font()


# ==============================================================================
# QUICK MENU
# ==============================================================================

default quick_menu = True

screen quick_menu():
    zorder 100
    if quick_menu:

        mousearea:
            area (0, config.screen_height - 50, config.screen_width, 50)
            hovered Function(_set_qm_hover, True)
            unhovered Function(_set_qm_hover, False)

        hbox:
            xpos 40
            yalign 1.0
            yoffset -14
            spacing 8
            at (qm_shown if quick_menu_hover else qm_hidden)
            for qm_label, qm_act in [
                (_("Home"), MainMenu(confirm=True)),
                (_("Back"), Rollback()),
                (_("History"), ShowMenu("history")),
                (_("Skip"), Skip()),
                (_("Auto"), Preference("auto-forward", "toggle")),
                (_("Save"), ShowMenu("save")),
                (_("Q.Save"), QuickSave()),
                (_("Q.Load"), QuickLoad()),
                (_("Clues"), ShowMenu("clues")),
                (_("Prefs"), ShowMenu("preferences")),
            ]:
                button:
                    xsize 96
                    ysize 34
                    background rbox("#0a0a0ecc", 17)
                    hover_background rbox("#ffffff22", 17)
                    action qm_act
                    at button_hover_anim
                    text qm_label:
                        align (0.5, 0.5)
                        size 17
                        color "#8888a0"
                        hover_color "#ffd700"
                        selected_color "#ffd700"
                        font GFONT


# ==============================================================================
# NAVIGATION (default escape menu fallback)
# ==============================================================================

screen navigation():
    vbox:
        xpos 0.05
        yalign 0.5
        spacing 12
        if main_menu:
            textbutton _("Play"):
                action Start()
        else:
            textbutton _("History"):
                action ShowMenu("history")
            textbutton _("Save"):
                action ShowMenu("save")
        textbutton _("Load"):
            action ShowMenu("load")
        textbutton _("Preferences"):
            action ShowMenu("preferences")
        if _in_replay:
            textbutton _("End Replay"):
                action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _("Main Menu"):
                action MainMenu()
        textbutton _("About"):
            action ShowMenu("about")
        if renpy.variant("pc") or renpy.variant("web"):
            textbutton _("Help"):
                action ShowMenu("help")
        if renpy.variant("pc"):
            textbutton _("Quit"):
                action Quit(confirm=not main_menu)


# ==============================================================================
# SHARED MENU CHROME
# ==============================================================================

screen game_menu_header(title):
    text title:
        size 40
        color "#ffffff"
        font GFONT
        at fade_in(0.1)
    add rbox("#e0521f", 2):
        xsize 160
        ysize 6
        at underline_in

screen game_menu_back(back_action):
    fixed:
        xpos 80
        yalign 0.95
        xsize 160
        ysize 50
        at fade_in(0.3)
        use rbtn(_("BACK"), back_action, w=160, h=50, r=14, size=24)

screen game_menu_overlay():
    add Solid("#0a0a0eee"):
        xsize config.screen_width
        ysize config.screen_height

screen game_menu_nav():
    if not main_menu:
        hbox:
            xalign 1.0
            xoffset -80
            ypos 52
            spacing 6
            at fade_in(0.2)

            for nav_label, nav_act in [
                (_("SAVE"), ShowMenu("save")),
                (_("LOAD"), ShowMenu("load")),
                (_("HISTORY"), ShowMenu("history")),
                (_("CLUES"), ShowMenu("clues")),
                (_("ACHIEVEMENTS"), ShowMenu("achievements")),
                (_("SETTINGS"), ShowMenu("preferences")),
                (_("MAIN MENU"), MainMenu()),
            ]:
                button:
                    padding (16, 8)
                    background rbox("#00000000", 14)
                    hover_background rbox("#ffffff14", 14)
                    action nav_act
                    at button_hover_anim
                    text nav_label:
                        size 18
                        color "#8888a0"
                        hover_color "#ffd700"
                        selected_color "#e0521f"
                        font GFONT


# ==============================================================================
# CLUE JOURNAL  (J key, CLUES in the pause menu, or the quick menu)
# ==============================================================================

define CLUE_LIST = [
    ("clue_tile_mismatch", "THE WRONG TILE", "The tile in Shunyu's hand is not part of his winning hand. Someone put it there after."),
    ("clue_body_moved", "A MOVED BODY", "Most of the blood is by the bar counter, not where he was found. He was moved after death."),
    ("clue_drug_wrapper", "THE WRAPPER", "A banned maple sugar wrapper in Himmel's luggage. He owed Alexander money."),
    ("clue_hidden_tile", "THE HIDDEN TILE", "The missing mahjong tile was tucked flat under the carpet in Misha's room."),
    ("clue_alexander_alibi", "ALEXANDER'S ALIBI", "Pattison would have heard the creaking door. Alexander never left the storage carriage."),
]

init python:
    def clue_rows():
        rows = []
        for cid, title, text in CLUE_LIST:
            got = bool(getattr(store, cid, False))
            rows.append({
                "title": title if got else "???",
                "text": text if got else "Not found yet.",
                "got": got,
            })
        return rows

screen clues():
    tag menu
    modal True

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    $ clue_data = clue_rows()
    $ clue_found = len([r for r in clue_data if r["got"]])
    $ clue_total = len(clue_data)

    add Solid("#0a0a0e")
    use game_menu_nav

    text _("CLUE JOURNAL"):
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

    $ obj_line = current_objective()
    text "NEXT: [obj_line]":
        xpos 80
        ypos 125
        size 20
        color "#8888a0"
        font GFONT

    text "[clue_found] / [clue_total] FOUND":
        xalign 0.95
        ypos 130
        size 20
        color "#e6a817"
        font GFONT

    vbox:
        xpos 80
        ypos 190
        spacing 14

        for idx, r in enumerate(clue_data):
            frame:
                xsize (config.screen_width - 160)
                background rbox("#17150d" if r["got"] else "#101014", 22)
                padding (26, 18)
                at row_pop(min(idx * 0.06, 0.5))

                hbox:
                    spacing 24
                    add rbox("#e6a817" if r["got"] else "#33334a", 6):
                        xsize 8
                        ysize 72
                        yalign 0.5
                    vbox:
                        spacing 6
                        yalign 0.5
                        text r["title"]:
                            size 26
                            color ("#ffd700" if r["got"] else "#666677")
                            font GFONT
                        text r["text"]:
                            size 18
                            color ("#e8e4dc" if r["got"] else "#55556a")
                            font GFONT
                            xsize (config.screen_width - 300)

    use game_menu_back(back_action)

screen clue_hotkey():
    zorder 1
    if not main_menu:
        key "j" action ShowMenu("clues")


# ==============================================================================
# PREFERENCES  (5 tabs)
# ==============================================================================

screen pref_toggle(label, act, selected=None, w=170):
    $ sel = renpy.is_selected(act) if selected is None else selected
    $ t_bg = "#1a1a24" if sel else "#101014"
    $ t_edge = "#e6a817" if sel else "#33334a"
    $ t_col = "#ffffff" if sel else "#8888a0"
    use rbtn(label, act, w=w, h=44, r=14, size=18, bg=t_bg, edge=t_edge, col=t_col, sel=sel)

screen pref_section(title):
    text title:
        size 18
        color "#e6a817"
        font GFONT

screen pref_row(title, desc="", delay=0.0):
    frame:
        xsize PREF_PANEL_W
        background rbox("#101014", 22)
        padding (28, 18)
        at row_pop(delay)

        hbox:
            vbox:
                xsize 540
                yalign 0.5
                spacing 4
                text title:
                    size 22
                    color "#f2e6d8"
                    font GFONT
                if desc:
                    text desc:
                        size 15
                        color "#666677"
                        font GFONT
                        xsize 520

            fixed:
                xsize 780
                ysize 48
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 12
                    transclude

screen pref_slider(val, readout=""):
    hbox:
        spacing 22
        yalign 0.5
        bar:
            style "pref_bar"
            value val
            yalign 0.5
            released Function(sfx_sample)
        text readout:
            size 18
            color "#e6a817"
            font GFONT
            xminimum 110
            yalign 0.5

# on / off row helper
screen pref_onoff(title, desc, field, delay=0.0):
    use pref_row(title, desc, delay):
        use pref_toggle(_("ON"), SetField(persistent, field, True), selected=bool(getattr(persistent, field)))
        use pref_toggle(_("OFF"), SetField(persistent, field, False), selected=(not getattr(persistent, field)))

define PREF_TABS = [
    ("display", _("DISPLAY"), 0.05),
    ("text", _("TEXT & SKIP"), 0.10),
    ("audio", _("AUDIO"), 0.15),
    ("gameplay", _("GAMEPLAY"), 0.20),
    ("access", _("ACCESSIBILITY"), 0.25),
]

screen preferences():
    tag menu
    modal True
    default pref_tab = "display"

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    add Solid("#0a0a0e")
    use game_menu_nav

    text _("SETTINGS"):
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

    # ---------------- TAB LIST ----------------
    vbox:
        xpos 80
        ypos 150
        xsize 300
        spacing 8

        for tkey, tlabel, tdelay in PREF_TABS:
            button:
                xsize 300
                ysize 60
                padding (0, 0)
                background rbox("#101014", 22)
                hover_background rbox("#1a1a22", 22)
                selected_background rbox("#1d1d28", 22)
                selected_hover_background rbox("#232330", 22)
                action SetScreenVariable("pref_tab", tkey)
                selected (pref_tab == tkey)
                at (fade_slide_in(tdelay), button_hover_anim)

                if pref_tab == tkey:
                    add rbox("#e0521f", 2):
                        xpos 12
                        yalign 0.5
                        xsize 6
                        ysize 30
                        at tab_ind_in
                text tlabel:
                    xpos 34
                    yalign 0.5
                    size 22
                    color "#8888a0"
                    hover_color "#ffd700"
                    selected_color "#ffffff"
                    font GFONT

        null height 28

        button:
            xsize 300
            ysize 50
            padding (0, 0)
            background rbox("#00000000", 22)
            hover_background rbox("#e0521f22", 22)
            action Function(reset_preferences)
            at (fade_slide_in(0.3), button_hover_anim)
            text _("RESET TO DEFAULTS"):
                align (0.5, 0.5)
                size 15
                color "#666677"
                hover_color "#e0521f"
                font GFONT

    # ---------------- CONTENT (each tab slides in/out) ----------------
    fixed:
        xpos 420
        ypos 150
        xsize PREF_PANEL_W
        ysize 800

        showif pref_tab == "display":
            vbox:
                spacing 14
                at tab_page

                use pref_row(_("WINDOW MODE"), _("Play in a window or take over the screen."), 0.0):
                    use pref_toggle(_("WINDOW"), Preference("display", "window"))
                    use pref_toggle(_("FULLSCREEN"), Preference("display", "fullscreen"))

                use pref_onoff(_("SCREEN SHAKE / RUMBLE"), _("The main menu and the train gently rattle."), "screen_shake_enabled", 0.06)

                use pref_row(_("DIALOGUE FONT SIZE"), _("Size of the text in the dialogue box."), 0.12):
                    for dsz, dlabel in DIALOGUE_SIZES:
                        use pref_toggle(dlabel, SetField(persistent, "dialogue_font_size", dsz), selected=(persistent.dialogue_font_size == dsz), w=90)

                use pref_onoff(_("MENU EFFECTS"), _("Light streaks and embers on the main menu."), "menu_fx", 0.18)
                use pref_onoff(_("ACHIEVEMENT POPUPS"), _("Show a banner when you unlock an achievement."), "ach_toasts", 0.24)

        showif pref_tab == "text":
            vbox:
                spacing 14
                at tab_page

                use pref_row(_("TEXT SPEED"), _("How fast dialogue appears."), 0.0):
                    use pref_slider(Preference("text speed"), text_speed_label())

                use pref_row(_("AUTO-FORWARD"), _("Delay before auto mode moves to the next line."), 0.06):
                    use pref_slider(Preference("auto-forward time"), auto_speed_label())

                use pref_row(_("DIALOGUE BOX OPACITY"), _("How see-through the dialogue box is."), 0.12):
                    use pref_slider(FieldValue(persistent, "dialogue_opacity", range=0.7, offset=0.3), opacity_label())

                use pref_row(_("SKIP"), _("Which text the skip button is allowed to fast-forward."), 0.18):
                    use pref_toggle(_("SEEN TEXT"), Preference("skip", "seen"))
                    use pref_toggle(_("ALL TEXT"), Preference("skip", "all"))

                use pref_row(_("AFTER CHOICES"), _("What skipping does when a choice appears."), 0.24):
                    use pref_toggle(_("STOP SKIPPING"), Preference("after choices", "stop"))
                    use pref_toggle(_("KEEP SKIPPING"), Preference("after choices", "skip"))

        showif pref_tab == "audio":
            vbox:
                spacing 14
                at tab_page

                use pref_row(_("MUSIC VOLUME"), _("Background music level."), 0.0):
                    use pref_slider(Preference("music volume"), vol_pct("music"))

                use pref_row(_("SOUND VOLUME"), _("Sound effects level."), 0.06):
                    use pref_slider(Preference("sound volume"), vol_pct("sfx"))

                use pref_row(_("VOICE VOLUME"), _("Voiced lines level (this game has no voiced lines yet)."), 0.12):
                    use pref_slider(Preference("voice volume"), vol_pct("voice"))

                use pref_row(_("MUTE ALL AUDIO"), _("Silence everything at once."), 0.18):
                    use pref_toggle(_("MUTED"), Preference("all mute", "enable"))
                    use pref_toggle(_("SOUND ON"), Preference("all mute", "disable"))

                use pref_onoff(_("MENU MUSIC ECHO"), _("Muffled, echoey music on the main menu. Applies instantly."), "menu_echo", 0.24)

        showif pref_tab == "gameplay":
            vbox:
                spacing 14
                at tab_page

                use pref_row(_("MINIGAME DIFFICULTY"), _("Changes speed, time limits and mistakes allowed."), 0.0):
                    use pref_toggle(_("EASY"), SetField(persistent, "mg_difficulty", 0), selected=(persistent.mg_difficulty == 0), w=130)
                    use pref_toggle(_("NORMAL"), SetField(persistent, "mg_difficulty", 1), selected=(persistent.mg_difficulty == 1), w=130)
                    use pref_toggle(_("HARD"), SetField(persistent, "mg_difficulty", 2), selected=(persistent.mg_difficulty == 2), w=130)

                use pref_onoff(_("MINIGAME TIMERS"), _("Turn off to play every minigame with no time limit."), "mg_timers", 0.06)
                use pref_onoff(_("ALLOW SKIPPING MINIGAMES"), _("Shows a SKIP button on every minigame (counts as a win)."), "mg_skip_allowed", 0.12)
                use pref_onoff(_("AUTO-SAVE ON NEW CARRIAGE"), _("Saves automatically when you enter a carriage."), "autosave_on", 0.18)
                use pref_onoff(_("BURN-REVEAL TRANSITION"), _("The ticket scene burns away to reveal the map."), "film_transition", 0.24)
                use pref_onoff(_("AGED MAP LOOK"), _("Old parchment, stains and lamp flicker over the carriage maps."), "old_map", 0.30)
                use pref_onoff(_("MAP OBJECTIVE LINE"), _("Show what to do next at the top of each carriage map."), "show_objective", 0.36)

        showif pref_tab == "access":
            vbox:
                spacing 14
                at tab_page

                use pref_onoff(_("REDUCE MOTION"), _("Stops shaking, swaying, embers, zooms and dialogue animations."), "reduce_motion", 0.0)
                use pref_onoff(_("TEXT OUTLINE"), _("Black outline around dialogue for easier reading."), "text_outline", 0.06)
                use pref_onoff(_("READABLE FONT"), _("Swap the dialogue font for a plain, clear one."), "readable_font", 0.12)

                use pref_row(_("SELF-VOICING"), _("Read the screen aloud (text-to-speech)."), 0.18):
                    use pref_toggle(_("ON"), Preference("self voicing", "enable"))
                    use pref_toggle(_("OFF"), Preference("self voicing", "disable"))

    use game_menu_back(back_action)


# ==============================================================================
# SAVE / LOAD
# ==============================================================================

screen save():
    tag menu
    use file_slots(_("SAVE"))

screen load():
    tag menu
    use file_slots(_("LOAD"))

screen file_slots(title):
    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    use game_menu_overlay
    use game_menu_nav

    frame:
        xsize config.screen_width
        ysize config.screen_height
        background None
        padding (80, 60)
        at fade_slide_in(0.0, xoff=-30)

        vbox:
            spacing 22

            use game_menu_header(title)

            hbox:
                spacing 8
                for pg in ["auto", "quick", 1, 2, 3, 4, 5, 6]:
                    button:
                        padding (20, 8)
                        background rbox("#101014", 14)
                        hover_background rbox("#1a1a22", 14)
                        selected_background rbox("#e0521f", 14)
                        action FilePage(pg)
                        at button_hover_anim
                        text str(pg).upper():
                            size 18
                            color "#8888a0"
                            hover_color "#ffd700"
                            selected_color "#0a0a0e"
                            font GFONT

            grid 3 2:
                spacing 22

                for i in range(6):
                    $ slot = i + 1

                    fixed:
                        xsize 540
                        ysize 200
                        at fade_slide_in(i * 0.05, xoff=-30)

                        button:
                            xfill True
                            yfill True
                            background rbox("#101014", 22)
                            hover_background rbox("#1c1c26", 22)
                            action FileAction(slot)
                            key "save_delete" action FileDelete(slot)
                            at nudge_hover

                            hbox:
                                spacing 20
                                xoffset 16
                                yalign 0.5

                                add FileScreenshot(slot):
                                    xysize (270, 152)
                                    fit "cover"
                                    yalign 0.5

                                vbox:
                                    yalign 0.5
                                    spacing 8
                                    text ("SLOT [slot]"):
                                        size 18
                                        color "#e6a817"
                                        font GFONT
                                    text FileTime(slot, format="%b %d, %H:%M", empty=_("EMPTY SLOT")):
                                        size 20
                                        color "#c9c9d8"
                                        hover_color "#ffd700"
                                        font GFONT

                        if FileLoadable(slot):
                            button:
                                xalign 1.0
                                yalign 0.0
                                xoffset -10
                                yoffset 10
                                xsize 34
                                ysize 34
                                background rbox("#00000000", 17)
                                hover_background rbox("#e0521f", 17)
                                action FileDelete(slot)
                                text "X":
                                    align (0.5, 0.5)
                                    size 16
                                    color "#666677"
                                    hover_color "#ffffff"
                                    font GFONT

    use game_menu_back(back_action)


# ==============================================================================
# HISTORY
# ==============================================================================

screen history():
    tag menu

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    use game_menu_overlay
    use game_menu_nav

    frame:
        xsize config.screen_width
        ysize config.screen_height
        background None
        padding (80, 60)
        at fade_slide_in(0.0, xoff=-30)

        vbox:
            xsize (config.screen_width - 160)
            spacing 20

            use game_menu_header(_("HISTORY"))

            viewport:
                xsize (config.screen_width - 160)
                ysize (config.screen_height - 260)
                mousewheel True
                draggable True
                scrollbars "vertical"
                yinitial 1.0
                vbox:
                    spacing 18
                    for entry in _history_list:
                        vbox:
                            spacing 4
                            if entry.who:
                                text entry.who:
                                    bold True
                                    size 24
                                    color "#ffd700"
                                    font GFONT
                            text entry.what:
                                size 24
                                color "#ffffff"
                                font say_font()
                    if not _history_list:
                        text _("The backlog is empty."):
                            color "#8888a0"
                            font GFONT

    use game_menu_back(back_action)


# ==============================================================================
# CREDITS  (ticket cards scrolling past a title panel)
# ==============================================================================

define CREDITS_LIST = [
    ("DIRECTION & DESIGN", ["Eric Zheng"]),
    ("GAME UI & PROGRAMMING", ["Eric Zheng"]),
    ("FINANCIAL AND BUDGET DIRECTOR", ["Eric Zheng"]),
    ("R&D AND TECHNICAL SUPPORT", ["Eric Zheng"]),
    ("VISUAL EFFECTS AND ANIMATION", ["Eric Zheng"]),
    ("PROGRAMMING", ["Ryan"]),
    ("LEAD GRAPHIC DESIGNERS", ["Hannah", "Aydin"]),
    ("STORY & WRITING", ["Hannah"]),
    ("CHARACTER DESIGN", ["Hannah", "Aydin"]),
    ("MAP DESIGN", ["Aydin"]),
]

init python:
    def credits_step(adj):
        try:
            if adj.value >= adj.range - 2:
                adj.change(0)
            else:
                adj.change(adj.value + 1.3)
        except Exception:
            pass

screen about():
    tag menu
    key "game_menu" action (ShowMenu("main_menu") if main_menu else Return())
    default cred_adj = ui.adjustment()

    add Solid("#08080c")

    if persistent.menu_fx and not persistent.reduce_motion:
        for sy, sdur, sdelay, slen in MENU_STREAKS:
            add Solid("#ffffff10", xsize=slen, ysize=2):
                ypos sy
                at streak(sdur, sdelay)

    # ---- left title panel ----
    frame:
        xpos 80
        ypos 70
        xsize 560
        ysize 830
        padding (2, 2)
        background rbox("#ffffff1e", 40)
        at fade_slide_in(0.0, xoff=-50)

        frame:
            xfill True
            yfill True
            padding (40, 40)
            background rbox("#14141aee", 38)

            vbox:
                spacing 26
                xfill True

                text _("CREDITS"):
                    xalign 0.5
                    size 54
                    color "#ffffff"
                    font GFONT

                add rbox("#e0521f", 2):
                    xalign 0.5
                    xsize 160
                    ysize 6

                add "game_logo_cycle":
                    xsize 440
                    ysize 260
                    fit "contain"
                    xalign 0.5

                text _("A MURDER MYSTERY ON THE GREKHOV EXPRESS"):
                    xalign 0.5
                    text_align 0.5
                    size 14
                    color "#8888a0"
                    font GFONT

                null height 10

                text _("Version [config.version]"):
                    xalign 0.5
                    size 20
                    color "#e6a817"
                    font GFONT

                text _("Made with Ren'Py [renpy.version_only]"):
                    xalign 0.5
                    size 16
                    color "#8888a0"
                    font GFONT

    # ---- scrolling ticket cards ----
    viewport:
        xpos 720
        ypos 70
        xsize 1120
        ysize 830
        yadjustment cred_adj
        mousewheel True
        draggable True

        vbox:
            xsize 1100
            spacing 22

            null height 760

            for ci, (role, names) in enumerate(CREDITS_LIST):
                frame:
                    xfill True
                    background rbox("#14141a", 26)
                    padding (0, 0)

                    # ticket stub on the left
                    hbox:
                        frame:
                            xsize 150
                            ysize 130
                            background rbox("#e0521f", 26)
                            text ("%02d" % (ci + 1)):
                                align (0.5, 0.5)
                                size 54
                                color "#0a0a0e"
                                font GFONT

                        # perforation dots
                        vbox:
                            xsize 24
                            yalign 0.5
                            spacing 10
                            for _d in range(6):
                                add rbox("#33334a", 4):
                                    xalign 0.5
                                    xsize 8
                                    ysize 8

                        vbox:
                            yalign 0.5
                            spacing 6
                            xoffset 14
                            text role:
                                size 20
                                color "#e0521f"
                                font GFONT
                            for nm in names:
                                text nm:
                                    size 44
                                    color "#ffffff"
                                    font GFONT

            frame:
                xfill True
                background rbox("#14141a", 26)
                padding (40, 34)
                vbox:
                    spacing 10
                    xalign 0.5
                    text _("SPECIAL CREDITS"):
                        xalign 0.5
                        size 20
                        color "#e6a817"
                        font GFONT
                    text _("larp music"):
                        xalign 0.5
                        size 44
                        color "#ffffff"
                        font GFONT

            text _("THANKS FOR PLAYING!"):
                xalign 0.5
                size 64
                italic True
                color "#8888a0"
                font GFONT

            null height 760

    timer 0.03 repeat True action Function(credits_step, cred_adj)

    fixed:
        xpos 80
        yalign 0.95
        xsize 160
        ysize 50
        use rbtn(_("BACK"), (ShowMenu("main_menu") if main_menu else Return()), w=160, h=50, r=14, size=24)


# ==============================================================================
# ENDING CARD
# ==============================================================================

screen ending_card(label_text, title, subtitle, accent="#e0521f"):
    modal True
    zorder 250

    add Solid("#000000")

    vbox:
        align (0.5, 0.5)
        spacing 24
        at fade_in(0.4)

        text label_text:
            xalign 0.5
            size 28
            color accent
            font GFONT
        text title:
            xalign 0.5
            size 84
            color "#ffffff"
            font GFONT
        add rbox(accent, 2):
            xalign 0.5
            xsize 240
            ysize 6
            at underline_in(0.9)
        text subtitle:
            xalign 0.5
            size 26
            color "#8888a0"
            font GFONT

    text _("Click to return to the main menu"):
        xalign 0.5
        yalign 0.94
        size 18
        color "#55556a"
        font GFONT
        at fade_in(2.0)

    button:
        xfill True
        yfill True
        background None
        action Return()
    key "dismiss" action Return()


# ==============================================================================
# HELP
# ==============================================================================

screen help():
    tag menu

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    use game_menu_overlay
    use game_menu_nav

    frame:
        xsize config.screen_width
        ysize config.screen_height
        background None
        padding (80, 60)
        at fade_slide_in(0.0, xoff=-30)

        vbox:
            xsize (config.screen_width - 160)
            spacing 20

            use game_menu_header(_("HELP"))

            vbox:
                spacing 10
                text _("Keyboard Controls"):
                    color "#e6a817"
                    font GFONT
                text _("Enter / Space: Advance dialogue"):
                    color "#ffffff"
                    font GFONT
                text _("Escape: Toggle Game Menu"):
                    color "#ffffff"
                    font GFONT
                text _("Ctrl: Fast Forward while held"):
                    color "#ffffff"
                    font GFONT
                text _("Tab: Toggle Skipping"):
                    color "#ffffff"
                    font GFONT
                text _("Delete (over a save slot): Delete that save"):
                    color "#ffffff"
                    font GFONT
                text _("Minigames: Space = act, Up/Down = stoke/vent (engine)"):
                    color "#ffffff"
                    font GFONT
                text _("J: Open the clue journal"):
                    color "#ffffff"
                    font GFONT

    use game_menu_back(back_action)


# ==============================================================================
# CONFIRM / NOTIFY / SKIP INDICATOR
# ==============================================================================

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200

    add Solid("#00000099"):
        xsize 1920
        ysize 1080

    frame:
        xalign 0.5
        yalign 0.5
        xsize 820
        background rbox("#14141aee", 40)
        padding (50, 40)
        at confirm_pop

        vbox:
            xfill True
            spacing 34

            text message:
                xalign 0.5
                text_align 0.5
                size 34
                color "#f2e6d8"
                font GFONT

            hbox:
                xalign 0.5
                spacing 24
                use rbtn(_("Yes"), yes_action, w=200, h=66, r=22, size=28, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")
                use rbtn(_("No"), no_action, w=200, h=66, r=22, size=28)

    key "game_menu" action no_action

screen notify(message):
    zorder 100
    frame:
        xalign 0.99
        yalign 0.93
        xoffset -240
        background rbox("#101014cc", 14)
        padding (18, 12)
        at notify_anim
        text message:
            size 20
            color "#ffffff"
            font GFONT
    timer 3.25:
        action Hide("notify")

screen skip_indicator():
    zorder 100
    frame:
        xpos 0.05
        yalign 0.1
        background rbox("#101014cc", 14)
        padding (16, 10)
        at loading_pulse
        text _("Skipping..."):
            font GFONT


# ##############################################################################
#   BURN TRANSITION, AGED MAP LOOK, MINIGAMES, EXTRAS MENU
# ##############################################################################

# ==============================================================================
# 1. BURN-REVEAL TRANSITION + AGED MAP LOOK
# ==============================================================================

define flash = Fade(0.08, 0.0, 0.35, color="#ffffff")

# Paper burns away from the middle outwards, ragged edge 120px wide
define burn_reveal = ImageDissolve("images/burn_mask.png", 2.4, ramplen=120)

transform map_settle:
    xalign 0.5
    yalign 0.5
    zoom 1.10
    ease 2.6 zoom 1.0

transform stamp_slam:
    transform_anchor True
    anchor (0.5, 0.5)
    alpha 0.0
    zoom 2.6
    rotate -10
    pause 0.3
    easein 0.16 alpha 1.0 zoom 1.0 rotate -4
    easeout 0.08 zoom 1.07
    ease 0.10 zoom 1.0
    pause 1.7
    ease 0.5 alpha 0.0

transform train_rumble:
    xalign 0.5
    yalign 0.5
    zoom 1.012
    block:
        linear 0.06 xoffset -2 yoffset 1
        linear 0.06 xoffset 2 yoffset -1
        linear 0.06 xoffset -1 yoffset -1
        linear 0.06 xoffset 2 yoffset 1
        linear 0.06 xoffset -2 yoffset 0
        linear 0.06 xoffset 0 yoffset 0
        pause 6.0
        repeat

transform map_title_in:
    alpha 0.0
    yoffset -20
    ease 0.6 alpha 1.0 yoffset 0

transform map_deco_in:
    alpha 0.0
    ease 1.0 alpha 1.0

transform lamp_flicker:
    alpha 0.05
    block:
        choice:
            linear 0.09 alpha 0.11
        choice:
            linear 0.14 alpha 0.03
        choice:
            linear 0.06 alpha 0.15
        choice:
            linear 0.2 alpha 0.07
        repeat

transform dust_mote(dur=14.0, delay=0.0, sway=30):
    alpha 0.0
    ypos 0.0
    pause delay
    block:
        ypos -0.05
        xoffset 0
        alpha 0.0
        parallel:
            linear dur ypos 1.05
        parallel:
            ease dur*0.3 alpha 0.55
            pause dur*0.4
            ease dur*0.3 alpha 0.0
        parallel:
            ease dur*0.5 xoffset sway
            ease dur*0.5 xoffset -sway
        repeat

screen burn_embers():
    zorder 92
    for ex, esz, edur, edelay, esway in MENU_EMBERS:
        add Solid("#ffb04acc"):
            xpos ex
            xsize esz + 2
            ysize esz + 2
            at ember(edur * 0.45, edelay * 0.12, esway)
    timer 3.4 action Hide("burn_embers")

screen map_stamp(title, sub=""):
    zorder 95
    frame:
        align (0.5, 0.42)
        padding (4, 4)
        background rbox("#7a1f12", 14)
        at stamp_slam
        frame:
            padding (60, 26)
            background rbox("#e9d9b4cc", 12)
            vbox:
                spacing 4
                text title:
                    xalign 0.5
                    size 96
                    color "#7a1f12"
                    font "gui/Graduate-Regular.ttf"
                if sub:
                    text sub:
                        xalign 0.5
                        size 30
                        color "#7a1f12"
                        font "gui/Graduate-Regular.ttf"
    timer 3.0 action Hide("map_stamp")

define MAP_TITLES = {
    "carriage_1_map": ("CARRIAGE 1", "FIRST CLASS"),
    "carriage_2_map": ("CARRIAGE 2", "THE LOUNGE"),
    "carriage_3_map": ("CARRIAGE 3", "SLEEPER CABINS"),
    "carriage_4_map": ("CARRIAGE 4", "STAFF CART"),
    "carriage_5_map": ("CARRIAGE 5", "STAFF & STORAGE"),
    "carriage_2_part2_map": ("CARRIAGE 2", "THE CRIME SCENE"),
    "carriage_2_part2_investigation_map": ("CARRIAGE 2", "THE CRIME SCENE"),
    "carriage_2_part2_after_map": ("CARRIAGE 2", "THE CRIME SCENE"),
    "carriage_3_part2_map": ("CARRIAGE 3", "SLEEPER CABINS"),
    "carriage_5_part2_map": ("CARRIAGE 5", "STAFF & STORAGE"),
}

init python:
    config.overlay_screens.append("old_map_fx")

    def active_map_title():
        if not persistent.old_map:
            return None
        for name, t in MAP_TITLES.items():
            if renpy.get_screen(name):
                return t
        return None

screen old_map_fx():
    zorder 40
    $ mt = active_map_title()
    if mt:
        if renpy.loadable("images/old_map_overlay.png"):
            add "images/old_map_overlay.png":
                xysize (config.screen_width, config.screen_height)
                blend "multiply"
        else:
            add Solid("#c9a46a"):
                xysize (config.screen_width, config.screen_height)
                blend "multiply"
                alpha 0.55
        if not persistent.reduce_motion:
            add Solid("#ffb050"):
                xysize (config.screen_width, config.screen_height)
                blend "add"
                at lamp_flicker
            for dx, dsz, ddur, ddelay, dsway in MENU_EMBERS[:14]:
                add Solid("#fff3d0aa"):
                    xpos dx
                    xsize max(2, dsz - 2)
                    ysize max(2, dsz - 2)
                    at dust_mote(ddur * 1.8, ddelay, dsway)
        if renpy.loadable("images/map_deco.png"):
            add "images/map_deco.png":
                xysize (config.screen_width, config.screen_height)
                at map_deco_in
        frame:
            xalign 0.5
            ypos 70
            padding (30, 8)
            background rbox("#e9d9b4c0", 14)
            at map_title_in
            hbox:
                spacing 18
                text mt[0]:
                    size 26
                    color "#5a2a12"
                    font "gui/Graduate-Regular.ttf"
                text mt[1]:
                    size 20
                    color "#7a4a28"
                    yalign 0.5
                    font "gui/Graduate-Regular.ttf"
        # objective line under the title plate (toggle in Settings > Gameplay)
        if persistent.show_objective:
            $ obj_text = current_objective()
            frame:
                xalign 0.5
                ypos 130
                padding (20, 6)
                background rbox("#e9d9b488", 12)
                at map_title_in
                text "OBJECTIVE: [obj_text]":
                    size 18
                    color "#5a2a12"
                    font "gui/Graduate-Regular.ttf"


# ==============================================================================
# 2. MISC HELPERS
# ==============================================================================

init python:
    def autosave_checkpoint():
        """Call as  $ autosave_checkpoint()  when entering a carriage."""
        if persistent.autosave_on:
            try:
                renpy.force_autosave(take_screenshot=True)
            except Exception:
                pass

    # ---- in-game train rumble (SCREEN SHAKE / RUMBLE setting) -------------------
    def apply_rumble(force=False):
        try:
            if getattr(store, "main_menu", False):
                return
            want = bool(persistent.screen_shake_enabled and not persistent.reduce_motion)
            if force or store.rumble_on != want:
                renpy.show_layer_at([train_rumble] if want else [], layer="master", reset=False)
                store.rumble_on = want
        except Exception:
            pass

    # label name -> ending id (used by the ENDINGS gallery; no script edits needed)
    ENDING_LABELS = {
        "ending_1_death": "death",
        "ending_2_escape": "escape",
        "ending_3_true": "true",
    }

    def _label_cb(name, abnormal=False):
        """Runs on every label: rumble on hubs, ending tracking, run counter."""
        try:
            if not isinstance(name, (type(u""), type(""))):
                return
            if name.endswith("_hub"):
                apply_rumble(True)
            elif name == "start":
                persistent.runs = (persistent.runs or 0) + 1
            elif name in ENDING_LABELS:
                unlock_ending(ENDING_LABELS[name])
        except Exception:
            pass

    config.label_callback = _label_cb

    def mg_mult():
        """Difficulty multiplier: >1 is harder."""
        try:
            return [0.75, 1.0, 1.35][persistent.mg_difficulty]
        except Exception:
            return 1.0

    def mg_timed():
        return bool(persistent.mg_timers)

    def mg_record(key, ach=None):
        if ach:
            try:
                achievement.grant(ach)
            except Exception:
                pass
        sfx("win")
        persistent.mg_won = set(persistent.mg_won) | set([key])
        try:
            achievement.progress("game_night", len(persistent.mg_won))
        except Exception:
            pass


# ==============================================================================
# 3. MINIGAME SHELL
# ==============================================================================

screen mg_shell(title, sub="", w=980, h=720, skippable=True):
    modal True
    zorder 300

    add Solid("#000000b8")

    fixed:
        xalign 0.5
        yalign 0.5
        xsize w
        ysize h
        at confirm_pop

        add rbox("#000000aa", 40):
            xsize w
            ysize h
            xoffset 8
            yoffset 14
            blur 24

        frame:
            xsize w
            ysize h
            background rbox("#14141aee", 40)
            padding (44, 34)

            vbox:
                spacing 12
                text title:
                    size 32
                    color "#ffd700"
                    font GFONT
                add rbox("#e0521f", 2):
                    xsize 160
                    ysize 6
                if sub:
                    text sub:
                        size 17
                        color "#8888a0"
                        font GFONT
                        xsize w - 90
                null height 6
                transclude

    if persistent.mg_skip_allowed:
        fixed:
            xalign (0.38 if renpy.get_screen("mahjong_minigame") else 0.5)
            yalign 0.975
            xsize 160
            ysize 48
            use rbtn(_("SKIP"), Return("win"), w=160, h=48, r=14, size=20)

screen mg_continue(result):
    hbox:
        xalign 0.5
        use rbtn(_("CONTINUE"), Return(result), w=260, h=58, r=22, size=24, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")


# ==============================================================================
# MINIGAME A  -  LOCKPICK  (Carriage 1 cupboard)
# ==============================================================================

default lp_pos = 0.0
default lp_dir = 1
default lp_pins = 0
default lp_fails = 0
default lp_zone = 0.4
default lp_w = 0.2
default lp_speed = 0.9
default lp_result = None

init python:
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
            if store.lp_pins < 3:
                sfx("lock_click")
            if store.lp_pins >= 3:
                store.lp_result = "win"
                mg_record("lockpick", "tumbler_talent")
            else:
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

screen mg_lockpick():
    use mg_shell(_("PICK THE LOCK"), _("Press TURN (or SPACE) while the marker is inside the green zone. Set 3 pins. 3 slips and the pick snaps.")):
        if lp_result is None:
            timer 0.025 repeat True action Function(lockpick_tick)
            key "K_SPACE" action Function(lockpick_turn)

        null height 14
        hbox:
            xalign 0.5
            spacing 18
            for i in range(3):
                add rbox("#e6a817" if i < lp_pins else "#33334a", 26):
                    xsize 54
                    ysize 54

        null height 18
        fixed:
            xalign 0.5
            xsize 860
            ysize 56
            add rbox("#101014", 22):
                xsize 860
                ysize 56
            add rbox("#2fa84f", 6):
                xpos 10 + int(lp_zone * 840)
                xsize max(14, int(lp_w * 840))
                ysize 36
                yalign 0.5
            add rbox("#ffffff", 4):
                xpos 10 + int(lp_pos * 840) - 4
                xsize 8
                ysize 56

        null height 14
        text "Slips: [lp_fails] / 3":
            xalign 0.5
            size 22
            color "#8888a0"
            font GFONT

        null height 10
        if lp_result is None:
            hbox:
                xalign 0.5
                use rbtn(_("TURN"), Function(lockpick_turn), w=260, h=64, r=22, size=28, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")
        elif lp_result == "win":
            text _("CLICK!"):
                xalign 0.5
                size 34
                color "#ffd700"
                font GFONT
            use mg_continue("win")
        else:
            text _("The pick snapped."):
                xalign 0.5
                size 30
                color "#e0521f"
                font GFONT
            use mg_continue("lose")


# ==============================================================================
# MINIGAME B  -  SWEEP THE GLASS  (Carriage 2 broken glass)
# ==============================================================================

default sh_pos = []
default sh_got = [False] * 6
default sh_time = 30
default sh_result = None

init python:
    def shards_reset():
        store.sh_pos = [(renpy.random.randint(20, 770), renpy.random.randint(20, 250), renpy.random.randint(-70, 70)) for _i in range(6)]
        store.sh_got = [False] * 6
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

screen mg_shards():
    use mg_shell(_("SWEEP UP THE GLASS"), _("Click every shard before time runs out.")):
        if sh_result is None and mg_timed():
            timer 1.0 repeat True action Function(shards_tick)

        hbox:
            xalign 0.5
            spacing 40
            text "Shards left: [sh_got.count(False)]":
                size 22
                color "#8888a0"
                font GFONT
            if mg_timed():
                text "Time: [sh_time]":
                    size 22
                    color "#8888a0"
                    font GFONT

        null height 10
        fixed:
            xalign 0.5
            xsize 860
            ysize 330
            add rbox("#0e0e12", 22):
                xsize 860
                ysize 330
            for i, sp in enumerate(sh_pos):
                if not sh_got[i]:
                    button:
                        xpos sp[0]
                        ypos sp[1]
                        xsize 72
                        ysize 30
                        background rbox("#bfe6f2", 8)
                        hover_background rbox("#ffffff", 8)
                        action Function(shards_pick, i)
                        at tilt(sp[2])

        null height 18
        if sh_result == "win":
            text _("All swept up."):
                xalign 0.5
                size 30
                color "#ffd700"
                font GFONT
            use mg_continue("win")
        elif sh_result == "lose":
            text _("Out of time!"):
                xalign 0.5
                size 30
                color "#e0521f"
                font GFONT
            use mg_continue("lose")


# ==============================================================================
# MINIGAME C  -  MAHJONG  (Carriage 2, Shunyu)
# ==============================================================================

default mj_tiles = []
default mj_matched = [False] * 12
default mj_revealed = [False] * 12
default mj_first = None
default mj_pending = None
default mj_lock = False
default mj_result = None
default mj_moves_left = 14
default mj_time_left = 45

init python:
    MJ_FACES = ["I", "II", "III", "IV", "V", "VI"]

    def mahjong_reset():
        d = persistent.mg_difficulty
        faces = MJ_FACES * 2
        renpy.random.shuffle(faces)
        store.mj_tiles = faces
        store.mj_matched = [False] * 12
        store.mj_revealed = [False] * 12
        store.mj_first = None
        store.mj_pending = None
        store.mj_lock = False
        store.mj_result = None
        store.mj_moves_left = [18, 14, 11][d]
        store.mj_time_left = [60, 45, 35][d]

    def _mahjong_check_end():
        if store.mj_result is not None:
            return
        if all(store.mj_matched):
            store.mj_result = "win"
            mg_record("mahjong", "high_roller_win")
        elif not store.mj_lock and store.mj_moves_left <= 0:
            store.mj_result = "lose"

    def mahjong_pick(i):
        if store.mj_result is not None or store.mj_lock:
            return
        if store.mj_matched[i] or store.mj_revealed[i]:
            return
        store.mj_revealed[i] = True
        if store.mj_first is None:
            store.mj_first = i
        else:
            j = store.mj_first
            store.mj_first = None
            store.mj_moves_left -= 1
            if store.mj_tiles[i] == store.mj_tiles[j]:
                store.mj_matched[i] = True
                store.mj_matched[j] = True
                store.mj_revealed[i] = False
                store.mj_revealed[j] = False
            else:
                store.mj_pending = (i, j)
                store.mj_lock = True
            _mahjong_check_end()
        renpy.restart_interaction()

    def mahjong_hide_mismatch():
        if store.mj_pending is not None:
            for idx in store.mj_pending:
                store.mj_revealed[idx] = False
        store.mj_pending = None
        store.mj_lock = False
        _mahjong_check_end()
        renpy.restart_interaction()

    def mahjong_tick():
        if store.mj_result is not None or not mg_timed():
            return
        store.mj_time_left -= 1
        if store.mj_time_left <= 0:
            store.mj_time_left = 0
            store.mj_result = "lose"
        renpy.restart_interaction()

screen mahjong_minigame():
    use mg_shell(_("MAHJONG - MATCH THE TILES"), "", w=760, h=700, skippable=False):
        if mj_result is None and mg_timed():
            timer 1.0 repeat True action Function(mahjong_tick)
        if mj_lock:
            timer 0.9 action Function(mahjong_hide_mismatch)

        hbox:
            xalign 0.5
            spacing 30
            text "Moves left: [mj_moves_left]":
                size 22
                color "#8888a0"
                font GFONT
            if mg_timed():
                text "Time: [mj_time_left]":
                    size 22
                    color "#8888a0"
                    font GFONT

        null height 8
        grid 4 3:
            xalign 0.5
            spacing 12
            for i in range(12):
                button:
                    xsize 120
                    ysize 100
                    background rbox("#e0521f" if mj_matched[i] else ("#33334a" if mj_revealed[i] else "#101014"), 22)
                    hover_background rbox("#e0521f" if mj_matched[i] else "#2a2a35", 22)
                    action Function(mahjong_pick, i)
                    at button_hover_anim
                    text (mj_tiles[i] if (mj_revealed[i] or mj_matched[i]) else "?"):
                        align (0.5, 0.5)
                        size 38
                        color "#ffffff"
                        font GFONT

        null height 8
        if mj_result == "win":
            text _("You matched them all!"):
                xalign 0.5
                size 26
                color "#ffd700"
                font GFONT
            use mg_continue("win")
        elif mj_result == "lose":
            text _("Out of moves or time!"):
                xalign 0.5
                size 26
                color "#e0521f"
                font GFONT
            use mg_continue("lose")

    fixed:
        xalign 0.5
        yalign 0.975
        xsize 200
        ysize 50
        use rbtn(_("WALK AWAY"), Return("lose"), w=200, h=50, r=14, size=22)


# ==============================================================================
# MINIGAME D  -  MISHA'S BLOCKS  (Carriage 3 toys)
# ==============================================================================

define MS_COLORS = ["#a83a2e", "#2c6a9c", "#2c8a4f", "#c9a21a"]
define MS_LIT    = ["#ff8a7a", "#7fcaff", "#7dffb0", "#fff08a"]
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
    use mg_shell(_("MISHA'S BLOCKS"), _("Watch the order the blocks light up, then repeat it. Don't lose track.")):
        if ms_phase == "show" and ms_result is None:
            timer (0.6 / mg_mult()) repeat True action Function(blocks_show_step)
        if ms_phase == "input" and ms_lit_i is not None:
            timer 0.25 action Function(blocks_unlight)

        $ ms_max = [4, 3, 2][persistent.mg_difficulty]
        hbox:
            xalign 0.5
            spacing 40
            text "Round [ms_round] / [MS_ROUNDS]":
                size 22
                color "#8888a0"
                font GFONT
            text "Mistakes: [ms_strikes] / [ms_max]":
                size 22
                color "#8888a0"
                font GFONT
            text ("WATCH" if ms_phase == "show" else "YOUR TURN"):
                size 22
                color ("#e6a817" if ms_phase == "show" else "#6dffa5")
                font GFONT

        null height 14
        grid 2 2:
            xalign 0.5
            spacing 18
            for i in range(4):
                button:
                    xsize 190
                    ysize 150
                    background rbox(MS_LIT[i] if ms_lit_i == i else MS_COLORS[i], 26)
                    hover_background rbox(MS_LIT[i], 26)
                    action Function(blocks_pick, i)
                    at button_hover_anim

        null height 14
        if ms_result == "win":
            text _("Misha claps, once."):
                xalign 0.5
                size 28
                color "#ffd700"
                font GFONT
            use mg_continue("win")
        elif ms_result == "lose":
            text _("Misha knocks the tower over."):
                xalign 0.5
                size 28
                color "#e0521f"
                font GFONT
            use mg_continue("lose")


# ==============================================================================
# MINIGAME E  -  ENGINE PRESSURE  (Carriage 4 engine)
# ==============================================================================

define EP_GOAL = 12.0

default ep_p = 50.0
default ep_drift = 4.0
default ep_ok = 0.0
default ep_t = 35.0
default ep_result = None

init python:
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
    use mg_shell(_("KEEP STEAM PRESSURE STEADY"), _("Stoke the fire (UP) or vent steam (DOWN). Keep the needle in the green for 12 seconds. Hit 0 or 100 and it's over.")):
        if ep_result is None:
            timer 0.1 repeat True action Function(engine_tick)
            key "K_UP" action Function(engine_push, 9)
            key "K_DOWN" action Function(engine_push, -9)

        hbox:
            xalign 0.5
            spacing 40
            text "Stable: [ep_ok:.1f] / [EP_GOAL:.0f] s":
                size 22
                color "#8888a0"
                font GFONT
            if mg_timed():
                text "Time: [ep_t:.0f]":
                    size 22
                    color "#8888a0"
                    font GFONT

        null height 18
        fixed:
            xalign 0.5
            xsize 860
            ysize 70
            add rbox("#101014", 22):
                xsize 860
                ysize 70
            add rbox("#2fa84f", 6):
                xpos 10 + int(0.38 * 840)
                xsize int(0.26 * 840)
                ysize 50
                yalign 0.5
            add rbox("#ff5a3c" if (ep_p > 85 or ep_p < 15) else "#ffffff", 4):
                xpos 10 + int(ep_p / 100.0 * 840) - 5
                xsize 10
                ysize 70

        null height 6
        hbox:
            xalign 0.5
            text "0":
                size 16
                color "#55556a"
                font GFONT
            null width 800
            text "100":
                size 16
                color "#55556a"
                font GFONT

        null height 22
        if ep_result is None:
            hbox:
                xalign 0.5
                spacing 30
                use rbtn(_("VENT  (DOWN)"), Function(engine_push, -9), w=300, h=70, r=22, size=24)
                use rbtn(_("STOKE  (UP)"), Function(engine_push, 9), w=300, h=70, r=22, size=24, bg="#8a4a22", hov="#b8631f", col="#f2e6d8", hcol="#ffffff")
        elif ep_result == "win":
            text _("Steady as she goes."):
                xalign 0.5
                size 30
                color "#ffd700"
                font GFONT
            use mg_continue("win")
        else:
            text _("The boiler shrieks."):
                xalign 0.5
                size 30
                color "#e0521f"
                font GFONT
            use mg_continue("lose")


# ==============================================================================
# MINIGAME F  -  SORT THE MAIL  (Carriage 5 mail room)
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

screen mg_mail():
    use mg_shell(_("SORT THE MAIL"), _("\"This goes to the clock, while this goes to the end. This goes to the fake ones and this goes to the friend.\"")):
        if ml_result is None and mg_timed():
            timer 0.1 repeat True action Function(mail_tick)

        $ ml_max = mail_allowed()
        hbox:
            xalign 0.5
            spacing 40
            text "Letter [min(ml_idx + 1, ML_COUNT)] / [ML_COUNT]":
                size 22
                color "#8888a0"
                font GFONT
            text "Mistakes: [ml_bad] / [ml_max]":
                size 22
                color "#8888a0"
                font GFONT
            if mg_timed() and ml_result is None:
                text "[ml_t:.1f]":
                    size 22
                    color "#e6a817"
                    font GFONT

        null height 12
        if ml_result is None:
            frame:
                xalign 0.5
                xsize 780
                ysize 150
                background rbox("#e8dcc0", 22)
                text ml_letters[ml_idx][0]:
                    align (0.5, 0.5)
                    text_align 0.5
                    xsize 700
                    size 30
                    color "#2a1f10"
                    font GFONT
            null height 8
            text ml_fb:
                xalign 0.5
                size 20
                color ("#6dffa5" if ml_fb == "RIGHT PILE" else "#ff7b6b")
                font GFONT
            null height 8
            hbox:
                xalign 0.5
                spacing 16
                use rbtn(_("CLOCK"), Function(mail_pick, "clock"), w=200, h=70, r=22, size=24)
                use rbtn(_("END"), Function(mail_pick, "end"), w=200, h=70, r=22, size=24)
                use rbtn(_("FAKE"), Function(mail_pick, "fake"), w=200, h=70, r=22, size=24)
                use rbtn(_("FRIEND"), Function(mail_pick, "friend"), w=200, h=70, r=22, size=24)
        elif ml_result == "win":
            null height 40
            text _("Every letter has a home."):
                xalign 0.5
                size 30
                color "#ffd700"
                font GFONT
            null height 30
            use mg_continue("win")
        else:
            null height 40
            text _("The mail pile collapses."):
                xalign 0.5
                size 30
                color "#e0521f"
                font GFONT
            null height 30
            use mg_continue("lose")


# ##############################################################################
#  EXTRAS
#   - Endings gallery (auto-tracked), Cast book, Stats, Secret tab (EXTRAS menu)
#   - Objective line / hint on the maps and in the clue journal
#   - Easter eggs: Konami code on the main menu, poke the key
# ##############################################################################

default persistent.endings_seen = set()
default persistent.secrets = set()
default persistent.met = set()
default persistent.playtime = 0.0
default persistent.runs = 0
default persistent.key_pokes = 0
default persistent.show_objective = True

# ---- extra achievements (registered here so ACHIEVEMENTS above stays untouched)
define NEW_ACHIEVEMENTS = [
    {"id": "konami", "title": _("Old Habits"), "description": _("Enter a very famous code on the main menu."), "hidden": True},
    {"id": "key_cut", "title": _("Loose Thread"), "description": _("Poke the key far too many times."), "hidden": True},
    {"id": "all_endings", "title": _("Every Line Ends"), "description": _("See all three endings."), "hidden": False},
]

init python:
    for _na in NEW_ACHIEVEMENTS:
        if _na["id"] not in [x["id"] for x in ACHIEVEMENTS]:
            ACHIEVEMENTS.append(_na)
            achievement.register(_na["id"])

    # ------------------------------------------------------------------ endings
    ENDINGS = [
        ("death",  "ENDING 1", "WRONG GUESS",    "Accuse the wrong person, or fail all three questions in Carriage 6.", "#a8281a", False),
        ("escape", "ENDING 2", "PARTIAL TRUTH",  "Name the killer, then answer only some of the questions in Carriage 6.", "#e6a817", False),
        ("true",   "ENDING 3", "THE TRUE LINE",  "Name the killer and answer all three questions in Carriage 6.", "#e0521f", False),
    ]

    def unlock_ending(key):
        persistent.endings_seen = set(persistent.endings_seen) | set([key])
        if len(persistent.endings_seen) >= len(ENDINGS):
            try:
                achievement.grant("all_endings")
            except Exception:
                pass

    def ending_rows():
        rows = []
        for key, lab, title, hint, accent, hidden in ENDINGS:
            seen = key in persistent.endings_seen
            rows.append({
                "label": lab,
                "title": title if seen else "???",
                "desc": hint if (seen or not hidden) else "A hidden ending.",
                "seen": seen,
                "accent": accent,
            })
        return rows

    # ------------------------------------------------------------------ cast book
    # (flag in the save, name, role, blurb). flag None = always known.
    CAST = [
        (None,                 "Dorothy",   "Ticket conductor",     "Punches tickets and asks very few questions. Not paid enough for this."),
        ("c1_talked_fedora",   "Fedora",    "Reporter",             "Here for a story. Her editor, Twinkles, is always calling."),
        ("c2_talked_eduard",   "Eduard",    "Bartender",            "Keeps a tab on everyone, especially the man at the mahjong table."),
        ("c2_talked_shunyu",   "Shunyu",    "Gambler",              "Cannot stop winning. Wants you to join in."),
        ("c3_talked_kimmy",    "Kimmy",     "Clock heiress",        "Family clock business. Travelling with her darling Himmel."),
        ("c3_talked_himmel",   "Himmel",    "Kimmy's partner",      "Jumpy around strangers. Says the toilet is to the left."),
        ("c3_talked_sebastian","Sebastian", "Butler",               "Guards the child in his care with perfect posture."),
        ("c3_talked_misha",    "Misha",     "Child, Carriage 3",    "Plays quietly with his blocks. Stares."),
        ("c4_talked_agatha",   "Agatha",    "Train medic",          "Short on patience, long on bandages."),
        ("c4_talked_ichora",   "Ichora",    "Engineer",             "Was expecting you. Gave you a key."),
        ("c5_talked_pattison", "Pattison",  "Mail worker",          "Sorts the mail to a rhyme only he understands."),
        ("c5_talked_alexander","Alexander", "Storage carriage",     "Sells the banned super maple sugar. First one is free."),
    ]

    def cast_rows():
        rows = []
        met_now = set(persistent.met)
        for flag, name, role, blurb in CAST:
            met = (flag is None) or bool(getattr(store, flag, False)) or (flag in met_now)
            if flag and met and flag not in met_now:
                met_now.add(flag)
            rows.append({
                "name": name if met else "???",
                "role": role if met else "Not met yet.",
                "blurb": blurb if met else "Talk to everyone on the train.",
                "met": met,
            })
        if met_now != set(persistent.met):
            persistent.met = met_now
        return rows

    # ------------------------------------------------------------------ playtime / stats
    _pt_last = [None]

    def playtime_poll():
        try:
            import time
            now = time.time()
            last = _pt_last[0]
            _pt_last[0] = now
            if last is not None and not getattr(store, "main_menu", False):
                dt = now - last
                if 0 < dt < 5:
                    persistent.playtime = (persistent.playtime or 0.0) + dt
        except Exception:
            pass

    if playtime_poll not in config.periodic_callbacks:
        config.periodic_callbacks.append(playtime_poll)

    def format_time(sec):
        sec = int(sec or 0)
        return "%dh %02dm" % (sec // 3600, (sec % 3600) // 60)

    def stats_rows():
        done, total = achievement_counts()
        return [
            ("TIME ON THE TRAIN", format_time(persistent.playtime)),
            ("JOURNEYS STARTED", str(persistent.runs or 0)),
            ("ENDINGS SEEN", "%d / %d" % (len(persistent.endings_seen), len(ENDINGS))),
            ("ACHIEVEMENTS", "%d / %d" % (done, total)),
            ("MINIGAMES WON", "%d / 6" % len(persistent.mg_won)),
            ("PASSENGERS MET", "%d / %d" % (len([1 for r in cast_rows() if r["met"]]), len(CAST))),
        ]

    # ------------------------------------------------------------------ objective / hint
    def current_objective():
        g = lambda n: bool(getattr(store, n, False))
        if not g("in_loop"):
            if not g("c1_talked_fedora"):
                return "Carriage 1: talk to Fedora."
            if not (g("c2_talked_eduard") and g("c2_talked_shunyu")):
                return "Carriage 2: talk to Eduard and Shunyu."
            if not (g("c3_talked_kimmy") and g("c3_talked_himmel") and g("c3_talked_sebastian") and g("c3_talked_misha")):
                return "Carriage 3: speak to everyone in the cabins."
            if not (g("c4_talked_agatha") and g("c4_talked_ichora")):
                return "Carriage 4: meet the staff."
            if not (g("c5_talked_pattison") and g("c5_talked_alexander")):
                return "Carriage 5: talk to Pattison and Alexander."
            return "Go through the door at the end of Carriage 5."
        if not g("c2_p2_found_body"):
            return "Search Carriage 2. Something is wrong at the second table."
        if not (g("c2_p2_reinterviewed_eduard") and g("c2_p2_reinterviewed_agatha")):
            return "Carriage 2: question Eduard and Agatha."
        if not g("clue_drug_wrapper"):
            return "Carriage 3: something is hidden in the luggage."
        if not g("clue_hidden_tile"):
            return "Carriage 3: that carpet has been sticking up all along."
        if not (g("kimmy_reinterviewed") and g("himmel_reinterviewed") and g("sebastian_reinterviewed") and g("misha_reinterviewed")):
            return "Carriage 3: question everyone again."
        if not (g("alexander_reinterviewed") and g("pattison_reinterviewed")):
            return "Carriage 5: question Alexander, then Pattison."
        return "You have everything. Decide who did it."

    # ------------------------------------------------------------------ secrets
    KONAMI = ["u", "u", "d", "d", "l", "r", "l", "r", "b", "a"]
    _konami_buf = []

    def konami_feed(k):
        _konami_buf.append(k)
        _konami_buf[:] = _konami_buf[-len(KONAMI):]
        if _konami_buf == KONAMI:
            del _konami_buf[:]
            if "konami" not in persistent.secrets:
                persistent.secrets = set(persistent.secrets) | set(["konami"])
                try:
                    achievement.grant("konami")
                except Exception:
                    pass
            sfx("win")
            renpy.show_screen("map_stamp", "4:01", "ONE MORE STOP")
            renpy.notify("EXTRAS: a new tab appeared.")
            renpy.restart_interaction()

    def key_poke():
        persistent.key_pokes = (persistent.key_pokes or 0) + 1
        n = persistent.key_pokes
        sfx("lock_click")
        if n == 10:
            renpy.notify("Stop poking the key. Please.")
        elif n == 25:
            persistent.secrets = set(persistent.secrets) | set(["key_cut"])
            try:
                achievement.grant("key_cut")
            except Exception:
                pass
            renpy.notify("The string creaks. It is holding... for now.")
        elif n == 50:
            renpy.notify("Ichora says: 'Hey! That is MY key!'")
        renpy.restart_interaction()

    SECRET_NOTES = [
        "Every timetable on this train says 4:00. Every single one.",
        "Pattison's rhyme has four lines. Not all of them are about mail.",
        "Thank you for playing, detective.  - Blackberry Studios",
    ]

# ---- Konami listener (used by the main menu) ---------------------------------
screen secret_listener():
    key "K_UP" action Function(konami_feed, "u")
    key "K_DOWN" action Function(konami_feed, "d")
    key "K_LEFT" action Function(konami_feed, "l")
    key "K_RIGHT" action Function(konami_feed, "r")
    key "K_b" action Function(konami_feed, "b")
    key "K_a" action Function(konami_feed, "a")

# ---- EXTRAS menu --------------------------------------------------------------
init python:
    def extras_tabs():
        tabs = [("endings", _("ENDINGS")), ("cast", _("CAST")), ("stats", _("STATS"))]
        if "konami" in persistent.secrets:
            tabs.append(("secret", _("4:01")))
        return tabs

screen extras_menu():
    tag menu
    modal True
    default xt = "endings"

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    $ ex_w = config.screen_width - 200

    add Solid("#0a0a0e")
    use game_menu_nav

    text _("EXTRAS"):
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

    hbox:
        xpos 80
        ypos 135
        spacing 10
        for tkey, tlabel in extras_tabs():
            button:
                padding (22, 10)
                background rbox("#101014", 14)
                hover_background rbox("#1a1a22", 14)
                selected_background rbox("#e0521f", 14)
                selected_hover_background rbox("#f06a35", 14)
                action SetScreenVariable("xt", tkey)
                selected (xt == tkey)
                at button_hover_anim
                text tlabel:
                    size 18
                    color "#8888a0"
                    hover_color "#ffd700"
                    selected_color "#0a0a0e"
                    selected_hover_color "#0a0a0e"
                    font GFONT

    viewport:
        id "ex_vp"
        xpos 80
        ypos 200
        xsize ex_w
        ysize (config.screen_height - 360)
        mousewheel True
        draggable True

        vbox:
            xsize ex_w
            spacing 12

            if xt == "endings":
                for idx, er in enumerate(ending_rows()):
                    frame:
                        xfill True
                        background rbox("#17150d" if er["seen"] else "#101014", 22)
                        padding (26, 20)
                        at row_pop(min(idx * 0.06, 0.5))
                        hbox:
                            spacing 24
                            add rbox(er["accent"] if er["seen"] else "#33334a", 6):
                                xsize 8
                                ysize 76
                                yalign 0.5
                            vbox:
                                spacing 6
                                yalign 0.5
                                text er["label"]:
                                    size 16
                                    color (er["accent"] if er["seen"] else "#55556a")
                                    font GFONT
                                text er["title"]:
                                    size 30
                                    color ("#ffffff" if er["seen"] else "#666677")
                                    font GFONT
                                text er["desc"]:
                                    size 18
                                    color ("#c9c9d8" if er["seen"] else "#55556a")
                                    font GFONT
                                    xsize (ex_w - 160)

            elif xt == "cast":
                for idx, cr in enumerate(cast_rows()):
                    frame:
                        xfill True
                        background rbox("#17150d" if cr["met"] else "#101014", 22)
                        padding (26, 14)
                        at row_pop(min(idx * 0.03, 0.5))
                        hbox:
                            spacing 24
                            add rbox("#e6a817" if cr["met"] else "#33334a", 6):
                                xsize 8
                                ysize 60
                                yalign 0.5
                            vbox:
                                spacing 4
                                yalign 0.5
                                text cr["name"]:
                                    size 26
                                    color ("#ffd700" if cr["met"] else "#666677")
                                    font GFONT
                                text cr["role"]:
                                    size 16
                                    color ("#e6a817" if cr["met"] else "#55556a")
                                    font GFONT
                                text cr["blurb"]:
                                    size 18
                                    color ("#e8e4dc" if cr["met"] else "#55556a")
                                    font GFONT
                                    xsize (ex_w - 160)

            elif xt == "stats":
                for idx, sr in enumerate(stats_rows()):
                    frame:
                        xfill True
                        background rbox("#101014", 22)
                        padding (26, 18)
                        at row_pop(min(idx * 0.05, 0.5))
                        fixed:
                            xfill True
                            ysize 36
                            text sr[0]:
                                size 22
                                color "#8888a0"
                                font GFONT
                                yalign 0.5
                            text sr[1]:
                                size 26
                                color "#ffd700"
                                font GFONT
                                xalign 1.0
                                yalign 0.5

            elif xt == "secret":
                text _("TICKET 4:01"):
                    size 40
                    color "#7fcaff"
                    font GFONT
                for idx, note in enumerate(SECRET_NOTES):
                    frame:
                        xfill True
                        background rbox("#0e1418", 22)
                        padding (26, 16)
                        at row_pop(min(idx * 0.08, 0.6))
                        text note:
                            size 20
                            color "#c9d8e0"
                            font GFONT
                            xsize (ex_w - 120)

    vbar:
        style "pref_vbar"
        value YScrollValue("ex_vp")
        xpos config.screen_width - 96
        ypos 200
        ysize (config.screen_height - 360)

    use game_menu_back(back_action)