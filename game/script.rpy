# Character Definitions
define d   = C("Dorothy")
define l   = C("Louis")
define m   = C("Matthew")
define f   = C("Fedora")
define j   = C("Jackie")
define ed  = C("Eduard")
define s   = C("Shunyu")
define k   = C("Kimmy")
define h   = C("Himmel")
define seb = C("Sebastian")
define mi  = C("Misha")
define a   = C("Agatha")
define ic  = C("Ichora")
define p   = C("Pattison")
define al  = C("Alexander")
define pas = C("Passenger")
define u   = C("???")

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
default winning_tile = 0

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

# Interaction Tracking Flags - Carriage 2, Part 2 (crime scene)
default c2_p2_found_body = False
default c2_p2_reinterviewed_eduard = False
default c2_p2_reinterviewed_agatha = False

# Loop Tracking
default in_loop = False

##Screens###

screen carriage_1_map():
    imagemap:
        ground "bg carriage_1.png"
        hover "bg carriage_1_hover.png"
        if not c1_talked_matthew and not in_loop:
            hotspot (200, 150, 200, 400) action Call("c1_matthew_dialogue")
        if not c1_talked_fedora or in_loop:
            hotspot (700, 150, 200, 400) action Call("c1_fedora_dialogue")
        hotspot (950, 620, 160, 160) action Call("c1_interact_window")
        hotspot (1150, 620, 160, 160) action Call("c1_interact_cupboard")
        hotspot (1350, 620, 160, 160) action Call("c1_interact_admin_door")
        hotspot (1550, 620, 160, 160) action Call("c1_interact_tea_stain")
        if (c1_talked_matthew and c1_talked_fedora) or in_loop:
            hotspot (1100, 200, 150, 400) action Call("c1_door_to_carriage_2")

screen carriage_2_map():
    imagemap:
        ground "bg carriage_2.png"
        hover "bg carriage_2_hover.png"
        hotspot (0, 600, 80, 300) action Jump("carriage_1_start")
        if not c2_talked_jackie:
            hotspot (100, 150, 180, 400) action Call("c2_jackie_dialogue")
        if not c2_talked_eduard:
            hotspot (350, 150, 180, 400) action Call("c2_eduard_dialogue")
        if not c2_talked_braun:
            hotspot (600, 150, 180, 400) action Call("c2_braun_dialogue")
        if not c2_talked_shunyu:
            hotspot (850, 150, 180, 400) action Call("c2_shunyu_dialogue")
        hotspot (950, 620, 160, 160) action Call("c2_interact_window")
        hotspot (1150, 620, 160, 160) action Call("c2_interact_broken_glass")
        if c2_talked_jackie and c2_talked_eduard and c2_talked_braun and c2_talked_shunyu:
            hotspot (1100, 200, 150, 400) action Jump("carriage_3_start")

screen carriage_3_map():
    imagemap:
        ground "bg carriage_3.png"
        hover "bg carriage_3_hover.png"
        hotspot (0, 600, 80, 300) action Jump("carriage_2_start")
        if not c3_talked_kimmy:
            hotspot (100, 150, 180, 400) action Call("c3_kimmy_dialogue")
        if not c3_talked_himmel:
            hotspot (350, 150, 180, 400) action Call("c3_himmel_dialogue")
        if not c3_talked_sebastian:
            hotspot (600, 150, 180, 400) action Call("c3_sebastian_dialogue")
        if not c3_talked_misha:
            hotspot (850, 150, 180, 400) action Call("c3_misha_dialogue")
        hotspot (950, 620, 160, 160) action Call("c3_interact_empty_room")
        hotspot (1150, 620, 160, 160) action Call("c3_interact_carpet")
        hotspot (1350, 620, 160, 160) action Call("c3_interact_toys")
        hotspot (1550, 620, 160, 160) action Call("c3_interact_luggage")
        if c3_talked_kimmy and c3_talked_himmel and c3_talked_sebastian and c3_talked_misha:
            hotspot (1100, 200, 150, 400) action Jump("carriage_4_start")

screen carriage_4_map():
    imagemap:
        ground "bg carriage_4.png"
        hover "bg carriage_4_hover.png"
        hotspot (0, 600, 80, 300) action Jump("carriage_3_start")
        if not c4_talked_agatha:
            hotspot (250, 150, 220, 400) action Call("c4_agatha_dialogue")
        if not c4_talked_ichora:
            hotspot (700, 150, 220, 400) action Call("c4_ichora_dialogue")
        hotspot (950, 620, 160, 160) action Call("c4_interact_syringe")
        hotspot (1150, 620, 160, 160) action Call("c4_interact_engine")
        if c4_talked_agatha and c4_talked_ichora:
            hotspot (1100, 200, 150, 400) action Jump("carriage_5_start")

