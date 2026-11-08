# Sound effects: button hover and press, the Carriage 3 cabin doors, and the
# mahjong and block minigames. All of them follow the SOUND VOLUME setting.

define SFX_HOVER = "audio/ui_hover.mp3"
define SFX_CLICK = "audio/ui_click.mp3"
# The door clip starts with half a second of silence; skip it so the door sounds on the click.
define SFX_DOOR = "<from 0.45>audio/door.mp3"
define SFX_TILE_CLICK = "audio/mahjong_click.mp3"
define SFX_TILE_MATCH = "audio/mahjong_match.mp3"
define SFX_BLOCK_PRESS = "audio/blocks_press.wav"
define SFX_BLOCK_SHOW = "audio/blocks_show.wav"
define SFX_BERRY = "audio/blackberry_touch.mp3"
# Pick the lock (the Carriage 1 cupboard): a wooden click for each pin, the old lock opening on a win.
define SFX_LOCK_PIN = "audio/lock_pin.mp3"
define SFX_LOCK_OPEN = "audio/lock_open.mp3"

init python:
    # The door and the minigame sounds get their own channels, so a button click
    # on the "sound" channel can't cut them off.
    renpy.music.register_channel("sfx_door", "sfx", loop=False)
    renpy.music.register_channel("sfx_game", "sfx", loop=False)

    def sfx(path, channel="sfx_game", volume=1.0):
        try:
            renpy.music.play(path, channel=channel, loop=False, relative_volume=volume)
        except Exception:
            pass

# Every button gets the hover and press sounds unless it says otherwise.
style button:
    hover_sound SFX_HOVER
    activate_sound SFX_CLICK


# ---------- Carriage 3: doors when going into and out of a cabin ----------

# The cabins are places of their own: the door sounds going in, and again on the
# way back out to the corridor.
define C3_CABINS = {"c3_cabin_kimmy_room", "c3_cabin_misha_room"}
define C3_HUBS = {"carriage_3_hub", "carriage_3_part2_hub"}

default c3_in_cabin = False

init python:
    def _c3_door_cb(name, abnormal):
        # Runs on every label, Ren'Py's own startup labels too (before any save data
        # exists), so it skips those and never assumes c3_in_cabin is set yet.
        if not name or name.startswith("_"):
            return
        if name in C3_CABINS:
            if not getattr(store, "c3_in_cabin", False):
                sfx(SFX_DOOR, "sfx_door")
            store.c3_in_cabin = True
        elif name.endswith("_hub") or name.endswith("_start"):
            # Back out in the corridor: the door closes behind you.
            if getattr(store, "c3_in_cabin", False) and name in C3_HUBS:
                sfx(SFX_DOOR, "sfx_door")
            store.c3_in_cabin = False

    config.label_callbacks.append(_c3_door_cb)
