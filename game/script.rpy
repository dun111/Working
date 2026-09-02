# Character Definitions
define d = Character("Dorothy")
define l = Character("Louis")
define m = Character("Matthew")
define f = Character("Fedora")
define j = Character("Jackie")
define ed = Character("Eduard")
define b = Character("Braun")
define s = Character("Shunyu")
define k = Character("Kimmy")
define h = Character("Himmel")
define seb = Character("Sebastian")
define mi = Character("Misha")
define a = Character("Agatha")
define ic = Character("Ichora")
define p = Character("Pattison")
define al = Character("Alexander")
define pas = Character("Passenger")
define u = Character("???")

# Interaction Tracking Flags - Carriage 1
default c1_talked_matthew = False
default c1_talked_fedora = False

# Interaction Tracking Flags - Carriage 2
default c2_talked_jackie = False
default c2_talked_eduard = False
default c2_talked_braun = False
default c2_talked_shunyu = False
default has_maple_sugar = False

# Interaction Tracking Flags - Carriage 3
default c3_talked_kimmy = False
default c3_talked_himmel = False
default c3_talked_sebastian = False
default c3_talked_misha = False

# Interaction Tracking Flags - Carriage 4
default c4_talked_agatha = False
default c4_talked_ichora = False
default has_key = False

# Interaction Tracking Flags - Carriage 5
default c5_talked_pattison = False
default c5_talked_alexander = False

# Loop Tracking
default in_loop = False

##Screens###
screen carriage_1_map():
    imagemap:
        ground "bg carriage_1.png"
        hover "bg carriage_1_hover.png"

        # Hotspots: (xpos, ypos, width, height)
        if not c1_talked_matthew:
            hotspot (200, 150, 200, 400) action Call("c1_matthew_dialogue")

        if not c1_talked_fedora:
            hotspot (700, 150, 200, 400) action Call("c1_fedora_dialogue")

        # Door to next carriage (unlocked after speaking to everyone in C1)
        if c1_talked_matthew and c1_talked_fedora:
            hotspot (1100, 200, 150, 400) action Jump("carriage_2_start")

screen carriage_2_map():
    imagemap:
        ground "bg carriage_2.png"
        hover "bg carriage_2_hover.png"

        if not c2_talked_jackie:
            hotspot (100, 150, 180, 400) action Call("c2_jackie_dialogue")
        if not c2_talked_eduard:
            hotspot (350, 150, 180, 400) action Call("c2_eduard_dialogue")
        if not c2_talked_braun:
            hotspot (600, 150, 180, 400) action Call("c2_braun_dialogue")
        if not c2_talked_shunyu:
            hotspot (850, 150, 180, 400) action Call("c2_shunyu_dialogue")

        # Move to Carriage 3 once all 4 are spoken to
        if c2_talked_jackie and c2_talked_eduard and c2_talked_braun and c2_talked_shunyu:
            hotspot (1100, 200, 150, 400) action Jump("carriage_3_start")

# ==============================================================================
# MAIN GAME FLOW
# ==============================================================================

label start:
    $ _preferences.afm_enable = True
    $ _preferences.afm_time = 15

    scene Train station
    show dorothy happy
    d "Thank you for boarding the Grekhov Express"
    show louis confused
    l "“Wh-where am i?”{w=1}"
    show dorothy confused
    d " Excuse me sir, tickets please{w=2}"
    show louis confused
    show dorothy confused
    d "Are you fine… sir?"
    show louis looking around
    l "uh uh yes the ticket. I think its somewhere here{w=2}"
    show louis confused
    l "Miss, what line is this?{w=2}"
    show dorothy supprised
    d "The Grekhov Express? Are you ill? Everyone knows that, why else would you be on this train?{w=2}"
    show louis neutral
    l "O-oh, sorry, I think I might have gotten a bit light headed…{w=2}"
    show dorothy neutral
    d "I see. Well sir, welcome aboard the Grekhov Express…{w=1} "
    show louis confused
    l "I don’t remember how I got here… That’s right, I was tryna go home… But… What happened? I’m gonna look around{w=2}"
    jump carriage_1_start

# ------------------------------------------------------------------------------
# CARRIAGE 1
# ------------------------------------------------------------------------------
label carriage_1_start:
    call screen carriage_1_map

label c1_matthew_dialogue:
    scene talk to matthew
    show matthew neutral
    m "Hello, kind stranger {w=2}" 
    show louis neutral
    l "Uh...hey...{w=2}"
    show matthew neutral
    m "I thank the lord for this lovely day on the Grekhov. What is your name, brother? {w=2}"
    show louis neutral
    l "Uh, My name is Louis…{w=2}"
    show matthew neutral
    m "A wonderful name! I am Father Matthew… tell me, brother Louis… are you well? You look a bit out of it! {w=2}"
    show louis neutral
    l "Oh, nothing’s wrong, I’m just slightly light headed{w=2}"
    show matthew neutral
    m "Ah, may God wish you a speedy recovery. Now, if you will excuse me, I will resume my prayers. Oh, and be careful out there, I sense a disruption in holiness today. God bless!{w=2}"
    $ c1_talked_matthew = True
    return

label c1_fedora_dialogue:
    scene talk to fedora
    show louis neutral
    l "Uh, excuse me miss?{w=2}"
    show fedora neutral
    f "Why Hello There! Whaddaya need?{w=2}"
    show louis neutral
    l " I was wondering, what are you planning to find on this line?{w=2}"
    show fedora neutral
    f "I boarded this train to speak to the conductor after we arrive in Grekhov, I heard a case will open up once we reach there. It’ll rack NUMBERS for the steamboat. I CAN'T WAIT to interview the conductor!{w=2}"
    show louis neutral
    l " Why… the conducto-{w=2}"
    show fedora neutral
    f "Well, it’s been LOVELY talking to you, but my editor Twinkles is calling me. Toodooloo!{w=2}"
    show louis neutral
    l "uh ok i suppose{w=2}"
    
    $ c1_talked_fedora = True
    return

# ------------------------------------------------------------------------------
# CARRIAGE 2
# ------------------------------------------------------------------------------
label carriage_2_start:
    l "Heading into Carriage 2..."
    call screen carriage_2_map

label c2_jackie_dialogue:
    j "Don’t distract me, I need to clean up this glass that that bloody gambler over there shattered."
    show louis neutral
    l "Uh… Okay…"
    $ c2_talked_jackie = True
    return

label c2_eduard_dialogue:
    ed "Good evening lad, I’m Eduard, your bartender. Wouldya like some drinks?"
    menu:
        "Would you like a drink?"
        "Yes":
            $ drank = True
            l "Sure"
            ed "Awh shucks, seems we just ran out! That gambler’s been drinking since he got here!"
            l "Wow…"
        "No":
            $ drank= False
            l "Uh, it’s okay… I’m not really thirsty right now."
            ed "All the better for me, I reckon. That mahjong monster almost got me out of whiskey! He better win quick, before his tab gets as large as his confidence."
    $ c2_talked_eduard = True
    return

label c2_braun_dialogue:
    b ""
    $ c2_talked_braun = True
    return

label c2_shunyu_dialogue:
    s "Enjoy some maple sugar."
    $ has_maple_sugar = True
    $ c2_talked_shunyu = True
    return

# ------------------------------------------------------------------------------
# CARRIAGE 3 & BEYOND (Placeholders)
# ------------------------------------------------------------------------------
label carriage_3_start:
    l "Made it to Carriage 3!"
    return