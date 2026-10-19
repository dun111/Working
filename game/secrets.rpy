# ==============================================================================
# DEPARTURE AT 4:00  -  secrets.rpy
# Secret stuff (spoilers!!)
#
#   type a crew member's name on the main menu
#   keep clicking the Blackberry logo after it tells you to stop
#   be on the main menu at 4:00 (am or pm)
#   + the MORE SECRETS section at the bottom of this file
#   + konami code and poking the key (in screens.rpy)
#
# Finding one unlocks a note in EXTRAS > 4:01
# ==============================================================================

default persistent.crew_found = set()

define SECRET_ACHIEVEMENTS = [
    {"id": "whole_crew", "title": _("You Will Before the End"), "description": _("Type all four crew names on the main menu."), "hidden": True},
    {"id": "pixel_parade", "title": _("They Always Come Back"), "description": _("Keep clicking the Blackberry logo after it tells you to stop."), "hidden": True},
    {"id": "right_on_time", "title": _("Departure at 4:00"), "description": _("Open the main menu at exactly 4:00."), "hidden": True},
]

# (secret id, note) - shows up in EXTRAS > 4:01 once you find that secret
define SECRET_NOTES = [
    ("konami", _("\"Every departure on it is printed the same way: 4:00.\"")),
    ("konami", _("\"This goes to the clock, while this goes to the end. This goes to the fake ones and this goes to the friend.\"")),
    ("key_cut", _("\"Sometimes, life gets hard, and a door is presented to escape. But we're too scared to use the key. Don't hesitate.\"")),
    ("crew", _("\"It's okay, you will before the end.\"")),
    ("parade", _("\"He'll come back though. They always come back. Don't they?\"")),
    ("on_time", _("\"Thank you for boarding the Grekhov Express.\"")),
    (None, _("THANKS FOR PLAYING!")),
]

init python:
    import time as _time
    import datetime as _datetime
    import random as _random

    for _sa in SECRET_ACHIEVEMENTS:
        if _sa["id"] not in [x["id"] for x in ACHIEVEMENTS]:
            ACHIEVEMENTS.append(_sa)
            achievement.register(_sa["id"])

    def secret_found(sid, ach=None):
        """Remember a secret (unlocks its EXTRAS note) and grant its achievement."""
        if sid not in persistent.secrets:
            give_tickets(TICKETS_FOR["secret"])
        persistent.secrets = set(persistent.secrets) | set([sid])
        if ach:
            try:
                achievement.grant(ach)
            except Exception:
                pass

    def secret_notes():
        found = set(persistent.secrets)
        return [note for sid, note in SECRET_NOTES if sid is None or sid in found]

    class _SECRET(object):
        """Per-session state (never saved)."""
        typed = ""
        berry_clicks = 0
        departed = False

    # ---------------------------------------------------------------- roll call
    def _crew_reveal(c):
        sfx("win")
        renpy.show_screen("map_stamp", c["name"].upper(), _random.choice(c["roles"]).upper())
        persistent.crew_found = set(persistent.crew_found) | set([c["key"]])
        if len(persistent.crew_found) >= len(CREW):
            secret_found("crew", "whole_crew")
            renpy.notify(_("\"We've been waiting for you a while.\""))
        else:
            renpy.notify("%d / %d" % (len(persistent.crew_found), len(CREW)))

    def secret_key(tok):
        """Every key the main menu listens for goes through here."""
        konami_feed(tok)
        if len(tok) != 1:
            _SECRET.typed = ""
            return
        _SECRET.typed = (_SECRET.typed + tok)[-12:]
        if _SECRET.typed.endswith("debug"):
            _SECRET.typed = ""
            toggle_cheats()
            return
        for c in CREW:
            if _SECRET.typed.endswith(c["key"]):
                _SECRET.typed = ""
                _crew_reveal(c)
                return
        if more_secret_word(_SECRET.typed):
            _SECRET.typed = ""

    # letters the listener needs: every crew name, plus "b a" for the Konami code
    # crew names, "b a" for the Konami code, "debug" for the cheat menu
    SECRET_LETTERS = sorted(set("".join(c["key"] for c in CREW)) | set("ba") | set("debug"))

    def blackberry_click():
        _SECRET.berry_clicks += 1
        n = _SECRET.berry_clicks
        if n in BERRY_LINES:
            renpy.notify(BERRY_LINES[n])
        if n >= 13:
            _SECRET.berry_clicks = 0
            sfx("win")
            renpy.show_screen("pixel_parade")
            secret_found("parade", "pixel_parade")

    # ------------------------------------------------------------ right on time
    def check_departure():
        if _SECRET.departed:
            return
        now = _datetime.datetime.now()
        if now.hour % 12 == 4 and now.minute == 0:
            _SECRET.departed = True
            sfx("win")
            renpy.show_screen("map_stamp", "4:00", _("WELCOME ABOARD"))
            secret_found("on_time", "right_on_time")


