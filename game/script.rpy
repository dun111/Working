define d   = C("Dorothy",   "dorothy",   "#4a4f5c")
define l   = C("Louis",     "louis",     "#5a2a7a")
define f   = C("Fedora",    "fedora",    "#2f5a3a")
define ed  = C("Eduard",    "eduard",    "#6a4628")
define s   = C("Shunyu",    "shunyu",    "#4a3a7a")
define k   = C("Kimmy",     "kimmy",     "#8a2a36")
define h   = C("Himmel",    "himmel",    "#2a4a6a")
define seb = C("Sebastian", "sebastian", "#3a3f46")
define mi  = C("Misha",     "misha",     "#3a5a3a")
define a   = C("Agatha",    "agatha",    "#2a5a5a")
define ic  = C("Ichora",    "ichora",    "#7a5a22")
define p   = C("Pattison",  "pattison",  "#5a3a6a")
define al  = C("Alexander", "alexander", "#6a6a22")
define pas = C("Passenger")
define gam = C("Other Gambler")
define u   = C("???", plate="#3a0a0a", creepy=True)

define shunyu_monster    = C("The Passenger",  "shunyu_monster",    "#5a0a0a", creepy=True)
define himmel_monster    = C("The Gentleman",  "himmel_monster",    "#5a0a0a", creepy=True)
define conductor_monster = C("The Conductor",  "conductor_monster", "#5a0a0a", creepy=True)

define pct = "%"

default in_loop = False
default visited_carriages = []

default c1_talked_fedora = False

default c2_talked_eduard = False
default c2_talked_shunyu = False
default has_maple_sugar = False
default drank = False
default played_mahjong = False

default c3_talked_kimmy = False
default c3_talked_himmel = False
default c3_talked_sebastian = False
default c3_talked_misha = False
default c3_kimmy_dangerous_choice = False

default c4_talked_agatha = False
default c4_talked_ichora = False
default has_key = False

default c5_talked_pattison = False
default c5_talked_alexander = False

default c2_p2_found_body = False
default c2_p2_reinterviewed_eduard = False
default c2_p2_reinterviewed_agatha = False

default clue_tile_mismatch = False
default clue_body_moved = False
default clue_alexander_alibi = False
default clue_hidden_tile = False
default c3_p2_returned = False
default clue_drug_wrapper = False

default kimmy_reinterviewed = False
default himmel_reinterviewed = False
default alexander_reinterviewed = False
default pattison_reinterviewed = False
default sebastian_reinterviewed = False
default misha_reinterviewed = False

default c6_q1_correct = False
default c6_q2_correct = False
default c6_q3_correct = False

default door_c2_open = False
default door_c4_open = False


screen carriage_1_map():
    add "bg carriage_1"
    use golden_ticket("c1", 420, 840)
    if in_loop or not c1_talked_fedora:
        use hs((1185, 625, 125, 180), Call("c1_fedora_dialogue"), "Fedora", "talk")
    use hs((860, 240, 200, 150), Call("c1_interact_window"), "Window", delay=0.05)
    use hs((30, 740, 110, 110), Call("c1_interact_cupboard"), "Cupboard", delay=0.1)
    use hs((30, 560, 110, 130), Call("c1_interact_mysterious_door"), "Mysterious door", delay=0.15)
    use hs((560, 600, 160, 90), Call("c1_interact_tea_stain"), "Tea stain", delay=0.2)
    if in_loop or c1_talked_fedora:
        use hs(DOOR_RIGHT, Jump("c1_door_to_carriage_2"), "Carriage 2", "door", 0.25)

screen carriage_2_map():
    add "bg carriage_2"
    use golden_ticket("c2", 1760, 880)
    use hs(DOOR_LEFT, Jump("carriage_1_hub"), "Carriage 1", "back")
    if not c2_talked_eduard:
        use hs((1430, 355, 140, 150), Call("c2_eduard_dialogue"), "Eduard", "talk")
    if not c2_talked_shunyu:
        use hs((440, 550, 130, 170), Call("c2_shunyu_dialogue"), "Shunyu", "talk", 0.05)
    use hs((555, 235, 225, 165), Call("c2_interact_window"), "Window", delay=0.1)
    use hs((1000, 460, 100, 110), Call("c2_interact_broken_glass"), "Broken glass", delay=0.15)
    if c2_talked_eduard and c2_talked_shunyu:
        use hs(DOOR_RIGHT, Jump("carriage_3_start"), "Carriage 3", "door", 0.2)

screen carriage_3_map():
    add "bg carriage_3"
    use golden_ticket("c3", 1820, 300)
    use hs(DOOR_LEFT, Jump("carriage_2_hub"), "Carriage 2", "back")
    if not c3_talked_kimmy:
        use hs((100, 150, 180, 400), Call("c3_kimmy_dialogue"), "Kimmy", "talk")
    if not c3_talked_himmel:
        use hs((350, 150, 180, 400), Call("c3_himmel_dialogue"), "Himmel", "talk", 0.05)
    if not c3_talked_sebastian:
        use hs((600, 150, 180, 400), Call("c3_sebastian_dialogue"), "Sebastian", "talk", 0.1)
    if not c3_talked_misha:
        use hs((850, 150, 180, 400), Call("c3_misha_dialogue"), "Misha", "talk", 0.15)
    use hs((950, 620, 160, 160), Call("c3_interact_empty_room"), "Empty room", delay=0.2)
    use hs((1150, 620, 160, 160), Call("c3_interact_carpet"), "Carpet", delay=0.25)
    use hs((1350, 620, 160, 160), Call("c3_interact_toys"), "Toys", delay=0.3)
    use hs((1550, 620, 160, 160), Call("c3_interact_luggage"), "Luggage", delay=0.35)
    if c3_talked_kimmy and c3_talked_himmel and c3_talked_sebastian and c3_talked_misha:
        use hs(DOOR_RIGHT, Jump("carriage_4_start"), "Carriage 4", "door", 0.4)

screen carriage_4_map():
    add "bg carriage_4"
    use golden_ticket("c4", 420, 860)
    use hs(DOOR_LEFT, Jump("carriage_3_hub"), "Carriage 3", "back")
    if not c4_talked_agatha:
        use hs((250, 150, 220, 400), Call("c4_agatha_dialogue"), "Agatha", "talk")
    if not c4_talked_ichora:
        use hs((700, 150, 220, 400), Call("c4_ichora_dialogue"), "Ichora", "talk", 0.05)
    use hs((950, 620, 160, 160), Call("c4_interact_syringe"), "Syringe", delay=0.1)
    if c4_talked_agatha and c4_talked_ichora:
        use hs(DOOR_RIGHT, Jump("carriage_5_start"), "Carriage 5", "door", 0.15)

screen carriage_5_map():
    add "bg carriage_5"
    use golden_ticket("c5", 1700, 560)
    use hs(DOOR_LEFT, Jump("carriage_4_hub"), "Carriage 4", "back")
    if not c5_talked_pattison:
        use hs((200, 345, 125, 205), Call("c5_pattison_dialogue"), "Pattison", "talk")
    if not c5_talked_alexander:
        use hs((1080, 645, 125, 165), Call("c5_alexander_dialogue"), "Alexander", "talk", 0.05)
    use hs((120, 640, 360, 200), Call("c5_interact_mail_room"), "Mail", delay=0.1)
    use hs((920, 470, 500, 170), Call("c5_interact_luggage_room"), "Luggage room", delay=0.15)
    use hs((1455, 344, 330, 166), Call("c5_interact_engine"), "Engine", delay=0.2)
    if c5_talked_pattison and c5_talked_alexander:
        use hs(DOOR_RIGHT, Jump("c5_carriage6_door"), "Carriage 6", "door", 0.25)


screen carriage_2_part2_map():
    add "bg carriage_2"
    use golden_ticket("c2b", 230, 900)
    use hs((100, 150, 180, 400), Call("c2_p2_interact_window"), "Window")
    use hs((350, 150, 180, 400), Call("c2_p2_talk_eduard"), "Eduard", "talk", 0.05)
    use hs((600, 150, 180, 400), Call("c2_p2_overturned_table"), "Overturned table", delay=0.1)
    use hs((850, 150, 180, 400), Call("c2_p2_broken_glass"), "Broken glass", delay=0.15)
    use hs((1100, 150, 180, 400), Call("c2_p2_bar_counter"), "Bar counter", delay=0.2)
    use hs((1350, 150, 180, 400), Jump("c2_p2_second_table"), "Second table", delay=0.25)

screen carriage_2_part2_investigation_map():
    add "bg carriage_2"
    if not c2_p2_reinterviewed_eduard:
        use hs((350, 150, 200, 400), Call("c2_p2_reinterview_eduard"), "Eduard", "talk")
    if not c2_p2_reinterviewed_agatha:
        use hs((600, 150, 200, 400), Call("c2_p2_reinterview_agatha"), "Agatha", "talk", 0.05)
    if c2_p2_reinterviewed_eduard and c2_p2_reinterviewed_agatha:
        use hs(DOOR_RIGHT, Jump("part2_chapter_end"), "Carriage 3", "door", 0.1)

screen carriage_2_part2_after_map():
    add "bg carriage_2"
    use hs(DOOR_RIGHT, Jump("carriage_3_part2_hub"), "Carriage 3", "door")

