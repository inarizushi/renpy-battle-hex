init -10 python:
    

    ###
    # FighterStats
    # This class provides stat-modification; calls back to the fighter so that class can munge based on
    # equipment, effects and so on.
    ###
    
    class FighterStats(object):
        def __init__(self, fighter):
            self._fighter = fighter
            
        def __getattribute__(self, name):
            
            # If it's an attribute that's been added to the instance, then pass it off to be modified.
            # (Ignore '_fighter' 'cause it's the one instance attribute on this instance.
            if name == "_fighter":
                return object.__getattribute__(self, name)
            
            if hasattr(self, "_fighter"):
                if name in self._fighter.GetStatsList():
                    value = getattr(self._fighter.RawStats, name)
                    
                    for effect in self._fighter.Effects:
                        value = effect.OnRetrieveStat(name, value)
                        
                    for equipment in self._fighter.Equipment.All:
                        value = equipment.OnRetrieveStat(name, value)
                    
                    return round(value*100000)/100000
            
            return object.__getattribute__(self, name)
            
        def __setattr__(self, name, value):
            
            if name == "_fighter" or hasattr(object, name):
                object.__setattr__(self, name, value)
                return
            else:
                # Do the setting in the complete opposite order to the getting, just to be as safe as possible.
                e = self._fighter.Equipment.All[:]
                e.reverse()

                for equipment in e:
                    value = equipment.OnSetStat(name, value)
                
                e = self._fighter.Effects[:]
                e.reverse()
                for effect in e:
                    value = effect.OnSetStat(name, value)
                
                if hasattr(self._fighter, "_battle"):
                    self._fighter._battle.FighterStatChange(self._fighter, name, getattr(self._fighter.RawStats, name), value)
                setattr(self._fighter.RawStats, name, value)
                return
                    
            
        def __hasattr__(self, name):
            

            if hasattr(object, name):
                return True
            elif hasattr(self._fighter, name):
                return True
            else:
                return False
    
    
    

    ###
    # Fighter
    # The Fighter class is the base class for all player-characters and enemies in the battle
    ###

    # The base class provides common functionality only, but would not function normally within a battle.
    class Fighter(BattleAware):
        def __init__(self, name, sprite=BattleDisplayable(None), blocksPosition=True, blocksLoS=True, attributes=[], portrait=None, **stats):
            self._name = name
            self._prioritiser = Prioritiser(self)
            self._sprite = sprite
            self._attributes = attributes
            self._blocksPosition = blocksPosition
            self._blocksLoS = blocksLoS
            self._portrait = portrait
            
            if isinstance(self._sprite, BattleDisplayable) == False:
                self._sprite = BattleSprite(self._sprite)
                self._sprite.SetBattle(self._battle)
            
            self._faction = 0
            self._turnComplete = True
            self._active = True
            self._position = None
            self._tag = None
            self._facing = None
            
            # Fighters which have stats which describe how they are
            self._statsList = []
            self._stats = FighterStats(self)
            self._rawStats = object()
            self._baseStats = object()
            
            for stat in iter(stats):
                self.RegisterStat(stat, stats[stat])
            
            # Each fighter has a list of effects which are currently applied to that fighter
            self._effects = {}
            
            # Fighters have skills which describe what they can do
            # We default to just Attack, because it's something nearly everybody is going to want.
            # The _skills member is a dictionary mapping labels/commands (as may be seen in a UI) to a tuple (name, weight).
            # - name is skill names (which are strings that get passed to the Act method and are a key to the _skillHandlers dict)
            # - weight is a numeric ordering by which to sort the labels when presented to the user in menus
            # Skill results may also be dicts for further nested skill 'menus'.
            self._skills = {}
            
            # _skillHandlers is a dict mapping skill names to the handler classes for actioning those skills.
            self._skillHandlers = {}
                
            self._inventory = BattleInventory()
            self._equipment = FighterEquipment()
            
            self._playerControlled = False
            self._invulnerable = False

        
            # All fighters have health (of some kind), and it's more convenient to keep it here
            self.RegisterStat("Health", 100)
            
        
        # Setup methods
        def SetPrioritiser(self, prioritiser):
            self._prioritiser = prioritiser
        
        def SetSprite(self, sprite):
            self._sprite = sprite

        def SetBattle(self, battle):
            self._battle = battle
            self._sprite.SetBattle(battle)
            
        def SetTag(self, tag):
            self._tag = tag
            
        # Add a skill to this fighter's list of abilities
        def RegisterSkill(self, skill):
            if (skill.Name in self._skillHandlers) == False:
                self._skillHandlers[skill.Name] = skill
                skill.RegisterFighter(self)
            
        # State methods
        def getFaction(self):
            return self._faction
        def setFaction(self, val):
            self._faction = val
        Faction = property(getFaction, setFaction)

        def getTurnComplete(self):
            return self._turnComplete
        TurnComplete = property(getTurnComplete)
        
        def getName(self):
            return self._name
        Name = property(getName)
        
        def getAttributes(self):
            return self._attributes
        Attributes = property(getAttributes)
        
        def getActive(self):
            return self._active
        def setActive(self, val):
            self._active = val
        Active = property(getActive, setActive)
        
        def getBlocksPosition(self):
            return self._blocksPosition
        def setBlocksPosition(self, val):
            self._blocksPosition = val
        BlocksPosition = property(getBlocksPosition, setBlocksPosition)

        def getBlocksLoS(self):
            return self._blocksLoS
        def setBlocksLoS(self, val):
            self._blocksLoS = val
        BlocksLoS = property(getBlocksLoS, setBlocksLoS)
        
        def getPlaceMark(self):
            return self._sprite.PlaceMark
        PlaceMark = property(getPlaceMark)
        
        def getFacing(self):
            return self._facing
        def setFacing(self, val):
            if val == None:
                return
            
            if self._battle == None:
                raise Exception('Fighter does not have a facing until it has been added to a battle')
            else:
                invalid = True
                if isinstance(val, BattleFacing) == False:
                    if (val in self._battle.Facings.keys()):
                        invalid = False
                        val = self._battle.Facings[val]
                else:
                    if (val in self._battle.Facings.values()):
                        invalid = False
                        
                if invalid:                    
                    raise Exception('Facing ' + str(val) + ' not valid for this battle.')
                else:
                    if self._facing != val:
                        self._facing = val
                        self._sprite.Facing = val.Name
                        #TODO: update sprite when not in init
        Facing = property(getFacing, setFacing)
        
        def getPlayerControlled(self):
            return self._playerControlled
        PlayerControlled = property(getPlayerControlled)
        
        def getInvulnerable(self):
            return self._invulnerable
        def setInvulnerable(self, value):
            self._invulnerable = value
        Invulnerable = property(getInvulnerable, setInvulnerable)
        
        def getStats(self):
            return self._stats
        Stats = property(getStats)
        
        def GetStat(self, stat):
            if hasattr(self.RawStats, stat):
                return getattr(self.Stats, stat)
            else:
                return None
                
        def SetStat(self, stat, value):
            setattr(self.RawStats, stat, value)

        def getRawStats(self):
            return self._rawStats
        RawStats = property(getRawStats)

        def getBaseStats(self):
            return self._baseStats
        BaseStats = property(getBaseStats)
        
        def GetBaseStat(self, stat):
            if hasattr(self.BaseStats, stat):
                return getattr(self.BaseStats, stat)
            else:
                return None
                
        def SetBaseStat(self, stat, value):
            setattr(self.BaseStats, stat, value)

        def RegisterStat(self, stat, default):
            
            if (self.GetStat(stat) == None):
                self._statsList.append(stat)
                self.SetStat(stat, default)
            if (self.GetBaseStat(stat) == None):
                self.SetBaseStat(stat, default)
                
        def GetStatsList(self):
            if hasattr(self, "_statsList"):
                return self._statsList[:]
            else:
                return []
                
        def getSkills(self):
            return self._skills
        Skills = property(getSkills)
        
        def getPosition(self):
            return self._position
        def setPosition(self, val):
            self._position = val
        Position = property(getPosition, setPosition)
            
        def getSprite(self):
            return self._sprite
        Sprite = property(getSprite)
        
        def getPortrait(self):
            return self._portrait
        Portrait = property(getPortrait)
        
        def getTag(self):
            return self._tag
        Tag = property(getTag)
        
        
        def AddEffect(self, name, effect):
            self._effects[name] = effect
            self._battle.RegisterForEvents(effect)
        
        def RemoveEffect(self, name):

            if name in self._effects.keys():
                self._effects[name].Hide()
                del self._effects[name]
                self._battle.UnregisterForEvents(name)
                

                
        def getEffects(self):
            return self._effects.values()
        Effects = property(getEffects)
            
        
        def getInventory(self):
            return self._inventory
        def setInventory(self, value):
            self._inventory = value
        Inventory = property(getInventory, setInventory)
        
        def getEquipment(self):
            return self._equipment
        def setEquipment(self, value):
            self._equipment = value
        Equipment = property(getEquipment, setEquipment)
        
        def getDebug(self):
            #First, output the name of this fighter
            out = self.Name
            
            fighterStats = dir(self.Stats)
            
            # Take a new object for reference, to check which attributes are new to Stats
            test = object()
            
            # Go through all the attributes of the stats object;
            # assume that any which don't also exist on the test object are game stats of this Fighter and output them 
            for stat in fighterStats:
                if (hasattr(test, stat)) == False:
                    out = "%(o)s %(st)s: %(v)s" % {"o": out, "st": stat, "v": str(self.GetStat(stat))}
            
            out = "\n%(o)s Priority: %(p)s" % {"o": out, "p": self.Priority}
            
            out = "%(o)s Position: %(x)i, %(y)i" % {"o": out, "x": self.Position.X, "y": self.Position.Y}
            
            return out
        Debug = property(getDebug)
            
        # Event methods
        def Tick(self):
            self._prioritiser.Tick()

        def StartTurn(self):
            self._prioritiser.StartTurn()
            
            for skill in self._skillHandlers.values():
                skill.FighterStartTurn(self)
            
            self._turnComplete = False
            
        def EndTurn(self):
            self._prioritiser.EndTurn()
            
            for skill in self._skillHandlers.values():
                skill.FighterEndTurn(self)

            self._turnComplete = True
            
            self._battle.FighterEndTurn(self)
        
        def Act(self):
            None
        
        def PerformAction(self, action):
            None
            
        def Damage(self, damage, damager):

            if self.Invulnerable:
                damage = 0
                self._battle.FighterDamage(self, damage, damager)
            else:
            
                # Cap health at base health or current health, whichever is higher.
                maxHealth = max(self.Stats.Health, self.BaseStats.Health)
                minHealth = 0
                
                self.Stats.Health = self.Stats.Health - damage
                
                self._battle.FighterDamage(self, damage, damager)
                
                if self.Stats.Health > maxHealth:
                    self.Stats.Health = maxHealth
                    
                if self.Stats.Health <= minHealth:
                    self.Stats.Health = minHealth
                    self.Die()
                    self._battle.FighterKilled(self, damager)

        def Die(self):
            self.Active = False
            if self._turnComplete == False:
                self.EndTurn()
            self._battle.FighterDie(self)
            self.Hide()
            

        
        # Prioritiser-Specific call-throughs
        def getPriority(self):
            return self._prioritiser.Priority
        def setPriority(self, value):
            self._prioritiser.Priority = value
            
        Priority = property(getPriority, setPriority)
        
        def Show(self, tag=None, what=None, position=None, transforms=[], layer=None, zorder=None):

            if tag == None:
                tag = self._tag
            if layer == None:
                layer = self._battle.GetLayer("Fighters")
            if zorder == None:
                zorder = self._position.Z
            if what == None:
                what = self._sprite
            if what == None: # still...
                renpy.hide(tag, layer=layer)
                return
            if isinstance(what, BattleDisplayable):
                # TODO: set anchor to something in an else, so it doesn't break later if it's not a BattleDisplayable!
                anchor = Transform(xanchor=what.Anchor[0], yanchor=what.Anchor[1])
            if position == None:
                position = self._position.Transform
                
            #position.set_child(what)            
                
            transforms = transforms[:]
            #transforms.append(position)
            #transforms.append(anchor)
            
            t = [position, anchor]
            t.extend(transforms)
            
            renpy.show(tag, what=what, at_list=t, layer=layer, zorder=zorder)
            
            for effect in self._effects.values():
                effect.Show(transforms=transforms, layer=layer, zorder=zorder+1)

                
                
        def Transition(self, transition, layer=None):
            if layer == None:
                layer = self._battle.GetLayer("Fighters")
            
            renpy.transition(transition, layer=layer)
            
            for effect in self._effects.values():
                effect.Transition(transition, layer=layer)

        
        def Hide(self):
            layer = self._battle.GetLayer("Fighters")
            renpy.hide(self._tag, layer=layer)
            
            for effect in self._effects.values():
                effect.Hide()

    ###
    # Scenery
    # A type of fighter which isn't really a fighter
    ###
    
    class Scenery(Fighter):
        
        def __init__(self, name, transparent=False, **stats):
            super(Scenery, self).__init__(name, **stats)
            self._transparent = transparent
        
        def Show(self, tag=None, what=None, position=None, transforms=[], layer=None, zorder=None):
            
            if zorder == None:
                zorder = self._position.Z

            
            if (self._transparent):
                
                super(Scenery, self).Show(tag=self._tag+"_Base", what=what, position=position, transforms=[], layer=self._battle.GetLayer("BG"), zorder=1)

                tl = [Transform(alpha=0.75)]
                # Just using 0.001 as a Z offset to make sure that 
                super(Scenery, self).Show(tag=tag, what=what, position=position, transforms=tl, layer=layer, zorder=zorder+0.001)
            else:
                super(Scenery, self).Show(tag=tag, what=what, position=position, transforms=transforms, layer=layer, zorder=zorder+0.001)

        def Hide(self):
            super(Scenery, self).Hide()
            renpy.hide(self._tag+"_Base")
            
    class AreaScenery(Scenery):
        
        def __init__(self, name, transparent=False, area=(1,1), **stats):
            super(AreaScenery, self).__init__(name, transparent=transparent, **stats)
            self._area = area
            
        def getArea(self):
            return self._area
        Area = property(getArea)
    
    ###
    # PlayerFighter
    # This class provides basic player-control functionality
    ###
        
    class PlayerFighter(Fighter):
        
        def __init__(self, name, **stats):
            super(PlayerFighter, self).__init__(name, **stats)
            
            self._playerControlled = True
            
        # Returns a list of skill choices in the form (name of skill, available)
        def GetSkillList(self):

            choices = []
            
            sh = self._skillHandlers
            s = self.Skills
            
            skillList = sorted(self.Skills.keys(), cmp=lambda x,y: s[x][1] - s[y][1])
            
            # Loop through all the keys in self.Skills
            for skill in skillList:
                
                # target = value for that key
                target = self.Skills[skill][0]
                
                
                #If it's a dictionary itself, it means it's a sub-menu of skills - in which case just present it as an option
                if isinstance(target, dict) == True:
                    choices.append( (skill, True, None) )
                else:
                    hotkey = self._skillHandlers[target].Hotkey
                    # Otherwise, we need to check whether it's available for use and add that value into the tuple.
                    if self._skillHandlers[target].IsAvailable(self):
                        choices.append( (skill, True, hotkey) )
                    else:
                        choices.append( (skill, False, hotkey) )

            return choices
            
        def GetSubSkillList(self, skills):
            choices = []
            
            skillList = sorted(skills.keys(), cmp=lambda x,y: skills[x][1] - skills[y][1])
            
            
            for skill in skillList:
                target = skills[skill][0]
                if isinstance(target, dict) == False:
                    if (self._skillHandlers[target]).IsAvailable(self):
                        choices.append( (skill, True) )
                    else:
                        choices.append( (skill, False) )
                else:
                    choices.append( (skill, True) )

            #choices.sort()

            return choices
            
        def PickSkill(self, includeCancel=False):
            choices = self.GetSkillList()
            
            if includeCancel:
                choices.append( ('Cancel', True) )
                
            result = None
            
            # Loop, because we need to re-play this choice if the user goes into a sub-skill menu (recurses) and then picks 'Back' to back out (which will return 'None')
            while result == None:     
            
                # First, select the skill name using whatever method the UI defines
                result = self._battle.UI.PickSkill(self, choices)
                
                if (result != 'Cancel' or includeCancel==False):
                    # Then, look it up in the top level of the skills tree to find out what it points to
                    result = self._skills[result][0]
    
                    # If it's a dict, it means it's a sub-menu of skills, so call through to the sub-menu picker to get an answer
                    # (Since this method is just for the top level, there's no need to recurse.)
                    if isinstance(result, dict):
                        result = self.PickSubSkill(result)
                        
                    else:
                        # If it's a skill, check it's Available. Shouldn't ever not be, but let's just check anyway.
                        if self._skillHandlers[result].IsAvailable(self) == False:
                            result = None
                        
            if (result == 'Cancel'):
                result = None
                        
            return result

        def PickSubSkill(self, skills):
            choices = self.GetSubSkillList(skills)

            result = None
            
            # Loop, because we need to re-play this choice if the user goes into a sub-skill menu (recurses) and then picks 'Back' to back out (which will return 'None')
            while result == None:

                # Pick the name of a skill from the presented sub-tree from the fighter's skill menu
                result = self._battle.UI.PickSubSkill(self, choices)
                
                # If it's a -1, it means the user has selected 'Back' from this sub-menu and needs to return to the parent menu
                if (result == -1):
                    return None
                
                # Otherwise, we look the skill name up in the dict we've been passed in to get the actual skill
                elif (result in iter(skills)):
                    
                    result = skills[result][0]
            
                    # If it's actually another dict, then it's a sub-menu again, so recurse.
                    if isinstance(result, dict):
                        result = self.PickSubSkill(result)
                    else:
                        if self._skillHandlers[result].IsAvailable(self) == False:
                            result = None

            return result
            
        def Act(self):
            
            while (self._turnComplete == False and self._battle.On):
                skill = self.PickSkill()
                self.PerformAction(skill)
                
        def PerformAction(self, action):
            
            if action == None or (action in self._skillHandlers.keys()) == False:
                return
                
            skill = self._skillHandlers[action]

            target = None
            noTarget = False
            
            targetData = skill.GetTargets(self)

            #TODO: pass TargetData instance alone to all targeting methods
            # Check for different types of targeting in most-general to most-specific order
            if (targetData.Factions):
                targets = self._battle.GetTargetFactions(self, targeting=targetData, skill=skill)
                target = self._battle.UI.PickTargetFaction(self, targets)
                None
            elif (targetData.Positions):
                targets = self._battle.GetTargetPositions(self, self.Position, targeting=targetData, skill=skill)
                target = self._battle.UI.PickTargetPosition(self, targets)
            elif (targetData.Fighters):
                targets = self._battle.GetTargetFighters(self, targeting=targetData, skill=skill)
                target = self._battle.UI.PickTargetFighter(self, targets)
            else:
                noTarget = True

            if (target != None) or (noTarget == True):

                self._battle.FighterAct(self, skill)
                skill.PerformAction(self, target)
                
    class SimpleAIFighter(Fighter):
        
        def __init__(self, name, **stats):
            super(SimpleAIFighter, self).__init__(name, **stats)

        #TODO: an extra parameter to tell whether this skill should target friendlies or enemies (e.g. 'heal' or 'attack' respectively)
        def RegisterSkill(self, skill, weight):
            if (skill.Name in self._skillHandlers) == False:
                self._skillHandlers[skill.Name] = skill
                self._skills[skill.Name] = weight
                skill.SetUpFighter(self)
       
        def Act(self):
            
            while (self._turnComplete == False):
                skill = self.PickSkill()
                self.PerformAction(skill)
                
        def PickSkill(self):
            
            total = 0
            
            for item in self._skills.keys():
                if self._skillHandlers[item].IsAvailable(self):
                    total = total + self._skills[item]
            
            choice = renpy.random.random() * total
            
            for item in self._skills.keys():
                if self._skillHandlers[item].IsAvailable(self):
                    if (choice < self._skills[item]):
                            return item
                
                    choice = choice - self._skills[item]
                    
            return None
                
        def PerformAction(self, action):
            
            # If we haven't found any available skill to use, then skip 
            if action == None:
                self.EndTurn()
                return
                
            skill = self._skillHandlers[action]
            
            target = None
            noTarget = False
            
            targetData = skill.GetTargets(self)
            
            #TODO: Mirror changes to PlayerFighter dealing with extra target parameters
            if (targetData.Factions):
                targets = self._battle.GetTargetFactions(self, targeting=targetData, skill=skill)
                target = renpy.random.choice(targets)
            elif (targetData.Positions):
                targets = self._battle.GetTargetPositions(self, self.Position, targeting=targetData)
                t = renpy.random.choice(targets.keys())
                target = (t, targets[t])
            elif (targetData.Fighters):
                targets = self._battle.GetTargetFighters(self, targeting=targetData, skill=skill)
                if len(targets) > 0:
                    t = renpy.random.choice(targets.keys())
                    target = (t, targets[t])
                else:
                    self.EndTurn()
            else:
                noTarget = True

            if (target != None) or (noTarget == True):
                
                #TODO: Re-add this with some switch or something
                #self._battle.Announce("%(f)s uses %(s)s" % {"f": self.Name, "s": skill.Name})

                self._battle.FighterAct(self, skill)
                skill.PerformAction(self, target)
                return True
            else:
                return False
        
        
    class MovingAIFighter(SimpleAIFighter):
        
        def __init__(self, name, moveSkill, idealDistance=0, alwaysMove=True, hide=False, needsLos=False, **stats):
            super(MovingAIFighter, self).__init__(name, **stats)
            self.RegisterSkill(moveSkill, 0)
            self._moveSkill = moveSkill
            moveSkill.SetUpFighter(self)
            self._alwaysMove = alwaysMove
            self._idealDistance = idealDistance
            self._hide = hide
            self._needsLos = needsLos
            
        def Act(self):
            
            moved = False
            
            if self._alwaysMove:
                self.Move()
            
            while (self._turnComplete == False):
                skill = self.PickSkill()
                if (skill == None):
                    if (self._alwaysMove == False) and (moved == False):
                        self.Move()
                        moved = True
                    else:
                        self.EndTurn()
                elif (skill != None):
                    self.PerformAction(skill)
        
        def Move(self):
            startPos = self.Position
            
            #TODO: Use a callback here to use for costing movement across different terrain/elevations
            targets = self._battle.GetTargetPositions(self, self.Position, range=self.Stats.Move, los=False)            

            weights = {}
            
            # For each potential position, check each fighter's range to that pos, and 
            for target in targets.keys():
                
                weight = 0
                
                for fighter in self._battle.Fighters:
                    if fighter.Active and (fighter.Faction != self.Faction):
                        #TODO: Use a callback here to use for costing movement across different terrain/elevations
                        range = self._battle.GetRange(target, fighter.Position)
                        diff = abs(self._idealDistance - range)
                        weight = weight - diff
                        
                        # Give a little extra weight to those squares which are right on the 'perfect' distance, to try and avoid fighters sitting equidistant from two 'perfect' squares 
                        if (diff == 0):
                            weight = weight + 2
                           
                        # Check if the fighter is trying to hide from enemies, and give a big penalty to a square which is within LoS - this should make squares out of LoS more attractive on the whole
                        if self._hide or self._needsLos:
                            if self._battle.GetLoSThreshold() <= self._battle.CheckLoS(fighter.Position, target, fightersImpede=True, sceneryImpedes=True):
                                if self._hide:
                                    weight = weight - 10
                                elif self._needsLos:
                                    weight = weight + 2 # A fighter who wants to hide wants to hide from everyone; a fighter who needs LoS probably only needs LoS to one guy at a time...
                        
                weights[target] = weight
            
                
            #for target in weights.keys():
            #   ui.textbutton(str(weights[target]), clicked=ui.returns(0), xpos=target.Transform.xpos, ypos=target.Transform.ypos)
            #ui.interact()
                
            bestTarget = None
            bestWeight = None
            
            for target in targets.keys():
                
                if (bestTarget == None):
                    bestTarget = target
                    bestWeight = weights[target]
                
                if (weights[target] > bestWeight):
                    bestTarget = target
                    bestWeight = weights[target]
            
            if bestTarget == None:
                return
            else:
                target = (bestTarget, targets[bestTarget])
            
                self._moveSkill.PerformAction(self, target)
                
                
                
                
    # For backwards compatibility, we define 'SimpleEnemyFighter' and 'MovingEnemyFighter' here as well -
    # these were the names 'SimpleAIFighter' and 'MovingAIFighter' had in Alphas 1 and 2.
    
    class SimpleEnemyFighter(SimpleAIFighter):
        None
        
    class MovingEnemyFighter(MovingAIFighter):
        None

    ###
    # NestingFighter
    # This class enables fighter-decorators, by default passing through all functionality to
    # an internal 'child' fighter.
    ###
    
    class NestingFighter(Fighter):
        def __init__(self, fighter, statsList=[], showPriority=True):
            self._child = fighter
            self._statsList=statsList
            self._showPriority = showPriority
        
        def __getattribute__(self, name):
            
            # If it's an attribute that's been added to the instance, then pass it off to be modified.
            # (Ignore '_fighter' 'cause it's the one instance attribute on this instance.
            if name == "_fighter":
                return object.__getattribute__(self, name)
            
            if hasattr(self, "_fighter"):
                if name in self._fighter.GetStatsList():
                    value = getattr(self._fighter.RawStats, name)
                    
                    for effect in self._fighter.Effects:
                        value = effect.OnRetrieveStat(name, value)
                        
                    for equipment in self._fighter.Equipment.All:
                        value = equipment.OnRetrieveStat(name, value)
                    
                    return int(round(value))
            
            return object.__getattribute__(self, name)
            
        def __setattr__(self, name, value):
            
            if name == "_fighter" or hasattr(object, name):
                object.__setattr__(self, name, value)
                return
            else:
                    e = self._fighter.Equipment.All[:]
                    e.reverse()
    
                    for equipment in e:
                        value = equipment.OnSetStat(name, value)
                    
                    e = self._fighter.Effects[:]
                    e.reverse()
                    for effect in e:
                        value = effect.OnSetStat(name, value)
                    
                    self._fighter._battle.FighterStatChange(self._fighter, name, getattr(self._fighter.RawStats, name), value)
                    setattr(self._fighter.RawStats, name, value)
                    return
                    