screen carriage_5_map():
    imagemap:
        ground "bg carriage_5.png"
        hover "bg carriage_5_hover.png"
        hotspot (0, 600, 80, 300) action Jump("carriage_4_start")
        if not c5_talked_pattison:
            hotspot (250, 150, 220, 400) action Call("c5_pattison_dialogue")
        if not c5_talked_alexander:
            hotspot (700, 150, 220, 400) action Call("c5_alexander_dialogue")
        hotspot (950, 620, 160, 160) action Call("c5_interact_mail_room")
        hotspot (1150, 620, 160, 160) action Call("c5_interact_luggage_room")
        if c5_talked_pattison and c5_talked_alexander:
            hotspot (1400, 200, 150, 400) action Call("c5_carriage6_door")

screen carriage_2_part2_map():
    imagemap:
        ground "bg carriage_2.png"
        hover "bg carriage_2_hover.png"
        if not c2_p2_found_body:
            hotspot (100, 150, 180, 400) action Call("c2_p2_interact_window")
            hotspot (350, 150, 180, 400) action Call("c2_p2_talk_eduard")
            hotspot (600, 150, 180, 400) action Call("c2_p2_overturned_table")
            hotspot (850, 150, 180, 400) action Call("c2_p2_broken_glass")
            hotspot (1100, 150, 180, 400) action Call("c2_p2_bar_counter")
            hotspot (1350, 150, 180, 400) action Call("c2_p2_second_table")

screen carriage_2_part2_investigation_map():
    imagemap:
        ground "bg carriage_2.png"
        hover "bg carriage_2_hover.png"
        if not c2_p2_reinterviewed_eduard:
            hotspot (350, 150, 200, 400) action Call("c2_p2_reinterview_eduard")
        if not c2_p2_reinterviewed_agatha:
            hotspot (600, 150, 200, 400) action Call("c2_p2_reinterview_agatha")
        if c2_p2_reinterviewed_eduard and c2_p2_reinterviewed_agatha:
            hotspot (1100, 150, 200, 400) action Jump("part2_chapter_end")

# ==============================================================================
# MAIN GAME FLOW
# ==============================================================================

label start:
    $ _preferences.afm_enable = True
    $ _preferences.afm_time = 15
    scene Train station
    $ achievement.grant("first_departure")

    show dorothy happy at speaker_focus(xalign=0.9)
    d "Thank you for boarding the Grekhov Express"
    show dorothy happy at speaker_background(xalign=0.9)
    show louis confused at speaker_focus(xalign=0.1)
    l "“Wh-where am i?”{w=1}"
    show louis confused at speaker_background(xalign=0.1)
    show dorothy confused at speaker_focus(xalign=0.9)
    d "Excuse me sir, tickets please{w=2}"
    d "Are you fine… sir?"
    show dorothy confused at speaker_background(xalign=0.9)
    show louis looking_around at speaker_focus(xalign=0.1)
    l "uh uh yes the ticket. I think its somewhere here{w=2}"
    show louis confused at speaker_focus(xalign=0.1)
    l "Miss, what line is this?{w=2}"
    show louis confused at speaker_background(xalign=0.1)
    show dorothy supprised at speaker_focus(xalign=0.9)
    d "The Grekhov Express? Are you ill? Everyone knows that, why else would you be on this train?{w=2}"
    show dorothy supprised at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "O-oh, sorry, I think I might have gotten a bit light headed…{w=2}"
    show louis neutral at speaker_background(xalign=0.1)
    show dorothy neutral at speaker_focus(xalign=0.9)
    d "I see. Well sir, welcome aboard the Grekhov Express…{w=1} "
    show dorothy neutral at speaker_background(xalign=0.9)
    show louis confused at speaker_focus(xalign=0.1)
    l "I don’t remember how I got here… That’s right, I was tryna go home… But… What happened? I’m gonna look around{w=2}"
    jump carriage_1_start

# ------------------------------------------------------------------------------
# CARRIAGE 1
# ------------------------------------------------------------------------------
label carriage_1_start:
    call screen carriage_1_map

