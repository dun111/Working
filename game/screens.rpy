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
    # --- rounded boxes ---------------------------------------------------------
    # rbox(color, r) is the background used by nearly every panel and button.
    # It's a 9-slice Frame of a white rounded-corner mask (gui/round/rN.png,
    # made by tools/gen_ui_assets.py) tinted to `color`. The nearest generated
    # radius is used, and results are cached so screens that redraw every frame
    # don't rebuild their backgrounds each time.
    ROUND_RADII = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 34, 38, 40, 48,
                   64, 96, 128, 160, 200, 256)
    _rbox_cache = {}

    def rbox(color, r=14):
        key = (color, r)
        d = _rbox_cache.get(key)
        if d is None:
            c = Color(color)
            if r <= 0:
                d = Solid(c)
            else:
                rr = min(ROUND_RADII, key=lambda v: abs(v - r))
                d = Transform(Frame("gui/round/r%d.png" % rr, rr, rr),
                              matrixcolor=TintMatrix(c.replace_opacity(1.0)),
                              alpha=c.alpha)
            _rbox_cache[key] = d
        return d

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
    bar_invert True             # the handle starts at the top
    unscrollable "hide"         # no scrollbar when there's nothing to scroll
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
    def C(name, tag=None, plate=None, creepy=False, **kwargs):
        """
        Character with an optional sprite tag (used for automatic speaker focus
        and the talking animations) and a name-plate colour for the say screen.
        creepy=True makes their lines shake (see the say screen).
        """
        if tag:
            kwargs.setdefault("image", tag)
        if plate:
            kwargs["show_plate"] = plate
        if creepy:
            kwargs["show_creepy"] = True
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

# settings panel width: 1380 at 1920 wide, grows on wider screens
define PREF_PANEL_W = GAME_W - 540
define PREF_PANEL_H = GAME_H - 280      # settings tabs scroll past this

# Key on the main menu.  KEY_SCALE 1.0 = the original size; everything about
# the key (string, loop, swing) scales with it.
define KEY_SCALE = 2.35


# ==============================================================================
# TRANSFORMS
# ==============================================================================

# the light behind the key breathes slowly
transform key_backlight:
    alpha 0.12
    block:
        ease 3.0 alpha 0.22
        ease 3.0 alpha 0.12
        repeat

init python:
    import time as _btime

    def _board_clock(st, at):
        return Text(_btime.strftime("%H:%M"), size=18, color="#ffd76a", font=CREDIT_FONT), 1.0

    BOARD_CLOCK = DynamicDisplayable(_board_clock)

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

# the main menu: quiet for a while, then every 10 seconds the carriage
# rumbles over a joint in the track and the logo goes red. Both read the same
# clock (menu_phase) so they stay in step - and a screen refresh can't restart
# them. No rotate here - tilting the menu threw the key off.
define MENU_RUMBLE_EVERY = 10.0     # seconds from one rumble to the next
define MENU_RUMBLE_LONG = 1.4       # how long each rumble lasts

init python:
    import math as _math
    import time as _time

    class _MENU_CLOCK(object):
        t0 = None

    def menu_phase():
        """Seconds into the current rumble loop. The rumble is at the end."""
        now = _time.time()
        if _MENU_CLOCK.t0 is None:
            _MENU_CLOCK.t0 = now
        return (now - _MENU_CLOCK.t0) % MENU_RUMBLE_EVERY

    def menu_rumbling():
        """How far through the rumble we are (0 to 1), or None when calm."""
        k = menu_phase() - (MENU_RUMBLE_EVERY - MENU_RUMBLE_LONG)
        return (k / MENU_RUMBLE_LONG) if k >= 0 else None

    def _menu_shake(trans, extreme):
        k = menu_rumbling()
        if k is None:
            trans.xoffset = 0
            trans.yoffset = 0
            return 0
        t = k * MENU_RUMBLE_LONG
        a = 12 if extreme else 3
        x = a * _math.sin(t * 157.0)
        y = a * 0.8 * _math.sin(t * 113.0 + 1.0)
        # the last part: one big jolt over the joint
        if k > 0.7:
            j = _math.sin((k - 0.7) / 0.3 * _math.pi)
            x += (-30 if extreme else -4) * j
            y += (26 if extreme else 9) * j
        trans.xoffset = int(x)
        trans.yoffset = int(y)
        return 0

    def menu_shake_normal(trans, st, at):
        return _menu_shake(trans, False)

    def menu_shake_extreme(trans, st, at):
        return _menu_shake(trans, True)

    def _menu_logo(st, at):
        # yellow, flashing up red while the carriage rumbles, then easing back
        k = menu_rumbling()
        if k is not None:
            red = min(1.0, k * MENU_RUMBLE_LONG / 0.08)
        else:
            red = max(0.0, 1.0 - menu_phase() / 0.6)
        return Fixed("images/Game_Logo_Yellow.webp",
                     Transform("images/Game_Logo_Red.webp", alpha=red),
                     fit_first=True), 0.03

# RUMBLE STRENGTH: EXTREME - violent shaking and a hard lurch
transform menu_rumble_extreme:
    function menu_shake_extreme

# in game the whole carriage shakes, zoomed in a little so the edges never show
transform train_rumble_extreme:
    xalign 0.5
    yalign 0.5
    zoom 1.07
    rotate 0
    block:
        linear 0.045 xoffset -10 yoffset 7 rotate -0.4
        linear 0.045 xoffset 11 yoffset -6 rotate 0.35
        linear 0.045 xoffset -8 yoffset 9 rotate -0.25
        linear 0.045 xoffset 10 yoffset -8 rotate 0.4
        repeat 5
        easeout 0.07 xoffset -28 yoffset 24 rotate -1.2
        easein 0.13 xoffset 22 yoffset -14 rotate 0.9
        easein 0.15 xoffset 0 yoffset 0 rotate 0
        repeat

init python:
    def menu_rumble_at():
        """The main menu's shake, from Settings > RUMBLE STRENGTH."""
        if persistent.reduce_motion or not persistent.screen_shake_enabled:
            return no_shake
        return menu_rumble_extreme if persistent.rumble_extreme else menu_rumble

    def set_rumble(level):
        persistent.screen_shake_enabled = (level != "off")
        persistent.rumble_extreme = (level == "extreme")
        apply_rumble(True)
        renpy.restart_interaction()

transform menu_rumble:
    function menu_shake_normal

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

# fades in/out at the ends so it never shows over a button's rounded corners
transform shine_sweep(delay=1.5):
    alpha 0.0
    xpos -90
    pause delay
    block:
        xpos -90
        alpha 0.0
        parallel:
            linear 0.9 xpos 410
        parallel:
            linear 0.22 alpha 0.0
            linear 0.12 alpha 0.25
            pause 0.3
            linear 0.14 alpha 0.0
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
# sprite shrinks, darkens and goes see-through. Positions are remembered from your show statements.

# First appearance slides in from the sprite's own side of the screen; after
# that the speaker hops on every new line and everyone else eases back;
# "hide" fades the sprite out.
# whoever isn't talking is darkened and see-through (SP_DIM / SP_BG_ALPHA)
define SP_LIT = BrightnessMatrix(0.0) * SaturationMatrix(1.0)
define SP_DIM = BrightnessMatrix(-0.16) * SaturationMatrix(0.8)
define SP_BG_ALPHA = 0.82

transform _sp_focus(xalign=0.7):
    xanchor 0.5
    xalign xalign
    yalign 1.0
    yoffset 40
    on show:
        alpha 0.0
        zoom 1.04
        matrixcolor SP_LIT
        xoffset (hover_lift(-80) if xalign < 0.5 else hover_lift(80))
        easein anim_t(0.4) alpha 1.0 zoom 1.08 xoffset 0
    on replace:
        parallel:
            linear anim_t(0.3) zoom 1.08 alpha 1.0 xoffset 0 matrixcolor SP_LIT
        parallel:
            # little hop every time this character starts a new line
            easeout anim_t(0.11) yoffset 40 - hover_lift(14)
            easein anim_t(0.16) yoffset 40
    on hide:
        easeout anim_t(0.3) alpha 0.0

transform _sp_bg(xalign=0.3):
    xanchor 0.5
    xalign xalign
    yalign 1.0
    yoffset 40
    on show:
        alpha 0.0
        zoom 0.92
        matrixcolor SP_DIM
        xoffset (hover_lift(-80) if xalign < 0.5 else hover_lift(80))
        easein anim_t(0.4) alpha SP_BG_ALPHA zoom 0.94 xoffset 0
    on replace:
        linear anim_t(0.3) zoom 0.94 alpha SP_BG_ALPHA xoffset 0 matrixcolor SP_DIM
    on hide:
        easeout anim_t(0.3) alpha 0.0

# tag -> (xalign, "f" focused / "b" background) for every sprite shown on master
default sprite_info = {}
# is the in-game train rumble currently applied?
default rumble_on = False

init python:
    _STRING_TYPES = (type(u""), type(""))

    class TALK(object):
        """
        Who is talking right now. Plain class attributes, so none of this ends
        up in saves or rollback.
          typing  - sprite tag whose line is still typing out (drives the bob)
          who     - script variable of the last speaker ("l", "d", ...)
          changed - True when this line has a different speaker than the last
        """
        typing = None
        who = None
        changed = True

    def speaker_tag(who):
        """Script variable name ("l") -> sprite tag ("louis"), or None."""
        if not isinstance(who, _STRING_TYPES):
            return None
        return getattr(getattr(store, who, None), "image_tag", None)

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
        who = getattr(store, "_last_say_who", None)
        tag = speaker_tag(who)

        if event in ("slow_done", "end"):
            TALK.typing = None
            return
        if event == "show":
            TALK.typing = tag
            return
        if event != "begin":
            return

        TALK.changed = (who != TALK.who)
        TALK.who = who
        try:
            apply_rumble()
        except Exception:
            pass
        try:
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
                # the speaker is always re-shown so it hops on every line
                if st == want and t != tag:
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
# Character sprites (and the Carriage 6 monsters) live in characters.rpy

image black = Solid("#000000")
# The opening / loop / ending conversations on the train use the mosaic too
image Train station = "talk_bg"
# Carriage 1 with Dorothy and Fedora drawn in; a different, wrecked version for
# Part 2 (the loop). The art has transparent edges, so it sits on the dark fill.
init python:
    def carriage_art(path):
        return Fixed(Solid("#150d0d"), Transform(path, xysize=(DESIGN_W, DESIGN_H)), xysize=(DESIGN_W, DESIGN_H))

# themed(): Settings > COLOUR THEME tints these backgrounds (gamepass.rpy)
image bg carriage_1 = themed(ConditionSwitch(
    "in_loop", wide_bg(carriage_art("images/PT2_Carriage_1_With_CharacterS.webp")),
    "True", wide_bg(carriage_art("images/Carriage_1_With_CharacterS.webp"))))

# the empty carriage (no one in it) - used by the empty train
image bg carriage_1_empty = wide_bg("images/bg_carriage_1.webp")
image bg carriage_5 = themed(wide_bg("images/bg_carriage_5.webp"))

# Placeholder backgrounds: the real bg carriage 2/3/4 .webp files are not in
# the project yet. Replace each Solid with "images/bg_carriage_N.webp" once the
# art is added.
image bg carriage_2 = themed(Solid("#2a2430"))
image bg carriage_3 = themed(Solid("#242a30"))
image bg carriage_4 = themed(Solid("#2a3024"))

