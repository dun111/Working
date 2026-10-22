# ==============================================================================
# DEPARTURE AT 4:00  -  empty_train.rpy
# SECRET: the empty train  (spoilers!!)
#
# How to get here: click the big faded "4:00" on the main menu four times.
# (Once you've finished it, the 4:01 gamepass lets you board it from EXTRAS.)
#
# Every carriage is empty, apart from Louis - blacked out, too tall, red eyes.
#   1  it's standing at the end of the carriage. Look at it and it's gone
#   2  it's sitting there, and it talks with his voice
#   3  four cabin doors. Only one goes on. The others aren't empty
#   4  pitch dark. Your light finds the door... and the things standing in the dark
#   5  it only moves when you're not looking at it. The door is stuck
#   6  it's waiting for you
#
# All the lines are from script.rpy.
# ==============================================================================

default persistent.empty_train_done = False

define lv = C("???", plate="#1a0a0a", creepy=True)       # the thing that looks like you

default et_c1_gone = False
default et_room_door = 0
default et_rooms_open = []
default et_wrong = 0
default et_door_xy = (1500, 300)
default et_shades = []
default et_step = 0
default et_watching = False
default et_push = 0

# runs after horror.rpy (it needs _eye from there)
init 1 python:
    # ---------------------------------------------------- the figure
    # Louis, blacked out: pitch-black, stretched a little too tall, with
    # glowing red eyes. Its natural size is 394 x 780.
    ET_SHADE = Fixed(
        Transform("images/louis_neutral.png", matrixcolor=flat_color("#030103"), zoom=0.53, yzoom=1.11),
        At(_eye(188, 137, 22, 8), Transform()),
        At(_eye(244, 137, 22, 8), Transform()),
        xysize=(394, 780))
    # what you keep seeing: the same thing, see-through, eyes still burning
    ET_PALE = ET_SHADE

    def et_vision(h=480, alpha=0.75):
        return Transform(ET_PALE, fit="contain", ysize=h, alpha=min(1.0, alpha + 0.15))

    def et_shade(h=480):
        return Transform(ET_SHADE, fit="contain", ysize=h)

    def et_scare(hold=0.7):
        """The figure rushes at the screen (instead of the usual jumpscare faces)."""
        if persistent.jumpscares:
            sfx("sting")
            renpy.invoke_in_new_context(renpy.call_screen, "et_lunge", hold)

    def et_flash():
        """A figure flickers at the edge of your eye."""
        if persistent.jumpscares:
            renpy.show_screen("et_edge", renpy.random.choice((0.06, 0.12, 0.88, 0.94)))

    # -------------------------------------------------- darkness and a torch
    class ETDark(renpy.Displayable):
        """Black over everything except a soft circle around the mouse."""

        def __init__(self, **kwargs):
            super(ETDark, self).__init__(**kwargs)
            self.hole = Transform("gui/flashlight.png", alpha=1.0)
            self.black = Solid("#000000fa")

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            x, y = ET_LIGHT.pos
            hs = 400
            hx, hy = int(x - hs // 2), int(y - hs // 2)

            # black above, below, left and right of the hole
            for px, py, w, h in [(0, 0, width, hy), (0, hy + hs, width, height - hy - hs),
                                 (0, hy, hx, hs), (hx + hs, hy, width - hx - hs, hs)]:
                if w > 0 and h > 0:
                    rv.blit(renpy.render(self.black, w, h, st, at), (px, py))
            rv.blit(renpy.render(self.hole, hs, hs, st, at), (hx, hy))
            return rv

        def event(self, ev, x, y, st):
            if (x, y) != ET_LIGHT.pos:
                ET_LIGHT.pos = (x, y)
                renpy.redraw(self, 0)
            return None

        # Ren'Py calls this itself, to load the flashlight picture ahead of time
        def visit(self):
            return [self.hole]

    class ET_LIGHT(object):
        pos = (-9999, -9999)

    ET_DARK = ETDark()

    # ------------------------------------------------------ the main menu clock
    class ET_CLOCK(object):
        n = 0

    def clock_poke():
        ET_CLOCK.n += 1
        sfx("lock_click")
        if ET_CLOCK.n >= 4:
            ET_CLOCK.n = 0
            renpy.music.stop(fadeout=1.0)
            Start("empty_train")()
        renpy.restart_interaction()

    def clock_color():
        return "#ffffff%02x" % (8 + ET_CLOCK.n * 12)

    # ---------------------------------------------------------------- carriage 4
    def et_c4_setup():
        store.et_door_xy = (renpy.random.choice([220, 1500]), 280)
        spots = [(renpy.random.randint(200, 1700), renpy.random.randint(260, 640)) for _i in range(7)]
        store.et_shades = [[x, y, 0.0] for x, y in spots if abs(x - store.et_door_xy[0] - 75) > 260]
        ET_LIGHT.pos = (-9999, -9999)

    def et_c4_tick():
        mx, my = ET_LIGHT.pos
        keep = []
        caught = False
        for x, y, t in store.et_shades:
            sx, sy = map_xy(x + 90, y + 120)
            if (mx - sx) ** 2 + (my - sy) ** 2 <= 170 ** 2:
                t += 0.1
            else:
                t = max(0.0, t - 0.05)
            if t >= 0.8 and not caught:
                caught = True          # it saw you looking
            else:
                keep.append([x, y, t])
        store.et_shades = keep
        if caught:
            et_scare(0.6)
        renpy.restart_interaction()

    # ---------------------------------------------------------------- carriage 5
    ET_STEPS = 8

    def et_c5_tick():
        if not store.et_watching:
            store.et_step += 1
            if store.et_step >= ET_STEPS:
                return "caught"
        renpy.restart_interaction()

    def et_c5_push():
        store.et_push += 1
        sfx("thud")
        if store.et_push >= 4:
            return "door"
        renpy.restart_interaction()


# ------------------------------------------------------------------------------
# LOOK AND FEEL
# ------------------------------------------------------------------------------

image et c1 = Transform("bg carriage_1_empty", matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.32) * TintMatrix("#a8b4c4"))
image et c2 = Solid("#0d0b10")
image et c3 = Solid("#0b0d10")
image et c4 = Solid("#0a0b09")
image et c5 = Transform("bg carriage_5", matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.42) * TintMatrix("#a8b4c4"))