screen carriage_3_part2_map():
    add "bg carriage_3"
    use golden_ticket("c3b", 1500, 120)
    use hs(DOOR_LEFT, Jump("carriage_2_part2_return"), "Carriage 2", "back")

    # Script order: luggage and Kimmy first, then the mail room (Carriage 5), then
    # back here for the carpet, Sebastian and Misha, then the decision.
    if clue_drug_wrapper and not kimmy_reinterviewed:
        use hs((100, 150, 180, 400), Call("c3_p2_kimmy_reinterview"), "Kimmy", "talk")
    if clue_drug_wrapper and not himmel_reinterviewed:
        use hs((350, 150, 180, 400), Call("c3_p2_himmel_reinterview"), "Himmel", "talk", 0.05)

    if clue_hidden_tile and not sebastian_reinterviewed:
        use hs((600, 150, 180, 400), Call("c3_p2_sebastian_reinterview"), "Sebastian", "talk", 0.1)
    if clue_hidden_tile and not misha_reinterviewed:
        use hs((850, 150, 180, 400), Call("c3_p2_misha_reinterview"), "Misha", "talk", 0.15)

    if clue_alexander_alibi:
        use hs((1150, 620, 160, 160), Call("c3_p2_interact_carpet"), "Carpet", delay=0.2)
    use hs((1350, 620, 160, 160), Call("c3_p2_interact_toys"), "Toys", delay=0.25)
    use hs((1550, 620, 160, 160), Call("c3_p2_interact_luggage"), "Luggage", delay=0.3)

    if kimmy_reinterviewed and not clue_alexander_alibi:
        use hs(DOOR_RIGHT, Jump("carriage_5_part2_start"), "Carriage 5", "door", 0.35)
    if sebastian_reinterviewed and misha_reinterviewed:
        use hs((1400, 200, 150, 400), Jump("accusation_scene"), "Time to decide", "decide", 0.1)

screen carriage_5_part2_map():
    add "bg carriage_5"
    use golden_ticket("c5b", 90, 200)
    use hs(DOOR_LEFT, Jump("carriage_3_part2_return" if clue_alexander_alibi else "carriage_3_part2_hub"), "Carriage 3", "back")
    if not alexander_reinterviewed:
        use hs((1080, 645, 125, 165), Call("c5_p2_alexander_dialogue"), "Alexander", "talk")
    if alexander_reinterviewed and not pattison_reinterviewed:
        use hs((200, 345, 125, 205), Call("c5_p2_pattison_dialogue"), "Pattison", "talk")


label start:
    $ menu_music_filter_off()
    if not persistent.tutorial_seen:
        scene black
        call screen tutorial_first
        # Reading the tutorial shouldn't use up hardcore time.
        $ hc = HardcoreClock(persistent.hardcore)

    $ in_loop = False
    scene Train station
    $ achievement.grant("first_departure")

    show dorothy happy at speaker_focus(xalign=0.9)
    d "{i}(distant voice){/i} Thank you for boarding the Grekhov Express."
    "{i}Louis wakes up violently to the sound of train tracks.{/i}"
    show dorothy happy at speaker_background(xalign=0.9)
    show louis confused at speaker_focus(xalign=0.1)
    l "Eugh… augh… guhhh… I feel the ground underneath me moving, and hear the sound of… chugging?"
    "{i}(Chugging){/i}"
    "{i}He opens his eyes.{/i}"
    l "“Wh-where am I?”"
    "{i}He looks around, and sees a ticket woman.{/i}"
    show louis confused at speaker_background(xalign=0.1)
    show dorothy confused at speaker_focus(xalign=0.9)
    d "Excuse me sir, tickets please."
    show dorothy confused at speaker_background(xalign=0.9)
    l "Excuse me miss, do you know where we are?"
    show louis confused at speaker_background(xalign=0.1)
    d "Hah… {i}(I'm not paid enough for this){/i}"
    d "Are you fine… sir?"
    show dorothy confused at speaker_background(xalign=0.9)
    show louis looking_around at speaker_focus(xalign=0.1)
    "{i}Louis feels something in his pocket, looks down and sees a ticket.{/i}"
    l "{i}(brain freeze){/i} Uh… uh… yes, the ticket. I think it's somewhere here…"
    call play_required("mg_ticket", ticket_reset) from _call_play_required
    "{i}He pulls the ticket out of his pocket.{/i}"
    show louis confused at speaker_focus(xalign=0.1)
    l "Miss, what line is this?"
    show louis confused at speaker_background(xalign=0.1)
    show dorothy surprised at speaker_focus(xalign=0.9)
    d "The Grekhov Express? Are you ill? Everyone knows that, why else would you be on this train?"
    show dorothy surprised at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "O-oh, sorry, I think I might have gotten a bit light headed…"
    show louis neutral at speaker_background(xalign=0.1)
    show dorothy neutral at speaker_focus(xalign=0.9)
    d "I see. Well sir, welcome aboard the Grekhov Express…"
    show dorothy neutral at speaker_background(xalign=0.9)
    show louis confused at speaker_focus(xalign=0.1)
    l "Huh, I don't remember how I got here… That's right, I was tryna go home… But… what happened?"
    l "I'm gonna look around."
    jump old_film_to_map


label carriage_1_start:
    $ autosave_checkpoint()
    jump carriage_1_hub

label carriage_1_hub:
    scene bg carriage_1
    call screen carriage_1_map
    jump carriage_1_hub

label c1_fedora_dialogue:
    scene talk to fedora with talk_in
    if in_loop:
        show louis neutral at speaker_focus(xalign=0.1)
        l "Uh, excuse me miss?"
        show louis neutral at speaker_background(xalign=0.1)
        show fedora neutral at speaker_focus(xalign=0.9)
        f "Why Hello There, are you ready for the CALAMITY?"
        l "Calamity?"
        f "I boarded this train to speak to the conductor after we arrived in Grekhov, I heard CALAMITY will open up once we reach there. It'll rack NUMBERS for the steamboat. I CAN'T WAIT to interview the KILLER."
        l "Killer?"
        f "Well, it's been LOVELY talking to you, but my editor Twinkles is calling me. WATCH OUT."
        l "OKAY…. or what?"
    else:
        show louis neutral at speaker_focus(xalign=0.1)
        l "Uh, excuse me miss?"
        show louis neutral at speaker_background(xalign=0.1)
        show fedora neutral at speaker_focus(xalign=0.9)
        f "Why Hello There! Whaddaya need?"
        l "I was wondering, what are you planning to find on this line?"
        f "I boarded this train to speak to the conductor after we arrive in Grekhov, I heard a case will open up once we reach there. It'll rack NUMBERS for the steamboat. I CAN'T WAIT to interview the conductor!"
        l "Why… the conducto-"
        f "Well, it's been LOVELY talking to you, but my editor Twinkles is calling me. Toodooloo!"
        l "Uh, ok I suppose."
    $ c1_talked_fedora = True
    return

label c1_interact_window:
    show screen window_view
    "What a beautiful sight outside! You can see everything from this train!"
    hide screen window_view with dissolve
    return


label c1_interact_mysterious_door:
    if has_pass("door_key"):
        call screen mysterious_room
        return
    "I'm not supposed to enter this carriage, am I…"
    return

label c1_interact_tea_stain:
    if in_loop:
        show louis confused at speaker_focus(xalign=0.5)
        l "W-why does it smell… like iron?"
    else:
        "Ooh, I thought this was blood for a second…"
    return

label c1_door_to_carriage_2:
    if not in_loop and not door_c2_open:
        $ dr_bg = "bg carriage_1"
        call play_required("mg_door", door_reset) from _call_play_required_1
        $ door_c2_open = True
    show louis neutral at speaker_focus(xalign=0.5)
    if in_loop:
        l "...It's quiet. Way too quiet."
        jump carriage_2_part2_start
    else:
        l "Oh, this place is quite fancy. Is it like some sort of restaurant?"
        jump carriage_2_start


label carriage_2_start:
    if "c2" not in visited_carriages:
        $ visited_carriages.append("c2")
        $ achievement.grant("carriage_1_complete")
        $ autosave_checkpoint()
        show screen map_stamp(_("CARRIAGE 2"), _("THE LOUNGE"))
    jump carriage_2_hub

label carriage_2_hub:
    scene bg carriage_2
    call screen carriage_2_map
    jump carriage_2_hub

label c2_eduard_dialogue:
    scene talk to eduard with talk_in
    show eduard neutral at speaker_focus(xalign=0.9)
    ed "Good evening lad, I'm Eduard, your bartender. Wouldya like some drinks?"
    menu:
        "Would you like a drink?"
        "Yes":
            $ drank = True
            show eduard neutral at speaker_background(xalign=0.9)
            show louis neutral at speaker_focus(xalign=0.1)
            l "Sure."
            ed "Awh shucks, seems we just ran out! That gambler's been drinking since he got here!"
            l "Wow…"
        "No":
            $ drank = False
            show eduard neutral at speaker_background(xalign=0.9)
            show louis neutral at speaker_focus(xalign=0.1)
            l "Uh, it's okay… I'm not really thirsty right now."
            ed "All the better for me, I reckon. That mahjong monster almost got me out of whiskey! He better win quick, before his tab gets as large as his confidence."
    $ c2_talked_eduard = True
    return