# "talk to <name>" conversation backgrounds live in characters.rpy

# Part 2 look: a flat red tint with a pulsing heartbeat wash on top
screen loop_overlay():
    zorder 50
    add Solid("#3a000020")
    add Solid("#ff2a1a") at heartbeat
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)


# ==============================================================================
# GLOBAL TRANSITIONS
# ==============================================================================

# Ren'Py opens its developer "Interactive Director" on D - but D is a game key
# (the door minigame uses A/D), so that shortcut is switched off.
init python:
    config.keymap["director"] = []

# keep more pictures loaded so carriages and characters don't stutter in
define config.image_cache_size_mb = 512

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

define audio.menu_theme = "Songs/main_menu.mp3"

# config.main_menu_music is set in music.rpy (MAIN MENU MUSIC: theme / shuffle)
init python:

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
    $ _RADIOUI.booting = False      # the boot screen is over: show the radio
    # start the menu's music (or the radio station that's on) - Ren'Py only
    # starts config.main_menu_music by itself, which is empty for the stations
    $ music_menu()
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
            blackberry_click()      # keeps going in secrets.rpy...

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

    _autocrop_disp = {}

    def autocrop_image(path):
        """The image with its transparent padding cropped off (built once)."""
        d = _autocrop_disp.get(path)
        if d is None:
            info = autocrop_info(path)
            d = path if info is None else Transform(path, crop=info)
            _autocrop_disp[path] = d
        return d

    # --- main-menu key ---------------------------------------------------------
    # Measured from images/Key.webp (source pixels). The file has a stray pixel
    # at the very top, so the key is cropped to its real bounds rather than
    # auto-detected at runtime (which used to scan pixels on every launch).
    KEY_CROP = (43, 903, 555, 1138)     # x, y, w, h of the key in the png
    KEY_RING_CX = 277                   # ring centre, from the crop's left edge
    KEY_BAR = (0, 79)                   # ring's top bar (top, bottom) from crop top

    # On screen (inside the swinging container, whose top is the hook):
    KEY_ZOOM = 0.257 * KEY_SCALE        # key size
    KEY_HANG = int(136 * KEY_SCALE)     # how far below the hook the ring top sits

    # gui/key_loop.png (tools/gen_ui_assets.py) is drawn at 4x for KEY_SCALE 1.5:
    # loop centre 34px and knot 10.5px below the image top, 34px wide.
    _LOOP_SC = KEY_ZOOM / 0.385
    KEY_LOOP_ZOOM = 0.25 * _LOOP_SC
    _bar_mid = (KEY_BAR[0] + KEY_BAR[1]) / 2.0 * KEY_ZOOM
    KEY_LOOP_Y = int(KEY_HANG + _bar_mid + 4 * _LOOP_SC - 34 * _LOOP_SC)
    KEY_STRING_H = int(KEY_LOOP_Y + 10.5 * _LOOP_SC)
    KEY_IMG_X = -int(KEY_RING_CX * KEY_ZOOM)
    KEY_W = int(KEY_CROP[2] * KEY_ZOOM)
    KEY_H = int(KEY_CROP[3] * KEY_ZOOM)

    KEY_IMAGE = Transform(Transform("images/Key.webp", crop=KEY_CROP), zoom=KEY_ZOOM)
    # the whole loop sits behind the key; only its front strand is drawn on top
    KEY_LOOP_BACK = Transform("gui/key_loop.png", zoom=KEY_LOOP_ZOOM)
    KEY_LOOP_FRONT = Transform("gui/key_loop_front.png", zoom=KEY_LOOP_ZOOM)

    # every save remembers whether it was made in the story or in a secret
    # game (the empty train), so CONTINUE only picks up the story
    def _save_tag(d):
        d["story"] = not getattr(store, "in_secret_game", False)

    config.save_json_callbacks.append(_save_tag)

    def latest_save():
        """The newest story save that can be loaded. Skips Ren'Py's own _reload
        slots, saves made in the secret empty-train game, and saves from before
        saves were tagged."""
        try:
            slots = renpy.list_slots(r"^(?!_)")
            slots.sort(key=lambda s: renpy.slot_mtime(s) or 0, reverse=True)
            broken = set(persistent.broken_saves or ())
            for slot in slots:
                info = renpy.slot_json(slot) or {}
                if (slot, renpy.slot_mtime(slot)) in broken:
                    continue        # tried before: made by an older version of the game
                if info.get("story") and renpy.can_load(slot):
                    return slot
        except Exception:
            pass
        return None

    def continue_game():
        """CONTINUE: load the newest save, or start a new game if there's nothing to continue.
        A save the game can't open any more goes to save_too_old, which marks it
        and comes back here to try the next one."""
        slot = latest_save()
        if slot:
            persistent.cont_trying = (slot, renpy.slot_mtime(slot))
            renpy.load(slot)
        else:
            persistent.cont_trying = None
            renpy.run(Start())

    def continue_after_fail():
        """On the main menu after a save couldn't be opened: say so, and if it
        was CONTINUE, carry on with the next save (or a new game)."""
        if persistent.cont_msg:
            persistent.cont_msg = False
            renpy.notify(_("That save is from an older version of the game and can't be opened."))
        if persistent.cont_retry:
            persistent.cont_retry = False
            continue_game()

    def _loaded_ok():
        persistent.cont_trying = None

    config.after_load_callbacks.append(_loaded_ok)

    # a save the current script can't restore: don't crash, go to save_too_old
    config.load_failed_label = "save_too_old"

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
default persistent.rumble_extreme = False     # RUMBLE STRENGTH: EXTREME
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
default persistent.broken_saves = set()   # (slot, time) of saves this version can't open
default persistent.cont_trying = None     # the save CONTINUE is opening
default persistent.cont_retry = False
default persistent.cont_msg = False
default in_secret_game = False       # True while playing the empty train (empty_train.rpy)
default persistent.film_transition = True
default persistent.old_map = True
default persistent.menu_style = "new"         # "new" or "classic" (the rounded sidebar)
default persistent.dialogue_style = "classic" # dialogue box look: classic / minimal / paper / film
default persistent.ach_toasts = True
# COMFORT / readability (Settings)
default persistent.reduce_flashes = False     # FLASHING LIGHTS: SOFTER
default persistent.brightness = 0             # SCREEN BRIGHTNESS: -2 .. +2
default persistent.hotspot_labels = "always"  # HOTSPOT LABELS: always / hover
default persistent.text_color = "light"       # DIALOGUE TEXT COLOUR (see TEXT_COLORS)
default persistent.line_spacing = 10          # LINE SPACING
default persistent.text_fx = "full"           # TEXT EFFECTS: full / still / off (text_fx.rpy)
default persistent.quick_menu_shown = True    # QUICK MENU BAR
default persistent.mg_won = set()

define DIALOGUE_SIZES = [(22, "S"), (26, "M"), (30, "L"), (34, "XL")]

init python:
    FONT_SIZE_STEPS = [22, 26, 30, 34]

    def cycle_font_size():
        cur = persistent.dialogue_font_size
        idx = FONT_SIZE_STEPS.index(cur) if cur in FONT_SIZE_STEPS else 1
        persistent.dialogue_font_size = FONT_SIZE_STEPS[(idx + 1) % len(FONT_SIZE_STEPS)]

    def erase_everything():
        """Delete every save, achievement and persistent unlock, then restart."""
        for slot in renpy.list_saved_games(fast=True):
            try:
                renpy.unlink_save(slot)
            except Exception:
                pass
        try:
            achievement.clear_all()
            achievement.sync()
        except Exception:
            pass
        persistent._clear(progress=True)
        renpy.save_persistent()
        renpy.full_restart()

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
        persistent.rumble_extreme = False
        persistent.reduce_flashes = False
        persistent.brightness = 0
        persistent.hotspot_labels = "always"
        persistent.text_color = "light"
        persistent.line_spacing = 10
        persistent.text_fx = "full"
        persistent.quick_menu_shown = True
        persistent.ingame_music = True
        persistent.song_popups = True
        persistent.radio_bar = True
        persistent.credits_style = "scroll"
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
        """afm_time is the wait before auto moves on: lower = faster."""
        try:
            t = int(_preferences.afm_time)
        except Exception:
            return ""
        word = _("FAST") if t <= 10 else (_("NORMAL") if t <= 22 else _("SLOW"))
        return "%s  %d" % (word, t)

    def afm_adjust(step):
        _preferences.afm_time = max(1, min(40, int(_preferences.afm_time) + step))
        renpy.restart_interaction()

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
    {"id": "game_night", "title": _("Game Night"), "description": _("Win every minigame on the train."), "hidden": False, "stat_max": 14},
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

            # (one hbox child: a frame given two children wraps them in a
            # full-screen fixed, which made the toast fill the screen height)
            hbox:
                spacing 16
                vbox:
                    spacing 6
                    xsize (360 if toast_icon else 456)
                    text _("ACHIEVEMENT UNLOCKED"):
                        size 14
                        color "#e6a817"
                        font GFONT
                    text title:
                        size 28
                        color "#ffffff"
                        font GFONT
                    text desc:
                        size 16
                        color "#8888a0"
                        font GFONT
                    null height 6
                    add rbox("#e6a817", 2):
                        xsize (360 if toast_icon else 456)
                        ysize 3
                        at toast_timer
                if toast_icon:
                    add toast_icon:
                        xysize (80, 80)
                        fit "contain"
                        yalign 0.0
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
# the main menu logo: yellow, and red while the carriage rumbles (_menu_logo)
image game_logo_rumble = DynamicDisplayable(_menu_logo)

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
    # no radio in the corner during the boot screen (shown again by before_main_menu)
    $ _RADIOUI.booting = True
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

# what each main-menu option does (shown when you point at it)
define MENU_HELP = {
    "NEW GAME": _("Start the story from the beginning."),
    "PLAY": _("Start the story from the beginning."),
    "CONTINUE": _("Pick up from your latest save, or start a new game if there isn't one."),
    "LOAD GAME": _("Choose a save to load."),
    "SETTINGS": _("Display, text, sound, gameplay and accessibility."),
    "ACHIEVEMENTS": _("See what you've unlocked."),
    "EXTRAS": _("Endings, cast, stats, minigames, gamepasses and more."),
    "CREDITS": _("The people who made the game."),
    "QUIT": _("Close the game."),
}

screen menu_entry(caption, act, delay=0.0, bright=False):
    button:
        xsize gui.sidebar_content_width
        ysize 50
        background rbox("#00000000", 14)
        hover_background rbox("#ffffff14", 14)
        action act
        tooltip MENU_HELP.get(caption, "")
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

define MENU_TAGLINES = [
    "Ryan is #####",
    "Blackberries are black",
    "AWWWWHHH",
    "Larp music intensifies",
    "Something is lurking",
    "Foreshadowing??",
]

init python:
    def next_tagline(i):
        """A random tagline that isn't the one already showing."""
        return renpy.random.choice([n for n in range(len(MENU_TAGLINES)) if n != i])

transform tagline_swap:
    on appear:
        alpha 1.0
    on show:
        # wait for the old line to fade out first, so they never overlap
        alpha 0.0
        yoffset 6
        pause 0.22
        easein 0.35 alpha 1.0 yoffset 0
    on hide:
        easeout 0.2 alpha 0.0

