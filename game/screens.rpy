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

# Key on the main menu.  KEY_SCALE 1.0 = the original size; everything about
# the key (string, loop, swing) scales with it.
define KEY_SCALE = 2.35


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

# the main menu: the carriage never stops rumbling, and every couple of
# seconds the wheels go over a joint in the track
transform menu_rumble:
    xoffset 0
    yoffset 0
    block:
        linear 0.05 xoffset -3 yoffset 2
        linear 0.05 xoffset 3 yoffset -2
        linear 0.05 xoffset -2 yoffset 3
        linear 0.05 xoffset 3 yoffset -1
        linear 0.05 xoffset -3 yoffset -2
        linear 0.05 xoffset 2 yoffset 2
        linear 0.05 xoffset -2 yoffset -3
        linear 0.05 xoffset 3 yoffset 1
        repeat 5
        # clack-clack
        easeout 0.06 yoffset 9 xoffset -4
        easein 0.12 yoffset -2 xoffset 2
        easeout 0.06 yoffset 7 xoffset 3
        easein 0.16 yoffset 0 xoffset 0
        repeat

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
# sprite shrinks and dims. Positions are remembered from your show statements.

# First appearance slides in from the sprite's own side of the screen; after
# that the speaker hops on every new line and everyone else eases back;
# "hide" fades the sprite out.
transform _sp_focus(xalign=0.7):
    xanchor 0.5
    xalign xalign
    yalign 1.0
    yoffset 40
    on show:
        alpha 0.0
        zoom 1.04
        xoffset (hover_lift(-80) if xalign < 0.5 else hover_lift(80))
        easein anim_t(0.4) alpha 1.0 zoom 1.08 xoffset 0
    on replace:
        parallel:
            linear anim_t(0.3) zoom 1.08 alpha 1.0 xoffset 0
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
        xoffset (hover_lift(-80) if xalign < 0.5 else hover_lift(80))
        easein anim_t(0.4) alpha 0.55 zoom 0.94 xoffset 0
    on replace:
        linear anim_t(0.3) zoom 0.94 alpha 0.55 xoffset 0
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

image bg carriage_1 = ConditionSwitch(
    "in_loop", wide_bg(carriage_art("images/PT2_Carriage_1_With_CharacterS.webp")),
    "True", wide_bg(carriage_art("images/Carriage_1_With_CharacterS.webp")))

# the empty carriage (no one in it) - used by the empty train
image bg carriage_1_empty = wide_bg("images/bg_carriage_1.webp")
image bg carriage_5 = wide_bg("images/bg_carriage_5.webp")

# Placeholder backgrounds: the real bg carriage 2/3/4 .webp files are not in
# the project yet. Replace each Solid with "images/bg_carriage_N.webp" once the
# art is added.
image bg carriage_2 = Solid("#2a2430")
image bg carriage_3 = Solid("#242a30")
image bg carriage_4 = Solid("#2a3024")

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
        padding (0, 3)
        background None
        action act
        at fade_slide_in(0.4 + i * 0.06, xoff=-30), cine_hover
        hbox:
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