# it never stands quite still
transform et_jitter:
    block:
        xoffset 0
        pause 1.1
        linear 0.04 xoffset 4
        linear 0.04 xoffset -3
        linear 0.04 xoffset 0
        pause 0.6
        alpha 0.55
        pause 0.06
        alpha 0.8
        pause 1.7
        repeat

transform et_vanish:
    on show:
        alpha 0.0
        linear 0.6 alpha 1.0
    on hide:
        linear 0.12 alpha 0.0

# FLASHING LIGHTS: SOFTER - the lights just dim and come back, slowly
transform et_lights_soft:
    alpha 0.0
    block:
        pause 4.0
        linear 2.0 alpha 0.4
        linear 2.5 alpha 0.0
        pause 3.0
        repeat

# the lights can't decide whether to stay on
transform et_lights:
    alpha 0.0
    block:
        pause 2.3
        alpha 0.6
        pause 0.05
        alpha 0.0
        pause 0.1
        alpha 0.75
        pause 0.08
        alpha 0.0
        pause 4.1
        linear 1.2 alpha 0.35
        linear 1.6 alpha 0.0
        pause 3.0
        repeat

# dark edges, failing lights, film grain, a red heartbeat at the edges of the
# screen that gets faster carriage by carriage (et_level), and something at
# the edge of your eye
default et_level = 1

transform grain_jitter:
    block:
        choice:
            xoffset -24
            yoffset -12
        choice:
            xoffset 18
            yoffset 14
        choice:
            xoffset -8
            yoffset 20
        choice:
            xoffset 26
            yoffset -16
        pause 0.05
        repeat

transform et_heartbeat(rest):
    alpha 0.0
    block:
        ease 0.09 alpha 0.55
        ease 0.22 alpha 0.12
        ease 0.09 alpha 0.42
        ease 0.45 alpha 0.0
        pause rest
        repeat

# the camera can't keep still either
transform et_breathe:
    xalign 0.5
    yalign 0.5
    zoom 1.0
    block:
        ease 3.2 zoom 1.035 rotate 0.25
        ease 3.2 zoom 1.0 rotate -0.2
        repeat