screen menu_tagline(xa=0.5, size=16):
    default tag_i = renpy.random.randint(0, len(MENU_TAGLINES) - 1)
    # SetLocalVariable: this screen is "use"d, so it has its own scope
    timer 4.0 repeat True action SetLocalVariable("tag_i", next_tagline(tag_i))
    for ti, tline in enumerate(MENU_TAGLINES):
        showif ti == tag_i:
            text tline:
                xalign xa
                size size
                color "#8888a0"
                font GFONT
                at tagline_swap

# ---- main menu: cinematic, with bits of the departure board ----------------------
# The carriage fills the screen, darker on the left where the menu is. The logo
# sits top-left with the tagline centered under it, and the menu is a list
# bottom-left where every option has its own departure time (they flip and
# change, then go back to 4:00).
#
# Everything lines up on CINE_X.

define CINE_X = 110                         # the left edge everything starts on
define CINE_EDGE = 50                       # gap at the top and bottom of the screen
define CINE_COL_W = 600                     # how wide the whole left column is
define CINE_LOGO_W = 420                    # how wide the logo is
define CINE_RAIL_H = 120                    # how tall the train-and-rail strip is
define CINE_TRAIN_W = 220                   # how wide the train is

init python:
    _LEFT_SHADE = []

    def left_shade():
        """Dark on the left of the screen, fading smoothly to nothing."""
        if not _LEFT_SHADE:
            w = int(config.screen_width * 0.62)
            n = 160
            step = w / float(n)
            strips = []
            for k in range(n):
                # strips sit edge to edge (no overlap), so there are no lines
                x0, x1 = int(round(k * step)), int(round((k + 1) * step))
                a = 0.82 * (1.0 - k / float(n)) ** 1.6
                strips.append(At(Solid("#000000"), Transform(xpos=x0, xsize=max(1, x1 - x0),
                                                             ysize=config.screen_height, alpha=a)))
            _LEFT_SHADE.append(Fixed(*strips, xysize=(w, config.screen_height)))
        return _LEFT_SHADE[0]
define CINE_TIME_W = 120                    # width of the time in front of each option

transform passing_light:
    xpos -900
    alpha 0.0
    block:
        pause 4.0
        alpha 0.12
        linear 2.6 xpos (config.screen_width + 200)
        alpha 0.0
        xpos -900
        pause 5.0
        repeat

transform board_flip(key, d=0.0):
    yzoom 0.0
    pause d
    ease 0.14 yzoom 1.0
    ease 0.05 yzoom 0.86
    ease 0.07 yzoom 1.0

transform board_blink:
    alpha 1.0
    block:
        pause 0.7
        alpha 0.3
        pause 0.5
        alpha 1.0
        repeat


# the times in front of the options: one at a time flips to a nearby time,
# and every so often they all go back to 4:00
default board_times = []

init python:
    BOARD_NEAR = ["3:47", "3:52", "3:56", "3:58", "3:59", "4:01", "4:03", "4:07", "4:12", "4:21"]

    class _BOARD(object):
        ticks = 0

    def board_time(i):
        if i < len(store.board_times):
            return store.board_times[i]
        return "4:00"

    def board_tick(n):
        times = (list(store.board_times) + ["4:00"] * n)[:n]
        _BOARD.ticks += 1
        if _BOARD.ticks % 7 == 0:
            times = ["4:00"] * n            # back to 4:00, all at once
        else:
            times[renpy.random.randint(0, n - 1)] = renpy.random.choice(BOARD_NEAR)
        store.board_times = times
        renpy.restart_interaction()

# one option: its time, its name (a line draws under it when you point at it)
screen cine_entry(i, label, act, primary=False):
    $ t = board_time(i)
    button:
        xsize (CINE_COL_W - 52)
        padding (6, 3)
        background None
        hover_background rbox("#ffffff0e", 8)
        # an orange bar down the left of the row you're pointing at
        hover_foreground Transform(Solid("#e0521f"), xsize=4)
        action act
        tooltip MENU_HELP.get(label, "")
        # the row slides in; its contents nudge right on hover (cine_hover).
        # Kept on separate things so the two can't mix and leave a row stuck.
        at fade_slide_in(0.4 + i * 0.06, xoff=-30)
        hbox:
            at cine_hover
            fixed:
                xysize (CINE_TIME_W, (56 if primary else 42))
                text t:
                    yalign 0.5
                    size (30 if primary else 24)
                    color (("#ffd76a" if primary else "#c9a24a") if t == "4:00" else "#e0521f")
                    font CREDIT_FONT
                    at board_flip(("t", i, t), 0.05)
            vbox:
                yalign 0.5
                spacing 3
                hbox:
                    spacing 22
                    text label:
                        size (44 if primary else 30)
                        color ("#e0521f" if primary else "#cfcac0")
                        hover_color ("#ff7a3d" if primary else "#ffffff")
                        font GFONT
                    if primary:
                        text _("BOARDING"):
                            yalign 0.5
                            size 20
                            color "#e0521f"
                            font CREDIT_FONT
                            at board_blink
                add Solid("#e0521f"):
                    xysize (int(len(label) * (26 if primary else 18)), 3)
                    at cine_line

transform cine_hover:
    on idle:
        ease 0.2 xoffset 0
    on hover:
        ease 0.2 xoffset 16

transform cine_line:
    xzoom 0.0
    on idle:
        ease 0.2 xzoom 0.0
    on hover:
        ease 0.3 xzoom 1.0

# ---- the little train on its rail (left column) ---------------------------------
# It rocks gently as if it's moving and puffs smoke. Click it and it fades away
# into the dark, then pulls back in from the left.

define TRAIN_CROP = (0, 230, 2048, 1075)    # just the train, out of Train_BP.webp

transform train_rock:
    yoffset 0
    block:
        ease 0.18 yoffset -2
        ease 0.18 yoffset 0
        repeat

transform train_arrive:
    alpha 0.0
    blur 8
    xoffset -40
    ease 1.4 alpha 1.0 blur 0 xoffset 0

transform smoke_puff(d):
    alpha 0.0
    zoom 0.4
    yoffset 0
    pause d
    block:
        alpha 0.55
        zoom 0.4
        yoffset 0
        xoffset 0
        parallel:
            easeout 1.8 yoffset -60 xoffset -40 zoom 1.4
        parallel:
            linear 1.8 alpha 0.0
        pause 0.3
        repeat

