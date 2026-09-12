# Character Definitions
define d = Character("Dorothy")
define l = Character("Louis")
define m = Character("Matthew")
define f = Character("Fedora")
define j = Character("Jackie")
define ed = Character("Eduard")
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
default c2_talked_shunyu = False
default c2_talked_braun = False
default has_maple_sugar = False
default drank = False
default played_mahjong = False

# Interaction Tracking Flags - Carriage 3
default c3_talked_kimmy = False
default c3_talked_himmel = False
default c3_talked_sebastian = False
default c3_talked_misha = False
default c3_kimmy_dangerous_choice = False

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

screen carriage_3_map():
    # NOTE: swap "bg carriage_3.png" / "bg carriage_3_hover.png" for your real art.
    # Hotspot coordinates are placeholders — adjust to match your background art.
    imagemap:
        ground "bg carriage_3.png"
        hover "bg carriage_3_hover.png"

        if not c3_talked_kimmy:
            hotspot (100, 150, 180, 400) action Call("c3_kimmy_dialogue")
        if not c3_talked_himmel:
            hotspot (350, 150, 180, 400) action Call("c3_himmel_dialogue")
        if not c3_talked_sebastian:
            hotspot (600, 150, 180, 400) action Call("c3_sebastian_dialogue")
        if not c3_talked_misha:
            hotspot (850, 150, 180, 400) action Call("c3_misha_dialogue")

        # Move to Carriage 4 once all 4 are spoken to
        if c3_talked_kimmy and c3_talked_himmel and c3_talked_sebastian and c3_talked_misha:
            hotspot (1100, 200, 150, 400) action Jump("carriage_4_start")

screen carriage_4_map():
    # NOTE: swap "bg carriage_4.png" / "bg carriage_4_hover.png" for your real art.
    imagemap:
        ground "bg carriage_4.png"
        hover "bg carriage_4_hover.png"

        if not c4_talked_agatha:
            hotspot (250, 150, 220, 400) action Call("c4_agatha_dialogue")
        if not c4_talked_ichora:
            hotspot (700, 150, 220, 400) action Call("c4_ichora_dialogue")

        # Move to Carriage 5 once both are spoken to
        if c4_talked_agatha and c4_talked_ichora:
            hotspot (1100, 200, 150, 400) action Jump("carriage_5_start")

screen carriage_5_map():
    # NOTE: swap "bg carriage_5.png" / "bg carriage_5_hover.png" for your real art.
    imagemap:
        ground "bg carriage_5.png"
        hover "bg carriage_5_hover.png"

        if not c5_talked_pattison:
            hotspot (250, 150, 220, 400) action Call("c5_pattison_dialogue")
        if not c5_talked_alexander:
            hotspot (700, 150, 220, 400) action Call("c5_alexander_dialogue")

        # End of current content once both are spoken to
        if c5_talked_pattison and c5_talked_alexander:
            hotspot (1100, 200, 150, 400) action Jump("carriage_5_end")

# ==============================================================================
# MAIN GAME FLOW
# ==============================================================================

label start:
    $ _preferences.afm_enable = True
    $ _preferences.afm_time = 15

    scene Train station
    $ achievement.grant("first_departure")
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
    show jackie neutral
    j "Don’t distract me, I need to clean up this glass that that bloody gambler over there shattered.{w=2}"
    show louis neutral
    l "Uh… Okay…{w=2}"

    $ c2_talked_jackie = True
    return

label c2_eduard_dialogue:
    show eduard neutral
    ed "Good evening lad, I’m Eduard, your bartender. Wouldya like some drinks?{w=2}"
    menu:
        "Would you like a drink?"
        "Yes":
            $ drank = True
            l "Sure"
            ed "Awh shucks, seems we just ran out! That gambler’s been drinking since he got here!"
            l "Wow…"
        "No":
            $ drank = False
            l "Uh, it’s okay… I’m not really thirsty right now."
            ed "All the better for me, I reckon. That mahjong monster almost got me out of whiskey! He better win quick, before his tab gets as large as his confidence."
    $ c2_talked_eduard = True
    return


label c2_braun_dialogue:
    l "Uh… hey."
    l "I think I’ll leave you to it."
    $ c2_talked_braun = True
    return