screen et_atmos():
    zorder 40
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)
    if not persistent.reduce_motion:
        add Transform("gui/vignette.png", matrixcolor=TintMatrix("#ff1a10")):
            xysize (config.screen_width, config.screen_height)
            at et_heartbeat(max(0.15, 1.5 - et_level * 0.24))
        add Transform("gui/grain.png", xysize=(config.screen_width + 60, config.screen_height + 40), alpha=0.11):
            pos (-30, -20)
            at grain_jitter
    add Solid("#000000") at (et_lights_soft if persistent.reduce_flashes else et_lights)
    timer max(2.5, 8.0 - et_level) repeat True action Function(et_flash)

# a hard cut: static, and for a moment it's right in front of you
transform cut_static:
    alpha 0.9
    linear 0.35 alpha 0.0

transform cut_glimpse:
    xalign 0.5
    yalign 1.0
    alpha 0.0
    pause 0.12
    alpha 0.9
    pause 0.07
    alpha 0.0

screen et_cut():
    zorder 280
    add Solid("#000000")
    add Transform("gui/grain.png", xysize=(config.screen_width, config.screen_height)) at cut_static
    if persistent.jumpscares:
        add Transform(ET_SHADE, fit="contain", ysize=int(config.screen_height * 1.1)) at cut_glimpse

label et_hard_cut:
    show screen et_cut
    $ renpy.pause(0.45, hard=True)
    hide screen et_cut
    return

# the last thing you see (the finale): eyes far away in the dark, then it lunges
screen et_finale():
    zorder 300
    add Solid("#000000")
    fixed:
        xysize (1, 1)
        at es_eyes_far
        add _eye(-46, 0, 46, 16)
        add _eye(46, 0, 46, 16)
    add SCARE_FACES["passenger"] at es_lunge
    add Solid("#6a0000") at es_red
    for k, (y, dx) in enumerate([(0.18, 60), (0.41, -90), (0.57, 120), (0.76, -70), (0.9, 40)]):
        add Solid("#000000"):
            xysize (config.screen_width, 40 + k * 9)
            at es_band(y, dx, k * 0.04)

# the crowd steps closer, all at once
transform crowd_step(near):
    xalign 0.5
    yalign 1.0
    ease 0.18 zoom (1.0 + near * 0.28)

# it rushes at you
transform et_rush:
    xanchor 0.5
    yanchor 0.15
    xpos 0.5
    ypos 0.5
    zoom 0.4
    alpha 0.0
    linear 0.06 alpha 1.0
    easein 0.22 zoom 2.6
    block:
        linear 0.03 xoffset 12
        linear 0.03 xoffset -12
        repeat

screen et_lunge(hold=0.7):
    zorder 300
    modal True
    add Solid("#000000")
    add Transform(ET_SHADE, fit="contain", ysize=900) at et_rush
    timer hold action Return()

transform et_edge_blip:
    alpha 0.0
    linear 0.03 alpha 0.8
    pause 0.1
    linear 0.03 alpha 0.0
    pause 0.06
    linear 0.02 alpha 0.5
    linear 0.15 alpha 0.0

screen et_edge(x):
    zorder 46
    add Transform(ET_SHADE, fit="contain", ysize=1000):
        xanchor 0.5
        xpos x
        yanchor 1.0
        ypos 1.05
        at et_edge_blip
    timer 0.5 action Hide("et_edge")


# ------------------------------------------------------------------------------
# THE CARRIAGES
# ------------------------------------------------------------------------------

screen et_c1():
    add "et c1"
    fixed:
        pos map_xy(0, 0)
        xysize (DESIGN_W, DESIGN_H)
        at Transform(zoom=MAP_K)
        showif not et_c1_gone:
            # look straight at it and it isn't there any more
            button:
                pos (1250, 330)
                xysize (200, 420)
                padding (0, 0)
                background None
                action NullAction()
                hovered SetVariable("et_c1_gone", True)
                at et_vanish
                add et_vision(420, 0.7) at et_jitter
    use hs(DOOR_RIGHT, Return("door"), "Carriage 2", "door")

screen et_c2():
    add "et c2"
    use hs(DOOR_RIGHT, Return("door"), "Carriage 3", "door")