screen menu_train():
    $ th = int(CINE_TRAIN_W * TRAIN_CROP[3] / float(TRAIN_CROP[2]))
    $ tx = (CINE_COL_W - CINE_TRAIN_W) // 2
    # the rail and its sleepers
    for k in range(CINE_COL_W // 26 + 1):
        add Solid("#e6a8172a"):
            pos (k * 26, CINE_RAIL_H - 9)
            xysize (12, 6)
    add Solid("#e6a81766"):
        ypos CINE_RAIL_H - 12
        xysize (CINE_COL_W, 2)
    # the train
    if renpy.loadable("images/Train_BP.webp"):
        button:
            pos (tx, CINE_RAIL_H - 12 - th)
            xysize (CINE_TRAIN_W, th)
            padding (0, 0)
            background None
            action Function(train_poke)
            at (train_leave(train_trips) if train_trips else train_arrive)
            fixed:
                xysize (CINE_TRAIN_W, th)
                at train_rock
                add Transform("images/Train_BP.webp", crop=TRAIN_CROP, xysize=(CINE_TRAIN_W, th), alpha=0.85)
                # smoke from the chimney
                for k in range(3):
                    add rbox("#cfcac0", 9):
                        xysize (18, 18)
                        pos (int(CINE_TRAIN_W * 0.75), int(th * 0.02))
                        at smoke_puff(k * 0.7)

screen main_menu():
    tag menu

    $ fx = persistent.menu_fx and not persistent.reduce_motion
    use secret_listener
    use cheat_hotkey
    on "show" action [Function(check_departure), Function(continue_after_fail)]
    timer 15.0 repeat True action Function(check_departure)
    timer 1.0 action Function(check_halloween)

    # ---- Atmosphere -----------------------------------------------------------
    add "images/1st_carriage_Visualnovel_Background.webp":
        fit "cover"
        xysize (config.screen_width, config.screen_height)
        matrixcolor theme_matrix()
        at ((menu_bg_drift, menu_rumble_at()) if (persistent.screen_shake_enabled and not persistent.reduce_motion)
            else (menu_bg_drift if not persistent.reduce_motion else menu_bg_still))
    add Solid("#08080cb8")

    # a light from outside sweeps through the carriage now and then
    if fx:
        add Transform("gui/glow.png", matrixcolor=TintMatrix("#ffd9a0")):
            xysize (700, int(config.screen_height * 1.6))
            yalign 0.5
            at passing_light

    fixed:
        at menu_rumble_at(), Transform(matrixcolor=theme_matrix())

        # psst: click the big 4:00 four times (empty_train.rpy)
        textbutton "4:00":
            xalign 0.74
            yalign 0.5
            padding (0, 0)
            background None
            text_size 520
            text_color clock_color()
            text_hover_color clock_color()
            text_font GFONT
            action Function(clock_poke)

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

        # a warm light glowing behind the key
        if not menu_hides_key():
            add Transform("gui/glow.png", matrixcolor=TintMatrix("#ffb060")):
                xysize (1100, 1100)
                xcenter 0.76
                ycenter 0.36
                at key_backlight

        # Key swinging from a string - scaled by KEY_SCALE. The string comes
        # down from the hook and is looped round the top bar of the key's ring.
        fixed:
            xpos 0.76
            ypos 0
            xysize (int(340 * KEY_SCALE), int(840 * KEY_SCALE))
            at (key_drop if not persistent.reduce_motion else key_static), Transform(alpha=(0.0 if menu_hides_key() else 1.0))

            add Solid("#7a7a88", xsize=3, ysize=KEY_STRING_H):
                xalign 0.5

            if renpy.loadable("images/Key.webp"):
                add KEY_LOOP_BACK:
                    xalign 0.5
                    ypos KEY_LOOP_Y

                button:
                    background None
                    padding (0, 0)
                    xysize (KEY_W, KEY_H)
                    xpos 0.5
                    xoffset KEY_IMG_X
                    ypos KEY_HANG
                    action Function(key_poke)      # easter egg: poke it
                    add (KEY_IMAGE_GOLD if has_pass("gold_key") else KEY_IMAGE)

                add KEY_LOOP_FRONT:
                    xalign 0.5
                    ypos KEY_LOOP_Y

    # soft dark edges
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)
        alpha 0.8

    # ---- The menu --------------------------------------------------------------
    # CONTINUE comes first; with nothing to continue it starts a new game
    $ rows = [(_("CONTINUE"), Function(continue_game), True), (_("NEW GAME"), Start(), False)]
    $ rows += [(_("LOAD GAME"), ShowMenu("load"), False),
               (_("SETTINGS"), ShowMenu("preferences"), False),
               (_("ACHIEVEMENTS"), ShowMenu("achievements"), False),
               (_("EXTRAS"), ShowMenu("extras_menu"), False),
               (_("CREDITS"), ShowMenu("about"), False)]
    if renpy.variant("pc"):
        $ rows.append((_("QUIT"), Quit(confirm=True), False))
    timer 2.6 repeat True action Function(board_tick, len(rows))

    $ mstyle = menu_style_now()
    if mstyle == "new":
        # ---- Darker on the left, fading out across the screen ----------------------
        add left_shade()

        # something walks through the carriage if you leave the menu alone (secrets.rpy)
        if idle_walk:
            add Transform("images/louis_neutral.png", matrixcolor=flat_color("#050002"), zoom=0.9):
                at idle_walker


    if mstyle == "centered":
        # darker in the middle, behind the menu
        add Solid("#00000070")

    # Settings > Display > MAIN MENU STYLE: the classic sidebar, the new layout,
    # or (THEME PACK) everything centered
    if mstyle == "classic":
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

                        add "game_logo_rumble":
                            xsize gui.sidebar_content_width
                            ysize 240
                            fit "contain"
                            at fade_slide_in(0.1)

                        fixed:
                            xfill True
                            ysize 22
                            at fade_slide_in(0.2)
                            use menu_tagline

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

                                text _("NEW GAME"):
                                    align (0.5, 0.5)
                                    size 32
                                    color "#0a0a0e"
                                    hover_color "#ffffff"
                                    font GFONT

                        vbox:
                            xsize gui.sidebar_content_width
                            spacing 8

                            use menu_entry(_("CONTINUE"), Function(continue_game), 0.34, True)
                            use menu_entry(_("LOAD GAME"), ShowMenu("load"), 0.40)
                            use menu_entry(_("SETTINGS"), ShowMenu("preferences"), 0.48)
                            use menu_entry(_("ACHIEVEMENTS"), ShowMenu("achievements"), 0.56)
                            use menu_entry(_("EXTRAS"), ShowMenu("extras_menu"), 0.60)
                            use menu_entry(_("CREDITS"), ShowMenu("about"), 0.64)
                            if renpy.variant("pc"):
                                use menu_entry(_("QUIT"), Quit(confirm=True), 0.72)

                        # what the option you're pointing at does
                        text (GetTooltip() or ""):
                            xsize gui.sidebar_content_width
                            size 15
                            color "#e6a817"
                            font GFONT

                    text "v[config.version]":
                        xalign 0.95
                        yalign 0.985
                        size 14
                        color "#55556a"
                        font GFONT


    elif mstyle in MENU_EXTRA:
        # minimal, panel, cinema, ticket, terminal, timetable (menu_styles.rpy)
        use expression ("mm_" + mstyle) pass (rows)

    elif mstyle == "centered":
        # ---- THEME PACK: the logo and the menu down the middle --------------------
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 0
            button:
                xalign 0.5
                xysize (560, int(560 * 808 / 1239.0))
                padding (0, 0)
                background None
                action Function(logo_poke)
                at fade_slide_in(0.1)
                add "game_logo_rumble":
                    xysize (560, int(560 * 808 / 1239.0))
                    fit "contain"
            fixed:
                xsize 900
                ysize 34
                at fade_slide_in(0.2)
                use menu_tagline(0.5, 22)
            null height 30
            for i, (lab, act, primary) in enumerate(rows):
                use mm_row(lab, act, (52 if primary else 34), ("#e0521f" if primary else "#cfcac0"), ("#ff7a3d" if primary else "#ffd76a"), 0.35 + i * 0.05, xa=0.5, pad=(30, 6))
            null height 20
            text (GetTooltip() or _("Point at an option to see what it does.")):
                xalign 0.5
                size 17
                color ("#e6a817" if GetTooltip() else "#55556a")
                font GFONT
            null height 10
            textbutton _("DEPARTURES"):
                xalign 0.5
                padding (10, 4)
                background None
                text_size 18
                text_color "#55556a"
                text_hover_color "#e6a817"
                text_font CREDIT_FONT
                action Function(casino_open)

    else:
        # ---- The left column ---------------------------------------------------------
        # Everything is the same width (CINE_COL_W) and centered on the same line:
        # logo, tagline, the train on its rail, then the departure board.
        vbox:
            xpos CINE_X
            yalign 0.5
            spacing 0

            # the logo (psst: click it three times)
            button:
                xalign 0.5
                xysize (CINE_LOGO_W, int(CINE_LOGO_W * 808 / 1239.0))
                padding (0, 0)
                background None
                action Function(logo_poke)
                at fade_slide_in(0.1)
                if logo_glitched:
                    add Transform("images/Game_Logo_Purple.webp", fit="contain", xysize=(CINE_LOGO_W, int(CINE_LOGO_W * 808 / 1239.0))) at logo_glitch
                else:
                    add "game_logo_rumble":
                        xysize (CINE_LOGO_W, int(CINE_LOGO_W * 808 / 1239.0))
                        fit "contain"

            null height 8

            # the tagline, centered under the logo
            fixed:
                xsize CINE_COL_W
                ysize 30
                at fade_slide_in(0.2)
                use menu_tagline(0.5, 20)

            null height 6

            # the train, on its rail (psst: click it)
            fixed:
                xysize (CINE_COL_W, CINE_RAIL_H)
                at fade_slide_in(0.3)
                use menu_train

            null height 22

            # the departure board: the menu, in a thin gold frame
            frame:
                xsize CINE_COL_W
                padding (2, 2)
                background rbox("#e6a81766", 20)
                at fade_slide_in(0.35)
                frame:
                    xfill True
                    padding (22, 14, 22, 12)
                    background rbox("#0a0a0ef2", 18)
                    vbox:
                        spacing 0
                        # header (psst: click it)
                        button:
                            xfill True
                            ysize 42
                            padding (0, 0)
                            background None
                            action Function(casino_open)
                            text _("DEPARTURES"):
                                yalign 0.5
                                size 24
                                color "#e6a817"
                                hover_color "#ffd76a"
                                font CREDIT_FONT
                            hbox:
                                xalign 1.0
                                yalign 0.5
                                spacing 14
                                text _("GREKHOV EXPRESS"):
                                    yalign 0.5
                                    size 18
                                    color "#55556a"
                                    font CREDIT_FONT
                                # the time right now, like a real station clock
                                add BOARD_CLOCK:
                                    yalign 0.5
                        hbox:
                            text _("TIME"):
                                min_width CINE_TIME_W
                                size 13
                                color "#44445a"
                                font GFONT
                            text _("DESTINATION"):
                                size 13
                                color "#44445a"
                                font GFONT
                        null height 6
                        add Solid("#2a2a35"):
                            xysize (CINE_COL_W - 48, 2)
                        null height 8
                        for i, (lab, act, primary) in enumerate(rows):
                            use cine_entry(i, lab, act, primary)
                            if i < len(rows) - 1:
                                add Solid("#ffffff0d"):
                                    xysize (CINE_COL_W - 48, 1)
                        null height 8
                        add Solid("#2a2a35"):
                            xysize (CINE_COL_W - 48, 2)
                        null height 6
                        # what the option you're pointing at does
                        text (GetTooltip() or _("Point at an option to see what it does.")):
                            size 15
                            color ("#e6a817" if GetTooltip() else "#55556a")
                            font GFONT
                        null height 4
                        # psst: click the version number five times
                        textbutton (_("v4:00") if version_pokes >= 5 else "v[config.version]"):
                            xalign 1.0
                            padding (0, 0)
                            background None
                            text_size 14
                            text_color ("#e0521f" if version_pokes >= 5 else "#55556a")
                            text_hover_color "#8888a0"
                            text_font GFONT
                            action Function(version_poke)

    # ---- Tickets (EXTRAS > GAMEPASS) and coins (click: the casino) ---------------
    button:
        xalign 1.0
        xoffset -40
        ypos 34
        padding (20, 10)
        background rbox("#0c0c10d8", 16)
        hover_background rbox("#2a2210e8", 16)
        action Function(casino_open)
        tooltip _("Open the 4:00 Casino: slots, roulette, horse racing and mahjong for coins.")
        at fade_slide_in(1.0, xoff=40)
        hbox:
            spacing 12
            if has_pass("eric"):
                text _("DEV"):
                    yalign 0.5
                    size 18
                    color "#61afef"
                    font CREDIT_FONT
            add rbox("#e6a817", 5):
                yalign 0.5
                xysize (30, 20)
            text (_("TICKETS  %d") % (persistent.tickets or 0)):
                yalign 0.5
                size 20
                color "#e6a817"
                font GFONT
            null width 8
            add circ_coin(20):
                yalign 0.5
            text (_("COINS  %d") % (persistent.coins or 0)):
                yalign 0.5
                size 20
                color "#ffd76a"
                font GFONT

    # the timers for the main-menu secrets (secrets.rpy)
    if logo_glitched:
        timer 2.6 action SetVariable("logo_glitched", False)
    if train_gone:
        timer 3.9 action SetVariable("train_gone", False)
    timer 60.0 action Function(idle_watch)

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

transform plate_pop:
    xoffset hover_lift(-30)
    alpha 0.0
    easein anim_t(0.25) xoffset 0 alpha 1.0

transform plate_still:
    alpha 1.0

# Settings > Display > DIALOGUE BOX STYLE picks one of these looks:
#   classic  the dark rounded box with a coloured name plate
#   minimal  no box - a soft dark fade up from the bottom of the screen
#   paper    old parchment with dark ink, like the maps
#   film     a black subtitle bar along the bottom, everything centred
init python:
    _SAY_FADE = []

    def say_fade():
        """Dark at the bottom of the screen, fading to nothing (minimal style)."""
        if not _SAY_FADE:
            h, n = 360, 72
            strips = []
            for k in range(n):
                y0, y1 = int(k * h / float(n)), int((k + 1) * h / float(n))
                strips.append(At(Solid("#000000"), Transform(ypos=y0, ysize=y1 - y0, xsize=config.screen_width,
                                                             alpha=0.9 * (k / float(n)) ** 1.4)))
            _SAY_FADE.append(Fixed(*strips, xysize=(config.screen_width, h)))
        return _SAY_FADE[0]