label c1_matthew_dialogue:
    scene talk to matthew
    show matthew neutral at speaker_focus(xalign=0.9)
    m "Hello, kind stranger {w=2}"
    show matthew neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Uh...hey...{w=2}"
    m "I thank the lord for this lovely day on the Grekhov. What is your name, brother? {w=2}"
    l "Uh, My name is Louis…{w=2}"
    m "A wonderful name! I am Father Matthew… tell me, brother Louis… are you well? You look a bit out of it! {w=2}"
    l "Oh, nothing’s wrong, I’m just slightly light headed{w=2}"
    m "Ah, may God wish you a speedy recovery. Now, if you will excuse me, I will resume my prayers. Oh, and be careful out there, I sense a disruption in holiness today. God bless!{w=2}"
    $ c1_talked_matthew = True
    return

label c1_fedora_dialogue:
    if in_loop:
        scene talk to fedora
        show louis neutral at speaker_focus(xalign=0.1)
        l "Uh, excuse me miss?{w=2}"
        show louis neutral at speaker_background(xalign=0.1)
        show fedora neutral at speaker_focus(xalign=0.9)
        f "Why Hello There, are you ready for the CALAMITY?{w=2}"
        l "Calamity?{w=2}"
        f "I boarded this train to speak to the conductor after we arrived in Grekhov, I heard CALAMITY will open up once we reach there. It’ll rack NUMBERS for the steamboat. I CAN'T WAIT to interview the KILLER.{w=2}"
        l "Killer?{w=2}"
        f "Well, it’s been LOVELY talking to you, but my editor Twinkles is calling me. WATCH OUT.{w=2}"
        l "OKAY…. or what?{w=2}"
    else:
        scene talk to fedora
        show louis neutral at speaker_focus(xalign=0.1)
        l "Uh, excuse me miss?{w=2}"
        show louis neutral at speaker_background(xalign=0.1)
        show fedora neutral at speaker_focus(xalign=0.9)
        f "Why Hello There! Whaddaya need?{w=2}"
        l "I was wondering, what are you planning to find on this line?{w=2}"
        f "I boarded this train to speak to the conductor after we arrive in Grekhov, I heard a case will open up once we reach there. It’ll rack NUMBERS for the steamboat. I CAN'T WAIT to interview the conductor!{w=2}"
        l "Why… the conducto-{w=2}"
        f "Well, it’s been LOVELY talking to you, but my editor Twinkles is calling me. Toodooloo!{w=2}"
        l "uh ok i suppose{w=2}"

    $ c1_talked_fedora = True
    return

label c1_interact_window:
    "What a beautiful sight outside! You can see everything from this train!{w=2}"
    return

label c1_interact_cupboard:
    if in_loop:
        u "Be careful, young one. Do you really wanna do that?{w=2}"
    else:
        "Hmm… It seems to be locked. What would be in there?{w=2}"
    return

label c1_interact_admin_door:
    "I'm not supposed to enter this carriage, am I…{w=2}"
    return

label c1_interact_tea_stain:
    if in_loop:
        show louis confused at speaker_focus(xalign=0.5)
        l "W-why does it smell… like iron?{w=2}"
    else:
        "Ooh, I thought this was blood for a second…{w=2}"
    return

label c1_door_to_carriage_2:
    if not in_loop:
        show louis neutral at speaker_focus(xalign=0.5)
        l "Oh, this place is quite fancy. Is it like some sort of restaurant?{w=2}"
        jump carriage_2_start
    else:
        show louis neutral at speaker_focus(xalign=0.5)
        l "...It's quiet. Way too quiet.{w=2}"
        jump carriage_2_part2_start

# ------------------------------------------------------------------------------
# CARRIAGE 2
# ------------------------------------------------------------------------------
label carriage_2_start:
    $ achievement.grant("carriage_1_complete")
    l "Heading into Carriage 2..."
    call screen carriage_2_map

label c2_jackie_dialogue:
    show jackie neutral at speaker_focus(xalign=0.9)
    j "Don’t distract me, I need to clean up this glass that that bloody gambler over there shattered.{w=2}"
    show jackie neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Uh… Okay…{w=2}"

    $ c2_talked_jackie = True
    return

label c2_eduard_dialogue:
    show eduard neutral at speaker_focus(xalign=0.9)
    ed "Good evening lad, I’m Eduard, your bartender. Wouldya like some drinks?{w=2}"
    menu:
        "Would you like a drink?"
        "Yes":
            $ drank = True
            show eduard neutral at speaker_background(xalign=0.9)
            show louis neutral at speaker_focus(xalign=0.1)
            l "Sure"
            ed "Awh shucks, seems we just ran out! That gambler’s been drinking since he got here!"
            l "Wow…"
        "No":
            $ drank = False
            show eduard neutral at speaker_background(xalign=0.9)
            show louis neutral at speaker_focus(xalign=0.1)
            l "Uh, it’s okay… I’m not really thirsty right now."
            ed "All the better for me, I reckon. That mahjong monster almost got me out of whiskey! He better win quick, before his tab gets as large as his confidence."
    $ c2_talked_eduard = True
    return