# ---- the little train on its rail (left column) ---------------------------------
# It rocks gently as if it's moving and puffs smoke. Click it and it fades away
# into the dark; a few seconds later it fades back in.

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
            at (train_leave if train_gone else train_arrive)
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

    $ newest_save = latest_save()
    $ fx = persistent.menu_fx and not persistent.reduce_motion
    use secret_listener
    use cheat_hotkey
    on "show" action Function(check_departure)
    timer 15.0 repeat True action Function(check_departure)
    timer 1.0 action Function(check_halloween)

    # ---- Atmosphere -----------------------------------------------------------
    add "images/1st_carriage_Visualnovel_Background.webp":
        fit "cover"
        xysize (config.screen_width, config.screen_height)
        at ((menu_bg_drift, menu_rumble) if (persistent.screen_shake_enabled and not persistent.reduce_motion)
            else (menu_bg_drift if not persistent.reduce_motion else menu_bg_still))
    add Solid("#08080cb8")

    # a light from outside sweeps through the carriage now and then
    if fx:
        add Transform("gui/glow.png", matrixcolor=TintMatrix("#ffd9a0")):
            xysize (700, int(config.screen_height * 1.6))
            yalign 0.5
            at passing_light

    fixed:
        at (menu_rumble if (persistent.screen_shake_enabled and not persistent.reduce_motion) else no_shake)

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

        # Key swinging from a string - scaled by KEY_SCALE. The string comes
        # down from the hook and is looped round the top bar of the key's ring.
        fixed:
            xpos 0.76
            ypos 0
            xysize (int(340 * KEY_SCALE), int(840 * KEY_SCALE))
            at (key_drop if not persistent.reduce_motion else key_static)

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
    $ rows = [((_("NEW GAME") if newest_save else _("PLAY")), Start(), True)]
    if newest_save:
        $ rows.append((_("CONTINUE"), Function(renpy.load, newest_save), False))
    $ rows += [(_("LOAD GAME"), ShowMenu("load"), False),
               (_("SETTINGS"), ShowMenu("preferences"), False),
               (_("ACHIEVEMENTS"), ShowMenu("achievements"), False),
               (_("EXTRAS"), ShowMenu("extras_menu"), False),
               (_("CREDITS"), ShowMenu("about"), False)]
    if renpy.variant("pc"):
        $ rows.append((_("QUIT"), Quit(confirm=True), False))
    timer 2.6 repeat True action Function(board_tick, len(rows))

    # ---- Darker on the left, fading out across the screen ----------------------
    add left_shade()

    # something walks through the carriage if you leave the menu alone (secrets.rpy)
    if idle_walk:
        add Transform("images/louis_neutral.png", matrixcolor=flat_color("#050002"), zoom=0.9):
            at idle_walker

    # ---- Tickets (EXTRAS > GAMEPASS) ---------------------------------------------
    frame:
        xalign 1.0
        xoffset -40
        ypos 34
        padding (20, 10)
        background rbox("#0c0c10d8", 16)
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
                add "game_logo_cycle":
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

        # the departure board: the menu
        frame:
            xsize CINE_COL_W
            padding (24, 16, 24, 14)
            background rbox("#0a0a0ecc", 18)
            at fade_slide_in(0.35)
            vbox:
                spacing 0
                # header (psst: click it)
                button:
                    xfill True
                    ysize 42
                    padding (0, 0)
                    background None
                    action Show("slot_machine")
                    text _("DEPARTURES"):
                        yalign 0.5
                        size 24
                        color "#e6a817"
                        hover_color "#ffd76a"
                        font CREDIT_FONT
                    text _("GREKHOV EXPRESS"):
                        xalign 1.0
                        yalign 0.5
                        size 18
                        color "#55556a"
                        hover_color "#8888a0"
                        font CREDIT_FONT
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

    # the timers for the main-menu secrets (secrets.rpy)
    if logo_glitched:
        timer 2.6 action SetVariable("logo_glitched", False)
    if train_gone:
        timer 9.0 action SetVariable("train_gone", False)
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

screen say(who, what, plate="#8a4a22", creepy=False):
    window:
        id "window"
        xalign 0.5
        yalign 1.0
        yoffset -18
        xsize (config.screen_width - 56)
        ysize 290
        background rbox(Color("#0a0a0e").replace_opacity(persistent.dialogue_opacity), 26)
        at say_rise

        # accent line along the top edge, inset so it clears the rounded corners
        add rbox("#e0521f", 2):
            xalign 0.5
            xsize (config.screen_width - 56 - 64)
            ysize 3
            yalign 0.0

        if who:
            fixed:
                xpos 40
                ypos 44
                xysize (260, 44)
                at (plate_pop if TALK.changed else plate_still)

                add rbox(plate, 22):
                    xysize (260, 44)

                text who:
                    id "who"
                    align (0.5, 0.5)
                    size (persistent.dialogue_font_size - 2)
                    bold True
                    color "#f2e6d8"
                    font GFONT

        text what:
            id "what"
            xpos 40
            xsize 0.85
            ypos 104
            size persistent.dialogue_font_size
            color "#e8e4dc"
            font say_font()
            line_spacing 10
            outlines ([(2, "#000000", 0, 0)] if persistent.text_outline else [])
            if creepy:
                color "#e8b4ac"
                textshader (None if persistent.reduce_motion else "jitter:u__jitter=(2.5, 2.5)")

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
                (_("People"), ShowMenu("manifest")),
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

                use pref_row(_("FILL WIDE SCREENS"), _("Use the whole screen on ultrawide and 16:10 monitors. Restart the game to apply."), 0.0):
                    use pref_toggle(_("ON"), SetField(persistent, "fill_screen", True), selected=(persistent.fill_screen is not False))
                    use pref_toggle(_("OFF"), SetField(persistent, "fill_screen", False), selected=(persistent.fill_screen is False))
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

                use pref_onoff(_("JUMPSCARES"), _("Jumpscares, the scary sounds and the shadows on the maps."), "jumpscares", 0.0)
                use pref_onoff(_("REDUCE MOTION"), _("Stops shaking, swaying, embers, zooms and dialogue animations."), "reduce_motion", 0.03)
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

