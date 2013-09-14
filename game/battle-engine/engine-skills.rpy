init -10 python:
    
    ###
    # TargetData
    # This class contains all the details necessary to describe targeting options
    ###
    
    class TargetData(object):
        
        def __init__(self, fighters=True, positions=False, factions=False, los=True, friendly=True, enemy=True, live=True, dead=False, range=1, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[], callback=None):
            self._fighters = fighters
            self._positions = positions
            self._factions = factions
            self._los = los
            self._friendly = friendly
            self._enemy = enemy
            self._live = live
            self._dead = dead
            self._range = range
            self._fightersImpede = fightersImpede
            self._sceneryImpedes = sceneryImpedes
            self._ignoreFactions = ignoreFactions
            self._callback = callback
        
        def getFighters(self):
            return self._fighters
        
        def getPositions(self):
            return self._positions
            
        def getFactions(self):
            return self._factions
            
        def getLos(self):
            return self._los
            
        def getFriendly(self):
            return self._friendly
            
        def getEnemy(self):
            return self._enemy

        def getLive(self):
            return self._live
            
        def getDead(self):
            return self._dead
            
        def getRange(self):
            return self._range
            
        def getFightersImpede(self):
            return self._fightersImpede
            
        def getSceneryImpedes(self):
            return self._sceneryImpedes
        
        def getIgnoreFactions(self):
            return self._ignoreFactions
            
        def getCallback(self):
            return self._callback
            
        Fighters = property(getFighters)
        Positions = property(getPositions)
        Factions = property(getFactions)
        Los = property(getLos)
        Friendly = property(getFriendly)
        Enemy = property(getEnemy)
        Live = property(getLive)
        Dead = property(getDead)
        Range = property(getRange)
        FightersImpede = property(getFightersImpede)
        SceneryImpedes = property(getSceneryImpedes)
        IgnoreFactions = property(getIgnoreFactions)
        Callback = property(getCallback)
        

        @staticmethod        
        def NoTarget():
            return TargetData(fighters=False, positions=False, factions=False, los=False, friendly=False, range=0)
        
        @staticmethod
        def TargetFightersLos(range=1, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[], callback=None):
            return TargetData(fighters=True, positions=False, factions=False, los=True, friendly=False, range=range, fightersImpede=fightersImpede, sceneryImpedes=sceneryImpedes, ignoreFactions=ignoreFactions, callback=callback)
        
        @staticmethod        
        def TargetFightersNoLos(range=1, callback=None):
            return TargetData(fighters=True, positions=False, factions=False, los=False, friendly=False, range=range, callback=callback)
            
        @staticmethod        
        def TargetPositionsLos(range=1, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[], callback=None):
            return TargetData(fighters=False, positions=True, factions=False, los=True, friendly=True, range=range, fightersImpede=fightersImpede, sceneryImpedes=sceneryImpedes, ignoreFactions=ignoreFactions, callback=callback)
            
        @staticmethod        
        def TargetPositionsNoLos(range=1, callback=None):
            return TargetData(fighters=False, positions=True, factions=False, los=False, friendly=True, range=range, callback=callback)
            
        @staticmethod        
        def TargetFactions():
            return TargetData(fighters=False, positions=False, factions=True, los=False, friendly=False, range=0)

    ###
    # Actionable
    # This class encapsulates a thing that a Fighter can do - it could be a skill like 'Attack' or 'Move', or it could be an item like 
    # 'healing potion' or 'bomb'.
    # Actionables should be singleton/flyweight classes; only one instance and no references back to the 'owning' Fighter.
    ###
    
    class Actionable(object):
        
        def __init__(self):
            self._name = "Actionable"
            self._targets = TargetData.NoTarget()
            self._hotkey = None
            self._weight = 0
    
        def getName(self):
            return self._name
        Name = property(getName)
        
        def getWeight(self):
            if hasattr(self, '_weight'):
                return self._weight
            else:
                return 0
        Weight = property(getWeight)

        def GetTargets(self, fighter):
            return self._targets
    
        def SetUpFighter(self, fighter):
            None
            
        def IsAvailable(self, fighter):
            return True
            
        def PerformAction(self, fighter, target):
            None

            
    ###
    # Skill
    # The Skill class encapsulates a thing that a Fighter can do - e.g. 'Attack' or 'Defend' or 'Move' or 'Summon' or whatever.
    # Ideally, a Skill instance should be a singleton/flyweight class, only one instance and no references back to the parent object. Or at least potentially be used like that.
    ###
    
    # TODO: Skill needs methods to listen to beginning and end of faction turn and Tick
    
    class Skill(Actionable):
        
        def __init__(self, name="Skill", command=None, hotkey=None, weight=0):
            
            if command == None:
                command = [(name, 0)]
            
            self._name = name
            self._command = command
            self._hotkey = hotkey
            self._weight = weight
            
        def RegisterFighter(self, fighter):
            
            nests = self._command[:len(self._command) - 1]
            command = self._command[len(self._command) - 1]
            
            fs = fighter.Skills
            
            for s in nests:
                if (s[0] in fs) == False:
                    fs[s[0]] = ({}, s[1])
                    
                fs = fs[s[0]][0]
            
            fs[command[0]] = (self._name, command[1])
            
            self.SetUpFighter(fighter)
            
        def FighterStartTurn(self, fighter):
            None
            
        def FighterEndTurn(self, fighter):
            None
            
        def FilterTargets(self, fighter, targets):
            return targets
            
        def getHotkey(self):
            if hasattr(self, '_hotkey'):
                return self._hotkey
            else:
                return None
        Hotkey = property(getHotkey)
        
            
    class AttackSkill(Skill):
        
        def __init__(self, multiplier=1, range=1, sfx=None, endTurn=True, name="Attack", command=None, attributes=["melee"], hotkey='a', weight=0):
            self._targets = TargetData.TargetFightersLos(range=range)
            self._endTurn = endTurn
            self._multiplier = multiplier
            self._sfx = sfx
            self._attributes = attributes
            
            super(AttackSkill, self).__init__(name = name, command = command, hotkey = hotkey, weight = weight)
            
        def SetUpFighter(self, fighter):
            fighter.RegisterStat("Attack", 10)
        
        def PerformAction(self, fighter, target):
            if (target != None):
                
                if self._sfx != None:
                    renpy.music.play(self._sfx, channel="sound", loop=False)
                
                face = fighter._battle.GetFacing(fighter.Position, target[0].Position)
                
                if (_preferences.battle_skip_combat == False):
                    fighter._battle.ChangeFighterState(fighter, "melee", facing=face)

                fighter._battle.Attack(fighter, fighter.Stats.Attack * self._multiplier, self._attributes, target[0], target[1])
                
                fighter._battle.ChangeFighterState(fighter, "default")
                
                if (self._endTurn):
                    fighter.EndTurn()
                    
        def IsAvailable(self, fighter):
            targets = fighter._battle.GetTargetFighters(fighter, self._targets, skill=self)
            if len(targets) > 0:
                return True
            else:
                return False

    class MoveSkill(Skill):
        
        def __init__(self, name="Move", command=None, move=3, endTurn=True, hotkey='m', weight=0, poi=False, period=0.5, leap=False, leapUpThreshold=0.3, leapDownThreshold=0.5, leapHeight=50):
            self._move = move
            self._endTurn = endTurn
            self._poi = poi
            self._period = period
            self._leap = leap
            self._leapUpThreshold = leapUpThreshold
            self._leapDownThreshold = leapDownThreshold
            self._leapHeight = leapHeight
            
            super(MoveSkill, self).__init__(name=name, command=command, hotkey=hotkey, weight=weight)
            
        def SetUpFighter(self, fighter):
            fighter.RegisterStat("Move", self._move)
            
        def GetTargets(self, fighter):
            return TargetData.TargetPositionsNoLos(range=fighter.Stats.Move, callback=self.GetCallback())
        
        def GetCallback(self):
            # Here we define a function ("Callback") which will be returned from this function ("GetCallback")
            # The function is passed off to the pathfinding algorithm, so it can call back to this function
            # whenever it needs to know the available spaces to go on to from a given space, and how much
            # each space costs.
            def Callback(pos, battlefield):
                joins = {}
                for pos2 in pos.Joins:
                    
                    # Get the height difference between the two positions
                    adh = pos2.Height - pos.Height
                    dh = adh
                    
                    # If the height is negative (we're going downhill) then write off the first
                    # 0.5 difference (it's faster going downhill, but takes more energy -
                    # so we don't want to make it cost more, but we won't make it cost less either.
                    if (dh < 0):
                        dh = min(dh + 0.5, 0)
                        #print "letting off 0.5 cost: dh now " + str(dh)
                    
                    # Allow traversal between 0.5 height and 2 depth 
                    if (dh < 0.5 and dh > -2):
                        joins[pos2] = 1 + math.fabs(dh)
                        
                    # If the next tile is below this one, check to see if we can jump
                    # over it to the next tile along
                    # (Games developers may wish to expand this check to include jumping over
                    # rivers, fences, bodies, whatever...)
                    # Check against the actual dh because we still want to allow jumps over short drops
                    # if it's actually more efficient.
                    if adh < 0:
                        if battlefield != None and isinstance(battlefield, GridBattlefield):
                            
                            for pos3 in pos2.Joins:
                                if (pos3 in pos.Joins) == False:
                                    dh = pos3.Height - pos.Height
                                    # We'll allow the jump so long as the target space is no more than .25 higher
                                    # or .5 lower than the space we're moving from - and it costs two movement + diff.
                                    if dh <= 0.25 and dh >= -0.5:
                                        # Add an extra 0.5 move to make it probably not cheaper than an equivalent walking route if one exists (e.g. jumping across diagonals)
                                        joins[pos3] = battlefield.GetRange(pos, pos3, useHeight=False) + 0.5
                        
                return joins
                
            return Callback
        
        def IsAvailable(self, fighter):
            return fighter.Stats.Move > 0
        
        def PerformAction(self, fighter, target):
            if (self.IsAvailable(fighter)):
                if (target != None):
                    
                    path = target[1][1][1:]
                    if (target[0] != fighter.Position):
                        path.append(target[0])
                    
                    # Default the 'do we skip animation?' variable to the skip-movement-animation preference
                    skip = _preferences.battle_skip_movement
                    
                    for step in path:
                        
                        # We have to decide whether we adjust the fighter's z (depth) at the
                        # beginning or the end of their movement between this square and the next.
                        # If the fighter is moving forwards, 'out' of the screen, we adjust their
                        # z immediately, so they don't appear 'behind' the square they're moving
                        # to - especially important for tile-based maps.
                        # If the fighter is moving backwards, 'into' the screen, we adjust their
                        # z at the end of their movement, so they don't skip to 'behind' the square
                        # they're leaving immediately, which would also look weird.
                        zAtStart = True
                        if (step.Z < fighter.Position.Z):
                            zAtStart = False
                            
                        
                        if (skip == False):
                            fighter.Transition(None)
                            
                            leapStep = False
                            movingState = "moving"
                            
                            face = fighter._battle.GetFacing(fighter.Position, step)
                            
                            if self._leap:
                                dh = step.Height - fighter.Position.Height
                                
                                dx = step.X - fighter.Position.X
                                dy = step.Y - fighter.Position.Y
                                stepDist = math.sqrt((dx*dx)+(dy*dy))
                                
                                
                                
                                if dh >= 0:
                                    if (dh >= self._leapUpThreshold) or (stepDist >= 2):
                                        leapStep = True
                                        movingState = "leapup"
                                else:
                                    if ((dh * -1) >= self._leapDownThreshold) or (stepDist >= 2):
                                        leapStep = True
                                        movingState = "leapdown"
                                    
                                if leapStep:
                                    fighter._battle.ChangeFighterState(fighter, "moving", facing=face)
                            
                            
                            
                            if zAtStart:
                                z = step.Z
                            else:
                                z = fighter.Position.Z
                            
                            fighter.Show(zorder=z)
                            
                            face = fighter._battle.GetFacing(fighter.Position, step)
                            
                            fighter._battle.ChangeFighterState(fighter, movingState, facing=face)
                            fighter.Facing = face
                            
                            if (leapStep):
                                mf = MoveJumpFunction(fighter.Position.Transform.xpos, fighter.Position.Transform.ypos, step.Transform.xpos, step.Transform.ypos, period=self._period, height=self._leapHeight)
                            else:
                                mf = MoveFunction(fighter.Position.Transform.xpos, fighter.Position.Transform.ypos, step.Transform.xpos, step.Transform.ypos, period=self._period)
                            
                            fighter.Position = step
                            
                            fighter.Show(transforms=[Transform(function=mf)], zorder=z)
                            
                            
                            if (self._poi):
                                _battle.PointOfInterest(position=step, fighter=fighter)
                                
                            skip = _battle.Pause(self._period)
                            
                            if zAtStart == False:
                                fighter.Show(zorder=step.Z)
                                
                            if (leapStep):
                                fighter._battle.ChangeFighterState(fighter, "moving", facing=face)

                    fighter.Position = target[0]
                    fighter.Stats.Move = fighter.Stats.Move - target[1][0]
                    
                    fighter._battle.Show()
                    
                    fighter._battle.PointOfInterest(position=fighter.Position, fighter=fighter)
                    fighter._battle.FighterAct(fighter, self)

                    
                    # Change state back to default after we're finished
                    fighter._battle.ChangeFighterState(fighter, "default")
                    
                    if (self._endTurn):
                        fighter.EndTurn()
                    
        def FighterStartTurn(self, fighter):
            fighter.Stats.Move = fighter.BaseStats.Move
    
    class MagicFighterAttackSkill(Skill):
        
        def __init__(self, name="Magic Fighter Attack", command=None, attributes=['magic'], damage=1, cost=1, range=5, sprite=None, pause=0, sfx=None, endTurn=True, hotkey=None, weight=0):
            self._damage = damage
            self._cost = cost
            self._targets = TargetData.TargetFightersLos(range=range)
            self._sprite = sprite
            self._pause = pause
            self._sfx = sfx
            self._endTurn = endTurn
            self._attributes = attributes
            
            if command == None:
                command = [("Magic", 5), (name, 0)]
            
            super(MagicFighterAttackSkill, self).__init__(name=name, command=command, hotkey=hotkey, weight=weight)


            
        def SetUpFighter(self, fighter):
            fighter.RegisterStat("Magic", 10)
            fighter.RegisterStat("MP", 10)

        def PerformAction(self, fighter, target):
            if (self.IsAvailable(fighter)):
                if (target != None):
                    
                    fighter.Stats.MP = fighter.Stats.MP - self._cost

                    if self._sfx != None:
                        renpy.music.play(self._sfx, channel="sound", loop=False)
                    
                    face = fighter._battle.GetFacing(fighter.Position, target[0].Position)
                    
                    if (_preferences.battle_skip_incidental == False):
                        fighter._battle.ChangeFighterState(fighter, "magic", facing=face)

                    # Make sure that the camera centres on the target before the spell goes off
                    fighter._battle.PointOfInterest(fighter=target[0])
                    
                    if self._sprite != None and self._pause > 0:
                        offset = Transform(xanchor=self._sprite.Anchor[0], yanchor=self._sprite.Anchor[1])
                        tag = "MagicFighterAttackSkill_"+target[0].Tag+"_"+str(renpy.random.random()*1000)
                        l = fighter._battle.GetLayer('Fighters')
                        renpy.show(tag, what=self._sprite, at_list=[target[0].Position.Transform, offset], layer=l, zorder=target[0].Position.Z + 0.001)
                        if (_preferences.battle_skip_combat == False):
                            _battle.Pause(self._pause)
                        renpy.hide(tag, layer=l)
                        
                    fighter._battle.Attack(fighter, fighter.Stats.Magic * self._damage, self._attributes, target[0], target[1])
                    
                    fighter._battle.ChangeFighterState(fighter, "default", facing=face)

                    
                    if (self._endTurn):
                        fighter.EndTurn()
                        
        def IsAvailable(self, fighter):
            if fighter.Stats.MP < self._cost:
                return False
            targets = fighter._battle.GetTargetFighters(fighter, self._targets, skill=self)
            if len(targets) > 0:
                return True
            else:
                return False

                    
    class MagicFactionAttackSkill(Skill):
        
        def __init__(self, name="Magic Faction Attack", command=None, attributes=['magic'], damage=1, cost=2, sprite=None, pause=0, sfx=None, endTurn=True, hotkey=None, weight=0):
            self._damage = damage
            self._cost = cost
            self._targets = TargetData.TargetFactions()
            self._sprite = sprite
            self._pause = pause
            self._sfx = sfx
            self._attributes = attributes
            self._endTurn = endTurn
            
            if command == None:
                command = [('Magic', 5), (name, 0)]
            
            super(MagicFactionAttackSkill, self).__init__(name=name, command=command, hotkey=hotkey, weight=weight)

            
        def SetUpFighter(self, fighter):
            fighter.RegisterStat("Magic", 10)
            fighter.RegisterStat("MP", 10)
            
        def PerformAction(self, fighter, target):
            if (self.IsAvailable(fighter)):
                if (target != None):
                    
                    fighter.Stats.MP = fighter.Stats.MP - self._cost

                    sprites=[]
                    l = fighter._battle.GetLayer('Fighters')
                            
                    if self._sfx != None:
                        renpy.music.play(self._sfx, channel="sound", loop=False)

                    if (_preferences.battle_skip_incidental == False):
                        fighter._battle.ChangeFighterState(fighter, "magic")

                    if self._sprite != None and self._pause > 0:
                        
                        for t in fighter._battle.FactionLists[target]:
                        
                            if t.Active:
                                offset = Transform(xanchor=self._sprite.Anchor[0], yanchor=self._sprite.Anchor[1])
                                tag = "MagicFactionAttackSkill_"+t.Tag+"_"+str(renpy.random.random())
                                
                                sprites.append(tag)
                                renpy.show(tag, what=self._sprite, at_list=[t.Position.Transform, offset], layer=l, zorder=t.Position.Z + 0.001)
                    
                    if (_preferences.battle_skip_combat == False):
                        _battle.Pause(self._pause)
                        
                    for s in sprites:
                        renpy.hide(s, layer=l)

                    for t in fighter._battle.FactionLists[target][:]:
                        if t.Active:
                            fighter._battle.Attack(fighter, fighter.Stats.Magic * self._damage, self._attributes, t, 0)

                    fighter._battle.ChangeFighterState(fighter, "default")

                    if (self._endTurn):
                        fighter.EndTurn()        
        
        def IsAvailable(self, fighter):
            if fighter.Stats.MP < self._cost:
                return False
            targets = fighter._battle.GetTargetFactions(fighter, self._targets, skill=self)
            if len(targets) > 0:
                return True
            else:
                return False
                
                
    class ItemSkill(Skill):
        
        def __init__(self, name='Item', command=None, hotkey='i', weight=0):
            self._targets = TargetData.NoTarget()

            super(ItemSkill, self).__init__(name=name, command=command, hotkey=hotkey, weight=weight)
            
        def PerformAction(self, fighter, target):
            
            battle = fighter._battle
            
            item = battle.UI.PickItem(fighter.Inventory.GetItems())
            
            if item == None:
                return
                
            #TODO: refactor target-picking code somewhere else, there's duplication between this and PlayerFighter

            target = None
            noTarget = False
            
            targetData = item.GetTargets(fighter)
            
            
            # Check for different types of targeting in most-general to most-specific order
            if (targetData.Factions):
                targets = fighter._battle.GetTargetFactions(fighter, targeting=targetData, skill=self)
                target = fighter._battle.UI.PickTargetFaction(fighter, targets)
                None
            elif (targetData.Positions):
                targets = fighter._battle.GetTargetPositions(fighter, fighter.Position, targeting=targetData, skill=self)
                target = fighter._battle.UI.PickTargetPosition(fighter, targets)
            elif (targetData.Fighters):
                targets = fighter._battle.GetTargetFighters(fighter, targeting=targetData, skill=self)
                target = fighter._battle.UI.PickTargetFighter(fighter, targets)
            else:
                noTarget = True

            if (target != None) or (noTarget == True):

                if (_preferences.battle_skip_incidental == False):
                    fighter._battle.ChangeFighterState(fighter, "item")

                fighter.Inventory.RemoveItem(item, 1)
                item.PerformAction(fighter, target)
                fighter.EndTurn()
                
                fighter._battle.ChangeFighterState(fighter, "default")

            
            
    
    class SkipSkill(Skill):
        
        def __init__(self, name="End Turn", command=None, hotkey='e', weight=0):
            self._targets = TargetData.NoTarget()

            super(SkipSkill, self).__init__(name=name, command=command, hotkey=hotkey, weight=weight)

            
        def PerformAction(self, fighter, target):
            fighter.EndTurn()
            
    class WaitSkill(Skill):
        
        def __init__(self, name="Wait", command=None, hotkey='w', weight=0):
            self._targets = TargetData.NoTarget()

            super(SkipSkill, self).__init__(name=name, command=command, hotkey=hotkey, weight=weight)
            
        def PerformAction(self, fighter, target):
            p = fighter.Priority - 25
            fighter.EndTurn()
            fighter.Priority = p
            
    class HasteSkill(Skill):
        
        def __init__(self, name="Haste", command=None, hotkey='h', weight=0, turns=2):

            self._targets = TargetData(fighters=True, los=True, friendly=True, enemy=False, range=4)

            if command == None:
                command=[("Magic",5), (name,0)]
            
            super(HasteSkill, self).__init__(name=name, command=command, hotkey=hotkey, weight=weight)
            
            self._turns = turns
            
        def SetUpFighter(self, fighter):
            fighter.RegisterStat("MP", 10)
            
        def IsAvailable(self, fighter):
            return fighter.Stats.MP >= 5
            
        def PerformAction(self, fighter, target):
            
            f = target[0]
            
            face = fighter._battle.GetFacing(fighter.Position, target[0].Position)
            fighter.Facing = face
                    
            if (_preferences.battle_skip_incidental == False):
                fighter._battle.ChangeFighterState(fighter, "magic", facing=face)

            
            f.AddEffect("Haste", HasteEffect(f, self._turns))
            
            fighter._battle.ChangeFighterState(fighter, "default", facing=face)

            
            fighter.EndTurn()
            
    class TeleportSkill(Skill):
        
        def __init__(self, name="Teleport", command=None, hotkey='t', weight=0, endTurn=False):
            
            self._targets = TargetData.TargetPositionsLos(range=20)
            self._endTurn = endTurn

            if command==None:
                command=[("Magic", 5), (name,0)]

            super(TeleportSkill, self).__init__(name=name, command=command, hotkey=hotkey, weight=weight)
            
        def PerformAction(self, fighter, target):
            
            if (_preferences.battle_skip_incidental == False):
                fighter._battle.ChangeFighterState(fighter, "magic")

            p = target[0]
            
            line = fighter._battle._battlefield.GetPositionsInLine(fighter.Position, p)
            
            for pos in line:
                fighter.Position = pos
                fighter.Show()
                fighter._battle.Announce(str(pos.X) + ', ' + str(pos.Y))
            
            if (self._endTurn):
                fighter.EndTurn()
                
            fighter._battle.ChangeFighterState(fighter, "default")

            
    # This skill just wins the game for the current faction. Obviously it's not that useful for most games, but
    # it's a handy get-out-of-a-demo-with-only-one-fighter-in skill...! ;-)
    class WinSkill(Skill):
        
        def __init__(self, name="Win", command=None, hotkey='w', weight=0):
            self._targets = TargetData.NoTarget()
            
            if command == None:
                command = [(name, weight)]
                
            super(WinSkill, self).__init__(name=name, command=command, hotkey=hotkey, weight=weight)
            
        def PerformAction(self, fighter, target):
            
            fighter._battle.End()
            fighter._battle.Win(fighter.Faction)