label c2_braun_dialogue:
    show louis neutral at speaker_focus(xalign=0.5)
    l "Uh… hey."
    l "I think I’ll leave you to it."
    $ c2_talked_braun = True
    return


label c2_shunyu_dialogue:
    show shunyu neutral at speaker_focus(xalign=0.9)
    s "Yes! I can’t stop winning!{w=2}"
    show shunyu neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Uhm… whatcha doin’?{w=2}"
    s "Playing Mahjong! Doncha just love winning!{w=2}"
    "{i}Louis watches Shunyu pick up a tile.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    show shunyu excited at speaker_focus(xalign=0.9)
    s "JACKKKPOTTTTTTT{w=2}"
    l "R-right, well, I’ll leave you-{w=2}"
    show shunyu neutral at speaker_focus(xalign=0.9)
    menu:
        "Wanna play? Think about it. You can only lose 100%%, but you can win 100000%%! Look at the odds!"
        "Yes":
            $ achievement.grant("high_roller")
            $ winning_tile = renpy.random.randint(0, 2)
            call screen mahjong_minigame
            if _return == "win":
                show shunyu excited at speaker_focus(xalign=0.9)
                s "JACKKKPOTTTTTTT! You win $2! Look at that, beginner's luck!{w=2}"
                $ played_mahjong = "won"
            else:
                show shunyu neutral at speaker_focus(xalign=0.9)
                s "Aw, shoot. Unlucky draw! Better luck next time, alright?{w=2}"
                $ played_mahjong = "lost"
        "No":
            $ played_mahjong = False
            l "I’m okay, don’t have much to gamble with anyway"
    $ c2_talked_shunyu = True
    return

label c2_interact_window:
    "What a beautiful sight outside! You can see everything from this train!{w=2}"
    return

label c2_interact_broken_glass:
    show louis neutral at speaker_focus(xalign=0.5)
    l "Damn, how'd that gambler guy even break it?{w=2}"
    u "Can yer shut up?{w=2}"
    return

# ------------------------------------------------------------------------------
# CARRIAGE 3
# ------------------------------------------------------------------------------
label carriage_3_start:
    $ achievement.grant("carriage_2_complete")
    l "Made it to Carriage 3!{w=2}"
    l "Shh… Looks like I better be quiet.{w=2}"
    call screen carriage_3_map

label c3_kimmy_dialogue:
    show kimmy neutral at speaker_focus(xalign=0.3)
    k "Yawns… Hello, are you room service?{w=2}"
    show kimmy neutral at speaker_background(xalign=0.3)
    show louis neutral at speaker_focus(xalign=0.1)
    l "N-no, my name is Louis… Nice to meet you.{w=2}"
    show louis neutral at speaker_background(xalign=0.1)
    show himmel neutral at speaker_focus(xalign=0.9)
    h "O-oh my god dear! Why is there a STRANGER here! I-I might faint!{w=2}"
    menu:
        "Don’t worry Sugar, he’s not dangerous… I think.{w=2}"
        "He is dangerous":
            $ c3_kimmy_dangerous_choice = True
            k "With THAT frame… I don't think so sweetie"
        "He is not dangerous":
            $ c3_kimmy_dangerous_choice = False
            k "Yeah, it’s kinda obvious, matchstick.{w=2}"
    l "Wow damn… So… Expensive cabin, huh?{w=2}"
    k "Well of course! My family has a clock business, so we’re quite well off.{w=2}"
    l "So what is such an important lady doing on a train like this?{w=2}"
    k "Oh, I have a meeting in █████████, and I wanted to make it a trip so I could spend more time with my darling, Himmel. Right, Sugar?{w=2}"
    h "Of course!{w=2}"
    l "wow… such love birds{w=2}"
    $ c3_talked_kimmy = True
    return

label c3_himmel_dialogue:
    scene talk to himmel
    show himmel neutral at speaker_focus(xalign=0.9)
    h "W-what do you want, stranger?{w=2}"
    show himmel neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Nothing, just uh… finding my way to the bathroom.{w=2}"
    h "It’s to the left! Now leave me alone!{w=2}"
    l "Holy moly, what’s that guy's problem…"
    $ c3_talked_himmel = True
    return