label c2_shunyu_dialogue:
    scene talk to shunyu with talk_in
    show shunyu neutral at speaker_focus(xalign=0.9)
    s "Yes! I can't stop winning!"
    show shunyu neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Uhm… whatcha doin'?"
    show louis neutral at speaker_background(xalign=0.1)
    s "Playing Mahjong! Doncha just love winning!"
    "{i}Louis watches Shunyu pick up a tile.{/i}"
    show shunyu excited at speaker_focus(xalign=0.9)
    s "JACKKKPOTTTTTTT!"
    show shunyu excited at speaker_background(xalign=0.9)
    l "R-right, well, I'll leave you-"
    show louis neutral at speaker_background(xalign=0.1)
    show shunyu neutral at speaker_focus(xalign=0.9)
    menu:
        s "Wanna play? Think about it. You can only lose 100[pct], but you can win 100000[pct]! Look at the odds!"
        "Yes":
            $ achievement.grant("high_roller")
            $ mahjong_reset()
            $ renpy.block_rollback()
            call screen mahjong_minigame
            if _return == "win":
                show shunyu excited at speaker_focus(xalign=0.9)
                s "JACKKKPOTTTTTTT! You win $2! Look at that, beginner's luck!"
                $ played_mahjong = "won"
            else:
                show shunyu neutral at speaker_focus(xalign=0.9)
                s "Aw, shoot. Unlucky draw! Better luck next time, alright?"
                $ played_mahjong = "lost"
        "No":
            $ played_mahjong = False
            show louis neutral at speaker_focus(xalign=0.1)
            l "I'm okay, don't have much to gamble with anyway."
    $ c2_talked_shunyu = True
    return

label c2_interact_window:
    $ window_looks += 1
    if window_looks == 5:
        $ secret_found("window", "window")
    show screen window_view
    "What a beautiful sight outside! You can see everything from this train!"
    hide screen window_view with dissolve
    return


label carriage_3_start:
    if "c3" not in visited_carriages:
        $ visited_carriages.append("c3")
        $ achievement.grant("carriage_2_complete")
        $ autosave_checkpoint()
        l "Shh… Looks like I better be quiet."
        show screen map_stamp(_("CARRIAGE 3"), _("SLEEPER CABINS"))
    jump carriage_3_hub

label carriage_3_hub:
    scene bg carriage_3
    call screen carriage_3_map
    jump carriage_3_hub

label c3_kimmy_dialogue:
    scene talk to kimmy with talk_in
    show kimmy neutral at speaker_focus(xalign=0.5)
    k "Yawns… Hello, are you room service?"
    show kimmy neutral at speaker_background(xalign=0.5)
    show louis neutral at speaker_focus(xalign=0.1)
    l "N-no, my name is Louis… Nice to meet you."
    show louis neutral at speaker_background(xalign=0.1)
    show himmel neutral at speaker_focus(xalign=0.9)
    h "O-oh my god dear! Why is there a STRANGER here! I-I might faint!"
    show himmel neutral at speaker_background(xalign=0.9)
    k "Don't worry Sugar, he's not dangerous… I think."
    show kimmy neutral at speaker_background(xalign=0.5)
    menu:
        "I AM dangerous.":
            $ c3_kimmy_dangerous_choice = True
            show louis neutral at speaker_focus(xalign=0.1)
            l "Actually… I might be dangerous."
            show louis neutral at speaker_background(xalign=0.1)
            show kimmy neutral at speaker_focus(xalign=0.5)
            k "With THAT frame… I don't think so, sweetie."
        "I am NOT dangerous.":
            $ c3_kimmy_dangerous_choice = False
            show louis neutral at speaker_focus(xalign=0.1)
            l "I'm really not dangerous."
            show louis neutral at speaker_background(xalign=0.1)
            show kimmy neutral at speaker_focus(xalign=0.5)
            k "Yeah, it's kinda obvious, matchstick."
    show kimmy neutral at speaker_background(xalign=0.5)
    l "Wow damn… So… Expensive cabin, huh?"
    show louis neutral at speaker_background(xalign=0.1)
    k "Well of course! My family has a clock business, so we're quite well off."
    show kimmy neutral at speaker_background(xalign=0.5)
    l "So what is such an important lady doing on a train like this?"
    show louis neutral at speaker_background(xalign=0.1)
    k "Oh, I have a meeting in █████████, and I wanted to make it a trip so I could spend more time with my darling, Himmel. Right, Sugar?"
    show kimmy neutral at speaker_background(xalign=0.5)
    show himmel neutral at speaker_focus(xalign=0.9)
    h "Of course!"
    show himmel neutral at speaker_background(xalign=0.9)
    l "Wow… such love birds."
    $ c3_talked_kimmy = True
    return

label c3_himmel_dialogue:
    scene talk to himmel with talk_in
    show himmel neutral at speaker_focus(xalign=0.9)
    h "W-what do you want, stranger?"
    show himmel neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Nothing, just uh… finding my way to the bathroom."
    h "It's to the left! Now leave me alone!"
    l "Holy moly, what's that guy's problem…"
    $ c3_talked_himmel = True
    return

label c3_sebastian_dialogue:
    scene talk to sebastian with talk_in
    show sebastian neutral at speaker_focus(xalign=0.9)
    seb "May I know your name, sir?"
    show sebastian neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Oh! It's Louis."
    seb "Good evening, Mr. Louis. My name is Sebastian, the butler for Mr. Popov, the child in this cabin. If you wish to enter, I will warn you, that if any harm or distress befalls the child, you will be prosecuted."
    l "Wow… Don't worry Sir, I won't."
    $ c3_talked_sebastian = True
    return

label c3_misha_dialogue:
    scene talk to misha with talk_in
    show misha neutral at speaker_background(xalign=0.9)
    "{i}Misha hums, playing with blocks. He looks up. Staring.{/i}"
    show louis neutral at speaker_focus(xalign=0.1)
    l "Hey buddy…"
    show louis neutral at speaker_background(xalign=0.1)
    show misha stares at speaker_focus(xalign=0.9)
    "{i}Misha stares, no response.{/i}"
    $ c3_talked_misha = True
    return

label c3_interact_empty_room:
    "Wow, so spacious! These must cost a lot."
    return

label c3_interact_carpet:
    "Why is it sticking up like that?"
    return


label c3_interact_luggage:
    "So much luggage… Do they really need this much for a worktrip?"
    return


label carriage_4_start:
    if not door_c4_open:
        $ dr_bg = "bg carriage_3"
        call play_required("mg_door", door_reset) from _call_play_required_3
        $ door_c4_open = True
    if "c4" not in visited_carriages:
        $ visited_carriages.append("c4")
        $ achievement.grant("carriage_3_complete")
        $ autosave_checkpoint()
        show screen map_stamp(_("CARRIAGE 4"), _("STAFF CART"))
    jump carriage_4_hub

label carriage_4_hub:
    scene bg carriage_4
    call screen carriage_4_map
    jump carriage_4_hub

label c4_agatha_dialogue:
    scene talk to agatha with talk_in
    show agatha neutral at speaker_focus(xalign=0.9)
    a "C'mon, put the bandage on."
    pas "Ouuuchhh it hurtssss oh my my poor finger, I may never play Marvel Rivals again!"
    a "I don't care. You pricked it, it's not bleeding. Put the bandaid on and stop wasting my time."
    pas "Fine."
    "{i}The passenger pouts for a second and storms off.{/i}"
    a "Actual infants…"
    "{i}Agatha looks at you.{/i}"
    a "What, need help too?"
    show agatha neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "No, but, what's this carriage?"
    show louis neutral at speaker_background(xalign=0.1)
    a "If you use your eyes, you can see it's the staff cart. Now, are you injured, or can I go back to my peace?"
    show agatha neutral at speaker_background(xalign=0.9)
    l "I'm… fine."
    $ c4_talked_agatha = True
    return

label c4_ichora_dialogue:
    scene talk to ichora with talk_in
    show ichora neutral at speaker_focus(xalign=0.9)
    ic "Hey! I've been waiting for ya, buddy!"
    show ichora neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "You have…?"
    show louis neutral at speaker_background(xalign=0.1)
    ic "Of course! Welcome to the train. The name's Ichora, I'm the train's engineer."
    show ichora neutral at speaker_background(xalign=0.9)
    l "My name's Louis."
    show louis neutral at speaker_background(xalign=0.1)
    ic "Oh, I know."
    show ichora neutral at speaker_background(xalign=0.9)
    l "How-"
    show louis neutral at speaker_background(xalign=0.1)
    ic "We've been waiting for you a while. Anyways, I got a gift for ya! Come with me!"
    scene engine room with dissolve
    show ichora neutral at speaker_focus(xalign=0.9)
    "{i}Ichora gives you a key.{/i}"
    ic "Here ya go!"
    show ichora neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "But what's it for?"
    show louis neutral at speaker_background(xalign=0.1)
    ic "Sometimes, life gets hard, and a door is presented to escape. But we're too scared to use the key. Don't hesitate."
    "{i}Ichora winks and walks off.{/i}"
    $ has_key = True
    $ achievement.grant("key_holder")
    $ got_item(_("Ichora's Key"), _("\"Don't hesitate.\""))
    $ c4_talked_ichora = True
    return

label c4_interact_syringe:
    "That looks sharp."
    return


label carriage_5_start:
    if "c5" not in visited_carriages:
        $ visited_carriages.append("c5")
        $ achievement.grant("carriage_4_complete")
        $ autosave_checkpoint()
        show louis neutral at speaker_focus(xalign=0.5)
        l "A lot is going on here, huh."
        show screen map_stamp(_("CARRIAGE 5"), _("THE MAIL ROOM"))
    jump carriage_5_hub

label carriage_5_hub:
    scene bg carriage_5
    call screen carriage_5_map
    jump carriage_5_hub

label c5_pattison_dialogue:
    scene talk to pattison with talk_in
    show pattison neutral at speaker_focus(xalign=0.9)
    p "This goes to the clock, while this goes to the end. This goes to the fake ones and this goes to the friend."
    show pattison neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "U-uhm… what?"
    show louis neutral at speaker_background(xalign=0.1)
    p "Hello Sir, you another mailworker?"
    show pattison neutral at speaker_background(xalign=0.9)
    l "No."
    l "I don't even know anybody on this express."
    show louis neutral at speaker_background(xalign=0.1)
    p "It's okay, you will before the end."
    show pattison neutral at speaker_background(xalign=0.9)
    l "What end?"
    "{i}Pattison stares at you blankly.{/i}"
    $ c5_talked_pattison = True
    return