screen say(who, what, plate="#8a4a22", creepy=False):
    $ ds = dialogue_style_now()
    $ op = persistent.dialogue_opacity
    # PAPER and TICKET are light boxes with dark ink
    $ inked = ds in ("paper", "ticket")
    $ boxed = ds not in ("film", "minimal")
    $ box_w = config.screen_width - 56

    if ds == "minimal":
        add say_fade():
            yalign 1.0

    window:
        id "window"
        xalign 0.5
        yalign 1.0
        yoffset (-18 if boxed else 0)
        xsize (box_w if boxed else config.screen_width)
        ysize (290 if boxed else 230)
        background say_background(ds, op)
        at say_rise

        if ds == "classic":
            # accent line along the top edge, inset so it clears the rounded corners
            add rbox("#e0521f", 2):
                xalign 0.5
                xsize (box_w - 64)
                ysize 3
                yalign 0.0
        elif ds == "paper":
            add rbox("#7a1f12", 2):
                xalign 0.5
                xsize (box_w - 64)
                ysize 3
                yalign 0.0
                yoffset 10
        elif ds == "terminal":
            # THEME PACK: a plain terminal window - title bar, three buttons, black inside
            add rbox("#2b2b2e", 10):
                xysize (box_w, 42)
            add Solid("#2b2b2e"):
                ypos 30
                xysize (box_w, 12)
            hbox:
                xpos 18
                ypos 14
                spacing 9
                for dot in ("#ff5f57", "#febc2e", "#28c840"):
                    add rbox(dot, 7):
                        xysize (14, 14)
            text "Terminal":
                xalign 0.5
                ypos 11
                size 16
                color "#9a9aa0"
                font "DejaVuSans.ttf"
        elif ds == "ticket":
            # THEME PACK: a train ticket - a stub on the left, torn along the dots
            for k in range(13):
                add Solid("#9a8a66"):
                    xpos 268
                    ypos 22 + k * 20
                    xysize (3, 10)
            fixed:
                xpos 30
                ypos 30
                xysize (220, 230)
                text "4:00":
                    xalign 0.5
                    yalign 0.62
                    size 74
                    color "#b0201a"
                    font CREDIT_FONT
                    at Transform(rotate=-8, alpha=0.85)
                text "GREKHOV EXPRESS":
                    xalign 0.5
                    yalign 0.96
                    size 14
                    color "#7a6a4a"
                    font GFONT

        if who:
            if ds == "classic" or ds == "paper":
                fixed:
                    xpos 40
                    ypos 44
                    xysize (260, 44)
                    at (plate_pop if TALK.changed else plate_still)
                    add rbox((plate if ds == "classic" else "#7a1f12"), 22):
                        xysize (260, 44)
                    text who:
                        id "who"
                        align (0.5, 0.5)
                        size (persistent.dialogue_font_size - 2)
                        bold True
                        color "#f2e6d8"
                        font GFONT
            elif ds == "terminal":
                text (who.lower() + " $"):
                    id "who"
                    xpos 40
                    ypos 58
                    size (persistent.dialogue_font_size - 6)
                    color "#28c840"
                    font "DejaVuSans.ttf"
                    at (plate_pop if TALK.changed else plate_still)
            elif ds == "ticket":
                # the name is stamped on the stub
                text who:
                    id "who"
                    xpos 140
                    xanchor 0.5
                    ypos 52
                    size (persistent.dialogue_font_size - 2)
                    bold True
                    color "#7a1f12"
                    font GFONT
                    at (plate_pop if TALK.changed else plate_still)
            else:
                # minimal / film: just the name, in the speaker's colour
                text who:
                    id "who"
                    xpos (0.5 if ds == "film" else 60)
                    xanchor (0.5 if ds == "film" else 0.0)
                    ypos 26
                    size (persistent.dialogue_font_size - 4)
                    bold True
                    color "#ffd76a"
                    font GFONT
                    at (plate_pop if TALK.changed else plate_still)

        text what:
            id "what"
            xpos (0.5 if ds == "film" else (60 if ds == "minimal" else (310 if ds == "ticket" else 40)))
            xanchor (0.5 if ds == "film" else 0.0)
            xsize (0.8 if ds == "film" else (box_w - 380 if ds == "ticket" else 0.85))
            text_align (0.5 if ds == "film" else 0.0)
            ypos (72 if not boxed else (40 if ds == "ticket" else (100 if ds == "terminal" else 104)))
            size persistent.dialogue_font_size
            color say_ink(ds)
            font ("DejaVuSans.ttf" if ds == "terminal" else say_font())
            line_spacing persistent.line_spacing
            outlines ([(2, "#000000", 0, 0)] if (persistent.text_outline or ds == "minimal") and not inked else [])
            if creepy:
                color ("#8a1f12" if inked else "#e8b4ac")
                textshader (None if persistent.reduce_motion else "jitter:u__jitter=(2.5, 2.5)")

        # little "next" marker bottom-right (a blinking cursor on the terminal)
        if ds == "terminal":
            text "_":
                xalign 0.97
                yalign 0.88
                size 34
                color "#d8d8d8"
                font "DejaVuSans.ttf"
                at soft_pulse
        else:
            add rbox(("#7a1f12" if inked else "#e0521f"), 2):
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
    # REWIND pass: remember where this choice was
    on "show" action Function(rewind_mark)

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

                # CHOICE REVEALER pass: where it leads, and what you picked before
                if has_pass("revealer"):
                    $ hint = choice_hint(i.caption)
                    hbox:
                        xalign 0.97
                        yalign 0.0
                        yoffset -18
                        spacing 8
                        if getattr(i, "chosen", False):
                            frame:
                                padding (12, 3)
                                background rbox("#2a2a35", 12)
                                text _("PICKED BEFORE"):
                                    size 14
                                    color "#a8a4b4"
                                    font GFONT
                        if hint:
                            frame:
                                padding (12, 3)
                                background rbox(hint[1], 12)
                                text hint[0]:
                                    size 14
                                    color "#0a0a0e"
                                    font GFONT


# ==============================================================================
# QUICK MENU
# ==============================================================================

default quick_menu = True

screen quick_menu():
    zorder 100
    if quick_menu and persistent.quick_menu_shown:

        mousearea:
            area (0, config.screen_height - 50, config.screen_width, 50)
            hovered Function(_set_qm_hover, True)
            unhovered Function(_set_qm_hover, False)

        # one dark bar; every button sized to its label, text centred in it
        frame:
            xpos 40
            yalign 1.0
            yoffset -12
            padding (8, 5)
            background rbox("#0a0a0ee0", 20)
            at (qm_shown if quick_menu_hover else qm_hidden)
            hbox:
                spacing 2
                for qm_label, qm_act in ([(_("REWIND"), Function(rewind_go))] if rewind_ready() else []) + [
                    (_("Home"), MainMenu(confirm=True)),
                    (_("Back"), Rollback()),
                    (_("History"), ShowMenu("history")),
                    (_("Skip"), Skip()),
                    (_("Auto"), Preference("auto-forward", "toggle")),
                    (_("Save"), ShowMenu("save")),
                    (_("Q.Save"), QuickSave()),
                    (_("Q.Load"), QuickLoad()),
                    (_("Clues"), ShowMenu("clues")),
                    (_("People"), ShowMenu("manifest")),
                    (_("Prefs"), ShowMenu("preferences")),
                ] + ([(_("Radio"), Function(radio_toggle))] if persistent.radio_bar else []):
                    button:
                        ysize 34
                        xminimum 74
                        padding (16, 0)
                        background None
                        hover_background rbox("#ffffff1c", 15)
                        selected_background rbox("#e0521f33", 15)
                        action qm_act
                        text qm_label:
                            align (0.5, 0.5)
                            layout "nobreak"
                            size 16
                            color "#a8a4b4"
                            hover_color "#ffd700"
                            selected_color "#ffd700"
                            font GFONT
                # auto-forward speed, right there while Auto is on
                if _preferences.afm_enable:
                    frame:
                        ysize 34
                        padding (12, 0)
                        background rbox("#ffffff10", 15)
                        hbox:
                            yalign 0.5
                            spacing 8
                            textbutton "−":
                                yalign 0.5
                                padding (6, 0)
                                text_size 20
                                text_color "#e8e4dc"
                                text_hover_color "#ffd700"
                                text_font "DejaVuSans.ttf"
                                action Function(afm_adjust, -3)
                            text auto_speed_label():
                                yalign 0.5
                                min_width 110
                                text_align 0.5
                                size 15
                                color "#e6a817"
                                font GFONT
                            textbutton "+":
                                yalign 0.5
                                padding (6, 0)
                                text_size 20
                                text_color "#e8e4dc"
                                text_hover_color "#ffd700"
                                text_font "DejaVuSans.ttf"
                                action Function(afm_adjust, 3)


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
                (_("PASSENGERS"), ShowMenu("manifest")),
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
    ("clue_tile_mismatch", "THE WRONG TILE", "\"That's not even from his hand. He had three of the dragon tiles laid out, not that one. Someone put that there after.\""),
    ("clue_body_moved", "A MOVED BODY", "\"He didn't die in this chair. He was moved here after.\""),
    ("clue_drug_wrapper", "THE WRAPPER", "\"...APLE SUGAR… BANNED SUBSTANCE, RESTRICTED USE ONLY.\" Why would Himmel have this?"),
    ("clue_hidden_tile", "THE HIDDEN TILE", "\"This was under Misha's carpet the whole time.\""),
    ("clue_alexander_alibi", "ALEXANDER'S ALIBI", "\"I would've heard the door. It creaks something awful.\""),
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
        key "m" action ShowMenu("manifest")


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
    ("comfort", _("COMFORT"), 0.25),
    ("access", _("ACCESSIBILITY"), 0.30),
]

# DIALOGUE TEXT COLOUR choices (the PAPER box always uses dark ink)
define TEXT_COLORS = {"light": "#e8e4dc", "white": "#ffffff", "yellow": "#ffe39a"}

# SCREEN BRIGHTNESS: -2 .. +2 ; drawn over everything by brightness_fx
init python:
    config.always_shown_screens.append("brightness_fx")

    class FlashTr(object):
        """A colour flash that turns into a gentle fade with FLASHING LIGHTS: SOFTER."""
        def __init__(self, color, out_t, in_t):
            self.color = color
            self.out_t = out_t
            self.in_t = in_t

        def __call__(self, old_widget=None, new_widget=None):
            if persistent.reduce_flashes:
                tr = Dissolve(self.in_t)
            else:
                tr = Fade(self.out_t, 0.0, self.in_t, color=self.color)
            return tr(old_widget=old_widget, new_widget=new_widget)

    def brightness_label():
        return {-2: _("DARKEST"), -1: _("DARKER"), 0: _("NORMAL"), 1: _("BRIGHTER"), 2: _("BRIGHTEST")}.get(persistent.brightness, _("NORMAL"))