label c3_sebastian_dialogue:
    scene talk to sebastian
    show sebastian neutral at speaker_focus(xalign=0.9)
    seb "May I know your name, sir?{w=2}"
    show sebastian neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Oh! It’s Louis.{w=2}"
    seb "Good evening, Mr. Louis. My name is Sebastian,  the butler for Mr. Popov, the child in this cabin. If you wish to enter, I will warn you, that if any harm or distress befalls the child, you will be prosecuted.{w=2}"
    l "Wow… Don’t worry Sir, I won’t.{w=2}"
    $ c3_talked_sebastian = True
    return

label c3_misha_dialogue:
    scene talk to misha
    show misha neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Hey buddy…{w=2}"
    show louis neutral at speaker_background(xalign=0.1)
    show misha stares at speaker_focus(xalign=0.9)
    $ c3_talked_misha = True
    return

label c3_interact_empty_room:
    "Wow, so spacious! These must cost a lot.{w=2}"
    return

label c3_interact_carpet:
    "Why is it sticking up like that?{w=2}"
    return

label c3_interact_toys:
    "Awh, they’re so cute.{w=2}"
    return

label c3_interact_luggage:
    "So much luggage… Do they really need this much for a worktrip?{w=2}"
    return

# ------------------------------------------------------------------------------
# CARRIAGE 4
# ------------------------------------------------------------------------------

label carriage_4_start:
    $ achievement.grant("carriage_3_complete")
    l "Opens the door to carriage 4...{w=2}"
    call screen carriage_4_map

label c4_agatha_dialogue:
    scene talk to agatha
    show agatha neutral at speaker_focus(xalign=0.9)
    a "cmon, put the bandage on.{w=2}"
    pas "It hurtssss oh my my poor finger, I may never play marvel rivals again!{w=2}"
    a "I don’t care. You pricked it, it’s not bleeding. Put the bandaid on and stop wasting my time.{w=2}"
    pas "Fine.{w=2}"
    "{i}The passenger pouts for a second and storms off.{/i}"
    a "Actual Infants…{w=2}"
    "{i}Agatha looks at you.{/i}"
    a "What, need help too?{w=2}"
    show agatha neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "No, but, what’s this carriage?{w=2}"
    a "If you use your eyes, you can see it's the staff cart. Now, are you injured, or can I go back to my peace?{w=2}"
    l "I’m… fine."
    $ c4_talked_agatha = True
    return

label c4_ichora_dialogue:
    scene talk to ichora
    show ichora neutral at speaker_focus(xalign=0.9)
    ic "Hey! I’ve been waiting for ya buddy!{w=2}"
    show ichora neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "You have…?{w=2}"
    ic "Of course! Welcome to the train. The name's Ichora, I’m the train’s engineer.{w=2}"
    l "My name’s Louis.{w=2}"
    ic "Oh, I know.{w=2}"
    l "How-{w=2}"
    ic "We’ve been waiting for you a while. Anyways, I got a gift for ya! Come with me!{w=2}"
    show engine room
    "{i}Ichora gives you a key.{/i}"
    ic "Here ya go!{w=2}"
    l "But what’s it for?{w=2}"
    ic "Sometimes, life gets hard, and a door is presented to escape. But we’re too scared to use the key. Don’t hesitate.{w=2}"
    "{i}Ichora winks and walks off.{/i}"
    $ has_key = True
    $ achievement.grant("key_holder")
    $ c4_talked_ichora = True
    return

label c4_interact_syringe:
    "That looks sharp.{w=2}"
    return

label c4_interact_engine:
    "This looks like it has a lot of… Zebra power? No, horse power.{w=2}"
    return

# ------------------------------------------------------------------------------
# CARRIAGE 5
# ------------------------------------------------------------------------------

label carriage_5_start:
    $ achievement.grant("carriage_4_complete")
    show louis neutral at speaker_focus(xalign=0.5)
    l "A lot is going on here, huh.{w=2}"
    call screen carriage_5_map

label c5_pattison_dialogue:
    scene talk to pattison
    show pattison neutral at speaker_focus(xalign=0.9)
    p "This goes to the clock, while this goes to the end. This goes to the fake ones and this goes to the friend.{w=2}"
    show pattison neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "U-uhm… what?{w=2}"
    p "Hello Sir, you another mailworker?{w=2}"
    l "no.{w=2}"
    l "I don't even know anybody on this express{w=2}"
    p "It’s okay, you will before the end.{w=2}"
    l "What end?{w=2}"
    "{i}Pattison stares at you blankly.{/i}"
    $ c5_talked_pattison = True
    return

