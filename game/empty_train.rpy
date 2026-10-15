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

            def blk(px, py, w, h):
                if w > 0 and h > 0:
                    rv.blit(renpy.render(self.black, w, h, st, at), (px, py))

            blk(0, 0, width, max(0, hy))
            blk(0, hy + hs, width, height - hy - hs)
            blk(0, hy, max(0, hx), hs)
            blk(hx + hs, hy, width - hx - hs, hs)
            rv.blit(renpy.render(self.hole, hs, hs, st, at), (hx, hy))
            return rv

        def event(self, ev, x, y, st):
            if (x, y) != ET_LIGHT.pos:
                ET_LIGHT.pos = (x, y)
                renpy.redraw(self, 0)
            return None

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
            sx, sy = x + MAP_X0 + 90, y + MAP_Y0 + 120
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

# dark edges, failing lights, and something at the edge of your eye
screen et_atmos():
    zorder 40
    add "gui/vignette.png":
        xysize (config.screen_width, config.screen_height)
    add Solid("#000000") at et_lights
    timer 7.0 repeat True action Function(et_flash)

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

# the vision stepping closer (carriage 5)
transform et_step_to(z):
    ease 0.12 zoom z


# ------------------------------------------------------------------------------
# THE CARRIAGES
# ------------------------------------------------------------------------------

screen et_c1():
    add "et c1"
    fixed:
        pos (MAP_X0, MAP_Y0)
        xysize (DESIGN_W, DESIGN_H)
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
                pos (rx + MAP_X0, 240 + MAP_Y0)
                xysize (300, 560)
                add rbox("#020102", 14)
                if i != et_room_door:
                    add et_shade(500):
                        xalign 0.5
                        yalign 1.0
                        at et_jitter
        else:
            # a closed cabin door, slightly ajar
            fixed:
                pos (rx + MAP_X0, 240 + MAP_Y0)
                xysize (300, 560)
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
        pos (MAP_X0, MAP_Y0)
        xysize (DESIGN_W, DESIGN_H)
        for x, y, t in et_shades:
            add et_shade(480):
                pos (x, y)
                at et_jitter
    use hs((et_door_xy[0], et_door_xy[1], 150, 420), Return("door"), "Carriage 5", "door")
    add ET_DARK:
        xysize (config.screen_width, config.screen_height)

screen et_c5():
    add "et c5"
    timer 0.5 repeat True action Function(et_c5_tick)
    fixed:
        pos (MAP_X0, MAP_Y0)
        xysize (DESIGN_W, DESIGN_H)
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
                at et_jitter
    # the door won't open first time
    use hs(DOOR_RIGHT, Function(et_c5_push), "Carriage 6", "door")

screen et_c6_crowd():
    zorder 5
    fixed:
        pos (MAP_X0, MAP_Y0)
        xysize (DESIGN_W, DESIGN_H)
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
    scene black
    pause 2.0
    "{i}Louis wakes up violently to the sound of train tracks.{/i}"
    "{i}He opens his eyes.{/i}"
    scene et c1 with Dissolve(2.5)
    show screen et_atmos
    "{i}No one is there.{/i}"
    l "...It's quiet. Way too quiet."

    # 1 ------------------------------------------------------------------------
    call screen et_c1
    $ et_flash()

    # 2 ------------------------------------------------------------------------
    scene et c2 with Dissolve(1.0)
    "{i}Louis enters. The lights feel dimmer, creepier than before.{/i}"
    show expression et_vision(560, 0.8) as vision:
        xalign 0.5
        yalign 1.0
        et_jitter
    with Dissolve(1.5)
    lv "...It's quiet. Way too quiet."
    l "H-hello?? Who said that…"
    hide vision
    with Dissolve(0.08)
    "{i}No one is there.{/i}"
    call screen et_c2

    # 3 ------------------------------------------------------------------------
    scene et c3 with Dissolve(1.0)
    "{i}The sleeper cabin is colder than before. The four rooms all sit slightly ajar, as if something moved through recently and didn't bother closing doors behind it.{/i}"
    $ et_room_door = renpy.random.randint(0, 3)
label et_c3_loop:
    call screen et_c3
    $ et_rooms_open = et_rooms_open + [_return]
    if _return == et_room_door:
        jump et_c4_start
    $ et_wrong += 1
    if et_wrong == 1:
        u "Be careful, young one. Do you really wanna do that?"
    elif et_wrong == 2:
        $ et_scare()
    else:
        mi "He'll come back though. They always come back. Don't they?"
    jump et_c3_loop

    # 4 ------------------------------------------------------------------------
label et_c4_start:
    scene et c4 with Dissolve(0.3)
    "Huh… It's dark.."
    $ et_c4_setup()
    call screen et_c4
    $ et_flash()

    # 5 ------------------------------------------------------------------------
label et_c5_start:
    $ et_step = 0
    $ et_push = 0
    $ et_watching = False
    scene et c5 with Dissolve(1.0)
    u "Not yet! Try to see the truth before you see the future."
    call screen et_c5
    if _return == "caught":
        $ et_scare(1.0)
        u "You'll see."
        jump et_c5_start

    # 6 ------------------------------------------------------------------------
    scene carriage_6 with fade
    show carriage_6_fog
    show screen et_c6_crowd
    "{i}You step through. The temperature drops.{/i}"
    show screen dark_eyes(((0.18, 0.22, 0.0), (0.82, 0.26, 0.4), (0.3, 0.55, 0.9), (0.7, 0.6, 1.3), (0.5, 0.15, 1.8)))
    l "...It's so quiet. Why is it so quiet."
    "{i}Two pairs of eyes glint in the blackness, watching.{/i}"
    l "What do you want from me?"
    u "Not me. Him."
    hide screen dark_eyes
    show expression et_vision(900, 0.9) as vision:
        xalign 0.5
        yalign 1.0
        yoffset 120
        et_jitter
    with Dissolve(2.0)
    lv "Man… This seems familiar…"
    lv "“Here again?”"
    $ et_scare(1.4)
    hide screen et_c6_crowd
    hide screen et_atmos
    scene black
    "{i}Louis is hit with the darkness.{/i}"
    pause 2.5
    "{i}Louis wakes up violently to the sound of train tracks.{/i}"
    l "I'm… back at the start?"

    $ persistent.empty_train_done = True
    $ secret_found("empty_train", "empty_train")
    $ MainMenu(confirm=False)()
    return