label c5_alexander_dialogue:
    scene talk to alexander with talk_in
    show alexander neutral at speaker_focus(xalign=0.9)
    al "Hahahaha… this stuff is so gooddddd…."
    show alexander neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "What you got there, buddy?"
    show louis neutral at speaker_background(xalign=0.1)
    al "The banned super maple sugar!!!"
    show alexander neutral at speaker_background(xalign=0.9)
    l "Damn… why's it banned?"
    show louis neutral at speaker_background(xalign=0.1)
    al "HAhaha… They tryna take the good stuff from us, don't want us having too much fun, haha…"
    show alexander neutral at speaker_background(xalign=0.9)
    l "Oh, I see."
    show louis neutral at speaker_background(xalign=0.1)
    al "Want some, buddy? First one is free, next one is 2000 perkels."
    menu:
        "Take the maple sugar?"
        "Yes":
            $ has_maple_sugar = True
            $ achievement.grant("forbidden_sweetness")
            show alexander neutral at speaker_background(xalign=0.9)
            show louis neutral at speaker_focus(xalign=0.1)
            l "Sure, I'll take some."
            show louis neutral at speaker_background(xalign=0.1)
            al "Attaboy! Here ya go - one satchel of pure happiness."
            $ got_item(_("Satchel of Maple Sugar"), _("\"First one is free, next one is 2000 perkels.\""))
        "No":
            $ has_maple_sugar = False
            show alexander neutral at speaker_background(xalign=0.9)
            show louis neutral at speaker_focus(xalign=0.1)
            l "I'm good. Thanks for the offer."
            show louis neutral at speaker_background(xalign=0.1)
            al "Suit yourself, brother."
    show alexander neutral at speaker_background(xalign=0.9)
    l "Has anyone else bought these things?"
    show louis neutral at speaker_background(xalign=0.1)
    al "Depends? Are you a narc?"
    show alexander neutral at speaker_background(xalign=0.9)
    l "No."
    show louis neutral at speaker_background(xalign=0.1)
    al "Well, there's this guy that keeps winning money from gambling, yet still hasn't paid for his last portion. Don't worry, I'll make him suffer."
    al "And as for the other one… the stuff was strong so I don't remember."
    show alexander neutral at speaker_background(xalign=0.9)
    l "Why did I expect that? But who's the other person?"
    "{i}Alexander looks at you blankly.{/i}"
    $ c5_talked_alexander = True
    return


label c5_interact_luggage_room:
    "Most of this is probably that couple's, I can't lie."
    return

label c5_carriage6_door:
    $ achievement.grant("carriage_5_complete")
    $ achievement.grant("eyes_in_the_dark")
    show louis confused at speaker_focus(xalign=0.5)
    l "Huh… it's…"
    scene black with dissolve
    u "Not yet! Try to see the truth before you see the future."
    "{i}Two pairs of eyes glint in the blackness, watching.{/i}"
    jump part2_start


label part2_start:
    $ achievement.grant("the_loop_begins")
    $ autosave_checkpoint()
    $ in_loop = True
    show screen loop_overlay
    scene Train station
    with Pause(0.3)
    show dorothy neutral at speaker_focus(xalign=0.9)
    d "{i}(distant voice){/i} Thank you for boarding the Grekhov Express."
    "{i}Louis wakes up violently to the sound of train tracks.{/i}"
    show dorothy neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Man… This seems familiar…"
    "{i}He opens his eyes.{/i}"
    l "“Here again?”"
    "{i}He looks around, and sees a ticket woman.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    show dorothy neutral at speaker_focus(xalign=0.9)
    d "Excuse me sir, tickets please."
    show dorothy neutral at speaker_background(xalign=0.9)
    show louis confused at speaker_focus(xalign=0.1)
    l "Didn't I already give you my ticket?"
    show louis confused at speaker_background(xalign=0.1)
    show dorothy neutral at speaker_focus(xalign=0.9)
    d "Are you fine… sir?"
    show dorothy neutral at speaker_background(xalign=0.9)
    show louis confused at speaker_focus(xalign=0.1)
    "{i}Louis feels something in his pocket, looks down and sees the ticket is still there. Now, it has a word on it: “DO OR DIE.”{/i}"
    l "Huh??"
    show louis confused at speaker_background(xalign=0.1)
    show dorothy neutral at speaker_focus(xalign=0.9)
    d "I see. Well sir, welcome aboard the Grekhov Express…"
    show dorothy neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "I'm… back at the start?"
    scene bg carriage_1 with dissolve
    show screen map_stamp(_("CARRIAGE 1"), _("HERE AGAIN?"))
    jump carriage_1_start


label carriage_2_part2_start:
    scene bg carriage_2 with dissolve
    "{i}Louis enters. The lights feel dimmer, creepier than before.{/i}"
    show screen map_stamp(_("CARRIAGE 2"), _("THE CRIME SCENE"))
    jump carriage_2_part2_hub

label carriage_2_part2_hub:
    scene bg carriage_2
    call screen carriage_2_part2_map
    jump carriage_2_part2_hub

label c2_p2_interact_window:
    show screen window_view(dark=True)
    "Huh… It's dark.."
    hide screen window_view with dissolve
    return

label c2_p2_talk_eduard:
    scene talk to eduard with talk_in
    show eduard neutral at speaker_focus(xalign=0.9)
    "{i}Eduard is standing behind the bar, unmoving, polishing the same glass over and over.{/i}"
    show eduard neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Uh… hey, you open?"
    show louis neutral at speaker_background(xalign=0.1)
    show eduard neutral at speaker_focus(xalign=0.9)
    ed "All the better for me, I reckon…"
    show eduard neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "...What?"
    show louis neutral at speaker_background(xalign=0.1)
    show eduard neutral at speaker_focus(xalign=0.9)
    ed "All the better for me, I reckon…"
    show eduard neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Are you okay, man?"
    "{i}Eduard stops polishing. He looks up. His eyes don't quite focus on Louis.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    ed "He better win quick. Before his tab gets as large as his confidence."
    show eduard neutral at speaker_background(xalign=0.9)
    l "Who? Eduard, who are you talking about-"
    "{i}Eduard goes back to polishing the glass. It was never dirty.{/i}"
    return

label c2_p2_overturned_table:
    "{i}There are mahjong tiles scattered on the floor beneath it. One of them is face down, pressed flat, like something heavy stood on it.{/i}"
    return

label c2_p2_broken_glass:
    show louis neutral at speaker_focus(xalign=0.5)
    l "This is the same glass from before… why hasn't anyone cleaned this up?"
    "{i}Louis notices a piece missing from the largest shard - snapped clean off, edges sharp.{/i}"
    u "Can yer shut up?"
    show louis confused at speaker_focus(xalign=0.5)
    l "H-hello?? Who said that…"
    "{i}No one is there.{/i}"
    return

label c2_p2_bar_counter:
    "{i}There's something dark pooling near the base of the counter, thin, creeping toward the tiles. Louis doesn't want to know what it is yet. He'll find out soon enough.{/i}"
    return

label c2_p2_second_table:
    show louis neutral at speaker_focus(xalign=0.5)
    "{i}Someone is slumped over the table.{/i}"
    l "...Hey. Hey, sir? You okay?"
    "{i}Louis reaches out and turns the figure over.{/i}"
    "{i}It's Shunyu.{/i}"
    show shunyu_dead with dissolve
    "{i}There's a jagged shard of glass buried in his side, dark red soaked deep into his shirt around it. His eyes are open. A mahjong tile is placed neatly in his open palm, resting there like it was set on purpose. The rest of the tiles from his winning hand are still fanned out in front of him on the table, undisturbed, as though he simply stopped playing mid-game and never picked it back up.{/i}"
    hide shunyu_dead with dissolve
    show louis confused at speaker_focus(xalign=0.5)
    l "Shunyu? Shunyu!! Hey, wake up. C'mon, this isn't f- oh god, is that- is that GLASS"
    "{i}Louis stumbles back, knocking into a barstool.{/i}"
    $ c2_p2_found_body = True
    "{i}The noise brings Dorothy in from the corridor, still holding her ticket punch out of habit.{/i}"
    jump c2_p2_dorothy_arrives

label c2_p2_dorothy_arrives:
    show dorothy neutral at speaker_focus(xalign=0.9)
    show louis confused at speaker_background(xalign=0.1)
    d "Sir, is something the-"
    "{i}She sees the body.{/i}"
    show dorothy sad at speaker_focus(xalign=0.9)
    d "...Oh..."
    show dorothy sad at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Dorothy, please, get help… get Agatha, get anyone…"
    show louis neutral at speaker_background(xalign=0.1)
    d "R-right. Right! Stay here, don't- don't touch anything else."
    "{i}She hurries out, nearly tripping over her own ticket punch on the way.{/i}"
    hide dorothy
    jump c2_p2_fedora_arrives