screen brightness_fx():
    zorder 2000
    $ b = persistent.brightness or 0
    if b < 0:
        add Solid("#000000", xysize=(config.screen_width, config.screen_height)):
            alpha (-b * 0.16)
    elif b > 0:
        add Transform(Solid("#ffffff", xysize=(config.screen_width, config.screen_height)), alpha=b * 0.07, blend="add")


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

        null height 8

        # wipes every save, unlock and setting, then starts the game over
        button:
            xsize 300
            ysize 50
            padding (0, 0)
            background rbox("#3a0a0a66", 22)
            hover_background rbox("#a8281a66", 22)
            action Confirm(_("Erase EVERYTHING? Every save, achievement, unlock, ticket, coin and setting will be deleted and the game will start fresh."), Function(erase_everything))
            at (fade_slide_in(0.35), button_hover_anim)
            text _("ERASE ALL DATA"):
                align (0.5, 0.5)
                size 15
                color "#a8281a"
                hover_color "#ff6b5a"
                font GFONT

    # ---------------- CONTENT (each tab slides in/out) ----------------
    fixed:
        xpos 420
        ypos 150
        xsize PREF_PANEL_W
        ysize PREF_PANEL_H

        showif pref_tab == "display":
            viewport:
                id "pref_vp_display"
                at tab_page
                xsize PREF_PANEL_W
                ysize PREF_PANEL_H
                mousewheel True
                vbox:
                    spacing 14

                    use pref_row(_("WINDOW MODE"), _("Play in a window or take over the screen."), 0.0):
                        use pref_toggle(_("WINDOW"), Preference("display", "window"))
                        use pref_toggle(_("FULLSCREEN"), Preference("display", "fullscreen"))

                    use pref_row(_("DIALOGUE FONT SIZE"), _("Size of the text in the dialogue box."), 0.12):
                        for dsz, dlabel in DIALOGUE_SIZES:
                            use pref_toggle(dlabel, SetField(persistent, "dialogue_font_size", dsz), selected=(persistent.dialogue_font_size == dsz), w=90)

                    use pref_row(_("DIALOGUE BOX STYLE"), _("How the dialogue box looks."), 0.0):
                        use pref_toggle(_("CLASSIC"), SetField(persistent, "dialogue_style", "classic"), selected=(dialogue_style_now() == "classic"), w=130)
                        use pref_toggle(_("MINIMAL"), SetField(persistent, "dialogue_style", "minimal"), selected=(persistent.dialogue_style == "minimal"), w=130)
                        use pref_toggle(_("PAPER"), SetField(persistent, "dialogue_style", "paper"), selected=(persistent.dialogue_style == "paper"), w=130)
                        use pref_toggle(_("FILM"), SetField(persistent, "dialogue_style", "film"), selected=(persistent.dialogue_style == "film"), w=130)

                    use pref_row(_("THEME PACK DIALOGUE BOXES"), (_("Exclusive: a plain terminal window, or a train ticket.") if has_pass("themes") else _("Unlock TERMINAL and TICKET with the THEME PACK gamepass (EXTRAS > GAMEPASS).")), 0.0):
                        if has_pass("themes"):
                            use pref_toggle(_("TERMINAL"), SetField(persistent, "dialogue_style", "terminal"), selected=(persistent.dialogue_style == "terminal"), w=150)
                            use pref_toggle(_("TICKET"), SetField(persistent, "dialogue_style", "ticket"), selected=(persistent.dialogue_style == "ticket"), w=150)
                        else:
                            text _("LOCKED"):
                                yalign 0.5
                                size 18
                                color "#55556a"
                                font GFONT

                    use pref_row(_("MAIN MENU STYLE"), menu_style_info()[1], 0.0):
                        use rbtn("‹", Function(menu_style_step, -1), w=56, h=44, r=14, size=24)
                        text menu_style_info()[0]:
                            yalign 0.5
                            min_width 220
                            text_align 0.5
                            size 20
                            color "#e6a817"
                            font GFONT
                        use rbtn("›", Function(menu_style_step, 1), w=56, h=44, r=14, size=24)

                    use pref_row(_("CREDITS STYLE"), _("How the credits look: SCROLL, TICKETS, FILM or SPOTLIGHT. You can also switch inside the credits."), 0.0):
                        for cid, cname in CREDIT_STYLES:
                            use pref_toggle(cname, Function(set_credits_style, cid), selected=(credits_style_now() == cid), w=(160 if cid == "departures" else 130))

                    use pref_row(_("COLOUR THEME"), (_("THEME PACK: a soft colour grade on the carriage backgrounds, the maps and the main menu. Characters and text are never tinted.") if has_pass("themes") else _("Unlock 10 colour themes with the THEME PACK gamepass (EXTRAS > GAMEPASS).")), 0.0):
                        if has_pass("themes"):
                            use rbtn("‹", Function(theme_step, -1), w=56, h=44, r=14, size=24)
                            text theme_name():
                                yalign 0.5
                                min_width 220
                                text_align 0.5
                                size 20
                                color "#e6a817"
                                font GFONT
                            use rbtn("›", Function(theme_step, 1), w=56, h=44, r=14, size=24)
                        else:
                            text _("LOCKED"):
                                yalign 0.5
                                size 18
                                color "#55556a"
                                font GFONT

                    use pref_row(_("FILL WIDE SCREENS"), _("Use the whole screen on ultrawide and 16:10 monitors. Restart the game to apply."), 0.0):
                        use pref_toggle(_("ON"), SetField(persistent, "fill_screen", True), selected=(persistent.fill_screen is not False))
                        use pref_toggle(_("OFF"), SetField(persistent, "fill_screen", False), selected=(persistent.fill_screen is False))
                    use pref_onoff(_("MENU EFFECTS"), _("Light streaks and embers on the main menu."), "menu_fx", 0.18)
                    use pref_onoff(_("ACHIEVEMENT POPUPS"), _("Show a banner when you unlock an achievement."), "ach_toasts", 0.24)

        showif pref_tab == "text":
            viewport:
                id "pref_vp_text"
                at tab_page
                xsize PREF_PANEL_W
                ysize PREF_PANEL_H
                mousewheel True
                vbox:
                    spacing 14

                    use pref_row(_("TEXT SPEED"), _("How fast dialogue appears."), 0.0):
                        use pref_slider(Preference("text speed"), text_speed_label())

                    use pref_row(_("AUTO-FORWARD SPEED"), _("How long auto mode waits on each line. Slide left for faster, right for slower. (Also in the quick menu while Auto is on.)"), 0.06):
                        use pref_slider(Preference("auto-forward time"), auto_speed_label())

                    use pref_row(_("DIALOGUE TEXT COLOUR"), _("Colour of the dialogue text. White and yellow stand out more. (The paper box keeps its dark ink.)"), 0.09):
                        use pref_toggle(_("LIGHT"), SetField(persistent, "text_color", "light"), selected=(persistent.text_color == "light"), w=130)
                        use pref_toggle(_("WHITE"), SetField(persistent, "text_color", "white"), selected=(persistent.text_color == "white"), w=130)
                        use pref_toggle(_("YELLOW"), SetField(persistent, "text_color", "yellow"), selected=(persistent.text_color == "yellow"), w=130)

                    use pref_row(_("LINE SPACING"), _("Space between lines of dialogue. Wider can be easier to read."), 0.10):
                        use pref_toggle(_("NORMAL"), SetField(persistent, "line_spacing", 10), selected=(persistent.line_spacing == 10), w=130)
                        use pref_toggle(_("WIDE"), SetField(persistent, "line_spacing", 20), selected=(persistent.line_spacing == 20), w=130)
                        use pref_toggle(_("WIDEST"), SetField(persistent, "line_spacing", 30), selected=(persistent.line_spacing == 30), w=130)

                    use pref_row(_("TEXT EFFECTS"), _("Shaking, waving and screaming words in dialogue. STILL keeps the colours and sizes but nothing moves."), 0.11):
                        use pref_toggle(_("FULL"), SetField(persistent, "text_fx", "full"), selected=(persistent.text_fx == "full"), w=130)
                        use pref_toggle(_("STILL"), SetField(persistent, "text_fx", "still"), selected=(persistent.text_fx == "still"), w=130)
                        use pref_toggle(_("OFF"), SetField(persistent, "text_fx", "off"), selected=(persistent.text_fx == "off"), w=130)

                    use pref_onoff(_("QUICK MENU BAR"), _("The row of buttons under the dialogue box. Esc still opens the menu when it's hidden."), "quick_menu_shown", 0.12)

                    use pref_row(_("DIALOGUE BOX OPACITY"), _("How see-through the dialogue box is."), 0.12):
                        use pref_slider(FieldValue(persistent, "dialogue_opacity", range=0.7, offset=0.3), opacity_label())

                    use pref_row(_("SKIP"), _("Which text the skip button is allowed to fast-forward."), 0.18):
                        use pref_toggle(_("SEEN TEXT"), Preference("skip", "seen"))
                        use pref_toggle(_("ALL TEXT"), Preference("skip", "all"))

                    use pref_row(_("AFTER CHOICES"), _("What skipping does when a choice appears."), 0.24):
                        use pref_toggle(_("STOP SKIPPING"), Preference("after choices", "stop"))
                        use pref_toggle(_("KEEP SKIPPING"), Preference("after choices", "skip"))

        showif pref_tab == "audio":
            viewport:
                id "pref_vp_audio"
                at tab_page
                xsize PREF_PANEL_W
                ysize PREF_PANEL_H
                mousewheel True
                vbox:
                    spacing 14

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

                    use pref_row(_("IN-GAME MUSIC"), _("Songs that fit each carriage, the investigation and the endings. Quiet when it matters."), 0.27):
                        use pref_toggle(_("ON"), Function(set_ingame_music, True), selected=bool(persistent.ingame_music))
                        use pref_toggle(_("OFF"), Function(set_ingame_music, False), selected=(not persistent.ingame_music))

                    use pref_row(_("MAIN MENU MUSIC"), _("The main theme on repeat, or shuffle through a few songs."), 0.30):
                        use pref_toggle(_("THEME"), Function(set_menu_music, "theme"), selected=(persistent.menu_music != "shuffle"))
                        use pref_toggle(_("SHUFFLE"), Function(set_menu_music, "shuffle"), selected=(persistent.menu_music == "shuffle"))

                    use pref_onoff(_("SONG POPUPS"), _("Show the song's name when a new one starts, like a radio."), "song_popups", 0.33)

                    use pref_row(_("NOW PLAYING"), now_playing_title(), 0.36):
                        use pref_toggle(_("NEXT SONG"), Function(music_skip), selected=False, w=200)

                    use pref_row(_("RADIO STATION"), _("GREKHOV FM plays songs that fit where you are. The other stations play their own songs everywhere, without being reset."), 0.39):
                        use rbtn("‹", Function(radio_station_step, -1), w=56, h=44, r=14, size=24)
                        text radio_station_name():
                            yalign 0.5
                            min_width 220
                            text_align 0.5
                            size 20
                            color "#e6a817"
                            font GFONT
                        use rbtn("›", Function(radio_station_step, 1), w=56, h=44, r=14, size=24)

                    use pref_onoff(_("RADIO BAR"), _("The little RADIO tab in the bottom-right corner. Point at it to open the radio, click it to keep it open."), "radio_bar", 0.42)

        showif pref_tab == "gameplay":
            viewport:
                id "pref_vp_gameplay"
                at tab_page
                xsize PREF_PANEL_W
                ysize PREF_PANEL_H
                mousewheel True
                vbox:
                    spacing 14

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

        showif pref_tab == "comfort":
            viewport:
                id "pref_vp_comfort"
                at tab_page
                xsize PREF_PANEL_W
                ysize PREF_PANEL_H
                mousewheel True
                vbox:
                    spacing 14

                    use pref_row(_("FLASHING LIGHTS"), _("SOFTER swaps flashes and flickering lights for slow fades. Recommended if you are sensitive to flashing."), 0.0):
                        use pref_toggle(_("NORMAL"), SetField(persistent, "reduce_flashes", False), selected=(not persistent.reduce_flashes), w=130)
                        use pref_toggle(_("SOFTER"), SetField(persistent, "reduce_flashes", True), selected=bool(persistent.reduce_flashes), w=130)

                    use pref_row(_("SCREEN BRIGHTNESS"), _("Lighten the game if it's too dark to see, or darken it for a dark room."), 0.06):
                        use pref_toggle("-", SetField(persistent, "brightness", max(-2, (persistent.brightness or 0) - 1)), selected=False, w=60)
                        text brightness_label():
                            yalign 0.5
                            xminimum 160
                            text_align 0.5
                            size 18
                            color "#e6a817"
                            font GFONT
                        use pref_toggle("+", SetField(persistent, "brightness", min(2, (persistent.brightness or 0) + 1)), selected=False, w=60)

                    use pref_row(_("HOTSPOT LABELS"), _("The little tags on things you can click. ON HOVER keeps the scene clear until you point at something."), 0.12):
                        use pref_toggle(_("ALWAYS"), SetField(persistent, "hotspot_labels", "always"), selected=(persistent.hotspot_labels != "hover"), w=150)
                        use pref_toggle(_("ON HOVER"), SetField(persistent, "hotspot_labels", "hover"), selected=(persistent.hotspot_labels == "hover"), w=150)

                    use pref_row(_("RUMBLE STRENGTH"), _("How hard the train shakes, on the main menu and in the carriages. EXTREME is violent. Turn it OFF if the movement makes you feel sick."), 0.18):
                        use pref_toggle(_("OFF"), Function(set_rumble, "off"), selected=(not persistent.screen_shake_enabled), w=120)
                        use pref_toggle(_("NORMAL"), Function(set_rumble, "normal"), selected=(persistent.screen_shake_enabled and not persistent.rumble_extreme), w=120)
                        use pref_toggle(_("EXTREME"), Function(set_rumble, "extreme"), selected=(persistent.screen_shake_enabled and persistent.rumble_extreme), w=120)

                    use pref_onoff(_("JUMPSCARES"), _("Jumpscares, the scary sounds and the shadows on the maps."), "jumpscares", 0.24)
                    use pref_onoff(_("REDUCE MOTION"), _("Stops shaking, swaying, embers, zooms and dialogue animations."), "reduce_motion", 0.30)

        showif pref_tab == "access":
            viewport:
                id "pref_vp_access"
                at tab_page
                xsize PREF_PANEL_W
                ysize PREF_PANEL_H
                mousewheel True
                vbox:
                    spacing 14

                    use pref_onoff(_("TEXT OUTLINE"), _("Black outline around dialogue for easier reading."), "text_outline", 0.06)
                    use pref_onoff(_("READABLE FONT"), _("Swap the dialogue font for a plain, clear one."), "readable_font", 0.12)

                    use pref_row(_("SELF-VOICING"), _("Read the screen aloud (text-to-speech)."), 0.18):
                        use pref_toggle(_("ON"), Preference("self voicing", "enable"))
                        use pref_toggle(_("OFF"), Preference("self voicing", "disable"))

                    text _("Flashing lights, brightness, rumble, jumpscares and reduce motion are in COMFORT. Text colour, line spacing and text effects are in TEXT & SKIP."):
                        xsize PREF_PANEL_W
                        size 16
                        color "#666677"
                        font GFONT

    # scrollbar for the open tab (hidden when it all fits)
    vbar:
        style "pref_vbar"
        value YScrollValue("pref_vp_" + pref_tab)
        xpos (420 + PREF_PANEL_W + 14)
        ypos 150
        ysize PREF_PANEL_H

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