label c5_alexander_dialogue:
    scene talk to alexander
    show alexander neutral at speaker_focus(xalign=0.9)
    al "Hahahaha… this stuff is so gooddddd…."
    show alexander neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "What you got there, buddy?"
    al "The banned super maple sugar!!!"
    l "Damn… why’s it banned?"
    al "HAhaha… They tryna take the good stuff from us, don’t want us having too much fun, haha…"
    l "Oh, I see."
    al "Want some, buddy? First one is free, next one is 2000 perkels."

    menu:
        "Take the maple sugar?":
            $ has_maple_sugar = True
            $ achievement.grant("forbidden_sweetness")
            l "Sure, I’ll take some."
            al "Attaboy! Here ya go — one satchel of pure happiness."
        "No":
            $ has_maple_sugar = False
            l "I’m good. Thanks for the offer."
            al "Suit yourself, brother."

    l "Has anyone else bought these things?"
    al "Depends? Are you a narc?"
    l "No."
    al "Well, there’s this guy that keeps winning money from gambling, yet still hasn’t paid for his last portion. Don’t worry, I’ll make him suffer."
    al "And as for the other one… the stuff was strong so I don't remember."
    l "Why did I expect that? But who’s the other person?"
    "{i}Alexander looks at you blankly.{/i}"
    $ c5_talked_alexander = True
    return

label c5_interact_mail_room:
    "Wow, so much mail comes to this train, how?{w=2}"
    return

label c5_interact_luggage_room:
    "Most of this is probably that couple's, I can't lie.{w=2}"
    return

label c5_carriage6_door:
    $ achievement.grant("carriage_5_complete")
    $ achievement.grant("eyes_in_the_dark")
    show louis confused at speaker_focus(xalign=0.5)
    l "Huh… it's…{w=2}"
    scene black with dissolve
    u "Not yet! Try to see the truth before you see the future.{w=2}"
    "{i}Two pairs of eyes glint in the blackness, watching.{/i}"
    jump part2_start

# ==============================================================================
# PART 2 — THE LOOP
# ==============================================================================

label part2_start:
    $ achievement.grant("the_loop_begins")
    $ in_loop = True
    scene black
    with Pause(0.3)
    show dorothy neutral at speaker_focus(xalign=0.9)
    d "Thank you for boarding the Grekhov Express{w=2}"
    show dorothy neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Man… This seems familiar…{w=2}"
    l "“Here again?”{w=2}"
    d "Excuse me sir, tickets please{w=2}"
    l "Didn’t I already give you my ticket?{w=2}"
    d "Are you fine… sir?{w=2}"
    show louis confused at speaker_focus(xalign=0.1)
    "{i}Louis feels something in his pocket. The ticket is still there — but now it reads: “DO OR DIE.”{/i}"
    l "Huh??{w=2}"
    d "I see. Well sir, welcome aboard the Grekhov Express…{w=2}"
    show louis neutral at speaker_focus(xalign=0.1)
    l "I’m… back at the start?{w=2}"
    jump carriage_1_start

label carriage_2_part2_start:
    "{i}Louis enters. The lights feel dimmer, creepier than before.{/i}"
    call screen carriage_2_part2_map

label c2_p2_interact_window:
    "Huh… It's dark..{w=2}"
    return

label c2_p2_talk_eduard:
    show eduard neutral at speaker_focus(xalign=0.9)
    "{i}Eduard is standing behind the bar, unmoving, polishing the same glass over and over.{/i}"
    show eduard neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Uh… hey, you open?{w=2}"
    ed "All the better for me, I reckon…{w=2}"
    l "...What?{w=2}"
    ed "All the better for me, I reckon…{w=2}"
    l "Are you okay, man?{w=2}"
    "{i}Eduard stops polishing. He looks up. His eyes don’t quite focus on Louis.{/i}"
    ed "He better win quick. Before his tab gets as large as his confidence.{w=2}"
    l "Who? Eduard, who are you talking about—{w=2}"
    "{i}Eduard goes back to polishing the glass. It was never dirty.{/i}"
    return

label c2_p2_overturned_table:
    "{i}There are mahjong tiles scattered on the floor beneath it. One of them is face down, pressed flat, like something heavy stood on it.{/i}"
    return

