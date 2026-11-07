define config.name = _("Departure at 4:00")


define gui.show_name = True


define config.version = "3.4 Beta"


define gui.about = _p("""
""")


define build.name = "DepartureAt4"

define build.executable_name = "Departure at 4.00"

define build.version = "3.4-beta"


define config.has_sound = True
define config.has_music = True
define config.has_voice = False


define config.window = "auto"


default preferences.text_cps = 0


default preferences.afm_time = 15


define config.save_directory = "Working-1779927219"


define config.window_icon = "gui/window_icon_mac.png" if renpy.macintosh else "gui/window_icon.png"


init python:


    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    build.classify('music_source/**', None)
    build.classify('video_source/**', None)
    build.classify('tools/**', None)
    build.classify('*.png', None)

    # Files kept in the folder but not used by the game: left out of every build.
    build.classify('game/movies/studio_intro_old.webm', None)
    build.classify('game/music/studio_jingle.mp3', None)
    build.classify('game/music/Carriage 5.mp3', None)
    build.classify('game/music/Part_2_Carriage_3.mp3', None)
    build.classify('game/music/audiomass-output.mp3', None)
    build.classify('game/images/bg_carriage_5.webp', None)
    build.classify('game/gui/TaskBar_icon_Departureat4.webp', None)

    build.classify('game/cheats.flag', 'cheats')
    build.package("pc-cheats", "zip", "windows linux renpy all cheats", "PC with cheats")
    build.package("mac-cheats", "app-zip", "mac renpy all cheats", "Mac with cheats")


    build.documentation('*.html')
    build.documentation('*.txt')


