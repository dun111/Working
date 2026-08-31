

#reserved space for definace of each character
define d = Character("Dorothy")
define l = Character("Louis")
define m = character("Matthew")
define f = character("Fedora")

#End of character define

label start:

    # text settings
    # Auto-forward mode
    $ _preferences.afm_enable = True
    # 2. Set the wait time (lower = faster, 15 is standard)
    $ _preferences.afm_time = 15
    #end of text settings


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
    #(reserve a spot for the ticket photo)
    show louis confused
    l "Miss, what line is this?{w=2}"
    show dorothy supprised
    d "The Grekhov Express? Are you ill? Everyone knows that, why else would you be on this train?{w=2}"
    show louis neutral
    l "O-oh, sorry, I think I might have gotten a bit light headed…{w=2}"
    show dorothy neutral
    d "I see. Well sir, welcome aboard the Grekhov Express…{w=1} "
    show louis confused
    l "stands up. Huh, I don’t remember how I got here… That’s right, I was tryna go home… But… What happened? I’m gonna look around{w=2}"
    
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
    #end of interaction

    #scene talk to journalist
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
    #end of interaction

    






    
    return