label c2_p2_fedora_arrives:
    "{i}Fedora bursts in moments later, notepad already out.{/i}"
    show fedora neutral at speaker_focus(xalign=0.9)
    f "I heard shouting, is there a STORY here-"
    "{i}She stops dead when she sees the body.{/i}"
    f "...Oh."
    show fedora neutral at speaker_background(xalign=0.9)
    show louis confused at speaker_focus(xalign=0.1)
    l "Fedora, thank god, please, you have to help me…"
    show louis confused at speaker_background(xalign=0.1)
    f "{i}(quiet, unusually so){/i} I told you to watch out."
    show fedora neutral at speaker_background(xalign=0.9)
    l "What?? You knew this would-"
    show louis confused at speaker_background(xalign=0.1)
    f "I said I CAN'T WAIT to interview the killer. I didn't say I knew who they were."
    "{i}She kneels by the body, professional mask sliding back over her face, though her hands are shaking slightly as she jots something down.{/i}"
    f "Tile placed in the palm. No struggle, far as I can tell. And that glass - that's not from a weapon someone brought with them. That's from HERE. Whoever did this either knew him, or he never saw them as a threat at all... well, not until it was already too late."
    show fedora neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "How are you so calm about this?"
    show louis neutral at speaker_background(xalign=0.1)
    f "I'm not. I just know how to look calm. Comes with the job."
    show fedora neutral at speaker_background(xalign=0.9)
    l "I need to find out what happened. Someone on this train did this."
    jump c2_p2_investigation_menu

label c2_p2_investigation_menu:
    menu:
        "What should Louis do?"
        "Search the crime scene for clues":
            show louis neutral at speaker_focus(xalign=0.1)
            "{i}Louis crouches by the table. Aside from the tile in Shunyu's hand, everything else looks staged to look untouched - his winning hand still fanned out, his drink still full and condensating like it was poured recently.{/i}"
            l "Someone wanted this to look like he just... stopped playing. But why leave the tile in his hand at all? Why not just walk away clean?"
            show louis neutral at speaker_background(xalign=0.1)
            show fedora neutral at speaker_focus(xalign=0.9)
            f "Careful. Killers who leave signatures aren't hiding. They're telling you something."
        "Wait for Dorothy to return with Agatha":
            show louis neutral at speaker_focus(xalign=0.1)
            l "She went to get Agatha already… I should stay in case anything else happens."
            show louis neutral at speaker_background(xalign=0.1)
            show fedora neutral at speaker_focus(xalign=0.9)
            f "Smart. Don't touch the body more than you already have, by the way."
            show fedora neutral at speaker_background(xalign=0.9)
            l "I… right. Sorry."
        "Ask Fedora what she knows":
            show louis neutral at speaker_focus(xalign=0.1)
            l "You said 'killer' back at the start. Not an 'accident.' How'd you know?"
            show louis neutral at speaker_background(xalign=0.1)
            show fedora neutral at speaker_focus(xalign=0.9)
            f "I didn't. Not for certain. But this train doesn't reset for nothing, matchstick. Something on here needed a body to make it real."
            show fedora neutral at speaker_background(xalign=0.9)
            l "Needed? What does that mean?"
            show louis neutral at speaker_background(xalign=0.1)
            f "...I don't know yet. That's the story I'm here to find."
    jump c2_p2_agatha_arrives

label c2_p2_agatha_arrives:
    show agatha neutral at speaker_focus(xalign=0.5)
    "{i}Agatha arrives, Dorothy and Ichora trailing behind her, Dorothy's face pale with dread while Ichora's is one of confusion.{/i}"
    a "Move."
    "{i}She examines the body with clinical speed: pulse, pupils, the tile in his hand.{/i}"
    a "Dead maybe twenty, thirty minutes. A single puncture wound, glass shard still lodged in it, went in at an upward angle, deep. Whoever did this either got lucky or knew exactly where to aim."
    show agatha neutral at speaker_background(xalign=0.5)
    show louis neutral at speaker_focus(xalign=0.1)
    l "The blood by the bar counter, that's-"
    show louis neutral at speaker_background(xalign=0.1)
    a "Doesn't match where he's sitting. Not enough of it here, too much of it there. He didn't die in this chair. He was moved here after."
    $ found_clue("clue_body_moved")
    show agatha neutral at speaker_background(xalign=0.5)
    l "Someone stabbed him at the bar, and then... carried him over? Sat him down? Why?"
    show louis neutral at speaker_background(xalign=0.1)
    a "That's the part that isn't my job to answer."
    show agatha neutral at speaker_background(xalign=0.5)
    "{i}Fedora scribbles furiously.{/i}"
    show fedora neutral at speaker_focus(xalign=0.9)
    f "Now THAT'S a headline."
    show fedora neutral at speaker_background(xalign=0.9)
    a "This isn't a story, reporter. This is a body."
    show agatha neutral at speaker_background(xalign=0.5)
    f "Everything's a story if you wait long enough."
    show fedora neutral at speaker_background(xalign=0.9)
    l "...Moved here. So whoever did this had time. Strength. And a reason to want him found exactly like this."
    l "I need to find out who was in this carriage. Everyone."
    hide agatha
    hide fedora
    jump c2_p2_investigation_hub

label c2_p2_investigation_hub:
    scene bg carriage_2
    call screen carriage_2_part2_investigation_map
    jump c2_p2_investigation_hub

label c2_p2_reinterview_eduard:
    scene talk to eduard with talk_in
    show eduard neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Eduard. I need you to actually talk to me this time."
    "{i}Eduard blinks, and for a moment seems more present than before.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    ed "...He's dead? Shunyu's… oh, hell. Hell, hell, hell."
    show eduard neutral at speaker_background(xalign=0.9)
    l "Where were you the last half hour?"
    show louis neutral at speaker_background(xalign=0.1)
    ed "Behind the bar! Where else would I be? I don't leave this counter during service, ask anyone."
    show eduard neutral at speaker_background(xalign=0.9)
    l "Anyone like who?"
    "{i}Eduard hesitates.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    ed "...I mean, no one else was really around. It's been quiet. Too quiet, actually, now that I think of it."
    show eduard neutral at speaker_background(xalign=0.9)
    l "Did you see the tile in his hand before? While he was playing?"
    show louis neutral at speaker_background(xalign=0.1)
    ed "No, no way. That's not even from his hand. He had three of the dragon tiles laid out, not that one. Someone put that there after."
    $ found_clue("clue_tile_mismatch")
    show eduard neutral at speaker_background(xalign=0.9)
    l "How do you know his hand that well?"
    show louis neutral at speaker_background(xalign=0.1)
    ed "Man complained about his own wins loud enough for the whole carriage to hear, all night, every night. Hard NOT to know it."
    $ c2_p2_reinterviewed_eduard = True
    return

label c2_p2_reinterview_agatha:
    scene talk to agatha with talk_in
    "{i}Louis finds Agatha packing up her kit after finishing with the body.{/i}"
    show agatha neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Can I ask you something?"
    show louis neutral at speaker_background(xalign=0.1)
    a "You're going to, whether I say yes or not. Go on."
    show agatha neutral at speaker_background(xalign=0.9)
    l "You said he was moved. Moved by who?"
    show louis neutral at speaker_background(xalign=0.1)
    a "That's your job to find out, not mine. I deal with bodies, not motives."
    show agatha neutral at speaker_background(xalign=0.9)
    l "Were you even in this carriage earlier tonight?"
    "{i}Agatha stops packing for a second.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    a "I was in the staff cabin. Had a passenger complaint to deal with. If you want an alibi, ask the idiot who pricked his finger and cried about it; he'll remember me being there."
    show agatha neutral at speaker_background(xalign=0.9)
    l "I wasn't accusing you though…"
    show louis neutral at speaker_background(xalign=0.1)
    a "You were thinking about it. Everyone thinks about it, when someone ends up dead and a woman happens to know exactly how. Ask your questions, matchstick. Just don't waste my time doing it."
    $ c2_p2_reinterviewed_agatha = True
    return

label part2_chapter_end:
    scene bg carriage_2
    $ achievement.grant("closer_to_the_truth")
    show louis neutral at speaker_focus(xalign=0.5)
    l "A tile that doesn't belong to the hand. A body moved after death. Barely anyone with a solid alibi for the last half hour."
    l "This isn't just going to be about finding who was angry at him. Someone wanted this scene in a very specific way."
    l "...I don't think I'm getting off this train until I find out why."
    l "I need to check the other carriages. Someone must have seen something."
    "{i}Louis heads toward the sleeper cabin, hoping Kimmy or Himmel saw something.{/i}"
    jump carriage_3_part2_start

label carriage_2_part2_return:
    scene bg carriage_2
    call screen carriage_2_part2_after_map
    jump carriage_2_part2_return


label carriage_3_part2_start:
    $ autosave_checkpoint()
    scene bg carriage_3 with dissolve
    show screen map_stamp(_("CARRIAGE 3"), _("SLEEPER CABINS"))
    jump carriage_3_part2_hub

# Back from the mail room, once Pattison has confirmed Alexander's alibi.
label carriage_3_part2_return:
    if not c3_p2_returned:
        $ c3_p2_returned = True
        $ autosave_checkpoint()
        scene bg carriage_3 with dissolve
        "{i}The sleeper cabin is colder than before. The four rooms all sit slightly ajar, as if something moved through recently and didn't bother closing doors behind it.{/i}"
    jump carriage_3_part2_hub

label carriage_3_part2_hub:
    scene bg carriage_3
    call screen carriage_3_part2_map
    jump carriage_3_part2_hub

label c3_p2_interact_toys:
    "Awh, they're so cute."
    return

label c3_p2_interact_luggage:
    if not clue_drug_wrapper:
        l "Sorry… I know this isn't really my business, but..."
        call play_required("mg_combo", combo_reset) from _call_play_required_7
        "{i}He nudges one of the bags open, just slightly. Something crinkles.{/i}"
        "{i}Louis finds a small, crumpled wrapper wedged between the folds of a coat. Printed on it, half torn: “...APLE SUGAR… BANNED SUBSTANCE, RESTRICTED USE ONLY.”{/i}"
        l "...This is the same stuff Alexander was selling."
        l "Why would Himmel have this?"
        $ found_clue("clue_drug_wrapper")
        $ achievement.grant("suspicious_luggage")
    else:
        "Already checked this."
    return

