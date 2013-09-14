# For when I start looking at Spritemanager:
# ui.detached(); b = ui.textbutton(...); sprite = sm.create(b); sprite.x = 100; sprite.y = 100
# sprite.events = True # (for allowing clicks on UI elements, etc.)


init 999 python:
    import sys
    
    # After [hopefully] all other config.layers manipulation, insert the battle layers just below the transient layer
    
    x = config.layers.index('transient')
    
    config.layers = config.layers[:x] + ["battle0", "battle1", "battle2", "battle3", "battle4", "battle5"] + config.layers[x:]
    
    # Python's default stack size is woefully inadequate
    sys.setrecursionlimit(20000)
    

init -10 python:
    
    import math
    from types import *

    ###
    # Styles
    ###
    

    # UIProvider
    style.BattleAnnounce = Style(style.say_thought)
    style.BattleButton = Style(style.button)
    style.BattleButtonText = Style(style.button_text)
    style.BattleMenuWindow = Style(style.menu_window)
    style.BattleMenu = Style(style.menu)
    style.BattleMenuTitle = Style(style.default)
    style.BattleMenuButtonText = Style(style.menu_choice)
    style.BattleMenuButton = Style(style.menu_choice_button)

    style.PickTargetFighterButton = Style(style.BattleButton)
    style.PickTargetFighterText = Style(style.BattleButtonText)
    style.CancelPickTargetFighterButton = Style(style.BattleButton)
    style.CancelPickTargetFighterText = Style(style.BattleButtonText)
    style.PickTargetPositionButton = Style(style.BattleButton)
    style.PickTargetPositionText = Style(style.BattleButtonText)
    style.CancelPickTargetPositionButton = Style(style.BattleButton)
    style.CancelPickTargetPositionText = Style(style.BattleButtonText)
    style.PickTargetFactionButton = Style(style.BattleMenuButton)
    style.PickTargetFactionText = Style(style.BattleMenuButtonText)
    style.PickTargetFactionMenu = Style(style.BattleMenu)
    style.PickTargetFactionMenuWindow = Style(style.BattleMenuWindow)
    style.CancelPickTargetFactionButton = Style(style.BattleButton)
    style.CancelPickTargetFactionText = Style(style.BattleButtonText)
    style.PickSkillText = Style(style.BattleMenuButtonText)
    style.PickSkillButton = Style(style.BattleMenuButton)
    style.PickSkillMenu = Style(style.BattleMenu)
    style.PickSkillMenuTitle = Style(style.BattleMenuTitle)
    style.PickSkillMenuWindow = Style(style.BattleMenuWindow)
    style.PickSubSkillText = Style(style.PickSkillText)
    style.PickSubSkillButton = Style(style.PickSkillButton)
    style.PickSubSkillMenu = Style(style.PickSkillMenu)
    style.PickSubSkillMenuWindow = Style(style.PickSkillMenuWindow)
    style.PickFighterText = Style(style.BattleMenuButtonText)
    style.PickFighterButton = Style(style.BattleMenuButton)
    style.PickFighterMenu = Style(style.BattleMenu)
    style.PickFighterMenuWindow = Style(style.BattleMenuWindow)
    style.EndTurnPickFighterText = Style(style.BattleButtonText)
    style.EndTurnPickFighterButton = Style(style.BattleButton)
    style.EndTurnPickTargetFighterText = Style(style.BattleButtonText)
    style.EndTurnPickTargetFighterButton = Style(style.BattleButton)
    
    style.PickItemText = Style(style.BattleMenuButtonText)
    style.PickItemButton = Style(style.BattleMenuButton)
    style.PickItemMenu = Style(style.BattleMenu)
    style.PickItemMenuWindow = Style(style.BattleMenuWindow)
    style.CancelPickItemButton = Style(style.BattleButton)
    style.CancelPickItemText = Style(style.BattleButtonText)
    
    # Elevation grid pick-position highlight
    style.PickElevationTargetPositionButton = Style(style.PickTargetPositionButton)
    style.PickElevationTargetPositionButton.background = None
    style.PickElevationTargetPositionButton.focus_mask = True
    
    # PanningControls
    style.PanButton = Style(style.BattleButton)
    style.PanButtonText = Style(style.BattleButtonText)
    
    # RotationControls
    style.RotateButton = Style(style.BattleButton)
    style.RotateButtonText = Style(style.BattleButtonText)
    
    # ActiveDisplay
    style.ActiveDisplayGrid = Style(style.default)
    style.ActiveDisplayBox = Style(style.default)
    style.ActiveDisplayWindow = Style(style.window)

    # GridStatsDisplay
    style.GridStatsGrid = Style(style.default)
    style.GridStatsWindow = Style(style.window)

    # Announcer
    style.AnnouncerTextWindow = Style(style.say_window)
    style.AnnouncerText = Style(style.say_thought)
    
    announcer=Character(None, window_style=style.AnnouncerTextWindow, what_style=style.AnnouncerText)

    

    ###
    # Transitions
    ###
    
    # (Note, these are not so widely used as they could be thanks to a Ren'Py bug which makes them uncooperative with panning.)
    
    define.move_transitions("battlemove", 0.5, layers=["battle0", "battle1", "battle2", "battle3", "battle4"])
    define.move_transitions("battleease", 0.5, _ease_time_warp, _ease_in_time_warp, _ease_out_time_warp, layers=["battle0", "battle1", "battle2", "battle3", "battle4"]) 
    
    battleease_start = MoveTransition(0.25, factory=store.MoveFactory(time_warp=_ease_out_time_warp))
    battleease_end = MoveTransition(0.25, factory=store.MoveFactory(time_warp=_ease_in_time_warp))

    
    ###
    # Preferences
    ###
    
    setattr(_preferences, 'battle_skip_movement', False)
    setattr(_preferences, 'battle_skip_combat', False)
    setattr(_preferences, 'battle_skip_incidental', False)
    setattr(_preferences, 'battle_automatic_skill', False)
    setattr(_preferences, 'battle_allow_rollback', False)
    
    
                
        
    class Battle(object):
        def __init__(self, schema):
            
            # Install self as the current battlecontext
            global _battle
            _battle = self
            
            # Display-related stuff
            self._cameraX = 0
            self._cameraY = 0
            self._rotation = 0
            
            self._cameraXLimit=(None, None)
            self._cameraYLimit=(None, None)
            
            
            self._pauseRequest = 0

            if isinstance(schema, BattleSchema) == False:
                raise Exception("Parameter 'schema' is not a valid BattleSchema.")
                
            self._schema = schema
            self._schema.SetBattle(self)

            # General battle stuff
            self._on = False
            self._won = None
            self._layers = self._schema.GetLayers()
            
            if ("BG" in self._layers) == False or ("Fighters" in self._layers) == False or ("Stats" in self._layers) == False or ("Effects" in self._layers) == False or ("UI" in self._layers) == False:
                    raise Exception("Schema GetLayers must return indices for 'BG', 'Fighters', 'Stats', 'Effects' and 'UI'.")
            
            self._mechanic = self._schema.GetMechanic()
            
            if isinstance(self._mechanic, BattleMechanic) == False:
                raise Exception("Schema GetMechanic must return a valid BattleMechanic instance.")
            
            self._attackResolver = self._schema.GetAttackResolver()
            
            if isinstance(self._attackResolver, AttackResolver) == False:
                raise Exception("Schema GetAttackResolver must return a valid AttackResolver instance.")
            
            self._uiProvider = self._schema.GetUIProvider()
            
            if isinstance(self._uiProvider, UIProvider) == False:
                raise Exception("Schema GetUIProvider must return a valid UIProvider instance.")
            
            self._panner = self._schema.GetPanner(self)
            
            if isinstance(self._panner, BattlePanner) == False:
                raise Exception("Schema GetPanner must return a valid BattlePanner instance.")
            
            # Battle-specific setup stuff
            self._fighters = []
            self._scenery = []
            self._factions = []
            self._corpses = []
            self._playerFactions = []
            self._factionLists = {}
            self._extras = []
            self._subscribers = []
            self._conditions = []
            self._currentFaction = None
            self._battlefield = Battlefield()
            
            # Flags to aid errors
            self._battlefieldSet = False
            self._factionSet = False
            
            
        ###
        # Accessors
        
        # This is available for the benefit of the rest of the battle engine, *not* as a method of adding fighters to the battle.
        # Other things need to be done when a Fighter is added, call the AddFighter() method instead.
        def getBattlefield(self):
            return self._battlefield
        Battlefield = property(getBattlefield)
        
        def getScenery(self):
            return self._scenery
        Scenery = property(getScenery)

        def getFighters(self):
            return self._fighters
        Fighters = property(getFighters)
        
        def getCorpses(self):
            return self._corpses
        Corpses = property(getCorpses)
        
        def getAll(self):
            all = self._fighters[:]
            all.extend(self._scenery)
            return all
        All = property(getAll)

        def getFactions(self):
            return self._factions
        Factions = property(getFactions)
        
        def getPlayerFactions(self):
            return self._playerFactions
        PlayerFactions = property(getPlayerFactions)
        
        def getFactionLists(self):
            return self._factionLists
        FactionLists = property(getFactionLists)

        
        def getUI(self):
            return self._uiProvider
        UI = property(getUI)

        ###
        # Display accessors
        
        def getCameraX(self):
            return self._cameraX
        def setCameraX(self, val):
            self._cameraX = val
            if (self._cameraXLimit[0] != None):
                if self._cameraX < self._cameraXLimit[0]:
                    self._cameraX = self._cameraXLimit[0]
            if (self._cameraXLimit[1] != None):
                if self._cameraX > self._cameraXLimit[1]:
                    self._cameraX = self._cameraXLimit[1]
            self._panner.OnPan()
            
        CameraX = property(getCameraX, setCameraX)
        
        def getCameraY(self):
            return self._cameraY
        def setCameraY(self, val):
            self._cameraY = val
            
            if (self._cameraYLimit[0] != None):
                if self._cameraY < self._cameraYLimit[0]:
                    self._cameraY = self._cameraYLimit[0]
            if (self._cameraYLimit[1] != None):
                if self._cameraY > self._cameraYLimit[1]:
                    self._cameraY = self._cameraYLimit[1]
            self._panner.OnPan()

        CameraY = property(getCameraY, setCameraY)     
        
        def getCameraXLimit(self):
            return self._cameraXLimit
        def setCameraXLimit(self, value):
            if (value[0] <= value[1]):
                self._cameraXLimit = value
            else:
                self._cameraXLimit = (value[1], value[0])
            
        CameraXLimit = property(getCameraXLimit, setCameraXLimit)
            
        def getCameraYLimit(self):
            return self._cameraYLimit
        def setCameraYLimit(self, value):
            if (value[0] <= value[1]):
                self._cameraYLimit = value
            else:
                self._cameraYLimit = (value[1], value[0])

        CameraYLimit = property(getCameraYLimit, setCameraYLimit)
        
        def getRotation(self):
            return self._rotation
        def setRotation(self, value):
            self._rotation = value % 360
            
        Rotation = property(getRotation, setRotation)
        
        def BattlePanningFunction(self, transform, st, at):
            return self._panner.Pan(transform, st, at)
        
        ###
        # Battle lifecycle members
        
        def Start(self):
            self._on = True
            
            # Set rollback to battle preference
            self._oldRollback = store._rollback
            store._rollback = _preferences.battle_allow_rollback
            
            self.RunBattle()
        
        def getOn(self):
            return self._on
        On = property(getOn)
        
        def getWon(self):
            return self._won
        Won = property(getWon)
   
        def Win(self, faction):
            self._won = faction
            self.End()
            
        def End(self):
            self.PauseAsRequested()
            
            # Set rollback back to whatever it was before the battle started.
            store._rollback = self._oldRollback
            
            self._on = False
        
        ###
        # Battle setup members
        
        def SetBattlefield(self, battlefield):
            
            if (isinstance(battlefield, Battlefield) == False):
                raise Exception("SetBattlefield must be called with a valid Battlefield instance.")
                    
            self._schema.SetUpBattlefield(battlefield)
            self._battlefield = battlefield
            self._battlefield.SetBattle(self)
            self._battlefieldSet = True
            
            self.RegisterForEvents(battlefield)
        
        def AddFaction(self, faction, playerFaction = True):
            
            if (self._battlefieldSet == False):
                raise Exception("You must call SetBattlefield before AddFaction.")
               
            if (faction != None):
                faction = str(faction)
                
            if (faction == None):
                raise Exception("No faction name specified.")
                
            if (faction in self._factions):
                raise Exception("Faction \"" + faction + "\" already exists in this battle.")
                
            self._factions.append(faction)
            self._factionLists[faction] = []
            self._currentFaction = faction
            
            if playerFaction:
                self._playerFactions.append(faction)
                
            self._factionSet = True
            
        def SetFaction(self, faction):
            
            if (faction in self._factions):
                self._currentFaction = faction
            else:
                raise Exception("Faction \"" + faction + "\" doesn't exist.")            
        
        def AddFighter(self, fighter, **properties):
            
            if (self._factionSet == False):
                raise Exception("You must call AddFaction before AddFighter.")
            
            if (isinstance(fighter, Fighter) == False):
                raise Exception("AddFighter must be called with a valid Fighter instance.")
            
            fighter.Faction = self._currentFaction
            
            self._schema.SetUpFighter(fighter, **properties)
            self._mechanic.SetUpFighter(fighter)
            self._attackResolver.SetUpFighter(fighter)
            self._fighters.append(fighter)
            self._factionLists[self._currentFaction].append(fighter)

            factionNo = self._factions.index(self._currentFaction)
            count = len(self._factionLists[self._currentFaction])
            
            fighter.SetTag("battle_%(f)s_%(no)s_%(name)s" % {"f":factionNo, "no": count, "name": fighter.Name.replace(" ", "_")})

            fighter.SetBattle(self)
            self._battlefield.RegisterFighter(fighter, **properties)
            self.RegisterForEvents(fighter)
            
            
        def AddScenery(self, scenery, **properties):
            
            if (self._battlefieldSet == False):
                raise Exception("You must call SetBattlefield before AddScenery")
            
            scenery.SetBattle(self)
            self._scenery.append(scenery)
            #TODO: There should be a separate RegisterScenery method for Scenery
            self._battlefield.RegisterFighter(scenery, **properties)
            self._battlefield.RegisterScenery(scenery, **properties)
            count = len(self._scenery)
            scenery.SetTag("battle_scenery_%(no)s_%(name)s" % {"no": count, "name": scenery.Name.replace(" ", "_")})
            
            
        def AddExtra(self, extra):

            if (isinstance(extra, Extra) == False):
                raise Exception("AddExtra must be called with a valid Extra instance.")
            
            extra.SetBattle(self)
            self._extras.append(extra)
            
            self.RegisterForEvents(extra)
            
        def AddCondition(self, condition):
            
            if (isinstance(condition, Condition) == False):
                raise Exception("AddCondition must be called with a valid Condition instance.")
                
            condition.SetBattle(self)
            self._conditions.append(condition)
            
            self.RegisterForEvents(condition)
            
        ###
        # Utility members
        
        # Announces the given text
        def Announce(self, text, speaker=None):

            if (speaker == None):
                self._uiProvider.Announce(text)
            else:
                self._uiProvider.Announce(text, speaker)
            
        def GetLayer(self, key):
            return "battle%(x)i" % {"x":self._layers[key]}
            
        def Attack(self, attacker, attack, attributes, target, range=1):
            return self._attackResolver.ResolveAttack(attacker, attack, attributes, target, range)
            
        def GetTargetFactions(self, fighter, targeting=None, skill=None):
            targets = self._battlefield.GetTargetFactions(fighter, targeting=targeting)
            
            if skill == None:
                return targets
            else:
                return skill.FilterTargets(fighter, targets)

        def GetTargetFighters(self, fighter, targeting=None, range=1, los=True, skill=None, callback=None):
            targets = self._battlefield.GetTargetFighters(fighter, targeting=targeting, range=range, los=los, callback=callback)
            
            if skill == None:
                return targets
            else:
                return skill.FilterTargets(fighter, targets)
            
        def GetTargetPositions(self, fighter, position, targeting=None, range=0, los=False, skill=None, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[], callback=None):
            targets = self._battlefield.GetTargetPositions(position, targeting=targeting, range=range, los=los, fightersImpede=fightersImpede, sceneryImpedes=sceneryImpedes, ignoreFactions=ignoreFactions, callback=callback)
            
            if skill == None or fighter == None:
                return targets
            else:
                return skill.FilterTargets(fighter, targets)
            
        def CheckLoS(self, pos, target, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[]):
            return self._battlefield.CheckLoS(pos, target, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[])

        def GetRange(self, pos1, pos2, callback=None):
            return self._battlefield.GetRange(pos1, pos2, callback=callback)
        
        def GetPathLength(self, pos1, pos2, breakPoint=None, callback=None):
            return self._battlefield.GetPathLength(pos1, pos2, breakPoint=breakPoint, callback=callback)
        
        def GetOccupants(self, position):
            return self._battlefield.GetOccupants(position)
            
        def GetFacing(self, source, target):
            return self._battlefield.GetFacing(source, target)
            
        def GetFacingFromAngle(self, angle):
            return self._battlefield.GetFacingFromAngle(angle)
            
        def GetAngleFromFacing(self, facing):
            return self._battlefield.GetAngleFromFacing(facing)
            
        def Rotate(self, degree, recenter=None):
            self._battlefield.Rotate(degree)
            
            if (recenter != None):
                self.CameraX = recenter.Transform.xpos - (config.screen_width / 2)
                self.CameraY = recenter.Transform.ypos - (config.screen_height / 2)
                self._panner.Reset()
                renpy.force_full_redraw()
            
        def getFacings(self):
            return self._battlefield.Facings
        Facings = property(getFacings)
        
        def ChangeFaction(self, fighter, faction):
            self._factionLists[fighter.Faction].remove(fighter)
            self._factionLists[faction].append(fighter)
            fighter.Faction = faction
            
        def GetLoSThreshold(self):
            return self._schema.GetLoSThreshold()
            
        # Allow code to request a pause of <duration> seconds before the next redraw, so they can
        # (for example) allow asynch animations to finish, etc.
        def RequestPause(self, duration):

            if duration > self._pauseRequest:
                self._pauseRequest = duration

        def DecreasePause(self, duration):
            self._pauseRequest = max(self._pauseRequest - duration, 0)

        def Pause(self, duration, hard=False):
            
            self.DecreasePause(duration)
            return renpy.pause(duration, hard=hard)
            
        ###
        # Events
        
        def RegisterForEvents(self, subscriber):
            self._subscribers.append(subscriber)
        
        def UnregisterForEvents(self, subscriber):
            if self._subscribers.count(subscriber) > 0:
                self._subscribers.remove(subscriber)
            
        def Tick(self):
            
            for subscriber in self._subscribers:
                subscriber.Tick()
                
        def StartTurn(self):

            for subscriber in self._subscribers:
                subscriber.StartTurn()

        def EndTurn(self):

            for subscriber in self._subscribers:
                subscriber.EndTurn()

        def FighterStartTurn(self, fighter):
            
            for subscriber in self._subscribers:
                subscriber.FighterStartTurn(fighter)

        def FighterEndTurn(self, fighter):

            if (fighter.Active):
                self.ChangeFighterState(fighter, "default")

            for subscriber in self._subscribers:
                subscriber.FighterEndTurn(fighter)

        def FighterAct(self, fighter, skill):

            self.ChangeFighterState(fighter, "acting")

            for subscriber in self._subscribers:
                subscriber.FighterAct(fighter, skill)

        def FighterDamage(self, fighter, damage, damager):

            self.ChangeFighterState(fighter, "damage")

            for subscriber in self._subscribers:
                subscriber.FighterDamage(fighter, damage, damager)

        def FighterDie(self, fighter):
            
            self.ChangeFighterState(fighter, "dying")

            fighter.Active = False
            
            self._corpses.append(fighter)

            for subscriber in self._subscribers:
                subscriber.FighterDie(fighter)
                
            self.UnregisterForEvents(fighter)
            
        def FighterKilled(self, fighter, killer):
            
            for subscriber in self._subscribers:
                subscriber.FighterKilled(fighter, killer)
            
        def FighterStatChange(self, fighter, stat, oldValue, newValue):
            
            for subscriber in self._subscribers:
                subscriber.FighterStatChange(fighter, stat, oldValue, newValue)
                            
        def PointOfInterest(self, position=None, fighter=None):
            
            for subscriber in self._subscribers:
                subscriber.PointOfInterest(position=position, fighter=fighter)

        def ChangeFighterState(self, fighter, state, facing=None):
            if isinstance(fighter.Sprite, BattleSprite):
                fighter.Sprite.ShowNewState(state, fighter.Tag, fighter.Position, facing=facing)
                
        def RedrawFighter(self, fighter):
            if isinstance(fighter.Sprite, BattleSprite):
                fighter.Sprite.ShowNewState(fighter.Sprite._currentState, fighter.Tag, fighter.Position)
        
        ###
        # Guts
        
        def RunBattle(self):
 
            self._battlefield.Show()
            
            while (self._on):
                
                self.Tick()
                
                self.Show()
                
                self.RunBattleRound()
            
            # After the battle, clear out all the battle layers
            for x in range(6):
                renpy.scene(layer="battle%(x)i" % {"x":x})
        
        def RunBattleRound(self):
            
            self._mechanic.RunBattleRound()
       
        def PauseAsRequested(self):
            if (self._pauseRequest > 0):
                
                _battle.Pause(self._pauseRequest)
            
        def Show(self, blank=True):
            
            # Wait for _pauseRequest seconds in case asynch on-screen animations are yet to finish
            self.PauseAsRequested()
            
            # blank out all the battle layers
            if (blank):
                for x in range(6):
                    renpy.scene(layer="battle%(x)i" % {"x":x})
            
            self._battlefield.Show()
            
            for extra in self._extras:
                extra.Show()
          
                    
    class NestingClass(object):
        
        def __init__(self, child):
            self._child = child
            
        def __getattr__(self, name):
            if name in self.__dict__.keys():
                return object.__getattribute__(self, name)
            else:
                if "_child" in self.__dict__.keys():
                    return getattr(self._child, name)
            return None
            
        def __setattr__(self, name, value):
            if hasattr(object, name):
                object.__setattr__(self, name, value)
                return
            elif hasattr(self._child, name):
                setattr(self._child, name, value)
            object.__setattr__(self, name, value)
            
        def getClass(self):
            return self._child.__class__
        __class__ = property(getClass)