init python:
    _FACE_CACHE = {}

    def history_face(who):
        """A small head-and-shoulders picture of whoever said a line."""
        if who in _FACE_CACHE:
            return _FACE_CACHE[who]
        face = None
        tag = (who or "").lower().replace("the ", "").replace(" ", "_")
        for img in (tag + " neutral", tag + "_monster neutral"):
            if renpy.has_image(img):
                face = Transform(img, crop=(0.2, 0.0, 0.6, 0.38), crop_relative=True, fit="contain", xysize=(80, 80))
                break
        _FACE_CACHE[who] = face
        return face

init python:
    import re as _hre

    def history_groups():
        """[(who, [entries])] - one folder per speaker, in the order they first
        spoke; narration gets a folder too (who = "")."""
        order, groups = [], {}
        for e in _history_list:
            k = e.who or ""
            if k not in groups:
                groups[k] = []
                order.append(k)
            groups[k].append(e)
        return [(k, groups[k]) for k in order]

    def history_preview(what, n=70):
        t = _hre.sub(r"\{[^}]*\}", "", what or "")
        return (t[:n] + "…") if len(t) > n else t

screen history():
    tag menu
    default hist_view = "folders"     # "folders" or "timeline"
    default hist_who = None           # an open folder (a speaker), or None

    $ back_action = ShowMenu("main_menu") if main_menu else Return()
    key "game_menu" action back_action

    $ h_w = config.screen_width - 200
    $ groups = history_groups()

    add Solid("#0a0a0e")
    use game_menu_nav

    text _("HISTORY"):
        xpos 80
        ypos 50
        size 40
        color "#ffffff"
        font GFONT
    add rbox("#e0521f", 2):
        xpos 80
        ypos 104
        xysize (120, 4)

    # FOLDERS / TIMELINE
    hbox:
        xpos 80
        ypos 128
        spacing 10
        for hv, hl in [("folders", _("CHARACTERS")), ("timeline", _("TIMELINE"))]:
            button:
                padding (18, 6)
                background rbox(("#e0521f" if hist_view == hv else "#16161e"), 14)
                hover_background rbox(("#f06a35" if hist_view == hv else "#22222e"), 14)
                action [SetScreenVariable("hist_view", hv), SetScreenVariable("hist_who", None)]
                text hl:
                    size 16
                    color ("#0a0a0e" if hist_view == hv else "#a8a4b4")
                    font GFONT

    viewport:
        id "hist_vp"
        xpos 80
        ypos 190
        xsize h_w
        ysize (config.screen_height - 330)
        mousewheel True
        draggable True
        yinitial (1.0 if (hist_view == "timeline" or hist_who is not None) else 0.0)
        vbox:
            xsize (h_w - 40)
            spacing 10
            if not _history_list:
                text _("The backlog is empty."):
                    size 22
                    color "#8888a0"
                    font GFONT

            # ---- every speaker as a folder ----
            elif hist_view == "folders" and hist_who is None:
                hbox:
                    box_wrap True
                    spacing 14
                    xmaximum (h_w - 40)
                    for who, entries in groups:
                        button:
                            xysize (440, 130)
                            padding (16, 14)
                            background rbox("#101014", 18)
                            hover_background rbox("#1a1a22", 18)
                            action SetScreenVariable("hist_who", who)
                            hbox:
                                spacing 16
                                frame:
                                    xysize (96, 96)
                                    padding (0, 0)
                                    background rbox("#1d1d26", 14)
                                    $ face = history_face(who) if who else None
                                    if face:
                                        add Transform(face, xysize=(92, 92)):
                                            align (0.5, 0.5)
                                    else:
                                        text ("…" if not who else "?"):
                                            align (0.5, 0.5)
                                            size 34
                                            color "#55556a"
                                            font GFONT
                                vbox:
                                    spacing 4
                                    text (who or _("Narration")):
                                        size 22
                                        color "#ffd700"
                                        hover_color "#ffffff"
                                        font GFONT
                                    text (_("%d lines") % len(entries)):
                                        size 14
                                        color "#8888a0"
                                        font GFONT
                                    text history_preview(entries[-1].what):
                                        xmaximum 290
                                        size 15
                                        color "#a8a4b4"
                                        italic True
                                        font say_font()

            # ---- one speaker's folder, opened ----
            elif hist_view == "folders":
                $ entries = [e for e in _history_list if (e.who or "") == hist_who]
                button:
                    padding (14, 6)
                    background rbox("#16161e", 12)
                    hover_background rbox("#22222e", 12)
                    action SetScreenVariable("hist_who", None)
                    text _("‹  ALL CHARACTERS"):
                        size 16
                        color "#a8a4b4"
                        hover_color "#ffd700"
                        font GFONT
                hbox:
                    spacing 18
                    $ face = history_face(hist_who) if hist_who else None
                    if face:
                        frame:
                            xysize (110, 110)
                            padding (0, 0)
                            background rbox("#1d1d26", 16)
                            add Transform(face, xysize=(104, 104)):
                                align (0.5, 0.5)
                    vbox:
                        yalign 0.5
                        text (hist_who or _("Narration")):
                            size 34
                            color "#ffd700"
                            font GFONT
                        text (_("%d lines") % len(entries)):
                            size 16
                            color "#8888a0"
                            font GFONT
                for n, e in enumerate(entries):
                    frame:
                        xmaximum 1500
                        padding (22, 12)
                        background rbox("#101014", 16)
                        hbox:
                            spacing 18
                            text ("%d" % (n + 1)):
                                min_width 36
                                size 16
                                color "#55556a"
                                font GFONT
                            text e.what:
                                xmaximum 1300
                                size 22
                                color ("#e8e4dc" if hist_who else "#a8a4b4")
                                italic (not hist_who)
                                font say_font()

            # ---- everything, in order ----
            else:
                for entry in _history_list:
                    frame:
                        xmaximum 1500
                        padding (22, 14)
                        background (rbox("#101014", 18) if entry.who else None)
                        if entry.who:
                            hbox:
                                spacing 22
                                frame:
                                    xysize (84, 84)
                                    padding (0, 0)
                                    background rbox("#1d1d26", 14)
                                    $ face = history_face(entry.who)
                                    if face:
                                        add face:
                                            align (0.5, 0.5)
                                    else:
                                        text "?":
                                            align (0.5, 0.5)
                                            size 34
                                            color "#55556a"
                                            font GFONT
                                vbox:
                                    spacing 6
                                    text entry.who:
                                        size 18
                                        color "#ffd700"
                                        font GFONT
                                    text entry.what:
                                        xmaximum 1200
                                        size 22
                                        color "#e8e4dc"
                                        font say_font()
                        else:
                            text entry.what:
                                xmaximum 1300
                                xoffset 106
                                size 21
                                color "#a8a4b4"
                                italic True
                                font say_font()

    vbar:
        style "pref_vbar"
        value YScrollValue("hist_vp")
        xpos config.screen_width - 96
        ypos 190
        ysize (config.screen_height - 330)

    use game_menu_back(back_action)


# ==============================================================================
# CREDITS  (ticket cards scrolling past a title panel)
# ==============================================================================

# The crew. "key" is what you type on the main menu to find them (secrets.rpy).
# the team: Eric, Hannah, Aydin and Ryan. Roles from the group's role sheet
# first, then the extra ones each person already had in the credits.
define CREW = [
    {"key": "eric", "name": "Eric", "roles": [
        "Story writer", "Generalist", "Game graphic design",
        "Programming/game functionality", "General game design",
        "Head Chief Supreme Programmer", "Game UI manager and supervisor",
        "Commander General Generalist of generalism",
        "Executive director of developing and engineering",
        "Chief Financial Officer", "Head visionist", "R&D department lead"]},
    {"key": "hannah", "name": "Hannah", "roles": [
        "Game graphic design", "General graphic design", "Story writer",
        "Generalist",
        "Lead graphic designer", "Lead designer", "Character designer", "Map designer"]},
    {"key": "aydin", "name": "Aydin", "roles": [
        "Story writer", "General graphic design", "Game graphic design",
        "Google Sites page/presentation", "Generalist",
        "Lead designer", "Lead graphic designer", "Character designer",
        "Lead website developer / manager"]},
    {"key": "ryan", "name": "Ryan", "roles": [
        "Google Sites page/presentation", "Research/resource finder",
        "General game design", "Programming/game functionality",
        "Programmer?", "Senior Junior Developer", "Probationary writer",
        "General Helper", "Probably a researcher"]},
]

init python:
    def credits_step(adj):
        try:
            if adj.value >= adj.range - 2:
                adj.change(0)
            else:
                adj.change(adj.value + 0.9)     # slow, so the credits take their time
        except Exception:
            pass

# SCROLL credits: the game's art drifts slowly behind, one picture fading
# into the next, while the roles and names roll up the middle.

# every role, in the order it first appears in CREW, with everyone who did it.
# Roles next to each other done by the same people share one block, so a name
# isn't repeated: ([role, role, ...], [person, ...])
init python:
    def credit_roles():
        order, who = [], {}
        for c in CREW:
            for r in c["roles"]:
                if r not in who:
                    order.append(r)
                    who[r] = []
                who[r].append(c)
        blocks = []
        for r in order:
            keys = [c["key"] for c in who[r]]
            if blocks and [c["key"] for c in blocks[-1][1]] == keys:
                blocks[-1][0].append(r)
            else:
                blocks.append(([r], who[r]))
        return blocks

# the slow drift across each picture
transform credits_drift(z0, z1, x0, x1):
    xalign x0
    yalign 0.5
    zoom z0
    linear 9.0 zoom z1 xalign x1