label c3_p2_interact_carpet:
    if not clue_hidden_tile:
        l "This again... It was like this the first time too."
        "{i}He kneels, and this time, pulls at the loose edge.{/i}"
        call play_required("mg_pry", pry_reset) from _call_play_required_8
        "{i}Underneath, tucked flat against the floorboard, is a single mahjong tile - the exact match to the one missing from Shunyu's winning hand.{/i}"
        l "...No. No way."
        l "This was under Misha's carpet the whole time."
        $ found_clue("clue_hidden_tile")
        $ achievement.grant("hidden_evidence")
    else:
        "Already found the tile here."
    return

label c3_p2_kimmy_reinterview:
    scene talk to kimmy with talk_in
    show kimmy neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Kimmy, can I ask you something a little... sensitive?"
    show louis neutral at speaker_background(xalign=0.1)
    k "Sensitive is my favorite kind of question, sugar. Go on."
    show kimmy neutral at speaker_background(xalign=0.9)
    l "Did Himmel ever buy anything from the storage carriage? From a man named Alexander?"
    "{i}Kimmy's smile falters, just barely.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    k "...He said it was for his nerves. Train rides make him anxious, he said. I didn't ask questions, matchstick. A wife who asks too many questions doesn't stay a wife for long."
    show kimmy neutral at speaker_background(xalign=0.9)
    l "Did he owe Alexander money?"
    show louis neutral at speaker_background(xalign=0.1)
    k "How would I know? I don't manage his little vices. I manage the family business."
    show kimmy neutral at speaker_background(xalign=0.9)
    l "Did Shunyu know about this? About Himmel buying from Alexander?"
    show louis neutral at speaker_background(xalign=0.1)
    k "Everyone on this train gossips like it's the last thing they'll ever do. Of course he knew. He probably teased Himmel about it, he teased everyone about everything."
    $ kimmy_reinterviewed = True
    return

label c3_p2_himmel_reinterview:
    scene talk to himmel with talk_in
    show himmel neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Himmel, I need to ask you about Alexander."
    show louis neutral at speaker_background(xalign=0.1)
    h "I- I don't know what you're talking about!"
    $ evidence_setup("himmel neutral", "Himmel", "I- I don't know what you're talking about!", "clue_drug_wrapper", "talk to himmel")
    call play_required("mg_evidence", evidence_reset) from _call_play_required_9
    show himmel neutral at speaker_background(xalign=0.9)
    l "I found a wrapper in your luggage. The banned maple sugar."
    "{i}Himmel's face goes pale.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    h "I- it's for my nerves! I have a condition!"
    show himmel neutral at speaker_background(xalign=0.9)
    l "Did you owe him money?"
    show louis neutral at speaker_background(xalign=0.1)
    h "I... I was going to pay him at the next stop. There's always a next stop..."
    show himmel neutral at speaker_background(xalign=0.9)
    l "There isn't a next stop, Himmel."
    show louis neutral at speaker_background(xalign=0.1)
    h "There has to be! There has to be!"
    $ himmel_reinterviewed = True
    return

label c3_p2_sebastian_reinterview:
    scene talk to sebastian with talk_in
    "{i}Sebastian stands exactly where he always does, posture rigid, eyes forward.{/i}"
    show sebastian neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Sebastian. I need to ask you about Misha."
    show louis neutral at speaker_background(xalign=0.1)
    seb "Mr. Popov has been in this cabin all evening, Mr. Louis. Under my supervision."
    show sebastian neutral at speaker_background(xalign=0.9)
    l "The whole evening? Never once out of your sight?"
    "{i}A pause. Barely long enough to notice. But Louis notices.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    seb "...Children require attending to. Baths. Meals. There are moments when a butler must step away."
    show sebastian neutral at speaker_background(xalign=0.9)
    l "How many moments?"
    show louis neutral at speaker_background(xalign=0.1)
    seb "I fail to see the relevance of this line of questioning."
    show sebastian neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    $ evidence_setup("sebastian neutral", "Sebastian", "Mr. Popov has been in this cabin all evening, Mr. Louis. Under my supervision.", "clue_hidden_tile", "talk to sebastian")
    call play_required("mg_evidence", evidence_reset) from _call_play_required_10
    "{i}Louis holds up the tile.{/i}"
    l "I found this under the carpet in his room, Sebastian. It matches the murder scene exactly."
    "{i}Sebastian's composure cracks, just barely - a flicker, gone as fast as it came.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    seb "...Mr. Popov collects things. Trinkets. It means nothing."
    show sebastian neutral at speaker_background(xalign=0.9)
    l "A dead man is missing a tile from his hand. That same tile turns up hidden in a child's bedroom. That means something, Sebastian."
    show louis neutral at speaker_background(xalign=0.1)
    seb "I would ask you to choose your next words very carefully, Mr. Louis."
    show sebastian neutral at speaker_background(xalign=0.9)
    l "Is that a threat?"
    show louis neutral at speaker_background(xalign=0.1)
    seb "It is a warning. For your own sake."
    $ sebastian_reinterviewed = True
    return

label c3_p2_misha_reinterview:
    scene talk to misha with talk_in
    show misha neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "...Misha?"
    "{i}Misha doesn't look up.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    mi "{i}(humming, quiet){/i} Tuck it in his hand… tuck it in his hand… that's how you keep the score..."
    show misha neutral at speaker_background(xalign=0.9)
    l "What score? Misha, what are you talking about?"
    "{i}Misha finally looks up, and smiles calmly.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    mi "You found it, didn't you? Under the carpet."
    show misha neutral at speaker_background(xalign=0.9)
    l "...H-how did you-"
    show louis neutral at speaker_background(xalign=0.1)
    mi "Everyone always finds it eventually. That's the game."
    show misha neutral at speaker_background(xalign=0.9)
    l "This isn't a game, Misha! Someone died!"
    "{i}Misha tilts his head, genuinely, unsettlingly confused.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    mi "He'll come back though. They always come back. Don't they?"
    "{i}Sebastian, from the doorway, sharply:{/i}"
    seb "Mr. Popov. That's enough."
    "{i}Misha goes quiet immediately, returning to his blocks as if nothing happened at all.{/i}"
    show misha neutral at speaker_background(xalign=0.9)
    l "{i}(to himself){/i} 'They always come back.' What does that even mean..."
    $ misha_reinterviewed = True
    if sebastian_reinterviewed:
        l "I have everything I think I'm going to get. The tile. The blood. The alibis. It's time to decide."
    return


label carriage_5_part2_start:
    if "p2_c5" not in visited_carriages:
        $ visited_carriages.append("p2_c5")
        $ autosave_checkpoint()
        scene bg carriage_5 with dissolve
        show screen map_stamp(_("CARRIAGE 5"), _("THE MAIL ROOM"))
    jump carriage_5_part2_hub

label carriage_5_part2_hub:
    scene bg carriage_5
    call screen carriage_5_part2_map
    jump carriage_5_part2_hub

label c5_p2_alexander_dialogue:
    scene talk to alexander with talk_in
    "{i}Alexander is slumped in his corner, twitchier than before, sweat on his brow despite the cold.{/i}"
    show alexander neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Alexander. I found this in Himmel's luggage."
    $ evidence_setup("alexander neutral", "Alexander", "And as for the other one… the stuff was strong so I don't remember.", "clue_drug_wrapper", "talk to alexander")
    call play_required("mg_evidence", evidence_reset) from _call_play_required_11
    "{i}Louis holds up the wrapper.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    al "...Ha. Haha. So? Rich folk get nervous too, y'know."
    show alexander neutral at speaker_background(xalign=0.9)
    l "Did he pay you? In full?"
    "{i}Alexander goes quiet, picking at his sleeve.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    al "...No. Not in full. Kept saying 'next stop, next stop.' There ain't no next stop on this train, is there?"
    show alexander neutral at speaker_background(xalign=0.9)
    l "And Shunyu, you told me before he still owed you too."
    show louis neutral at speaker_background(xalign=0.1)
    al "Yeah. Yeah, he did. Funny thing, huh? Two men who owe me money, and one of 'em ends up dead with a glass stickin' outta him."
    show alexander neutral at speaker_background(xalign=0.9)
    l "Are you admitting to something?"
    "{i}Alexander laughs, too loud, too long.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    al "I'm admitting I'm really good at picking customers who don't pay. That's all I'm admitting to, brother."
    show alexander neutral at speaker_background(xalign=0.9)
    l "Where were you when Shunyu was killed?"
    show louis neutral at speaker_background(xalign=0.1)
    al "Here. Same as always. Ask the postman, he's always lurking round here too."
    $ alexander_reinterviewed = True
    scene bg carriage_5 with dissolve
    show louis neutral at speaker_focus(xalign=0.5)
    l "Two unpaid debts. Two people connected to him, and one of them's already dead."
    l "...Alexander had a reason. But did he have the chance?"
    l "He said the postman would vouch for him. Guess it's worth checking."
    return