label c2_p2_broken_glass:
    show louis neutral at speaker_focus(xalign=0.5)
    l "This is the same glass from before… why hasn’t anyone cleaned this up?{w=2}"
    "{i}Louis notices a piece missing from the largest shard — snapped clean off, edges sharp.{/i}"
    u "Can yer shut up?{w=2}"
    show louis confused at speaker_focus(xalign=0.5)
    l "H-hello?? Who said that…{w=2}"
    "{i}No one is there.{/i}"
    return

label c2_p2_bar_counter:
    "{i}There’s something dark pooling near the base of the counter, thin, creeping toward the tiles. Louis doesn’t want to know what it is yet. He’ll find out soon enough.{/i}"
    return

label c2_p2_second_table:
    show louis neutral at speaker_focus(xalign=0.5)
    l "...Hey. Hey, sir? You okay?{w=2}"
    "{i}Louis reaches out and turns the figure over.{/i}"
    "{i}It’s Shunyu.{/i}"
    "{i}There’s a jagged shard of glass buried in his side, dark red soaked deep into his shirt around it. His eyes are open. A mahjong tile is placed neatly in his open palm, resting there like it was set on purpose. The rest of the tiles from his winning hand are still fanned out in front of him on the table, undisturbed, as though he simply stopped playing mid-game and never picked it back up.{/i}"
    show louis confused at speaker_focus(xalign=0.5)
    l "Shunyu? Shunyu!! Hey, wake up. C’mon, this isn’t f- oh god, is that- is that GLASS{w=2}"
    "{i}Louis stumbles back, knocking into a barstool.{/i}"
    $ c2_p2_found_body = True
    jump c2_p2_dorothy_arrives

label c2_p2_dorothy_arrives:
    show dorothy neutral at speaker_focus(xalign=0.9)
    show louis confused at speaker_background(xalign=0.1)
    d "Sir, is something the—{w=2}"
    "{i}She sees the body.{/i}"
    d "...Oh...{w=2}"
    show dorothy neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Dorothy, please, get help… get Agatha, get anyone…{w=2}"
    d "R-right. Right! Stay here, don't— don't touch anything else.{w=2}"
    "{i}She hurries out, nearly tripping over her own ticket punch on the way.{/i}"
    jump c2_p2_fedora_arrives

label c2_p2_fedora_arrives:
    show fedora neutral at speaker_focus(xalign=0.9)
    f "I heard shouting, is there a STORY here-{w=2}"
    "{i}She stops dead when she sees the body.{/i}"
    f "...Oh.{w=2}"
    l "Fedora, thank god, please, you have to help me…{w=2}"
    f "{i}(quiet, unusually so){/i} I told you to watch out.{w=2}"
    show fedora neutral at speaker_background(xalign=0.9)
    show louis confused at speaker_focus(xalign=0.1)
    l "What?? You knew this would-{w=2}"
    f "I said I CAN’T WAIT to interview the killer. I didn’t say I knew who they were.{w=2}"
    "{i}She kneels by the body, professional mask sliding back over her face, though her hands are shaking slightly as she jots something down.{/i}"
    f "Tile placed in the palm. No struggle, far as I can tell. And that glass — that’s not from a weapon someone brought with them. That’s from HERE. Whoever did this either knew him, or he never saw them as a threat at all — well, not until it was already too late.{w=2}"
    l "How are you so calm about this?{w=2}"
    f "I’m not. I just know how to look calm. Comes with the job.{w=2}"
    l "I need to find out what happened. Someone on this train did this.{w=2}"
    jump c2_p2_investigation_menu

label c2_p2_investigation_menu:
    menu:
        "What should Louis do?"
        "Search the crime scene for clues":
            show louis neutral at speaker_focus(xalign=0.1)
            "{i}Louis crouches by the table. Aside from the tile in Shunyu’s hand, everything else looks staged to look untouched — his winning hand still fanned out, his drink still full and condensating like it was poured recently.{/i}"
            l "Someone wanted this to look like he just... stopped playing. But why leave the tile in his hand at all? Why not just walk away clean?{w=2}"
            f "Careful. Killers who leave signatures aren't hiding. They're telling you something.{w=2}"
        "Wait for Dorothy to return with Agatha":
            show louis neutral at speaker_focus(xalign=0.1)
            l "She went to get Agatha already… I should stay in case anything else happens.{w=2}"
            f "Smart. Don't touch the body more than you already have, by the way.{w=2}"
            l "I… right. Sorry.{w=2}"
        "Ask Fedora what she knows":
            l "You said ‘killer’ back at the start. Not an ‘accident.’ How'd you know?{w=2}"
            f "I didn't. Not for certain. But this train doesn't reset for nothing, matchstick. Something on here needed a body to make it real.{w=2}"
            l "Needed? What does that mean?{w=2}"
            f "...I don't know yet. That's the story I'm here to find.{w=2}"

    jump c2_p2_agatha_arrives

