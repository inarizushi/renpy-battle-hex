# In this file, image definitions and methods are included to set up and return the
# various directional sprites, to avoid having to redefine them in different demos. 


# First we define all the images we need

init:

    ###
    # Clyde
    ###

    # Clyde Standing    
    image clyde n = 'gfx/clyde-stand-n.png'
    image clyde e = 'gfx/clyde-stand-e.png'
    image clyde s = 'gfx/clyde-stand-s.png'
    image clyde w = 'gfx/clyde-stand-w.png'

    # Clyde Walking
    image clyde walk n = anim.Filmstrip('gfx/clyde-walk-n.png', (200, 200), (6, 1), 0.1)
    image clyde walk e = anim.Filmstrip('gfx/clyde-walk-e.png', (200, 200), (6, 1), 0.1)
    image clyde walk s = anim.Filmstrip('gfx/clyde-walk-s.png', (200, 200), (6, 1), 0.1)
    image clyde walk w = anim.Filmstrip('gfx/clyde-walk-w.png', (200, 200), (6, 1), 0.1)

    image clyde crouch n = "gfx/clyde-jump-n-1.png"
    image clyde crouch e = "gfx/clyde-jump-e-1.png"
    image clyde crouch s = "gfx/clyde-jump-s-1.png"
    image clyde crouch w = "gfx/clyde-jump-w-1.png"
    
    image clyde leap n = "gfx/clyde-jump-n-2.png"
    image clyde leap e = "gfx/clyde-jump-e-2.png"
    image clyde leap s = "gfx/clyde-jump-s-2.png"
    image clyde leap w = "gfx/clyde-jump-w-2.png"
    
    # Clyde Attacking
    # These sprites will be a pre-attack transition, so you see the sword-swing
    # before the attack actually connects. 0.7s long in each case.
    image clyde melee pre n:
        "gfx/clyde-attack-n-1.png"
        time 0.15
        "gfx/clyde-attack-n-2.png"
        time 0.25
        "gfx/clyde-attack-n-3.png"
        time 0.3
        "gfx/clyde-attack-n-4.png"
    image clyde melee pre e:
        "gfx/clyde-attack-e-1.png"
        time 0.15
        "gfx/clyde-attack-e-2.png"
        time 0.25
        "gfx/clyde-attack-e-3.png"
        time 0.3
        "gfx/clyde-attack-e-4.png"
    image clyde melee pre s:
        "gfx/clyde-attack-s-1.png"
        time 0.15
        "gfx/clyde-attack-s-2.png"
        time 0.25
        "gfx/clyde-attack-s-3.png"
        time 0.3
        "gfx/clyde-attack-s-4.png"
    image clyde melee pre w:
        "gfx/clyde-attack-w-1.png"
        time 0.15
        "gfx/clyde-attack-w-2.png"
        time 0.25
        "gfx/clyde-attack-w-3.png"
        time 0.3
        "gfx/clyde-attack-w-4.png"

    # And these are the actual 'hold an attack pose' sprites - just the last
    # frame of the swing.
    
    image clyde melee n = "gfx/clyde-attack-n-4.png"
    image clyde melee e = "gfx/clyde-attack-e-4.png"
    image clyde melee s = "gfx/clyde-attack-s-4.png"
    image clyde melee w = "gfx/clyde-attack-w-4.png"

    # Magic anims are done the same way as the attack
    image clyde magic pre n:
        "gfx/clyde-magic-n-1.png"
        time 0.3
        "gfx/clyde-magic-n-2.png"
        time 0.6
        "gfx/clyde-magic-n-3.png"
    image clyde magic pre e:
        "gfx/clyde-magic-e-1.png"
        time 0.3
        "gfx/clyde-magic-e-2.png"
        time 0.6
        "gfx/clyde-magic-e-3.png"
    image clyde magic pre s:
        "gfx/clyde-magic-s-1.png"
        time 0.3
        "gfx/clyde-magic-s-2.png"
        time 0.6
        "gfx/clyde-magic-s-3.png"
    image clyde magic pre w:
        "gfx/clyde-magic-w-1.png"
        time 0.3
        "gfx/clyde-magic-w-2.png"
        time 0.6
        "gfx/clyde-magic-w-3.png"

    image clyde magic n = "gfx/clyde-magic-n-3.png"
    image clyde magic e = "gfx/clyde-magic-e-3.png"
    image clyde magic s = "gfx/clyde-magic-s-3.png"
    image clyde magic w = "gfx/clyde-magic-w-3.png"
    
    ###
    # Clyde for Hexes
    ###

    # Clyde Standing    
    image clydehex n = 'gfx/clyde-stand-hex-n.png'
    image clydehex ne = 'gfx/clyde-stand-e.png'
    image clydehex nw = 'gfx/clyde-stand-n.png'
    image clydehex s = 'gfx/clyde-stand-hex-s.png'
    image clydehex se = 'gfx/clyde-stand-s.png'
    image clydehex sw = 'gfx/clyde-stand-w.png'
    
    # Clyde Walking
    image clydehex walk n = anim.Filmstrip('gfx/clyde-walk-hex-n.png', (200, 200), (6, 1), 0.1)
    image clydehex walk ne = anim.Filmstrip('gfx/clyde-walk-e.png', (200, 200), (6, 1), 0.1)
    image clydehex walk nw = anim.Filmstrip('gfx/clyde-walk-n.png', (200, 200), (6, 1), 0.1)
    image clydehex walk s = anim.Filmstrip('gfx/clyde-walk-hex-s.png', (200, 200), (6, 1), 0.1)
    image clydehex walk se = anim.Filmstrip('gfx/clyde-walk-s.png', (200, 200), (6, 1), 0.1)
    image clydehex walk sw = anim.Filmstrip('gfx/clyde-walk-w.png', (200, 200), (6, 1), 0.1)

    ###
    # Knight
    ###

    # Standing    
    image knight n = 'gfx/knight-stand-n.png'
    image knight e = 'gfx/knight-stand-e.png'
    image knight s = 'gfx/knight-stand-s.png'
    image knight w = 'gfx/knight-stand-w.png'

    # Walking
    image knight walk n = anim.Filmstrip('gfx/knight-walk-n.png', (200, 200), (6, 1), 0.1)
    image knight walk e = anim.Filmstrip('gfx/knight-walk-e.png', (200, 200), (6, 1), 0.1)
    image knight walk s = anim.Filmstrip('gfx/knight-walk-s.png', (200, 200), (6, 1), 0.1)
    image knight walk w = anim.Filmstrip('gfx/knight-walk-w.png', (200, 200), (6, 1), 0.1)

    image knight crouch n = "gfx/knight-jump-n-1.png"
    image knight crouch e = "gfx/knight-jump-e-1.png"
    image knight crouch s = "gfx/knight-jump-s-1.png"
    image knight crouch w = "gfx/knight-jump-w-1.png"
    
    image knight leap n = "gfx/knight-jump-n-2.png"
    image knight leap e = "gfx/knight-jump-e-2.png"
    image knight leap s = "gfx/knight-jump-s-2.png"
    image knight leap w = "gfx/knight-jump-w-2.png"
    
    # Attacking
    image knight melee pre n:
        "gfx/knight-attack-n-1.png"
        time 0.15
        "gfx/knight-attack-n-2.png"
        time 0.25
        "gfx/knight-attack-n-3.png"
        time 0.3
        "gfx/knight-attack-n-4.png"
    image knight melee pre e:
        "gfx/knight-attack-e-1.png"
        time 0.15
        "gfx/knight-attack-e-2.png"
        time 0.25
        "gfx/knight-attack-e-3.png"
        time 0.3
        "gfx/knight-attack-e-4.png"
    image knight melee pre s:
        "gfx/knight-attack-s-1.png"
        time 0.15
        "gfx/knight-attack-s-2.png"
        time 0.25
        "gfx/knight-attack-s-3.png"
        time 0.3
        "gfx/knight-attack-s-4.png"
    image knight melee pre w:
        "gfx/knight-attack-w-1.png"
        time 0.15
        "gfx/knight-attack-w-2.png"
        time 0.25
        "gfx/knight-attack-w-3.png"
        time 0.3
        "gfx/knight-attack-w-4.png"

    image knight melee n = "gfx/knight-attack-n-4.png"
    image knight melee e = "gfx/knight-attack-e-4.png"
    image knight melee s = "gfx/knight-attack-s-4.png"
    image knight melee w = "gfx/knight-attack-w-4.png"

    ###
    # Mage
    ###

    # Standing    
    image mage n = 'gfx/mage-stand-n.png'
    image mage e = 'gfx/mage-stand-e.png'
    image mage s = 'gfx/mage-stand-s.png'
    image mage w = 'gfx/mage-stand-w.png'

    # Walking
    image mage walk n = anim.Filmstrip('gfx/mage-walk-n.png', (200, 200), (6, 1), 0.1)
    image mage walk e = anim.Filmstrip('gfx/mage-walk-e.png', (200, 200), (6, 1), 0.1)
    image mage walk s = anim.Filmstrip('gfx/mage-walk-s.png', (200, 200), (6, 1), 0.1)
    image mage walk w = anim.Filmstrip('gfx/mage-walk-w.png', (200, 200), (6, 1), 0.1)

    image mage crouch n = "gfx/mage-jump-n-1.png"
    image mage crouch e = "gfx/mage-jump-e-1.png"
    image mage crouch s = "gfx/mage-jump-s-1.png"
    image mage crouch w = "gfx/mage-jump-w-1.png"
    
    image mage leap n = "gfx/mage-jump-n-2.png"
    image mage leap e = "gfx/mage-jump-e-2.png"
    image mage leap s = "gfx/mage-jump-s-2.png"
    image mage leap w = "gfx/mage-jump-w-2.png"
    
    # Magic
    image mage magic pre n:
        "gfx/mage-magic-n-1.png"
        time 0.15
        "gfx/mage-magic-n-2.png"
        time 0.3
        "gfx/mage-magic-n-3.png"
    image mage magic pre e:
        "gfx/mage-magic-e-1.png"
        time 0.15
        "gfx/mage-magic-e-2.png"
        time 0.3
        "gfx/mage-magic-e-3.png"
    image mage magic pre s:
        "gfx/mage-magic-s-1.png"
        time 0.15
        "gfx/mage-magic-s-2.png"
        time 0.3
        "gfx/mage-magic-s-3.png"
    image mage magic pre w:
        "gfx/mage-magic-w-1.png"
        time 0.15
        "gfx/mage-magic-w-2.png"
        time 0.3
        "gfx/mage-magic-w-3.png"

    image mage magic n = "gfx/mage-magic-n-3.png"
    image mage magic e = "gfx/mage-magic-e-3.png"
    image mage magic s = "gfx/mage-magic-s-3.png"
    image mage magic w = "gfx/mage-magic-w-3.png"
 
    