# ------------------------------------------------------------------------------
# HEARTS
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# PIXEL PARADE  (the pixel passengers, see PIXEL_CROPS in characters.rpy)
# ------------------------------------------------------------------------------

transform parade_walk(delay=0.0):
    yanchor 1.0
    xanchor 0.5
    ypos 1.0
    yoffset -14
    xpos config.screen_width + 160
    alpha 0.0
    pause delay
    alpha 1.0
    parallel:
        linear 10.0 xpos -160
    parallel:
        block:
            easeout 0.17 yoffset -34
            easein 0.17 yoffset -14
            repeat

screen pixel_parade():
    zorder 90
    for i, px in enumerate(PIXEL_PASSENGERS):
        add px at parade_walk(i * 0.85)
    timer (10.0 + len(PIXEL_PASSENGERS) * 0.85 + 0.5) action Hide("pixel_parade")


# ==============================================================================
# MORE SECRETS
#
#   click each name in the credits (Eric's keeps going if you keep clicking)
#   type any passenger's name on the main menu
#   type "kanye" on the main menu
#   look out of the Carriage 2 window five times
#   open the game on Halloween
# ==============================================================================

define ENDING_VIDEO = "movies/ending_video.webm"
define CREDITS_MUSIC = "Songs/larp.opus"   # the larp song; the credits play MUSIC_FOR["credits"] (music.rpy)

# the little text that pops up in the corner when you click someone in the
# credits (placeholders for now - put your own text here)
define CREDITS_CORNER_TEXT = {
    "eric": "PLACEHOLDER",
    "hannah": "PLACEHOLDER",
    "aydin": "PLACEHOLDER",
    "ryan": "PLACEHOLDER",
}

default persistent.ending_video_seen = False
default persistent.credits_clicked = set()
default persistent.cast_called = set()
default persistent.eric_clicks = 0
default window_looks = 0

define MORE_SECRET_ACHIEVEMENTS = [
    {"id": "empty_train", "title": _("Not me. Him."), "description": _("Ride the empty train to the end."), "hidden": True},
    {"id": "golden_tickets", "title": _("Uh… uh… yes, the ticket."), "description": _("Find every golden ticket hidden on the train."), "hidden": False},
    {"id": "credits_all", "title": _("Anyone like who?"), "description": _("Click everyone in the credits."), "hidden": True},
    {"id": "cast_call", "title": _("Everyone."), "description": _("Type every passenger's name on the main menu."), "hidden": True},
    {"id": "quiet", "title": _("Way too quiet."), "description": _("Type a certain rapper's name on the main menu."), "hidden": True},
    {"id": "window", "title": _("What a beautiful sight outside!"), "description": _("Look out of the Carriage 2 window five times."), "hidden": True},
]