#                object.__setattr__(self, name, value)
            
        def __hasattr__(self, name):
            
            if hasattr(object, name):
                return True
            elif hasattr(self._fighter, name):
                return True
            else:
                return False
            
    ###
    # StatsBoxFighter
    # This class allows you to use a fighter which is displayed as a stats box on the screen,
    # as in the Dragon Quest style of battles. It wraps an existing fighter instance.
    ###

    class StatsBoxFighter(NestingClass):
        
        def __init__(self, fighter, headSprite, showPriority):
            # Call to base to set up child
            super(StatsBoxFighter, self).__init__(fighter)
            
            # Set the head sprite, use the child's displayable if necessary
            self._headSprite = headSprite
            if self._headSprite == None:
                self._headSprite = self._child._sprite
            

            # Can't use '_statsList' because that would override the field on the nested Fighter
            # instance and make stats break!
            # For statsBoxList, we expect a tuple of (Label, stat, <bool>showBase, <bool>showAsBar)
            self._statsBoxList = []
            self._showPriority = showPriority
            
        def AddBoxStat(self, label, stat, showBase, showAsBar):
            self._statsBoxList.append( (label, stat, showBase, showAsBar) )
            
        # The only method on Fighter we're interested in 
        def Show(self, tag=None, what=None, position=None, transforms=[], layer=None, zorder=None):
            
            if tag == None:
                tag = self._tag
            if layer == None:
                layer = self._battle.GetLayer("UI")
            if zorder == None:
                zorder = self._position.Z
            if what == None:
                what = self._headSprite
            if what == None: # still...
                renpy.hide(tag, layer=layer)
                return

            anchor = Transform(xanchor=0.5, yanchor=0.5)
            
            if position == None:
                position = self._position.Transform
                
            transforms = transforms[:]
            
            t = [position, anchor]
            t.extend(transforms)
            
            
            # now draw a statsbox with UI Displayable widgets and show that instead of the
            # regular fighter displayable.
            
            
            items = []
            
            items.append( Text(self.Name) )
            
            for statLine in self._statsBoxList:
                
                value = self.GetStat(statLine[1])
                range = self.GetBaseStat(statLine[1])
                
                if statLine[3]: # show as bar
                    statBox = HBox(Text(statLine[0] + ': '), Bar(range, value, xmaximum=100), xmaximum=200)
                    items.append(statBox)
                else:
                    statText = statLine[0] + ": " + str(value)
                    if (statLine[2]): # show base stat
                        statText = statText + "/"+ str(range)
                    items.append(Text(statText))
                
            if self._showPriority:
                items.append( Bar(100, min(100, self.Priority), xmaximum=150) )
                
            stats = VBox(*items)
            head = Window(what, style=style.BattleButton)
            
            contents = HBox(head, stats)
            
            outerBox = Window(contents, style=style.BattleButton)            
            
            renpy.show(tag, what=outerBox, at_list=t, layer=layer, zorder=zorder)
            
            #for effect in self._effects.values():
            #    effect.Show(transforms=transforms, layer=layer, zorder=zorder+1)