# Then we create the sprites in Python methods

init python:

    # Clyde is the rough and blobby white character that we use to demonstrate the animations
    def GetClydeSprite():

        clydeSprite = BattleSprite('clyde n', anchor=(0.5, 0.9), placeMark=(0,-80))

        # Various directional standing sprites
        clydeSprite.AddStateSprite('default', 'clyde e', facing='E')
        clydeSprite.AddStateSprite('default', 'clyde s', facing='S')
        clydeSprite.AddStateSprite('default', 'clyde w', facing='W')
        clydeSprite.AddStateSprite('default', 'clyde n', facing='N')

        # Walking in each direction
        clydeSprite.AddStateSprite('moving', 'clyde walk e', facing='E')
        clydeSprite.AddStateSprite('moving', 'clyde walk s', facing='S')
        clydeSprite.AddStateSprite('moving', 'clyde walk w', facing='W')
        clydeSprite.AddStateSprite('moving', 'clyde walk n', facing='N')
        
        # Jumping upward
        clydeSprite.AddStateSprite('leapup', 'clyde leap e', facing='E')
        clydeSprite.AddStateSprite('leapup', 'clyde leap s', facing='S')
        clydeSprite.AddStateSprite('leapup', 'clyde leap w', facing='W')
        clydeSprite.AddStateSprite('leapup', 'clyde leap n', facing='N')
        
        # Jumping downward (same sprites, as it happens)
        clydeSprite.AddStateSprite('leapdown', 'clyde leap e', facing='E')
        clydeSprite.AddStateSprite('leapdown', 'clyde leap s', facing='S')
        clydeSprite.AddStateSprite('leapdown', 'clyde leap w', facing='W')
        clydeSprite.AddStateSprite('leapdown', 'clyde leap n', facing='N')
        
        # When leaping we will always transition from moving to leaping, and then
        # from leaping to either moving or default. So if we want a brief transition
        # of Clyde crouching before the leap to get more height, and crouching
        # after the leap to absorb the impact, then we need to define that transition
        # for all three potential state transitions, in all four directions, for
        # both leapup and leapdown...
        clydeSprite.AddStateTransition('moving', 'leapup', 'clyde crouch e', 0.25, fromFacing='E', toFacing='E')
        clydeSprite.AddStateTransition('moving', 'leapup', 'clyde crouch s', 0.25, fromFacing='S', toFacing='S')
        clydeSprite.AddStateTransition('moving', 'leapup', 'clyde crouch w', 0.25, fromFacing='W', toFacing='W')
        clydeSprite.AddStateTransition('moving', 'leapup', 'clyde crouch n', 0.25, fromFacing='N', toFacing='N')
        
        clydeSprite.AddStateTransition('leapup', 'moving', 'clyde crouch e', 0.25, fromFacing='E', toFacing='E')
        clydeSprite.AddStateTransition('leapup', 'moving', 'clyde crouch s', 0.25, fromFacing='S', toFacing='S')
        clydeSprite.AddStateTransition('leapup', 'moving', 'clyde crouch w', 0.25, fromFacing='W', toFacing='W')
        clydeSprite.AddStateTransition('leapup', 'moving', 'clyde crouch n', 0.25, fromFacing='N', toFacing='N')
        
        clydeSprite.AddStateTransition('leapup', 'default', 'clyde crouch e', 0.25, fromFacing='E', toFacing='E')
        clydeSprite.AddStateTransition('leapup', 'default', 'clyde crouch s', 0.25, fromFacing='S', toFacing='S')
        clydeSprite.AddStateTransition('leapup', 'default', 'clyde crouch w', 0.25, fromFacing='W', toFacing='W')
        clydeSprite.AddStateTransition('leapup', 'default', 'clyde crouch n', 0.25, fromFacing='N', toFacing='N')
        
        clydeSprite.AddStateTransition('moving', 'leapdown', 'clyde crouch e', 0.25, fromFacing='E', toFacing='E')
        clydeSprite.AddStateTransition('moving', 'leapdown', 'clyde crouch s', 0.25, fromFacing='S', toFacing='S')
        clydeSprite.AddStateTransition('moving', 'leapdown', 'clyde crouch w', 0.25, fromFacing='W', toFacing='W')
        clydeSprite.AddStateTransition('moving', 'leapdown', 'clyde crouch n', 0.25, fromFacing='N', toFacing='N')
        
        clydeSprite.AddStateTransition('leapdown', 'moving', 'clyde crouch e', 0.25, fromFacing='E', toFacing='E')
        clydeSprite.AddStateTransition('leapdown', 'moving', 'clyde crouch s', 0.25, fromFacing='S', toFacing='S')
        clydeSprite.AddStateTransition('leapdown', 'moving', 'clyde crouch w', 0.25, fromFacing='W', toFacing='W')
        clydeSprite.AddStateTransition('leapdown', 'moving', 'clyde crouch n', 0.25, fromFacing='N', toFacing='N')
        
        clydeSprite.AddStateTransition('leapdown', 'default', 'clyde crouch e', 0.25, fromFacing='E', toFacing='E')
        clydeSprite.AddStateTransition('leapdown', 'default', 'clyde crouch s', 0.25, fromFacing='S', toFacing='S')
        clydeSprite.AddStateTransition('leapdown', 'default', 'clyde crouch w', 0.25, fromFacing='W', toFacing='W')
        clydeSprite.AddStateTransition('leapdown', 'default', 'clyde crouch n', 0.25, fromFacing='N', toFacing='N')
        
        # Attacking in each direction
        # First we define a default->melee transition so the short animation plays before
        # the actual attack gets calculated and the damage shown.
        clydeSprite.AddStateTransition('acting', 'melee', 'clyde melee pre n', 0.6, toFacing='N')
        clydeSprite.AddStateTransition('acting', 'melee', 'clyde melee pre e', 0.6, toFacing='E')
        clydeSprite.AddStateTransition('acting', 'melee', 'clyde melee pre s', 0.6, toFacing='S')
        clydeSprite.AddStateTransition('acting', 'melee', 'clyde melee pre w', 0.6, toFacing='W')
        
        clydeSprite.AddStateSprite('melee', 'clyde melee n', facing='N')
        clydeSprite.AddStateSprite('melee', 'clyde melee e', facing='E')
        clydeSprite.AddStateSprite('melee', 'clyde melee s', facing='S')
        clydeSprite.AddStateSprite('melee', 'clyde melee w', facing='W')
        
        # Casting in each direction
        clydeSprite.AddStateTransition('acting', 'magic', 'clyde magic pre n', 0.9, toFacing='N')
        clydeSprite.AddStateTransition('acting', 'magic', 'clyde magic pre e', 0.9, toFacing='E')
        clydeSprite.AddStateTransition('acting', 'magic', 'clyde magic pre s', 0.9, toFacing='S')
        clydeSprite.AddStateTransition('acting', 'magic', 'clyde magic pre w', 0.9, toFacing='W')
        
        clydeSprite.AddStateSprite('magic', 'clyde magic n', facing='N')
        clydeSprite.AddStateSprite('magic', 'clyde magic e', facing='E')
        clydeSprite.AddStateSprite('magic', 'clyde magic s', facing='S')
        clydeSprite.AddStateSprite('magic', 'clyde magic w', facing='W')
        
        return clydeSprite
    
    # Clyde is the rough and blobby white character that we use to demonstrate the animations
    def GetClydeHexSprite():

        clydeSprite = BattleSprite('clydehex n', anchor=(0.5, 0.9), placeMark=(0,-80))

        # Various directional standing sprites
        clydeSprite.AddStateSprite('default', 'clydehex ne', facing='NE')
        clydeSprite.AddStateSprite('default', 'clydehex nw', facing='NW')
        clydeSprite.AddStateSprite('default', 'clydehex s', facing='S')
        clydeSprite.AddStateSprite('default', 'clydehex se', facing='SE')
        clydeSprite.AddStateSprite('default', 'clydehex sw', facing='SW')
        clydeSprite.AddStateSprite('default', 'clydehex n', facing='N')

        # Walking in each direction
        clydeSprite.AddStateSprite('moving', 'clydehex walk ne', facing='NE')
        clydeSprite.AddStateSprite('moving', 'clydehex walk nw', facing='NW')
        clydeSprite.AddStateSprite('moving', 'clydehex walk s', facing='S')
        clydeSprite.AddStateSprite('moving', 'clydehex walk se', facing='SE')
        clydeSprite.AddStateSprite('moving', 'clydehex walk sw', facing='SW')
        clydeSprite.AddStateSprite('moving', 'clydehex walk n', facing='N')
        
        
        return clydeSprite
    
    # This is the knight used for the elevation demo
    def GetKnightSprite():

        knightSprite = BattleSprite('knight n', anchor=(0.5, 0.9), placeMark=(0,-80))

        # Various directional standing sprites
        knightSprite.AddStateSprite('default', 'knight e', facing='E')
        knightSprite.AddStateSprite('default', 'knight s', facing='S')
        knightSprite.AddStateSprite('default', 'knight w', facing='W')
        knightSprite.AddStateSprite('default', 'knight n', facing='N')

        # Walking in each direction
        knightSprite.AddStateSprite('moving', 'knight walk e', facing='E')
        knightSprite.AddStateSprite('moving', 'knight walk s', facing='S')
        knightSprite.AddStateSprite('moving', 'knight walk w', facing='W')
        knightSprite.AddStateSprite('moving', 'knight walk n', facing='N')
        
        # Jumping upward
        knightSprite.AddStateSprite('leapup', 'knight leap e', facing='E')
        knightSprite.AddStateSprite('leapup', 'knight leap s', facing='S')
        knightSprite.AddStateSprite('leapup', 'knight leap w', facing='W')
        knightSprite.AddStateSprite('leapup', 'knight leap n', facing='N')
        
        # Jumping downward (same sprites, as it happens)
        knightSprite.AddStateSprite('leapdown', 'knight leap e', facing='E')
        knightSprite.AddStateSprite('leapdown', 'knight leap s', facing='S')
        knightSprite.AddStateSprite('leapdown', 'knight leap w', facing='W')
        knightSprite.AddStateSprite('leapdown', 'knight leap n', facing='N')
        
        # Leaping Transitions
        knightSprite.AddStateTransition('moving', 'leapup', 'knight crouch e', 0.25, fromFacing='E', toFacing='E')
        knightSprite.AddStateTransition('moving', 'leapup', 'knight crouch s', 0.25, fromFacing='S', toFacing='S')
        knightSprite.AddStateTransition('moving', 'leapup', 'knight crouch w', 0.25, fromFacing='W', toFacing='W')
        knightSprite.AddStateTransition('moving', 'leapup', 'knight crouch n', 0.25, fromFacing='N', toFacing='N')
        
        knightSprite.AddStateTransition('leapup', 'moving', 'knight crouch e', 0.25, fromFacing='E', toFacing='E')
        knightSprite.AddStateTransition('leapup', 'moving', 'knight crouch s', 0.25, fromFacing='S', toFacing='S')
        knightSprite.AddStateTransition('leapup', 'moving', 'knight crouch w', 0.25, fromFacing='W', toFacing='W')
        knightSprite.AddStateTransition('leapup', 'moving', 'knight crouch n', 0.25, fromFacing='N', toFacing='N')
        
        knightSprite.AddStateTransition('leapup', 'default', 'knight crouch e', 0.25, fromFacing='E', toFacing='E')
        knightSprite.AddStateTransition('leapup', 'default', 'knight crouch s', 0.25, fromFacing='S', toFacing='S')
        knightSprite.AddStateTransition('leapup', 'default', 'knight crouch w', 0.25, fromFacing='W', toFacing='W')
        knightSprite.AddStateTransition('leapup', 'default', 'knight crouch n', 0.25, fromFacing='N', toFacing='N')
        
        knightSprite.AddStateTransition('moving', 'leapdown', 'knight crouch e', 0.25, fromFacing='E', toFacing='E')
        knightSprite.AddStateTransition('moving', 'leapdown', 'knight crouch s', 0.25, fromFacing='S', toFacing='S')
        knightSprite.AddStateTransition('moving', 'leapdown', 'knight crouch w', 0.25, fromFacing='W', toFacing='W')
        knightSprite.AddStateTransition('moving', 'leapdown', 'knight crouch n', 0.25, fromFacing='N', toFacing='N')
        
        knightSprite.AddStateTransition('leapdown', 'moving', 'knight crouch e', 0.25, fromFacing='E', toFacing='E')
        knightSprite.AddStateTransition('leapdown', 'moving', 'knight crouch s', 0.25, fromFacing='S', toFacing='S')
        knightSprite.AddStateTransition('leapdown', 'moving', 'knight crouch w', 0.25, fromFacing='W', toFacing='W')
        knightSprite.AddStateTransition('leapdown', 'moving', 'knight crouch n', 0.25, fromFacing='N', toFacing='N')
        
        knightSprite.AddStateTransition('leapdown', 'default', 'knight crouch e', 0.25, fromFacing='E', toFacing='E')
        knightSprite.AddStateTransition('leapdown', 'default', 'knight crouch s', 0.25, fromFacing='S', toFacing='S')
        knightSprite.AddStateTransition('leapdown', 'default', 'knight crouch w', 0.25, fromFacing='W', toFacing='W')
        knightSprite.AddStateTransition('leapdown', 'default', 'knight crouch n', 0.25, fromFacing='N', toFacing='N')
        
        # Attacking in each direction
        knightSprite.AddStateTransition('acting', 'melee', 'knight melee pre n', 0.6, toFacing='N')
        knightSprite.AddStateTransition('acting', 'melee', 'knight melee pre e', 0.6, toFacing='E')
        knightSprite.AddStateTransition('acting', 'melee', 'knight melee pre s', 0.6, toFacing='S')
        knightSprite.AddStateTransition('acting', 'melee', 'knight melee pre w', 0.6, toFacing='W')
        
        knightSprite.AddStateSprite('melee', 'knight melee e', facing='E')
        knightSprite.AddStateSprite('melee', 'knight melee s', facing='S')
        knightSprite.AddStateSprite('melee', 'knight melee w', facing='W')
        knightSprite.AddStateSprite('melee', 'knight melee n', facing='N')
        
        return knightSprite
        
    # This is the mage used for the elevation demo
    def GetMageSprite():

        mageSprite = BattleSprite('mage n', anchor=(0.5, 0.9), placeMark=(0,-80))

        # Various directional standing sprites
        mageSprite.AddStateSprite('default', 'mage e', facing='E')
        mageSprite.AddStateSprite('default', 'mage s', facing='S')
        mageSprite.AddStateSprite('default', 'mage w', facing='W')
        mageSprite.AddStateSprite('default', 'mage n', facing='N')

        # Walking in each direction
        mageSprite.AddStateSprite('moving', 'mage walk e', facing='E')
        mageSprite.AddStateSprite('moving', 'mage walk s', facing='S')
        mageSprite.AddStateSprite('moving', 'mage walk w', facing='W')
        mageSprite.AddStateSprite('moving', 'mage walk n', facing='N')
        
        # Jumping upward
        mageSprite.AddStateSprite('leapup', 'mage leap e', facing='E')
        mageSprite.AddStateSprite('leapup', 'mage leap s', facing='S')
        mageSprite.AddStateSprite('leapup', 'mage leap w', facing='W')
        mageSprite.AddStateSprite('leapup', 'mage leap n', facing='N')
        
        # Jumping downward (same sprites, as it happens)
        mageSprite.AddStateSprite('leapdown', 'mage leap e', facing='E')
        mageSprite.AddStateSprite('leapdown', 'mage leap s', facing='S')
        mageSprite.AddStateSprite('leapdown', 'mage leap w', facing='W')
        mageSprite.AddStateSprite('leapdown', 'mage leap n', facing='N')
        
        # Leaping Transitions
        mageSprite.AddStateTransition('moving', 'leapup', 'mage crouch e', 0.25, fromFacing='E', toFacing='E')
        mageSprite.AddStateTransition('moving', 'leapup', 'mage crouch s', 0.25, fromFacing='S', toFacing='S')
        mageSprite.AddStateTransition('moving', 'leapup', 'mage crouch w', 0.25, fromFacing='W', toFacing='W')
        mageSprite.AddStateTransition('moving', 'leapup', 'mage crouch n', 0.25, fromFacing='N', toFacing='N')
        
        mageSprite.AddStateTransition('leapup', 'moving', 'mage crouch e', 0.25, fromFacing='E', toFacing='E')
        mageSprite.AddStateTransition('leapup', 'moving', 'mage crouch s', 0.25, fromFacing='S', toFacing='S')
        mageSprite.AddStateTransition('leapup', 'moving', 'mage crouch w', 0.25, fromFacing='W', toFacing='W')
        mageSprite.AddStateTransition('leapup', 'moving', 'mage crouch n', 0.25, fromFacing='N', toFacing='N')
        
        mageSprite.AddStateTransition('leapup', 'default', 'mage crouch e', 0.25, fromFacing='E', toFacing='E')
        mageSprite.AddStateTransition('leapup', 'default', 'mage crouch s', 0.25, fromFacing='S', toFacing='S')
        mageSprite.AddStateTransition('leapup', 'default', 'mage crouch w', 0.25, fromFacing='W', toFacing='W')
        mageSprite.AddStateTransition('leapup', 'default', 'mage crouch n', 0.25, fromFacing='N', toFacing='N')
        
        mageSprite.AddStateTransition('moving', 'leapdown', 'mage crouch e', 0.25, fromFacing='E', toFacing='E')
        mageSprite.AddStateTransition('moving', 'leapdown', 'mage crouch s', 0.25, fromFacing='S', toFacing='S')
        mageSprite.AddStateTransition('moving', 'leapdown', 'mage crouch w', 0.25, fromFacing='W', toFacing='W')
        mageSprite.AddStateTransition('moving', 'leapdown', 'mage crouch n', 0.25, fromFacing='N', toFacing='N')
        
        mageSprite.AddStateTransition('leapdown', 'moving', 'mage crouch e', 0.25, fromFacing='E', toFacing='E')
        mageSprite.AddStateTransition('leapdown', 'moving', 'mage crouch s', 0.25, fromFacing='S', toFacing='S')
        mageSprite.AddStateTransition('leapdown', 'moving', 'mage crouch w', 0.25, fromFacing='W', toFacing='W')
        mageSprite.AddStateTransition('leapdown', 'moving', 'mage crouch n', 0.25, fromFacing='N', toFacing='N')
        
        mageSprite.AddStateTransition('leapdown', 'default', 'mage crouch e', 0.25, fromFacing='E', toFacing='E')
        mageSprite.AddStateTransition('leapdown', 'default', 'mage crouch s', 0.25, fromFacing='S', toFacing='S')
        mageSprite.AddStateTransition('leapdown', 'default', 'mage crouch w', 0.25, fromFacing='W', toFacing='W')
        mageSprite.AddStateTransition('leapdown', 'default', 'mage crouch n', 0.25, fromFacing='N', toFacing='N')
        
        # Casting in each direction
        mageSprite.AddStateTransition('acting', 'magic', 'mage magic pre n', 0.9, toFacing='N')
        mageSprite.AddStateTransition('acting', 'magic', 'mage magic pre e', 0.9, toFacing='E')
        mageSprite.AddStateTransition('acting', 'magic', 'mage magic pre s', 0.9, toFacing='S')
        mageSprite.AddStateTransition('acting', 'magic', 'mage magic pre w', 0.9, toFacing='W')
        
        mageSprite.AddStateSprite('magic', 'mage magic e', facing='E')
        mageSprite.AddStateSprite('magic', 'mage magic s', facing='S')
        mageSprite.AddStateSprite('magic', 'mage magic w', facing='W')
        mageSprite.AddStateSprite('magic', 'mage magic n', facing='N')
        
        return mageSprite
        
