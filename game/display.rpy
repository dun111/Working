# ==============================================================================
# DEPARTURE AT 4:00  -  display.rpy
# Fit the game to the player's monitor instead of letterboxing it.
#
# The game is designed at 1920x1080. On a wider monitor (21:9, 32:9) the game
# gets wider instead (1080 tall, extra width); on a taller one (16:10, 4:3) it
# gets taller (1920 wide, extra height). So there are never black bars.
#
#   GAME_W, GAME_H     the real game size, picked once at startup
#   MAP_X0, MAP_Y0     where the 1920x1080 design area sits inside it
#   wide_bg(path)      a 1920x1080 background that fills any screen shape
#
# Settings > Display > FILL WIDE SCREENS turns it off (needs a restart).
# ==============================================================================

init -100 python:
    DESIGN_W, DESIGN_H = 1920, 1080

    def _monitor_aspect():
        try:
            import pygame_sdl2
            if not pygame_sdl2.display.get_init():
                pygame_sdl2.display.init()
            x, y, w, h = pygame_sdl2.display.get_display_bounds(0)
            if w > 0 and h > 0:
                return float(w) / h
        except Exception:
            pass
        return 16.0 / 9.0

    def _game_size():
        if persistent.fill_screen is False or renpy.variant("mobile") or renpy.variant("web"):
            return DESIGN_W, DESIGN_H
        aspect = min(max(_monitor_aspect(), 4.0 / 3.0), 32.0 / 9.0)
        if aspect >= 16.0 / 9.0:
            return int(round(DESIGN_H * aspect)) // 2 * 2, DESIGN_H
        return DESIGN_W, int(round(DESIGN_W / aspect)) // 2 * 2

    GAME_W, GAME_H = _game_size()
    MAP_X0 = (GAME_W - DESIGN_W) // 2
    MAP_Y0 = (GAME_H - DESIGN_H) // 2

default persistent.fill_screen = True

init -2 python:
    def wide_bg(path):
        """
        A 1920x1080 background for any screen shape: the art stays sharp and
        centred, and a blurred, darkened copy fills the space around it.
        """
        if (GAME_W, GAME_H) == (DESIGN_W, DESIGN_H):
            return path
        # render the art tiny, then stretch it back up: a cheap, smooth blur
        tiny = Flatten(Transform(path, xysize=(64, 36)))
        back = Transform(tiny, fit="cover", xysize=(GAME_W, GAME_H),
                         matrixcolor=BrightnessMatrix(-0.22))
        front = Transform(path, xysize=(DESIGN_W, DESIGN_H), xpos=MAP_X0, ypos=MAP_Y0)
        return Fixed(back, front, xysize=(GAME_W, GAME_H))

    def full_cover(path, **kwargs):
        """An image cropped to fill the whole screen whatever its shape."""
        return Transform(path, fit="cover", xysize=(GAME_W, GAME_H), **kwargs)