label c2_shunyu_dialogue:
    show shunyu neutral
    s "Yes! I can’t stop winning!{w=2}"
    show louis neutral
    l "Uhm… whatcha doin’?{w=2}"
    show shunyu neutral
    s "Playing Mahjong! Doncha just love winning!{w=2}"
    # Louis watches Shunyu pick up a tile.
    show shunyu excited
    s "JACKKKPOTTTTTTT{w=2}"
    show louis neutral
    l "R-right, well, I’ll leave you-{w=2}"
    show shunyu neutral
    menu:
        "Wanna play? Think about it. You can only lose 100%, but you can win 100000%! Look at the odds!"
        "Yes":
            $ played_mahjong = True
            s "You win $2"
        "No":
            $ played_mahjong = False
            l "I’m okay, don’t have much to gamble with anyway"
    $ c2_talked_shunyu = True
    return


# ------------------------------------------------------------------------------
# CARRIAGE 3
# ------------------------------------------------------------------------------
label carriage_3_start:
    l "Made it to Carriage 3!{w=2}"
    call screen carriage_3_map

label c3_kimmy_dialogue:
    show kimmy neutral
    k "Yawns… Hello, are you room service?{w=2}"
    show louis neutral
    l "N-no, my name is Louis… Nice to meet you.{w=2}"
    show himmel neutral
    h "O-oh my god dear! Why is there a STRANGER here! I-I might faint!{w=2}"
    show kimmy neutral
    menu:
        "Don’t worry Sugar, he’s not dangerous… I think.{w=2}"
        "He is dangerous":
            $ c3_kimmy_dangerous_choice = True
            k "With THAT frame… I don't think so sweetie"
        "He is not dangerous":
            $ c3_kimmy_dangerous_choice = False
            k "Yeah, it’s kinda obvious, matchstick.{w=2}"

    # Both branches continue into the same follow-up conversation
    show louis neutral
    l "Wow damn… So… Expensive cabin, huh?{w=2}"
    show kimmy neutral
    k "Well of course! My family has a clock business, so we’re quite well off.{w=2}"
    show louis neutral
    l "So what is such an important lady doing on a train like this?{w=2}"
    show kimmy neutral
    k "Oh, I have a meeting in █████████, and I wanted to make it a trip so I could spend more time with my darling, Himmel. Right, Sugar?{w=2}"
    show himmel neutral
    h "Of course!{w=2}"
    show louis neutral
    l "wow… such love birds{w=2}"
    $ c3_talked_kimmy = True
    return

label c3_himmel_dialogue:
    scene talk to himmel
    show himmel neutral
    h "W-what do you want, stranger?{w=2}"
    show louis neutral
    l "Nothing, just uh… finding my way to the bathroom.{w=2}"
    show himmel neutral
    h "It’s to the left! Now leave me alone!{w=2}"
    show louis neutral
    l "Holy moly, what’s that guy's problem…"
    $ c3_talked_himmel = True
    return

label c3_sebastian_dialogue:
    scene talk to sebastian
    show sebastian neutral
    seb "May I know your name, sir?{w=2}"
    show louis neutral
    l "Oh! It’s Louis.{w=2}"
    show sebastian neutral
    seb "Good evening, Mr. Louis. My name is Sebastian,  the butler for Mr. Popov, the child in this cabin. If you wish to enter, I will warn you, that if any harm or distress befalls the child, you will be prosecuted.{w=2}"
    show louis neutral
    l "Wow… Don’t worry Sir, I won’t.{w=2}"
    $ c3_talked_sebastian = True
    return

label c3_misha_dialogue:
    scene talk to misha
    show misha neutral
    show louis neutral
    l "Hey buddy…{w=2}" 
    show misha stares
    $ c3_talked_misha = True
    return

#Interact with Carpet next to misha
#Why is it sticking up like that?

#Interact with toys
#Awh, they’re so cute.

#Interact with Kimmy and Himmel’s luggage
#So much luggage… Do they really need this much for a worktr

# ------------------------------------------------------------------------------
# CARRIAGE 4
# ------------------------------------------------------------------------------

label carriage_4_start:
    l "Opens the door to carriage 4...{w=2}"
    call screen carriage_4_map