label c5_p2_pattison_dialogue:
    scene talk to pattison with talk_in
    "{i}Pattison is exactly where he always is, sorting the same mail, murmuring the same rhyme under his breath.{/i}"
    show pattison neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "Pattison. I need to ask you something important."
    show louis neutral at speaker_background(xalign=0.1)
    p "This goes to the clock, while this goes to the end..."
    show pattison neutral at speaker_background(xalign=0.9)
    l "Pattison, please. Was Alexander here the whole night? In this carriage?"
    "{i}Pattison stops sorting. Looks at Louis properly for the first time.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    p "He's always here. Never leaves. Poor thing thinks the walls listen back to him."
    show pattison neutral at speaker_background(xalign=0.9)
    l "So he didn't leave at all? Not even for a minute?"
    show louis neutral at speaker_background(xalign=0.1)
    p "I don't watch him every second, sir. I look at the mail. But I would've heard the door. It creaks something awful."
    show pattison neutral at speaker_background(xalign=0.9)
    l "Did you hear it? The door, I mean. Any time in the last hour?"
    "{i}Pattison tilts his head, thinking, or pretending to.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    p "...No. No, I don't believe I did."
    show pattison neutral at speaker_background(xalign=0.9)
    l "So he really didn't leave."
    show louis neutral at speaker_background(xalign=0.1)
    p "That's what I said, isn't it?"
    show pattison neutral at speaker_background(xalign=0.9)
    l "...Right. Thank you, Pattison."
    show louis neutral at speaker_background(xalign=0.1)
    show pattison neutral at speaker_focus(xalign=0.9)
    p "This goes to the clock, while this goes to the end..."
    "{i}He returns to his sorting like the conversation never happened.{/i}"
    scene bg carriage_5 with dissolve
    show louis neutral at speaker_focus(xalign=0.5)
    l "No creaking door. No one saw him leave. If Pattison's telling the truth, Alexander physically couldn't have made it to Carriage 2 and back without being noticed."
    l "...He had every reason to want Shunyu gone. He just didn't have the chance to actually do it."
    $ found_clue("clue_alexander_alibi")
    $ achievement.grant("alibi_confirmed")
    $ pattison_reinterviewed = True
    return


label accusation_scene:
    $ autosave_checkpoint()
    scene bg carriage_3
    $ renpy.notify("COMPLETED CLUES!")
    pause 1.0
    scene black with dissolve
    "The train lurches. Every character you spoke to gathers: Eduard behind his bar, Agatha with her kit, Dorothy clutching her ticket punch, Fedora with her notepad ready, Pattison murmuring at the doorway, Alexander shaking in the corner, Kimmy and Himmel arm in arm, Sebastian standing protectively in front of Misha."
    scene bg carriage_5 with dissolve
    show fedora neutral at speaker_focus(xalign=0.9)
    f "Well? You've had your little investigation. Who's it going to be, matchstick?"
    show fedora neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.5)
    l "..."
    menu:
        "Accuse Eduard":
            jump accusation_eduard
        "Accuse Alexander":
            jump accusation_alexander
        "Accuse Agatha":
            jump accusation_agatha
        "Accuse Misha":
            jump accusation_misha

label accusation_eduard:
    hide fedora
    show louis neutral at speaker_focus(xalign=0.1)
    l "It was you."
    show eduard neutral at speaker_focus(xalign=0.9)
    ed "Me?? I- I never even left the counter."
    jump wrong_ending

label accusation_alexander:
    hide fedora
    show louis neutral at speaker_focus(xalign=0.1)
    l "It was you."
    show alexander neutral at speaker_focus(xalign=0.9)
    al "Wha? No, no no no, I didn't leave this carriage, ask the postman, ASK HIM!"
    jump wrong_ending

label accusation_agatha:
    hide fedora
    show louis neutral at speaker_focus(xalign=0.1)
    l "It was you."
    show agatha neutral at speaker_focus(xalign=0.9)
    a "...You're joking. Tell me you're joking."
    jump wrong_ending

label wrong_ending:
    "{i}The accused freezes. The others go dead silent.{/i}"
    if not persistent.reduce_motion:
        show lights_dying
        pause 1.3
    scene black with dissolve
    "The lights die. Every window goes black at once. The train's chugging stops entirely - dead, total silence."
    f "{i}(barely a whisper){/i} That's not... that's not how this works..."
    "Something moves in the dark, fast, wrong-shaped, dragging itself down the length of the carriage. Louis doesn't get a chance to run."
    l "W-wait, I-"
    scene black
    u "Wrong guess. The train doesn't forgive wrong guesses."
    $ achievement.grant("wrong_guess")
    jump ending_1_death

label accusation_misha:
    hide fedora
    show louis neutral at speaker_focus(xalign=0.1)
    if not (clue_tile_mismatch and clue_body_moved and clue_alexander_alibi and clue_hidden_tile):
        l "It was Misha."
        show misha neutral at speaker_focus(xalign=0.9)
        mi "...Why would you say that?"
        l "I... I don't actually have enough to prove it."
        jump wrong_ending

    show misha neutral at speaker_background(xalign=0.9)
    l "It was Misha."
    $ evidence_setup("misha neutral", "Misha", "You found it, didn't you? Under the carpet.", "clue_hidden_tile", "bg carriage_5")
    call play_required("mg_evidence", evidence_reset) from _call_play_required_12
    l "The tile is missing from Shunyu's hand. Hidden under your carpet. The blood at the bar not matching where he was found, someone strong enough, or careless enough, to move a body without thinking twice about what that means. And you kept humming about a 'score.' About people coming back."
    l "It was you the whole time, wasn't it?"
    "{i}Sebastian steps forward, voice cracking for the first time since Louis met him.{/i}"
    show sebastian neutral at speaker_focus(xalign=0.5)
    seb "Mr. Popov, is this-"
    "{i}Misha looks between them both. The practiced calm finally slips.{/i}"
    show sebastian neutral at speaker_background(xalign=0.5)
    mi "...But he always comes back. Everyone always comes back. That's how it's always been. That's the rule."
    show misha neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    l "{i}(gently){/i} Not this time, Misha. This time it's real. He's not coming back."
    "{i}Misha's eyes well up, not manipulation, not a performance. Genuine, dawning horror.{/i}"
    show louis neutral at speaker_background(xalign=0.1)
    mi "...Oh."
    mi "Oh, no. No no no, that's not… that's not how the game is supposed to go!"
    scene black with dissolve
    "The train shudders violently. The key Ichora gave to Louis, now hoisted on his waist, is snatched and shoved into the keyhole of the Carriage 6 door. The door to Carriage 6, sealed the entire journey, creaks open on its own, spilling cold light into the carriage."
    show door_light
    u "Truth accepted. Come see what you've won."
    scene bg carriage_5 with dissolve
    show door_light
    show sebastian neutral at speaker_focus(xalign=0.5)
    "{i}Sebastian kneels beside Misha, and for the first time, his composure fully breaks.{/i}"
    seb "...I should have seen it. I should have- I told myself it was nothing. I told myself trinkets meant nothing."
    hide sebastian
    show fedora neutral at speaker_focus(xalign=0.9)
    "{i}Fedora, quietly, notepad lowering for the first time all night:{/i}"
    f "...I don't think I want to interview the killer anymore."
    show fedora neutral at speaker_background(xalign=0.9)
    show louis neutral at speaker_focus(xalign=0.1)
    "{i}Louis looks toward Carriage 6.{/i}"
    l "...I need to see this through. All the way."
    $ achievement.grant("true_detective")
    jump carriage_6_start


label carriage_6_start:
    scene carriage_6 with fade
    show carriage_6_fog
    "{i}You step through. The temperature drops.{/i}"
    l "...It's so quiet. Why is it so quiet."
    "{i}Fedora's voice, distant, echoing, from nowhere and everywhere:{/i}"
    f "...I don't think this carriage was ever meant to be found."
    pause 1.0
    l "...Shunyu?"
    show shunyu_monster neutral at speaker_focus(xalign=0.2)
    shunyu_monster "{i}(wet, clicking){/i} Wanna play... you can only lose 100[pct]... but win... 100,000[pct]..."
    show shunyu_monster neutral at speaker_background(xalign=0.2)
    show himmel_monster neutral at speaker_focus(xalign=0.8)
    himmel_monster "{i}(rapid, overlapping with itself){/i} Next stop, next stop, next stop, there's no next stop, there's no next stop, there's-"
    "{i}He doesn't seem to notice you.{/i}"
    show himmel_monster neutral at speaker_background(xalign=0.8)
    show conductor_monster neutral at speaker_focus(xalign=0.5)
    conductor_monster "Thank you for boarding…."
    l "The ^#&#(*&?"
    u "You found the truth. Good. Now see what the truth costs."
    "{i}The three shapes - Shunyu, Himmel, and the Conductor-thing - turn toward you at exactly the same moment.{/i}"
    l "...I figured out who did it. I did what you wanted. Isn't that enough?"
    u "Knowing isn't the same as surviving."
    l "What do you want from me?"
    u "Not me. Him."
    show misha neutral at speaker_focus(xalign=0.5) with dissolve
    mi "This is my game. You have to play it right, or it doesn't end."
    l "...This whole carriage. This is all… this is what you imagine, isn't it? What you think happens when someone 'doesn't come back.'"
    u "A child's mind, given a body big enough to hold it. Everything he doesn't understand about death, it comes here to grow. Answer him truly, and it rests. Lie, or guess, or refuse, and it doesn't."
    l "...What happens if I get it wrong?"
    "{i}The Passenger's grin stretches wider. The Gentleman's shaking speeds up, wrappers peeling further off his skin like scabs. The Conductor-thing unfolds another half-foot taller, the ceiling groaning under it.{/i}"
    u "You'll see. Three questions. Three chances. Choose carefully, Louis."
    hide misha with dissolve
    jump c6_question_1

