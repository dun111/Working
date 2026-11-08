define config.name = _("Departure at 4:00")


define gui.show_name = True


define config.version = "3.5 Beta"


define gui.about = _p("""
""")


define build.name = "DepartureAt4"

define build.executable_name = "Departure at 4.00"

define build.version = "3.5-beta"


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

    # Local release folders never go into a build.
    build.classify('release-*/**', None)

    build.classify('game/cheats.flag', 'cheats')
    build.package("pc-cheats", "zip", "windows linux renpy all cheats", "PC with cheats")
    build.package("mac-cheats", "app-zip", "mac renpy all cheats", "Mac with cheats")


    build.documentation('*.html')
    build.documentation('*.txt')