screen et_c3():
    add "et c3"
    for i in range(4):
        $ rx = 200 + i * 400
        if i in et_rooms_open:
            # an open room: the dark inside, and whoever's in it
            fixed:
                pos map_xy(rx, 240)
                xysize (300, 560)
                at Transform(zoom=MAP_K)
                add rbox("#020102", 14)
                if i != et_room_door:
                    add et_shade(500):
                        xalign 0.5
                        yalign 1.0
                        at et_jitter
        else:
            # a closed cabin door, slightly ajar
            fixed:
                pos map_xy(rx, 240)
                xysize (300, 560)
                at Transform(zoom=MAP_K)
                add rbox("#1b1920", 14)
                add rbox("#232129", 10):
                    pos (20, 20)
                    xysize (260, 230)
                add rbox("#232129", 10):
                    pos (20, 290)
                    xysize (260, 250)
                add rbox("#5a4a2a", 8):
                    pos (250, 270)
                    xysize (16, 16)
                add Solid("#000000"):
                    xpos 296
                    xysize (4, 560)
            use hs((rx, 240, 300, 560), Return(i), "Room", "look", i * 0.05)

screen et_c4():
    add "et c4"
    timer 0.1 repeat True action Function(et_c4_tick)
    fixed:
        pos map_xy(0, 0)
        xysize (DESIGN_W, DESIGN_H)
        at Transform(zoom=MAP_K)
        for x, y, t in et_shades:
            add et_shade(480):
                pos (x, y)
                at et_jitter
    use hs((et_door_xy[0], et_door_xy[1], 150, 420), Return("door"), "Carriage 5", "door")
    add ET_DARK:
        xysize (config.screen_width, config.screen_height)

transform et_closeness_shake(amount):
    block:
        linear 0.05 xoffset amount
        linear 0.05 xoffset (-amount)
        repeat

screen et_c5():
    add "et c5"
    timer 0.5 repeat True action Function(et_c5_tick)
    # the closer it gets, the redder it goes
    add Solid("#5a0000"):
        xysize (config.screen_width, config.screen_height)
        alpha (et_step / float(ET_STEPS) * 0.45)
    fixed:
        pos map_xy(0, 0)
        xysize (DESIGN_W, DESIGN_H)
        at Transform(zoom=MAP_K)
        # it only moves while you're not looking at it
        $ z = 0.45 + et_step * 0.16
        button:
            xcenter 760
            yanchor 1.0
            ypos 1040
            xysize (int(260 * z), int(560 * z))
            padding (0, 0)
            background None
            action NullAction()
            hovered SetVariable("et_watching", True)
            unhovered SetVariable("et_watching", False)
            add et_vision(int(560 * z), 0.8):
                xalign 0.5
                yalign 1.0
                at et_jitter, et_closeness_shake(et_step * 2)
    # the door won't open first time
    use hs(DOOR_RIGHT, Function(et_c5_push), "Carriage 6", "door")

default et_near = 0

screen et_c6_crowd():
    zorder 5
    # all of them step closer at once whenever et_near goes up
    fixed:
        xysize (config.screen_width, config.screen_height)
        at crowd_step(et_near)
        fixed:
            pos map_xy(0, 0)
            xysize (DESIGN_W, DESIGN_H)
            at Transform(zoom=MAP_K)
            for i, (x, h) in enumerate([(80, 620), (300, 520), (480, 440), (620, 380),
                                        (1180, 380), (1320, 440), (1500, 520), (1720, 620)]):
                add et_shade(h):
                    xcenter x
                    yanchor 1.0
                    ypos 1080
                    at et_jitter


# ------------------------------------------------------------------------------
# THE STORY
# ------------------------------------------------------------------------------

label empty_train:
    $ in_secret_game = True        # saves made in here don't count for CONTINUE
    $ renpy.block_rollback()
    stop music fadeout 2.0
    hide screen loop_overlay
    hide screen dark_eyes
    $ in_loop = False
    $ et_c1_gone = False
    $ et_rooms_open = []
    $ et_wrong = 0
    $ et_step = 0
    $ et_push = 0
    $ et_near = 0
    $ et_level = 1
    scene black
    pause 2.0
    "{i}Louis wakes up violently to the sound of train tracks.{/i}"
    "{i}He opens his eyes.{/i}"
    scene et c1 with Dissolve(2.5)
    if not persistent.reduce_motion:
        show layer master at et_breathe
    show screen et_atmos
    "{whisper}{i}No one is there.{/i}{/whisper}"
    l "{tremble}...It's quiet. Way too quiet.{/tremble}"

    # 1 ------------------------------------------------------------------------
    call screen et_c1
    call et_hard_cut from _call_et_hard_cut

    # 2 ------------------------------------------------------------------------
    $ et_level = 2
    scene et c2
    "{i}Louis enters. The lights feel dimmer, creepier than before.{/i}"
    show expression et_vision(560, 0.8) as vision:
        xalign 0.5
        yalign 1.0
        et_jitter
    with Dissolve(1.5)
    lv "{glitch}...It's quiet. Way too quiet.{/glitch}"
    l "{tremble}H-hello?? Who said that…{/tremble}"
    hide vision
    with Dissolve(0.08)
    "{whisper}{i}No one is there.{/i}{/whisper}"
    call screen et_c2
    call et_hard_cut from _call_et_hard_cut_1

    # 3 ------------------------------------------------------------------------
    $ et_level = 3
    scene et c3
    "{i}The sleeper cabin is colder than before. The four rooms all sit slightly ajar, as if something moved through recently and didn't bother closing doors behind it.{/i}"
    $ et_room_door = renpy.random.randint(0, 3)
