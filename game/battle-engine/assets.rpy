# First, graphics and animations and stuff like that.

init:
    
    # Background Images
    image bg woodland = 'gfx/battle-bg.jpg'
    image bg woodland simple grid = 'gfx/battle-bg-simple-grid.png'
    image bg woodland iso grid = 'gfx/battle-bg-iso-grid.png'
    image bg woodland path = 'gfx/battle-bg-path.png'
    image bg hex grid = 'gfx/battle-bg-hexes.jpg'
    image bg hex ocean = 'gfx/battle-bg-ocean.png'
    
    image bg rocky valley = 'gfx/scroll-bg.jpg'
    
    # Scenery Images
    image scenery tree = 'gfx/tree.png'
    image scenery rocks = 'scenery/rocks.png'
    image scenery tree solid = 'gfx/tree-solid.png'
    image scenery front = 'gfx/scenery-front-trees.png'

    image scenery rocks 1 = 'gfx/rocks1.png'
    image scenery rocks 2 = 'gfx/rocks2.png'
    
    # UI Images
    
    image iso select = im.MatrixColor("gfx/iso-select.png", im.matrix.opacity(.5))
    image iso select hover = "gfx/iso-select.png"
    
    
    # Character Images
    image bob = 'gfx/bob.png'
    image geoff = 'gfx/geoff.png'
    
    image bandit = 'gfx/bandit.png'
    image bandit chief = 'gfx/bandit_chief.png'
    image demon = 'gfx/gator.png'
    image earth elemental = 'gfx/earth.png'
    image fire elemental = 'gfx/fire.png'
    image water elemental = 'gfx/water.png'

    # Character Portrait Images
    image bob portrait = 'gfx/bob-portrait.jpg'
    image geoff portrait = 'gfx/geoff-portrait.jpg'
    
    image testportrait1 = 'gfx/head1.jpg'
    image testportrait2 = 'gfx/head2.jpg'
    image testportrait3 = 'gfx/head3.jpg'

    # Stan Standing    
    image stan ne = 'gfx/stan-stand-ne.png'
    image stan nw = 'gfx/stan-stand-nw.png'
    image stan se = 'gfx/stan-stand-se.png'
    image stan sw = 'gfx/stan-stand-sw.png'

    # Stan Running
    image stan run ne = anim.Filmstrip('gfx/stan-run-ne.png', (96, 96), (8, 1), 0.1)
    image stan run nw = anim.Filmstrip('gfx/stan-run-nw.png', (96, 96), (8, 1), 0.1)
    image stan run se = anim.Filmstrip('gfx/stan-run-se.png', (96, 96), (8, 1), 0.1)
    image stan run sw = anim.Filmstrip('gfx/stan-run-sw.png', (96, 96), (8, 1), 0.1)
    
    # Boat
    
    image boat n = 'gfx/boat-n.png'
    image boat ne = 'gfx/boat-ne.png'
    image boat nw = 'gfx/boat-nw.png'
    image boat s = 'gfx/boat-s.png'
    image boat se = 'gfx/boat-se.png'
    image boat sw = 'gfx/boat-sw.png'
    
    
    # Images for wargame counters
    
    image red counter knight = 'gfx/counter-knight-red.png'
    image red counter archer = 'gfx/counter-archer-red.png'
    image red counter halberdier = 'gfx/counter-halberdier-red.png'
    image red counter cannon = 'gfx/counter-cannon-red.png'
    image red counter swordsman = 'gfx/counter-swordsman-red.png'

    image blue counter knight = 'gfx/counter-knight-blue.png'
    image blue counter archer = 'gfx/counter-archer-blue.png'
    image blue counter halberdier = 'gfx/counter-halberdier-blue.png'
    image blue counter cannon = 'gfx/counter-cannon-blue.png'
    image blue counter swordsman = 'gfx/counter-swordsman-blue.png'
    
    
    # Fire 1 animation
    image fire 1:
        "gfx/fire-1.png"
        pause 0.10
        "gfx/fire-2.png"
        pause 0.10
        "gfx/fire-3.png"
        pause 0.10
        "gfx/fire-4.png"

    # We'll cheat and just play the fire 1 animation twice for fire 2        
    image fire 2:
        "gfx/fire-1.png"
        pause 0.10
        "gfx/fire-2.png"
        pause 0.10
        "gfx/fire-3.png"
        pause 0.10
        "gfx/fire-4.png"
        pause 0.10
        "gfx/fire-1.png"
        pause 0.10
        "gfx/fire-2.png"
        pause 0.10
        "gfx/fire-3.png"
        pause 0.10
        "gfx/fire-4.png"
        
    image water 1:
        "gfx/water-1.png"
        pause 0.15
        "gfx/water-2.png"
        pause 0.15
        "gfx/water-1.png"
        pause 0.15
        "gfx/water-3.png"
        
    image water 2:
        "gfx/water-1.png"
        pause 0.15
        "gfx/water-2.png"
        pause 0.15
        "gfx/water-1.png"
        pause 0.15
        "gfx/water-3.png"
        pause 0.15
        "gfx/water-1.png"
        pause 0.15
        "gfx/water-2.png"
        pause 0.15
        "gfx/water-1.png"
        pause 0.15
        "gfx/water-3.png"

    image earth 1:
        "gfx/small-earth-1.png"
        pause 0.10
        "gfx/small-earth-2.png"
        pause 0.10
        "gfx/small-earth-3.png"
        pause 0.40
        
    image earth 2:
        "gfx/earth-1.png"
        pause 0.10
        "gfx/earth-2.png"
        pause 0.10
        "gfx/earth-3.png"
        pause 0.40
        
        
    