# (secret id, note) - added to EXTRAS > 4:01, just before THANKS FOR PLAYING!
define MORE_SECRET_NOTES = [
    ("empty_train", _("\"Not me. Him.\"")),
    ("credits_all", _("\"I don't even know anybody on this express.\"")),
    ("cast_call", _("\"I need to find out who was in this carriage. Everyone.\"")),
    ("quiet", _("\"...It's quiet. Way too quiet.\"")),
    ("window", _("\"What a beautiful sight outside! You can see everything from this train!\"")),
    ("halloween", _("\"...I don't think this carriage was ever meant to be found.\"")),
    ("golden", _("\"Uh… uh… yes, the ticket. I think it's somewhere here…\"")),
    ("logo", _("\"Man… This seems familiar…\"")),
    ("slots", _("\"JACKKKPOTTTTTTT! You win $2! Look at that, beginner's luck!\"")),
    ("train", _("\"Wow damn… So… Expensive cabin, huh?\"")),
    ("version", _("\"I'm… back at the start?\"")),
    ("four_hundred", _("\"Thank you for boarding….\"")),
    ("idle", _("\"Two pairs of eyes glint in the blackness, watching.\"")),
]

# type their name on the main menu: (name, picture, their line from the script)
define CAST_CALLS = [
    ("louis", "louis neutral", _("I'm gonna look around.")),
    ("dorothy", "dorothy neutral", _("Excuse me sir, tickets please.")),
    ("fedora", "fedora neutral", _("Why Hello There, are you ready for the CALAMITY?")),
    ("eduard", "eduard neutral", _("All the better for me, I reckon…")),
    ("shunyu", "shunyu excited", _("JACKKKPOTTTTTTT!")),
    ("kimmy", "kimmy neutral", _("Yawns… Hello, are you room service?")),
    ("himmel", "himmel neutral", _("W-what do you want, stranger?")),
    ("sebastian", "sebastian neutral", _("May I know your name, sir?")),
    ("misha", "misha neutral", _("You play nice. Not like the others. They always forget the order.")),
    ("agatha", "agatha neutral", _("C'mon, put the bandage on.")),
    ("ichora", "ichora neutral", _("Oh, I know.")),
    ("pattison", "pattison neutral", _("This goes to the clock, while this goes to the end...")),
    ("alexander", "alexander neutral", _("Depends? Are you a narc?")),
]

