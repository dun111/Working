

#reserved space for definace of each character
define d = Character("Dorothy")
define l = Character("Louis")



#End of character define

label start:

    # text settings
    # Auto-forward mode
    $ _preferences.afm_enable = True
    # 2. Set the wait time (lower = faster, 15 is standard)
    $ _preferences.afm_time = 15
    #end of text settings


    scene bg room
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


    return



