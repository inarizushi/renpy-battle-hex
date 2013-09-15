label battle:

    # The Elevation Hex Grid Demo assumes that you've already read and understood the comments
    # in the Elevation Demo, and will not repeat those concepts. Only new things are commented in 
    # this demo.
    
    #play music "audio/battle.ogg" fadein 0.5

    python:
        
        # When using a hex map, we still create a TileMap using the same class as for square grids.
        # Hex battlefields can still be considered to have rectangular areas of spaces, with every
        # other column shifted up by half a space.
        demoTileMap = TileMap("map/hextest.tm")
        
        # This time we use a hex-shaped select highlight image, which matches the size and shape of our hex tiles.
        # We also set a default rotation amount of 60 degrees, since each facing on a hex tile is 60 degrees around
        # from the previous one.
        battle = Battle(CustomSchema(ActiveSchema, attackResolver=ElementalAttackResolver, uiProvider=TileUIProvider(highlight="img/tiles/hex-select.png", rotation=60)))
        
        # Instead of the square grid's ElevationGridSprite, we now use ElevationHexGridSprite for the battlefield
        # sprite - as you can imagine, the difference is that this one draws a hex grid instead of a square one.
        fieldSprite = ElevationHexGridSprite(Image('img/bg/cave.jpg'), demoTileMap, origin=(362, 441), spaceSize=(75, -40), heightStep=100)
        
        battle.SetBattlefield(HexGridBattlefield(fieldSprite, map=demoTileMap, origin=(362, 441), gridSize=(demoTileMap.XSize, demoTileMap.YSize), spaceSize=(75, -40), heightStep=100))
        
        #Add player team
        battle.AddFaction('Player', playerFaction=True)
        
        eileen = PlayerFighter("Eileen", Speed=99, Move=4, Attack=30, Defence=0, Health=10000, sprite=GetClydeHexSprite()) 
        eileen.RegisterSkill(Library.Skills.ElevationMove)
        eileen.RegisterSkill(Library.Skills.Win)
        eileen.RegisterSkill(Library.Skills.Fire1)
        eileen.RegisterSkill(Library.Skills.Skip)
        
        
        battle.AddFighter(eileen, x=0, y=4)
        
        #Add the opposing team
        battle.AddFaction("lucys", playerFaction=False)
        
        lucy = SimpleAIFighter("Lucy", Speed=99, Move=4, Attack=10, Defence=0, Health=50, sprite=GetClydeHexSprite()) 
        lucy.RegisterSkill(Library.Skills.Fire2, 2)
        lucy.RegisterSkill(Library.Skills.ElevationMove, 1)
        battle.AddFighter(lucy, x=1, y=1)
        
        #add extra functionality to game
        battle.AddExtra(RPGActionBob())
        battle.AddExtra(SimpleWinCondition())
        battle.AddExtra(ActionPanner())
        battle.AddExtra(PanningControls(leftLabel=u'pan left', rightLabel=u'pan right', upLabel=u'pan up', downLabel=u'pan down', distance=250))
        battle.AddExtra(ActiveDisplay("Player", {"HP": "Health", "Move": "Move", "MP":"MP"}))
        battle.AddExtra(RPGDeath())
        
        #START!!
        battle.Start()
        
        winner = battle.Won
        
    if (winner == 'Player'):
        return True
    else: 
        return False
    return