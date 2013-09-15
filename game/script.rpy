init python hide:
#run through the list of image files in the game directory and add them
    for file in renpy.list_files():
        if file.startswith('img/'): 
            if file.endswith('.jpg') | file.endswith('.png'):
                name = file.replace('img/', '').replace('/', ' ').replace('.png', '').replace('.jpg', '')
                renpy.image(name, Image(file))

    

# In the init section you should only define or create static variables
init:
    # Declare characters used by this game.
    # If you define a character with an image attribute
    # you can change this:
    #   show eileen happy
    #   e "Mackerel is my fav"
    # to this: 
    #   e happy "Mackerel is my fav"
    #   It just streamlines things.
    define e = Character('Eileen', image='eileen', color="#c8ffc8")
    define l = Character('Lucy', image='lucy', color="#c8ff00")

# The game starts here.
label start:
    scene bg cave
    show eileen happy at left
    
    e vhappy "I like fish"
    show lucy happy at right with moveinright
    show eileen happy
    l mad "I hate fish!" with sshake
    l "Let us battle!"
    call battle

    show lucy happy
    if _return:
        "Eileen won"
        e vhappy "I won the match so I decide that today is a day for eating fish."
        show eileen happy
    else:
           "Lucy won"
           l "Fish is terrible and you cannot force me to consume it."
           centered "Bad Ending"
           return
    e "Is the fish monger's store even open? What day was it?"
    menu:
        "Today is Sunday.":        
            call fishMonger (False)
        "Today is Tuesday.":
            call fishMonger (True)
    if _return:
        "Eileen goes to the fishmonger"
        centered "Good Ending"
    else:
        "Eileen doesn't go to the fishmonger."
        centered "Bad Ending"
    return

label fishMonger (fishMongerOpen):
    e "Should I go buy some fish from the fishmonger?"
    if fishMongerOpen:
        l mad "Do whatever you like, it's not like I care!" with sshake
        show lucy happy
        menu:
            "Yes, I needs some fish":
                return True
            "No, I don't like the smell of the fish shop.":
                pass
    else:
        l mad "No, stupid! It's Sunday. They\'re obviously closed."
        show lucy happy
        e "Closed?? Oh well, I guess I'll just starve."
    return False