# one picture: a carriage, with someone standing in it now and then
init python:
    def _credit_slide(bg, who=None, side=1.0):
        kids = [Transform(bg, fit="cover", xysize=(config.screen_width, config.screen_height))]
        if who:
            kids.append(At(Transform(who, fit="contain", ysize=int(config.screen_height * 0.95)),
                           Transform(xalign=side, yalign=1.0, xoffset=(-160 if side > 0.5 else 160))))
        return Fixed(*kids, xysize=(config.screen_width, config.screen_height))

    CREDIT_SLIDES = [
        _credit_slide("images/1st_carriage_Visualnovel_Background.webp"),
        _credit_slide("images/bg_carriage_1.webp", "images/louis_neutral.png", 1.0),
        _credit_slide("images/Carriage_1_With_CharacterS.webp"),
        _credit_slide("images/bg_carriage_5.webp", "images/fedora.png", 0.0),
        _credit_slide("images/PT2_Carriage_1_With_CharacterS.webp"),
        _credit_slide("images/bg_carriage_1.webp", "images/dorothy_normal.png", 1.0),
        _credit_slide("images/Train_BP.webp"),
        _credit_slide("images/bg_carriage_5.webp", "images/Kimmy_Idle.png", 0.0),
    ]

image credits_art:
    At(CREDIT_SLIDES[0], credits_drift(1.05, 1.15, 0.3, 0.7)) with Dissolve(2.0)
    pause 7.0
    At(CREDIT_SLIDES[1], credits_drift(1.15, 1.05, 0.6, 0.4)) with Dissolve(2.0)
    pause 7.0
    At(CREDIT_SLIDES[2], credits_drift(1.05, 1.15, 0.7, 0.3)) with Dissolve(2.0)
    pause 7.0
    At(CREDIT_SLIDES[3], credits_drift(1.15, 1.05, 0.4, 0.6)) with Dissolve(2.0)
    pause 7.0
    At(CREDIT_SLIDES[4], credits_drift(1.05, 1.15, 0.3, 0.7)) with Dissolve(2.0)
    pause 7.0
    At(CREDIT_SLIDES[5], credits_drift(1.15, 1.05, 0.6, 0.4)) with Dissolve(2.0)
    pause 7.0
    At(CREDIT_SLIDES[6], credits_drift(1.0, 1.1, 0.5, 0.5)) with Dissolve(2.0)
    pause 7.0
    At(CREDIT_SLIDES[7], credits_drift(1.15, 1.05, 0.4, 0.6)) with Dissolve(2.0)
    pause 7.0
    repeat

# with REDUCE MOTION the pictures still change, they just don't move
image credits_art_still:
    CREDIT_SLIDES[0] with Dissolve(2.0)
    pause 7.0
    CREDIT_SLIDES[2] with Dissolve(2.0)
    pause 7.0
    CREDIT_SLIDES[4] with Dissolve(2.0)
    pause 7.0
    CREDIT_SLIDES[6] with Dissolve(2.0)
    pause 7.0
    repeat

transform logo_float:
    yoffset 0
    block:
        ease 2.4 yoffset -10
        ease 2.4 yoffset 0
        repeat

screen about():
    tag menu
    key "game_menu" action (ShowMenu("main_menu") if main_menu else Return())

    # the credits have their own songs (music.rpy)
    on "show" action Function(credits_music_on)
    on "replace" action Function(credits_music_on)
    on "hide" action Function(credits_music_off)
    on "replaced" action Function(credits_music_off)

    # Settings > Display > CREDITS STYLE (credits_styles.rpy)
    use expression ("credits_" + credits_style_now())

    fixed:
        xpos 80
        yalign 0.95
        xsize 160
        ysize 50
        use rbtn(_("BACK"), (ShowMenu("main_menu") if main_menu else Return()), w=160, h=50, r=14, size=24)

    # switch style right here
    hbox:
        xalign 0.97
        ypos 30
        spacing 10
        use rbtn("‹", Function(credits_style_step, -1), w=50, h=44, r=14, size=22)
        frame:
            ysize 44
            padding (16, 0)
            background rbox("#0a0a0ecc", 14)
            text credits_style_name():
                yalign 0.5
                min_width 170
                text_align 0.5
                size 18
                color "#e6a817"
                font GFONT
        use rbtn("›", Function(credits_style_step, 1), w=50, h=44, r=14, size=22)


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

    add Solid("#00000099")

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

define flash = FlashTr("#ffffff", 0.08, 0.35)

# Paper burns away from the middle outwards, ragged edge 120px wide
define burn_reveal = ImageDissolve(Transform("images/burn_mask.png", xysize=(GAME_W, GAME_H)), 2.4, ramplen=120)

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
    "carriage_5_map": ("CARRIAGE 5", "THE MAIL ROOM"),
    "carriage_2_part2_map": ("CARRIAGE 2", "THE CRIME SCENE"),
    "carriage_2_part2_investigation_map": ("CARRIAGE 2", "THE CRIME SCENE"),
    "carriage_2_part2_after_map": ("CARRIAGE 2", "THE CRIME SCENE"),
    "carriage_3_part2_map": ("CARRIAGE 3", "SLEEPER CABINS"),
    "carriage_5_part2_map": ("CARRIAGE 5", "THE MAIL ROOM"),
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
        # a plain warm tint makes the map look old
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
        # the carriage name: a slim plate at the very top
        frame:
            xalign 0.5
            ypos 18
            padding (22, 5)
            background rbox("#e9d9b4d0", 12)
            at map_title_in
            hbox:
                spacing 14
                text mt[0]:
                    yalign 0.5
                    size 22
                    color "#5a2a12"
                    font "gui/Graduate-Regular.ttf"
                text mt[1]:
                    yalign 0.5
                    size 16
                    color "#7a4a28"
                    font "gui/Graduate-Regular.ttf"
        # what to do next, out of the way at the bottom (Settings > Gameplay)
        if persistent.show_objective:
            $ obj_text = current_objective()
            frame:
                xalign 0.5
                yalign 1.0
                yoffset -18
                padding (18, 5)
                background rbox("#0a0806b0", 10)
                at map_title_in
                hbox:
                    spacing 10
                    text _("OBJECTIVE"):
                        yalign 0.5
                        size 13
                        color "#e6a817"
                        font "gui/Graduate-Regular.ttf"
                    text obj_text:
                        yalign 0.5
                        size 16
                        color "#e9d9b4"
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
            want = None
            if persistent.screen_shake_enabled and not persistent.reduce_motion:
                want = "extreme" if persistent.rumble_extreme else "normal"
            if force or store.rumble_on != want:
                t = {"normal": [train_rumble], "extreme": [train_rumble_extreme]}.get(want, [])
                renpy.show_layer_at(t, layer="master", reset=False)
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
        if key not in persistent.mg_won:
            give_tickets(TICKETS_FOR["minigame"])
        persistent.mg_won = set(persistent.mg_won) | set([key])
        try:
            achievement.progress("game_night", len([k for k in persistent.mg_won if k in [g[0] for g in MINIGAME_LIST]]))
        except Exception:
            pass


# ==============================================================================
# 3. MINIGAMES  -  see minigames.rpy
# ==============================================================================


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
        if key not in persistent.endings_seen:
            give_tickets(TICKETS_FOR["ending"])
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
        (None,                 "Dorothy",   "Ticket inspector", "\"Excuse me sir, tickets please.\""),
        ("c1_talked_fedora",   "Fedora",    "Reporter",         "\"I CAN'T WAIT to interview the conductor!\""),
        ("c2_talked_eduard",   "Eduard",    "Bartender",        "\"Good evening lad, I'm Eduard, your bartender.\""),
        ("c2_talked_shunyu",   "Shunyu",    "Gambler",          "\"Yes! I can't stop winning!\""),
        ("c3_talked_kimmy",    "Kimmy",     "Carriage 3",       "\"My family has a clock business, so we're quite well off.\""),
        ("c3_talked_himmel",   "Himmel",    "Carriage 3",       "\"It's to the left! Now leave me alone!\""),
        ("c3_talked_sebastian","Sebastian", "Butler",           "\"My name is Sebastian, the butler for Mr. Popov, the child in this cabin.\""),
        ("c3_talked_misha",    "Misha",     "Carriage 3",       "Misha stares, no response."),
        ("c4_talked_agatha",   "Agatha",    "Staff cart",       "\"Put the bandaid on and stop wasting my time.\""),
        ("c4_talked_ichora",   "Ichora",    "Engineer",         "\"The name's Ichora, I'm the train's engineer.\""),
        ("c5_talked_pattison", "Pattison",  "Mail",             "\"This goes to the clock, while this goes to the end.\""),
        ("c5_talked_alexander","Alexander", "Mail room",        "\"The banned super maple sugar!!!\""),
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
            ("MINIGAMES WON", "%d / %d" % (len([k for k in persistent.mg_won if k in [g[0] for g in MINIGAME_LIST]]), len(MINIGAME_LIST))),
            ("PASSENGERS MET", "%d / %d" % (len([1 for r in cast_rows() if r["met"]]), len(CAST))),
            ("GOLDEN TICKETS", "%d / %d" % (len(persistent.golden_found), len(GOLDEN_IDS))),
            ("SECRETS FOUND", str(len([n for sid, n in SECRET_NOTES if sid and sid in persistent.secrets]))),
            ("TICKETS / COINS", "%d / %d" % (persistent.tickets or 0, persistent.coins or 0)),
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
    KONAMI = ["UP", "UP", "DOWN", "DOWN", "LEFT", "RIGHT", "LEFT", "RIGHT", "b", "a"]
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

    # SECRET_NOTES lives in secrets.rpy

# ---- Konami listener (used by the main menu) ---------------------------------
screen secret_listener():
    key "K_UP" action Function(secret_key, "UP")
    key "K_DOWN" action Function(secret_key, "DOWN")
    key "K_LEFT" action Function(secret_key, "LEFT")
    key "K_RIGHT" action Function(secret_key, "RIGHT")
    for ch in SECRET_LETTERS:
        key ("K_" + ch) action Function(secret_key, ch)

# ---- EXTRAS menu --------------------------------------------------------------
init python:
    def extras_tabs():
        tabs = [("endings", _("ENDINGS")), ("cast", _("CAST")), ("stats", _("STATS")), ("arcade", _("ARCADE")), ("gamepass", _("GAMEPASS"))]
        tabs += dlc_tabs()
        if persistent.secrets:
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

            elif xt == "arcade":
                use arcade_list(ex_w)

            elif xt == "gamepass":
                use gamepass_list(ex_w)

            elif xt == "gallery":
                use gallery_list(ex_w)

            elif xt == "jukebox":
                use jukebox_list(ex_w)

            elif xt == "theatre":
                use theatre_list(ex_w)

            elif xt == "secret":
                text _("TICKET 4:01"):
                    size 40
                    color "#7fcaff"
                    font GFONT
                for idx, note in enumerate(secret_notes()):
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


# ------------------------------------------------------------------------------
# A save that this version of the game can't open (config.load_failed_label):
# back to the main menu with a message. If CONTINUE was opening it, it's marked
# so CONTINUE skips it, and CONTINUE tries the next save or starts a new game.
# ------------------------------------------------------------------------------

label save_too_old:
    python:
        if persistent.cont_trying:
            persistent.broken_saves = set(persistent.broken_saves or ()) | set([tuple(persistent.cont_trying)])
            persistent.cont_retry = True
        persistent.cont_trying = None
        persistent.cont_msg = True
        renpy.save_persistent()
    $ renpy.full_restart()