label c2_p2_agatha_arrives:
    show agatha neutral at speaker_focus(xalign=0.9)
    "{i}Agatha arrives, Dorothy and Ichora trailing behind her, Dorothy's face pale with dread while Ichora's is one of confusion.{/i}"
    a "Move.{w=2}"
    "{i}She examines the body with clinical speed: pulse, pupils, the tile in his hand.{/i}"
    a "Dead maybe twenty, thirty minutes. A single puncture wound, glass shard still lodged in it, went in at an upward angle, deep. Whoever did this either got lucky or knew exactly where to aim.{w=2}"
    show agatha neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "The blood by the bar counter, that's—{w=2}"
    a "Doesn't match where he's sitting. Not enough of it here, too much of it there. He didn't die in this chair. He moved here after.{w=2}"
    l "Someone stabbed him at the bar, and then... carried him over? Sat him down? Why?{w=2}"
    a "That's the part that isn't my job to answer.{w=2}"

    "{i}Fedora scribbles furiously.{/i}"
    show fedora neutral at speaker_focus(xalign=0.9)
    show agatha neutral at speaker_background(xalign=0.5)
    show louis neutral at speaker_background(xalign=0.1)
    f "Now THAT'S a headline.{w=2}"
    a "This isn't a story, reporter. This is a body.{w=2}"
    f "Everything's a story if you wait long enough.{w=2}"
    l "...Moved here. So whoever did this had time. Strength. And a reason to want him found exactly like this.{w=2}"
    l "I need to find out who was in this carriage. Everyone.{w=2}"
    call screen carriage_2_part2_investigation_map

label c2_p2_reinterview_eduard:
    show eduard neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Eduard. I need you to actually talk to me this time.{w=2}"
    "{i}Eduard blinks, and for a moment seems more present than before.{/i}"
    ed "...He's dead? Shunyu's… oh, hell. Hell, hell, hell.{w=2}"
    l "Where were you the last half hour?{w=2}"
    ed "Behind the bar! Where else would I be? I don't leave this counter during service, ask anyone.{w=2}"
    l "Anyone like who?{w=2}"
    "{i}Eduard hesitates.{/i}"
    ed "...I mean, no one else was really around. It's been quiet. Too quiet, actually, now that I think of it.{w=2}"
    l "Did you see the tile in his hand before? While he was playing?{w=2}"
    ed "No, no way. That's not even from his hand. He had three of the dragon tiles laid out, not that one. Someone put that there after.{w=2}"
    l "How do you know his hand that well?{w=2}"
    ed "Man complained about his own wins loud enough for the whole carriage to hear, all night, every night. Hard NOT to know it.{w=2}"
    $ c2_p2_reinterviewed_eduard = True
    return

label c2_p2_reinterview_agatha:
    show agatha neutral at speaker_focus(xalign=0.9)
    "{i}Louis finds Agatha packing up her kit after finishing with the body.{/i}"
    l "Can I ask you something?{w=2}"
    a "You're going to, whether I say yes or not. Go on.{w=2}"
    l "You said he was moved. Moved by who?{w=2}"
    a "That's your job to find out, not mine. I deal with bodies, not motives.{w=2}"
    l "Were you even in this carriage earlier tonight?{w=2}"
    "{i}Agatha stops packing for a second.{/i}"
    a "I was in the staff cabin. Had a passenger complaint to deal with. If you want an alibi, ask the idiot who pricked his finger and cried about it — he'll remember me being there.{w=2}"
    l "I wasn't accusing you though…{w=2}"
    a "You were thinking about it. Everyone thinks about it, when someone ends up dead and a woman happens to know exactly how. Ask your questions, matchstick. Just don't waste my time doing it.{w=2}"
    $ c2_p2_reinterviewed_agatha = True
    return

label part2_chapter_end:
    $ achievement.grant("closer_to_the_truth")
    show louis neutral at speaker_focus(xalign=0.5)
    l "A tile that doesn't belong to the hand. A body moved after death. Barely anyone with a solid alibi for the last half hour.{w=2}"
    l "This isn't just going to be about finding who was angry at him. Someone wanted this scene in a very specific way.{w=2}"
    l "...I don't think I'm getting off this train until I find out why.{w=2}"
    scene black with dissolve
    centered "{i}ryan start here{/i}"
    return