label et_c3_loop:
    call screen et_c3
    $ et_rooms_open = et_rooms_open + [_return]
    if _return == et_room_door:
        call et_hard_cut from _call_et_hard_cut_2
        jump et_c4_start
    $ et_wrong += 1
    if et_wrong == 1:
        u "{glitch}Be careful, young one. Do you really wanna do that?{/glitch}"
    elif et_wrong == 2:
        $ et_scare()
    else:
        mi "{wave}He'll come back though. They always come back. Don't they?{/wave}"
    jump et_c3_loop

    # 4 ------------------------------------------------------------------------
label et_c4_start:
    $ et_level = 4
    scene et c4
    "{whisper}Huh… It's dark..{/whisper}"
    $ et_c4_setup()
    call screen et_c4
    call et_hard_cut from _call_et_hard_cut_3

    # 5 ------------------------------------------------------------------------
label et_c5_start:
    $ et_level = 5
    $ et_step = 0
    $ et_push = 0
    $ et_watching = False
    scene et c5
    u "{glitch}Not yet! Try to see the truth before you see the future.{/glitch}"
    call screen et_c5
    if _return == "caught":
        $ et_scare(1.0)
        u "{glitch}You'll see.{/glitch}"
        jump et_c5_start
    call et_hard_cut from _call_et_hard_cut_4

    # 6 ------------------------------------------------------------------------
    $ et_level = 6
    scene carriage_6 with fade
    show carriage_6_fog
    show screen et_c6_crowd
    "{i}You step through. The temperature drops.{/i}"
    show screen dark_eyes(((0.18, 0.22, 0.0), (0.82, 0.26, 0.4), (0.3, 0.55, 0.9), (0.7, 0.6, 1.3), (0.5, 0.15, 1.8)))
    l "{tremble}...It's so quiet. Why is it so quiet.{/tremble}"
    # they all step closer
    $ et_near = 1
    $ renpy.pause(0.6, hard=True)
    "{i}Two pairs of eyes glint in the blackness, watching.{/i}"
    $ et_near = 2
    $ renpy.pause(0.6, hard=True)
    l "{shake}What do you want from me?{/shake}"
    u "{glitch}Not me. Him.{/glitch}"
    hide screen dark_eyes
    # the lights die
    show black as lights_out
    with Dissolve(0.15)
    $ renpy.pause(0.5, hard=True)
    hide lights_out
    show expression et_vision(900, 0.9) as vision:
        xalign 0.5
        yalign 1.0
        yoffset 120
        et_jitter
    with Dissolve(1.2)
    lv "{glitch}Man… This seems familiar…{/glitch}"
    lv "{glitch}“Here again?”{/glitch}"
    # and then it comes for you
    if persistent.jumpscares:
        show screen et_finale
        $ renpy.pause(ES_DARK + ES_HOLD, hard=True)
        hide screen et_finale
    hide screen et_c6_crowd
    hide screen et_atmos
    show layer master
    scene black
    "{i}Louis is hit with the darkness.{/i}"
    pause 2.5
    "{i}Louis wakes up violently to the sound of train tracks.{/i}"
    l "{tremble}I'm… back at the start?{/tremble}"
    # one last look
    call et_hard_cut from _call_et_hard_cut_5

    $ persistent.empty_train_done = True
    $ secret_found("empty_train", "empty_train")
    $ MainMenu(confirm=False)()
    return