label c6_question_1:
    "{i}The Passenger lurches forward, tiles clicking and clattering out of his throat, arranging themselves on the floor into a crude, shifting sentence only Louis can read.{/i}"
    show shunyu_monster neutral at speaker_focus(xalign=0.2)
    shunyu_monster "{i}(wet, clicking){/i} You can only lose one hundred percent... but you can win one hundred thousand percent... So tell me, matchstick... what did I actually lose?"
    menu:
        "“Your life.”":
            l "Your life. You lost your life."
            "{i}The Passenger's grin cracks wider, tiles bursting from new places along his arms, his neck, clattering to the floor in a wave.{/i}"
            shunyu_monster "WRONG. Life isn't at stake. It was never a stake."
            $ c6_q1_correct = False
        "“Your winning streak.”":
            l "I… your winning streak, maybe?"
            "{i}The Passenger tilts his head unnaturally far, tiles raining out of his mouth in a disappointed clatter.{/i}"
            shunyu_monster "Shallow. Small. WRONG."
            "{i}His bloated form swells slightly, the wound in his side widening.{/i}"
            $ c6_q1_correct = False
        "“Nothing. You never really understood what you were risking.”":
            l "...Nothing. Because you never understood what you were actually risking in the first place. You thought it was just a game, all the way to the end."
            shunyu_monster "{i}(barely a whisper, almost human){/i} ...Oh. That's... that's an awfully sad way to have gone, isn't it."
            hide shunyu_monster with Dissolve(1.5)
            $ c6_q1_correct = True
    jump c6_question_2

label c6_question_2:
    "{i}The Gentleman vibrates closer, wrappers crinkling with every juddering step, hands still clawing at his own chest.{/i}"
    show himmel_monster neutral at speaker_focus(xalign=0.8)
    himmel_monster "{i}(rapid, overlapping){/i} Tell me, tell me, WHAT was I actually running toward? Every time. Every single time. WHAT WAS IT."
    menu:
        "“Peace.”":
            l "Peace, maybe?"
            "{i}The Gentleman's shaking intensifies violently, veins pulsing black beneath his waxen skin.{/i}"
            himmel_monster "PEACE ISN'T SOMETHING YOU BUY IN A CORNER OF A STORAGE CART. WRONG."
            $ c6_q2_correct = False
        "“Kimmy's approval.”":
            l "Maybe… maybe you wanted Kimmy to notice you more?"
            "{i}The Gentleman freezes for a moment, then lets out a horrible, warped laugh that isn't really a laugh at all.{/i}"
            himmel_monster "Close. Cruelly close. But WRONG."
            $ c6_q2_correct = False
        "“Nothing real. Just a feeling that let you stop feeling everything else.”":
            l "Nothing real. You weren't running toward anything, Himmel. You were just trying to stop feeling everything else, even if just for a minute."
            "{i}The Gentleman stops shaking, all at once, like a held breath finally released. The wrappers slide off him one by one, dissolving into the fog. His waxy skin softens, and for a moment he looks like nothing more than a tired, frightened man.{/i}"
            himmel_monster "{i}(quiet, human){/i} ...I never even told her. I don't think I ever really wanted her to know."
            hide himmel_monster with Dissolve(2.0)
            "{i}He fades, gently, the fog closing over where he stood.{/i}"
            $ c6_q2_correct = True
    jump c6_question_3

label c6_question_3:
    "{i}The Conductor-thing unfolds to its full, impossible height, the faceless expanse of fabric-skin tilting down toward Louis. The mouth-hole opens, and Dorothy's stolen voice pours out, layered and wrong.{/i}"
    show conductor_monster neutral at speaker_focus(xalign=0.5)
    conductor_monster "Thank you for boarding... the Grekhov Express... Tell me, passenger... what is a conductor FOR... if none of you ever truly get off?"
    menu:
        "“To keep the train running forever.”":
            l "Maybe… maybe just to keep it moving?"
            "{i}The Conductor-thing's form ripples, limbs multiplying, extra joints bending the wrong way all along its arms.{/i}"
            conductor_monster "WRONG. Motion without purpose is not a duty. It is a curse."
            $ c6_q3_correct = False
        "“To punish the ones who did wrong.”":
            l "To… to punish people? For what they did?"
            "{i}The Conductor-thing lets out a sound like a hundred whispered apologies played backward at once.{/i}"
            conductor_monster "WRONG."
            $ c6_q3_correct = False
        "“To help everyone finally understand it's over, so they can stop waiting for a stop that isn't coming.”":
            l "...To help everyone understand it's already over. So they can finally stop waiting for a stop that was never going to come."
            "{i}The Conductor-thing goes utterly still. Slowly, impossibly slowly, it smiles.{/i}"
            conductor_monster "...Thank you... for finally letting us go..."
            hide conductor_monster with Dissolve(2.0)
            $ c6_q3_correct = True
    jump carriage_6_aftermath

label carriage_6_aftermath:
    if c6_q1_correct and c6_q2_correct and c6_q3_correct:
        $ achievement.grant("perfect_understanding")
        jump ending_3_true
    elif c6_q1_correct or c6_q2_correct or c6_q3_correct:
        $ achievement.grant("partial_truth")
        jump ending_2_escape
    else:
        $ achievement.grant("total_failure")
        scene black with dissolve
        "You found the truth, and still couldn't carry it. That may be worse than never finding it at all."
        "{i}Louis is hit with the darkness.{/i}"
        jump ending_1_death


label ending_1_death:
    hide screen loop_overlay
    scene black with dissolve
    call screen ending_card(_("ENDING 1"), _("WRONG GUESS"), _("The train doesn't forgive wrong guesses."))
    call ending_video from _call_ending_video
    $ MainMenu(confirm=False)()
    return

label ending_2_escape:
    hide screen loop_overlay
    scene black with dissolve
    "Nice, you escaped!"
    call screen ending_card(_("ENDING 2"), _("PARTIAL TRUTH"), _("You escaped, but not everything was resolved."))
    call ending_video from _call_ending_video_1
    $ MainMenu(confirm=False)()
    return

label ending_3_true:
    hide screen loop_overlay
    $ in_loop = False
    scene bg carriage_1 with dissolve
    show dorothy happy at speaker_focus(xalign=0.9)
    d "Thank you for saving us. You can finally leave!"
    scene black with dissolve
    call screen ending_card(_("ENDING 3"), _("THE TRUE LINE"), _("You solved the mystery and freed everyone from the loop."))
    call ending_video from _call_ending_video_2
    $ MainMenu(confirm=False)()
    return


label ending_video:
    stop music fadeout 1.0
    $ renpy.movie_cutscene(ENDING_VIDEO, stop_music=True)
    $ persistent.ending_video_seen = True
    return


label old_film_to_map:
    window hide

    if persistent.reduce_motion:
        scene bg carriage_1 with fade
        jump carriage_1_start

    show screen burn_embers
    show layer master at map_settle
    scene bg carriage_1
    with burn_reveal

    show screen map_stamp(_("CARRIAGE 1"), _("FIRST CLASS"))
    pause 2.2

    show layer master
    jump carriage_1_start


label c1_interact_cupboard:
    if in_loop:
        u "Be careful, young one. Do you really wanna do that?"
        return

    "Hmm… It seems to be locked. What would be in there?"
    menu:
        "Try picking the lock?"
        "Pick it":
            $ lockpick_reset()
            $ renpy.block_rollback()
            call screen mg_lockpick
            if _return == "win":
                $ found_timetable = True
                "{i}The lock clicks open. Inside is a dusty timetable. Every departure on it is printed the same way: 4:00.{/i}"
                l "…Every single one? Even the ones from years ago?"
            elif _return == "lose":
                "{i}The pick snaps. The lock stays shut.{/i}"
        "Leave it":
            pass
    return

label c2_interact_broken_glass:
    show louis neutral at speaker_focus(xalign=0.5)
    l "Damn, how'd that gambler guy even break it?"
    gam "Can yer shut up?"
    if not in_loop:
        menu:
            "Sweep up the glass?"
            "Sweep it up":
                $ shards_reset()
                $ renpy.block_rollback()
                call screen mg_shards
                if _return == "win":
                    l "Got it all… huh. I only counted six shards. Wasn't there a bigger one?"
                elif _return == "lose":
                    "{i}You give up and leave the glass where it is.{/i}"
            "Leave it":
                pass
    return

label c3_interact_toys:
    "Awh, they're so cute."
    menu:
        "Play with the blocks?"
        "Play":
            $ blocks_reset()
            $ renpy.block_rollback()
            call screen mg_blocks
            if _return == "win":
                "{i}Misha looks up. He almost smiles.{/i}"
                mi "You play nice. Not like the others. They always forget the order."
                l "…The order of what?"
                "{i}Misha goes back to his blocks.{/i}"
            elif _return == "lose":
                "{i}Misha stares at the fallen blocks, then at you. Sebastian clears his throat from the doorway.{/i}"
        "Leave them":
            pass
    return

label c5_interact_engine:
    "This looks like it has a lot of… Zebra power? No, horse power."
    menu:
        "Give the engine a hand?"
        "Take the controls":
            $ engine_reset()
            $ renpy.block_rollback()
            call screen mg_engine
            if _return == "win":
                ic "Not bad, buddy! Steady hands. You'd make a fine engineer."
            elif _return == "lose":
                ic "Whoa-whoa-whoa! Hands off, buddy! …I'll fix it."
        "Not today":
            pass
    return

label c5_interact_mail_room:
    "Wow, so much mail comes to this train, how?"
    menu:
        "Help sort the mail?"
        "Sort mail":
            $ mail_reset()
            $ renpy.block_rollback()
            call screen mg_mail
            if _return == "win":
                p "This goes to the clock, while this goes to the end… thank you, Sir. You'll be needed before it ends."
            elif _return == "lose":
                p "No, no, no. That goes to the fake ones. Never mind. I'll do it."
        "Leave it":
            pass
    return