# The crew. "key" is what you type on the main menu to find them (secrets.rpy).
define CREW = [
    {"key": "hannah", "name": "Hannah", "roles": [
        "Lead graphic designer", "Lead designer", "Story writer",
        "Character designer", "Map designer"]},
    {"key": "aydin", "name": "Aydin", "roles": [
        "Lead designer", "Lead graphic designer", "Character designer",
        "Lead website developer / manager"]},
    {"key": "hanyu", "name": "Hanyu", "roles": [
        "Emotional support animal"]},
    {"key": "eric", "name": "Eric", "roles": [
        "Head Chief Supreme Programmer", "Game UI manager and supervisor",
        "Commander General Generalist of generalism",
        "Executive director of developing and engineering",
        "Chief Financial Officer", "Head visionist", "R&D department lead"]},
    {"key": "ryan", "name": "Ryan", "roles": [
        "Programmer?", "Senior Junior Developer", "Probationary writer",
        "General Helper", "Probably a researcher"]},
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

# the little badge next to each name (what they did)
define CREW_BADGES = {"eric": "</>", "hannah": "✎", "aydin": "www", "ryan": "☕", "hanyu": "♥"}

# one ticket card in the credits: number stub, name, every role they took on
screen crew_card(ci, c):
    $ card_h = max(150, 96 + 34 * len(c["roles"]))
    hbox:
        frame:
            xsize 150
            ysize card_h
            background rbox(credit_accent(), 26)
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
            for _d in range(max(6, len(c["roles"]) + 3)):
                add rbox("#33334a", 4):
                    xalign 0.5
                    xsize 8
                    ysize 8

        vbox:
            yalign 0.5
            spacing 4
            xoffset 14
            hbox:
                spacing 18
                text c["name"]:
                    size 60
                    color "#f2ead8"
                    hover_color credit_accent()
                    font CREDIT_FONT
                    outlines [(0, "#00000080", 2, 3)]
                if c["key"] in CREW_BADGES:
                    frame:
                        yalign 0.6
                        padding (12, 4)
                        background rbox("#22222c", 10)
                        text CREW_BADGES[c["key"]]:
                            size 22
                            color "#8888a0"
                            hover_color "#e8e4dc"
                            font "DejaVuSans.ttf"
            null height 4
            for role in c["roles"]:
                hbox:
                    spacing 12
                    add rbox(credit_accent(), 2):
                        xysize (8, 8)
                        yalign 0.5
                    text role:
                        size 22
                        color "#e6a817"
                        font GFONT

# credits: cards slide in one after another, lean out when you point at them,
# and the logo floats
transform card_in(d):
    alpha 0.0
    xoffset 260
    pause d
    easein 0.6 alpha 1.0 xoffset 0

transform card_hover:
    on idle:
        ease 0.25 xoffset 0 zoom 1.0
    on hover:
        ease 0.25 xoffset -18 zoom 1.01

transform logo_float:
    yoffset 0
    block:
        ease 2.4 yoffset -10
        ease 2.4 yoffset 0
        repeat

screen about():
    tag menu
    key "game_menu" action (ShowMenu("main_menu") if main_menu else Return())

    # larp music plays while the credits are open
    on "show" action Function(credits_music_on)
    on "replace" action Function(credits_music_on)
    on "hide" action Function(credits_music_off)
    on "replaced" action Function(credits_music_off)
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
                    at logo_float

                fixed:
                    xfill True
                    ysize 22
                    use menu_tagline

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
        xsize (config.screen_width - 800)
        ysize 830
        yadjustment cred_adj
        mousewheel True
        draggable True

        vbox:
            xsize (config.screen_width - 820)
            spacing 22

            null height 760

            for ci, c in enumerate(CREW):
                # psst: everyone's card does something when you click it (credits_fx.rpy)
                frame:
                    xfill True
                    padding (0, 0)
                    background None
                    at card_in(0.3 + ci * 0.15)
                    button:
                        xfill True
                        padding (0, 0)
                        background rbox("#14141a", 26)
                        hover_background rbox("#1d1820", 26)
                        action Function(credits_click, c["key"])
                        at card_hover
                        use crew_card(ci, c)

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

define flash = Fade(0.08, 0.0, 0.35, color="#ffffff")

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