init python:
    for _sa in MORE_SECRET_ACHIEVEMENTS:
        if _sa["id"] not in [x["id"] for x in ACHIEVEMENTS]:
            ACHIEVEMENTS.append(_sa)
            achievement.register(_sa["id"])

    # slot the new notes in before the last one (THANKS FOR PLAYING!)
    SECRET_NOTES = SECRET_NOTES[:-1] + MORE_SECRET_NOTES + SECRET_NOTES[-1:]

    # the main menu also listens for passenger names, "kanye" and "400"
    SECRET_LETTERS = sorted(set(SECRET_LETTERS) | set("".join(n for n, _i, _l in CAST_CALLS)) | set("kanye") | set("40"))

    def more_secret_word(typed):
        """Called by secret_key with what's been typed so far. True if it matched."""
        if typed.endswith("400"):
            # every departure on the board, back to 4:00
            store.board_times = []
            sfx("win")
            renpy.show_screen("map_stamp", "4:00", _("GREKHOV EXPRESS"))
            renpy.notify(_("\"Thank you for boarding….\""))
            secret_found("four_hundred")
            return True
        if typed.endswith("kanye"):
            secret_found("quiet", "quiet")
            play_ending_video()
            return True
        for name, img, line in CAST_CALLS:
            if typed.endswith(name):
                cast_call(name, img, line)
                return True
        return False

    def play_ending_video():
        if renpy.loadable(ENDING_VIDEO):
            renpy.music.stop(fadeout=0.5)
            renpy.invoke_in_new_context(renpy.movie_cutscene, ENDING_VIDEO)
            persistent.ending_video_seen = True
            if main_menu:
                music_menu()
            renpy.restart_interaction()

    # ------------------------------------------------------------ passengers
    def cast_call(name, img, line):
        sfx("ui_click")
        renpy.show_screen("cast_peek", img)
        renpy.notify("\"" + line + "\"")
        persistent.cast_called = set(persistent.cast_called) | set([name])
        if len(persistent.cast_called) >= len(CAST_CALLS):
            secret_found("cast_call", "cast_call")

    # --------------------------------------------------------------- credits
    def credits_click(key):
        persistent.credits_clicked = set(persistent.credits_clicked) | set([key])
        c = [x for x in CREW if x["key"] == key][0]
        if key == "eric":
            persistent.eric_clicks = (persistent.eric_clicks or 0) + 1
            sfx("win")
            renpy.show_screen("eric_surprise")
            renpy.notify(CREDITS_CORNER_TEXT["eric"])
        elif key == "hannah":
            sfx("win")
            renpy.show_screen("hannah_surprise")
            renpy.notify(CREDITS_CORNER_TEXT["hannah"])
        elif key == "aydin":
            sfx("win")
            renpy.show_screen("aydin_surprise")
            renpy.notify(CREDITS_CORNER_TEXT["aydin"])
        elif key == "ryan":
            sfx("win")
            renpy.show_screen("ryan_surprise")
            renpy.notify(CREDITS_CORNER_TEXT["ryan"])
        if len(persistent.credits_clicked) >= len(CREW):
            secret_found("credits_all", "credits_all")

    # ------------------------------------------------------------ credits music
    class _CREDMUS(object):
        before = None       # where the music was before the credits opened

    def credits_music_on():
        """The credits' own songs, or larp music for the TICKETS style."""
        if _MUSIC.place not in ("credits", "credits_tickets"):
            _CREDMUS.before = _MUSIC.place
        menu_music_filter_off()
        music_for("credits_tickets" if persistent.credits_style == "tickets" else "credits", fade=1.0)

    def credits_music_off():
        if main_menu:
            menu_music_filter_on()
            music_menu()
        else:
            before = _CREDMUS.before
            _MUSIC.place = None
            if before and persistent.ingame_music:
                music_for(before, fade=1.0)
            else:
                renpy.music.stop(channel="music", fadeout=1.0)

    # -------------------------------------------------------------- halloween
    def check_halloween():
        if getattr(_SECRET, "spooked", False):
            return
        now = _datetime.datetime.now()
        if now.month == 10 and now.day == 31:
            _SECRET.spooked = True
            secret_found("halloween")
            renpy.invoke_in_new_context(jumpscare, "eyes")


# ------------------------------------------------------------------------------
# A PASSENGER PEEKS IN  (type their name on the main menu)
# ------------------------------------------------------------------------------

transform peek_in:
    xanchor 0.5
    yanchor 1.0
    xpos 1.12
    ypos 1.08
    easein 0.45 xpos 0.86
    pause 2.2
    easeout 0.45 xpos 1.12

screen cast_peek(img):
    zorder 150
    add img at peek_in
    timer 3.2 action Hide("cast_peek")

# The credits surprises (each person's name scene) live in credits_fx.rpy


# ------------------------------------------------------------------------------
# MAIN MENU SECRETS
#   click the logo three times     - it glitches into the old purple logo
#   click the train drawing        - it fades away (and comes back)
#   click the version five times   - v4:00
#   type 400                       - every departure goes back to 4:00
#   leave the menu alone a minute  - something walks through the carriage
#   click DEPARTURES on the board  - a slot machine (slots.rpy)
# ------------------------------------------------------------------------------

default logo_glitched = False
default train_gone = False
default train_trips = 0
default idle_walk = False
default version_pokes = 0