# Next, we'll define some things which will be useful across all our battle types, like skills    
    
init python:
    
    # Here we're just creating an object as a convenient place to store skills and extras and stuff
    Library = object()
    
    
    # Fill out items
    Library.Items = object()
    Library.Items.Potion = PotionItem(cost=20)
    Library.Items.Superpotion = PotionItem(name="Superpotion", gain=200, cost=100)
    Library.Items.Elixir = ElixirItem(cost=20)
    Library.Items.Superlixir = ElixirItem(name="Superlixir", gain=30, cost=100)

    # Fill out equipment
    Library.Equipment = object()
    
    Library.Equipment.Knife = Weapon("Knife", attack=5, cost=5)
    Library.Equipment.ShortSword = Weapon("Short Sword", attack=7, cost=10)
    Library.Equipment.Sword = Weapon("Sword", attack=10, cost=15)
    Library.Equipment.Spear = Weapon("Spear", attack=12, hands=2, cost=17)
    Library.Equipment.Halberd = Weapon("Halberd", attack=14, hands=2, cost=25)
    
    Library.Equipment.LeatherArmour = Armour("Leather Armour", defence=5, cost=15)
    Library.Equipment.Chainmail = Armour("Chainmail", defence=10, cost=28)
    Library.Equipment.ScaleMail = Armour("Scale Mail", defence=13, cost=45)

    Library.Equipment.RoundShield = Shield("Round Shield", defence=5, cost=10)
    Library.Equipment.Scutum = Shield("Scutum", defence=10, hands=2, cost=30)
    
    Library.Equipment.FeltHat = Helmet("Felt Hat", defence=0, cost=2)
    Library.Equipment.LeatherHelmet = Helmet("Leather Helmet", defence=1, cost=5)
    Library.Equipment.SteelHelmet = Helmet("Steel Helmet", defence=2, cost=10)
    
    Library.Equipment.HealthAmulet = HealthAmulet(cost=300)
    Library.Equipment.AttackAmulet = AttackAmulet(cost=300)

    Library.Skills = object()

    # Now we're creating individual skills one by one and adding them to the library
    Library.Skills.SwordAttack = AttackSkill(command=[('Attack', -1)], multiplier=1.2, sfx="audio/sword.wav")
    Library.Skills.KnifeAttack = AttackSkill(command=[('Attack', -1)], multiplier=0.8, sfx="audio/knife.wav", name="Knife")
    Library.Skills.ClawAttack = AttackSkill(command=[('Attack', -1)], multiplier=1, sfx="audio/sword.wav", name="Slash")

    # Here we're setting the MoveSkill to not end the fighter's turn, so they can take a move and then perform some other action. 
    Library.Skills.Move = MoveSkill(endTurn=False)

    # For Path battles, though, we want the fighter to be able to move /or/ act, so we create a second instance
    # of the MoveSkill with a different value for the parameter:
    Library.Skills.PathMove = MoveSkill(endTurn=True)

    # This version of the move skill is used for the scrolling demo, which need to pan to the
    # fighter's position for each step the fighter takes.
    Library.Skills.ScrollMove = MoveSkill(endTurn=True, poi=True)
    
    # Lastly, this version of the move skill is used for the elevation demo, where we want to
    # enable leaping up/down elevation levels or across short gaps.
    Library.Skills.ElevationMove = MoveSkill(endTurn=True, leap=True, leapUpThreshold=0.35, leapDownThreshold=0.5)
    
    Library.Skills.Skip = SkipSkill(command=[('Skip', 1)], )

    # We'll use this WinSkill to allow the player to end demos that he's had enough of, which don't have
    # a win condition.
    Library.Skills.Win = WinSkill(name="End Demo")
    
    # Some skills may need many parameters because they're specific instances (e.g. 'fireball') of a more generic skill ('magic attack')
    # We'll stick with generic and unimaginative names for now, for simplicity's sake.
    # Spell 1 is a generic single-target attack
    # Spell 2 is a more-powerful version of that attack
    # Spell 3 is a middling power version which attacks everyone in the targeted faction.
    Library.Skills.Fire1 = MagicFighterAttackSkill("Fire 1", command=[("Magic", 5), ("Fire 1", 1)], attributes=['magic', 'fire'], damage=5, cost=5, range=4, sprite=BattleSprite('fire 1', anchor=(0.5, 0.8)), pause=0.4, sfx="audio/fire.wav")
    Library.Skills.Fire2 = MagicFighterAttackSkill("Fire 2", command=[("Magic", 5), ("Fire 2", 2)], attributes=['magic', 'fire'], damage=10, cost=8, range=4, sprite=BattleSprite('fire 2', anchor=(0.5, 0.8)), pause=0.8, sfx="audio/fire2.wav")
    Library.Skills.Fire3 = MagicFactionAttackSkill("Fire 3", command=[("Magic", 5), ("Fire 3", 3)], attributes=['magic', 'fire'], damage=7, cost=10, sprite=BattleSprite('fire 1', anchor=(0.5, 0.8)), pause=0.4, sfx="audio/fire.wav")

    Library.Skills.Water1 = MagicFighterAttackSkill("Water 1", command=[("Magic", 5), ("Water 1", 4)], attributes=['magic', 'water'], damage=5, cost=5, range=4, sprite=BattleSprite('water 1', anchor=(0.5, 0.8)), pause=0.6, sfx="audio/water.wav")
    Library.Skills.Water2 = MagicFighterAttackSkill("Water 2", command=[("Magic", 5), ("Water 2", 5)], attributes=['magic', 'water'], damage=10, cost=8, range=4, sprite=BattleSprite('water 2', anchor=(0.5, 0.8)), pause=1.2, sfx="audio/water2.wav")
    Library.Skills.Water3 = MagicFactionAttackSkill("Water 3", command=[("Magic", 5), ("Water 3", 6)], attributes=['magic', 'water'], damage=7, cost=10, sprite=BattleSprite('water 1', anchor=(0.5, 0.8)), pause=0.6, sfx="audio/water.wav")

    Library.Skills.Earth1 = MagicFighterAttackSkill("Earth 1", command=[("Magic", 5), ("Earth 1", 7)], attributes=['magic', 'earth'], damage=5, cost=5, range=4, sprite=BattleSprite('earth 1', anchor=(0.5, 0.8)), pause=0.6, sfx="audio/earth.wav")
    Library.Skills.Earth2 = MagicFighterAttackSkill("Earth 2", command=[("Magic", 5), ("Earth 2", 8)], attributes=['magic', 'earth'], damage=10, cost=8, range=4, sprite=BattleSprite('earth 2', anchor=(0.5, 0.8)), pause=0.6, sfx="audio/earth2.wav")
    Library.Skills.Earth3 = MagicFactionAttackSkill("Earth 3", command=[("Magic", 5), ("Earth 3", 9)], attributes=['magic', 'earth'], damage=7, cost=10, sprite=BattleSprite('earth 1', anchor=(0.5, 0.8)), pause=0.6, sfx="audio/earth.wav")

    # We'll create alternate spells which use the same sprites for the magic
    # that enemy creatures use:
    Library.Skills.Fireball = MagicFighterAttackSkill("Fireball", attributes=['magic', 'fire'], damage=6, cost=0, range=3, sprite=BattleSprite('fire 1', anchor=(0.5, 0.8)), pause=0.4, sfx="audio/fire.wav")
    Library.Skills.Aqua = MagicFighterAttackSkill("Aqua", attributes=['magic', 'water'], damage=6, cost=0, range=3, sprite=BattleSprite('water 1', anchor=(0.5, 0.8)), pause=0.6, sfx="audio/water.wav")
    Library.Skills.Tremor = MagicFighterAttackSkill("Tremor", attributes=['magic', 'earth'], damage=6, cost=0, range=3, sprite=BattleSprite('earth 1', anchor=(0.5, 0.8)), pause=0.6, sfx="audio/earth.wav")
    
    
    # Other skills
    Library.Skills.Haste = HasteSkill()
    Library.Skills.Item = ItemSkill()
    Library.Skills.Teleport = TeleportSkill()
    
    
    # Lastly, we'll set up some styles.
    # There are many more sub-styles to choose from in the engine.rpy file if you need to.

    # Put a frame around the stats display
    style.ActiveDisplayWindow.background = Frame("gfx/frame.png", 24, 24)
    style.ActiveDisplayWindow.xpadding = 15
    style.ActiveDisplayWindow.ypadding = 15

    style.GridStatsWindow.background = Frame("gfx/frame.png", 24, 24)
    style.GridStatsWindow.xpadding = 15
    style.GridStatsWindow.ypadding = 15

    # Put a frame around the menu    
    style.BattleMenuWindow.background = Frame("gfx/frame.png", 24, 24)
    style.BattleMenuWindow.xpadding = 15
    style.BattleMenuWindow.ypadding = 15
    style.BattleMenuWindow.xalign=0.5
    style.BattleMenuWindow.yalign=0.5

    style.BattleMenuButton.xminimum=200

    # Give buttons a smaller version of the frame (thinner border)    
    style.BattleButton.background = Frame("gfx/frame-small.png", 14, 14)
    style.BattleButton.xpadding = 10
    style.BattleButton.ypadding = 10
    style.BattleButton.xalign = 0.0
    style.BattleButton.yalign = 0.0
    
    # Battle button text should be coloured to denote hover and disabled states
    style.BattleButtonText.color = "#AAA"
    style.BattleButtonText.hover_color = "#FFF"
    style.BattleButtonText.insensitive_color = "#888"
    
    # Battle Menu Buttons shouldn't have graphics, just coloured text 
    style.BattleMenuButton.background=  None
    style.BattleMenuButtonText.color = "#AAA"
    style.BattleMenuButtonText.hover_color = "#FFF"
    style.BattleMenuButtonText.insensitive_color = "#888"
    
    # Target-position buttons should be a little red gem 20x20px
    style.PickTargetPositionButton.background="gfx/gem.png"
    style.PickTargetPositionButton.hover_background ="gfx/gem-hover.png"
    style.PickTargetPositionButton.xpadding = 0
    style.PickTargetPositionButton.ypadding = 0
    style.PickTargetPositionButton.xmaximum=20
    style.PickTargetPositionButton.ymaximum=20
    style.PickTargetPositionButton.xminimum=20
    style.PickTargetPositionButton.yminimum=20
    style.PickTargetPositionButton.clipping=False
    style.PickTargetPositionText.size=5 # Because the default UIProvider puts a space in the box to make it bigger unstyled

    # Target-fighter buttons should be a button with a pointing-hand on it 50x100px
    style.PickTargetFighterButton.background="gfx/pointer_idle.png"
    style.PickTargetFighterButton.hover_background="gfx/pointer_hover.png"
    style.PickTargetFighterButton.xpadding = 0
    style.PickTargetFighterButton.ypadding = 0
    style.PickTargetFighterButton.xmaximum = 50
    style.PickTargetFighterButton.ymaximum = 100
    style.PickTargetFighterButton.xminimum = 50
    style.PickTargetFighterButton.yminimum = 100
    style.PickTargetFighterText.size=5

    # We'll override the default ui.bar bar because I forgot to define a new one for ActiveDisplay...
    style.bar.left_bar = "gfx/left_bar.png"
    style.bar.right_bar = "gfx/right_bar.png"
    style.bar.thumb = None
    
    # Position the directional pan buttons in a D-pan in the top right
    style.PanButton['left'].xminimum = 50
    style.PanButton['left'].xmaximum = 50
    style.PanButton['left'].yminimum = 50
    style.PanButton['left'].ymaximum = 50
    style.PanButton['left'].xpos = 675
    style.PanButton['left'].ypos = 50
    
    style.PanButton['right'].xminimum = 50
    style.PanButton['right'].xmaximum = 50
    style.PanButton['right'].yminimum = 50
    style.PanButton['right'].ymaximum = 50
    style.PanButton['right'].xpos = 750
    style.PanButton['right'].ypos = 50
    
    style.PanButton['up'].xminimum = 50
    style.PanButton['up'].xmaximum = 50
    style.PanButton['up'].yminimum = 50
    style.PanButton['up'].ymaximum = 50
    style.PanButton['up'].xpos = 712
    style.PanButton['up'].ypos = 25
    
    style.PanButton['down'].xminimum = 50
    style.PanButton['down'].xmaximum = 50
    style.PanButton['down'].yminimum = 50
    style.PanButton['down'].ymaximum = 50
    style.PanButton['down'].xpos = 712
    style.PanButton['down'].ypos = 75
    

    # Lastly, the announcer character is used for battle announcements in the default UIProvider, so we'll 
    # create a style for that character so their text gets shown in the appropriate kind of box at the top
    # of the screen.
    
    style.AnnouncerTextWindow = Style(style.say_window)
    style.AnnouncerTextWindow.background = Frame("gfx/frame.png", 24, 24)
    style.AnnouncerTextWindow.xpadding = 30
    style.AnnouncerTextWindow.ypadding = 15
    style.AnnouncerTextWindow.ymargin=10
    style.AnnouncerTextWindow.xalign = 0.5
    style.AnnouncerTextWindow.yalign = 0.0
    style.AnnouncerTextWindow.xminimum = 0
    style.AnnouncerTextWindow.yminimum = 0
    style.AnnouncerTextWindow.xfill = 0
    
    
    style.AnnouncerText = Style(style.say_thought)
    style.AnnouncerText.text_align = 0.5

    announcer=Character(None, window_style=style.AnnouncerTextWindow, what_style=style.AnnouncerText)



    