label c4_agatha_dialogue:
    scene talk to agatha
    show agatha neutral
    a "cmon, put the bandage on.{w=2}"
    pas "It hurtssss oh my my poor finger, I may never play marvel rivals again!{w=2}"
    show agatha neutral
    a "I don’t care. You pricked it, it’s not bleeding. Put the bandaid on and stop wasting my time.{w=2}"
    pas "Fine.{w=2}"
    pas "~The passenger pouts for a second and storms off~"
    show agatha neutral
    a "Actual Infants…{w=2}"
    a "~agatha looks at you~"
    a "What, need help too?{w=2}"
    show louis neutral
    l "No, but, what’s this carriage?{w=2}"
    show agatha neutral
    a "If you use your eyes, you can see it's the staff cart. Now, are you injured, or can I go back to my peace?{w=2}"    
    show louis neutral
    l "I’m… fine."
    $ c4_talked_agatha = True
    return

label c4_ichora_dialogue:
    scene talk to ichora
    show ichora neutral
    ic "Hey! I’ve been waiting for ya buddy!{w=2}"
    show louis neutral
    l "You have…?{w=2}"
    show ichora neutral
    ic "Of course! Welcome to the train. The name's Ichora, I’m the train’s engineer.{w=2}"
    show louis neutral
    l "My name’s Louis.{w=2}"
    show ichora neutral
    ic "Oh, I know.{w=2}"
    show louis neutral
    l "How-{w=2}"
    show ichora neutral
    ic "We’ve been waiting for you a while. Anyways, I got a gift for ya! Come with me!{w=2}"
    show engine room
    ic "~ichora gives u a key~"
    ic "Here ya go!{w=2}"
    show louis neutral
    l "But what’s it for?{w=2}"
    show ichora neutral
    ic "Sometimes, life gets hard, and a door is presented to escape. But we’re too scared to use the key. Don’t hesitate.{w=2}"
    ic "~Ichora winks and walks off~"
    $ has_key = True
    $ c4_talked_ichora = True
    return

#Interact with syringe
#“That looks sharp.”

#Interact with engine
#“This looks like it has a lot of… Zebra power? No, horse power.”

# ------------------------------------------------------------------------------
# CARRIAGE 5
# ------------------------------------------------------------------------------

label carriage_5_start:
    show louis neutral
    l "A lot is going on here, huh.{w=2}"
    call screen carriage_5_map

label c5_pattison_dialogue:
    scene talk to pattison
    # TODO: Pattison's dialogue hasn't been written yet.
    show louis neutral
    l "..."
    $ c5_talked_pattison = True
    return

label c5_alexander_dialogue:
    scene talk to alexander
    show alexander neutral
    al "Hahahaha… this stuff is so gooddddd…."
    show louis neutral
    l "What you got there, buddy?"
    show alexander neutral
    al "The banned super maple sugar!!!"
    show louis neutral
    l "Damn… why’s it banned?"
    show alexander neutral
    al "HAhaha… They tryna take the good stuff from us, don’t want us having too much fun, haha…"
    show louis neutral
    l "Oh, I see."
    show alexander neutral
    al "Want some, buddy? First one is free, next one is 2000 perkels."

    menu:
        "Take the maple sugar?":
            $ has_maple_sugar = True
            show louis neutral
            l "Sure, I’ll take some."
            show alexander neutral
            al "Attaboy! Here ya go — one satchel of pure happiness."
        "No":
            $ has_maple_sugar = False
            show louis neutral
            l "I’m good. Thanks for the offer."
            show alexander neutral
            al "Suit yourself, brother."

    show louis neutral
    l "Has anyone else bought these things?"
    show alexander neutral
    al "Depends? Are you a narc?"
    show louis neutral
    l "No."
    show alexander neutral
    al "Well, there’s this guy that keeps winning money from gambling, yet still hasn’t paid for his last portion. Don’t worry, I’ll make him suffer."
    al "And as for the other one… the stuff was strong so I don't remember."
    show louis neutral
    l "Why did I expect that? But who’s the other person?"
    show alexander neutral
    al "~Alexander looks at you blankly.~"
    $ c5_talked_alexander = True
    return

# ------------------------------------------------------------------------------
# TEMPORARY ENDING STUB — replace with Carriage 6 or a real ending once written
# ------------------------------------------------------------------------------
label carriage_5_end:
    scene black with dissolve
    centered "{i}...to be continued...{/i}"
    return