init python:
    class _MENU_SECRET(object):
        logo = 0

    def logo_poke():
        _MENU_SECRET.logo += 1
        if _MENU_SECRET.logo >= 3:
            _MENU_SECRET.logo = 0
            store.logo_glitched = True
            sfx("static")
            renpy.notify(_("\"Man… This seems familiar…\""))
            secret_found("logo")
        renpy.restart_interaction()

    def train_poke():
        if store.train_gone:
            return
        store.train_gone = True
        store.train_trips += 1
        sfx("win")
        renpy.notify(_("\"Wow damn… So… Expensive cabin, huh?\""))
        secret_found("train")
        renpy.restart_interaction()

    def version_poke():
        store.version_pokes += 1
        if store.version_pokes == 5:
            renpy.notify(_("\"I'm… back at the start?\""))
            secret_found("version")
        renpy.restart_interaction()

    def idle_watch():
        if persistent.jumpscares and not store.idle_walk:
            store.idle_walk = True
            secret_found("idle")
            renpy.restart_interaction()

# the purple logo, glitching
transform logo_glitch:
    alpha 1.0
    block:
        linear 0.04 xoffset 8
        linear 0.04 xoffset -6
        alpha 0.6
        linear 0.04 xoffset 0
        alpha 1.0
        pause 0.25
        linear 0.03 xoffset -10
        linear 0.03 xoffset 0
        pause 0.4
        repeat

# the train fades away into the dark (and comes back a few seconds later)
# clicked: the train fades away, then pulls back in from the left
transform train_leave(trip):
    alpha 1.0
    xoffset 0
    blur 0
    parallel:
        ease 1.4 alpha 0.0
    parallel:
        ease 1.4 xoffset 40 blur 8
    pause 0.6
    xoffset -320
    blur 8
    parallel:
        easein 1.8 xoffset 0
    parallel:
        ease 1.4 alpha 1.0 blur 0

# something walks slowly past, far away in the carriage
transform idle_walker:
    xanchor 0.5
    yanchor 1.0
    ypos 1.12
    xpos -0.1
    alpha 0.0
    parallel:
        ease 2.0 alpha 0.55
    parallel:
        linear 26.0 xpos 1.1
    parallel:
        block:
            ease 0.6 yoffset -8
            ease 0.6 yoffset 0
            repeat


# ------------------------------------------------------------------------------
# GOLDEN TICKETS
# A tiny golden ticket is hidden on each carriage map (Part 1 and Part 2). It
# glints every few seconds. Each one is worth coins and a ticket; find them all
# for an achievement. They stay found across playthroughs.
#   use golden_ticket("c1", x, y)    in a map screen (x, y in the 1920x1080 map)
# ------------------------------------------------------------------------------

default persistent.golden_found = set()

define GOLDEN_IDS = ["c1", "c2", "c3", "c4", "c5", "c2b", "c3b", "c5b"]
define GOLDEN_COINS = 25

init python:
    def find_golden(gid):
        if gid in persistent.golden_found:
            return
        persistent.golden_found = set(persistent.golden_found) | set([gid])
        n = len(persistent.golden_found)
        sfx("win")
        give_coins(GOLDEN_COINS)
        give_tickets(1)
        renpy.show_screen("map_stamp", _("GOLDEN TICKET"), "%d / %d" % (n, len(GOLDEN_IDS)))
        if n >= len(GOLDEN_IDS):
            secret_found("golden", "golden_tickets")
            renpy.notify(_("\"Uh… uh… yes, the ticket. I think it's somewhere here…\""))
        renpy.restart_interaction()

# mostly hard to see; every few seconds it catches the light
transform golden_glint(d=0.0):
    alpha 0.22
    pause d
    block:
        pause 3.2
        ease 0.25 alpha 1.0 zoom 1.25
        ease 0.45 alpha 0.22 zoom 1.0
        repeat

screen golden_ticket(gid, x, y):
    if gid not in persistent.golden_found:
        button:
            pos map_xy(x, y)
            xysize (40, 28)
            padding (0, 0)
            background None
            action Function(find_golden, gid)
            at golden_glint((len(gid) * 0.37) % 2.0)
            add rbox("#c9921a", 5):
                xysize (40, 28)
            add rbox("#ffd76a", 4):
                pos (3, 3)
                xysize (34, 22)
            add Solid("#c9921a"):
                pos (12, 3)
                xysize (2, 22)

