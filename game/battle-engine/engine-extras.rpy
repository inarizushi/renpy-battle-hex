init:
    
    transform BattleBounce:
        alpha 1
        yoffset 0
        easein 0.25 yoffset -60
        easeout 0.25 yoffset 0
        easein 0.25 yoffset -35
        easeout 0.25 yoffset 0
        linear 0.5 alpha 0
            
    transform BattleBob:
        yoffset 0
        easein 0.1 yoffset -10
        easeout 0.1 yoffset 0

        

init -11 python:
    
    ###
    # BattleAware
    # The BattleAware class is the base class of anything which needs to be aware of battle events
    ###
    
    class BattleAware(object):
        
        def Tick(self):
            None
            
        def StartTurn(self):
            None
            
        def EndTurn(self):
            None
            
        def FighterStartTurn(self, fighter):
            None
            
        def FighterEndTurn(self, fighter):
            None
            
        def FighterAct(self, fighter, skill):
            None
            
        def FighterDamage(self, fighter, damage, damager):
            None
            
        def FighterDie(self, fighter):
            None
            
        def FighterKilled(self, fighter, killer):
            None
            
        def PointOfInterest(self, position=None, fighter=None):
            None
            
        def FighterStatChange(self, fighter, stat, oldValue, newValue):
            None
        

    
init -10 python:
    
    ###
    # Extra
    # Extras are responsible for adding arbitrary effects to the battle, e.g. narration, fog of war, priority displays, etc.
    ###
    
    class Extra(BattleAware):
        
        #TODO: Add methods to hook into the drawing of various things
        
        def SetBattle(self, battle):
            self._battle = battle
            
        def Show(self):
            None
            
    class PanningControls(Extra):
        
        def __init__(self, leftLabel='<', rightLabel='>', upLabel='^', downLabel='v', distance=100):
            self._leftLabel = leftLabel
            self._rightLabel = rightLabel
            self._upLabel = upLabel
            self._downLabel = downLabel
            self._distance = distance
        
        def Show(self):
            l = self._battle.GetLayer('UI')

            b = Button(Text(self._leftLabel, style=style.PanButtonText['left']), clicked=self.PanLeft, style=style.PanButton['left'])
            renpy.show('_battlePanLeftButton', what=b, layer=l)
            b = Button(Text(self._rightLabel, style=style.PanButtonText['right']), clicked=self.PanRight, style=style.PanButton['right'])
            renpy.show('_battlePanRightButton', what=b, layer=l)
            b = Button(Text(self._upLabel, style=style.PanButtonText['up']), clicked=self.PanUp, style=style.PanButton['up'])
            renpy.show('_battlePanUpButton', what=b, layer=l)
            b = Button(Text(self._downLabel, style=style.PanButtonText['down']), clicked=self.PanDown, style=style.PanButton['down'])
            renpy.show('_battlePanDownButton', what=b, layer=l)

                
        def PanLeft(self):
            self._battle.CameraX = self._battle.CameraX - self._distance
        def PanRight(self):
            self._battle.CameraX = self._battle.CameraX + self._distance
        def PanUp(self):
            self._battle.CameraY = self._battle.CameraY - self._distance
        def PanDown(self):
            self._battle.CameraY = self._battle.CameraY + self._distance

    class ActionPanner(Extra):
        
        def __init__(self, panPeriod=0.25, panTolerance=20):
            self._panPeriod = panPeriod
            self._panTolerance = panTolerance
        
        def Tick(self):
            None
            
        def FighterStartTurn(self, fighter):
            self.PanTo(fighter.Position)
            
        def FighterAct(self, fighter, skill):
            self.PanTo(fighter.Position)
            
        def FighterDamage(self, fighter, damage, damager):
            self.PanTo(fighter.Position)
            
        def FighterDie(self, fighter):
            self.PanTo(fighter.Position)
            
        def PointOfInterest(self, position=None, fighter=None):
            if fighter != None:
                self.PanTo(fighter.Position)
            elif position != None:
                self.PanTo(position)

            
        def PanTo(self, position):
            newX = position.Transform.xpos - (config.screen_width / 2)
            newY = position.Transform.ypos - (config.screen_height / 2)
            
            changed = False
            
            if (abs(newX - self._battle.CameraX) > self._panTolerance) or (abs(newY - self._battle.CameraY) > self._panTolerance):

                self._battle.CameraX = newX
                self._battle.CameraY = newY
                _battle.RequestPause(self._panPeriod)
            
                renpy.force_full_redraw()
            
    class DebugExtra(Extra):
        
        def Tick(self):
            
            s = ""
            
            for faction in self._battle._factions:
                s += "Faction: %(f)s:\n" % {"f": faction}
                for fighter in self._battle._fighters:
                    if fighter.Faction == faction:
                        s += "- %(f)s\n" % {"f": fighter.Debug}
            
            self._battle.Announce(s)
            
        def StartTurn(self):
            self._battle.Announce("Start Turn")
            
        def EndTurn(self):
            self._battle.Announce("End Turn")
            
        def FighterStartTurn(self, fighter):
            self._battle.Announce("%(f)s Begin Turn" % {"f": fighter.Name})
            
        def FighterEndTurn(self, fighter):
            self._battle.Announce("%(f)s End Turn" % {"f": fighter.Name})
            
        def FighterDamage(self, fighter, damage, damager):
            self._battle.Announce("%(name)s took %(dam)i damage." % {"name": fighter.Name, "dam": damage})
    
        def FighterDie(self, fighter):
            self._battle.Announce("%(name)s has died." % {"name": fighter.Name})
            
        def FighterAct(self, fighter, skill):
            self._battle.Announce("%(name)s performs skill %(skill)s" % {"name": fighter.Name, "skill": skill.Name})
    
    # Causes a bouncing number to appear over any fighter who gets damaged
    class RPGDamage(Extra):
        
        def FighterDamage(self, fighter, damage, damager):
            
            col = "#F11"
            
            # If the 'damage' is less than one - that is, it's a healing event - then change the colour to green
            # and change the sign of the displayed damage.
            if (damage < 0):
                col = "#1F1" 
                damage = damage * -1
            
            num = Text("%(dam)s" % {"dam":damage}, bold=True, size=15, color=col, drop_shadow=(1, 1), drop_shadow_color="#000", text_align=0.5)
       
            # base position
            
            if isinstance(fighter.Sprite, BattleDisplayable):
                a = Transform(xoffset=fighter.Sprite.PlaceMark[0], yoffset=fighter.Sprite.PlaceMark[1])
            else:
                a = Transform()
            
            p = fighter.Position.Transform
            l = self._battle.GetLayer("Effects")
            tag = "RPGDamage_%(f)s_%(n)d" % {"f": fighter.Name.replace(' ','_'), "n": renpy.random.random()*1000}
            
            if (_preferences.battle_skip_incidental):
                at_list=[p, a]
            else:
                at_list=[p, a, BattleBounce]
            
            renpy.show(tag, what=num, at_list=at_list, layer=l, zorder=1000)
            
            # No need to hide, necessarily, since next time the battle redraws it'll clear these out anyway...
            # but we do need to request a pause of the duration of the bounce, otherwise the redraw will wipe out the bounce
            fighter._battle.Pause(0.4)
            if (_preferences.battle_skip_incidental == False):
                fighter._battle.RequestPause(1.1)
            
            return
            
    # Using this extra will cause a state called 'damage' to be triggered whenever a fighter takes damage.
    class DamageState(Extra):
        
        def FighterDamage(self, fighter, damage, damager):
            if (damage > 0):
                fighter._battle.ChangeFighterState(fighter, "damage")
                fighter._battle.ChangeFighterState(fighter, "default")
     
            
    # Causes any fighter who gets killed to be faded out
    class RPGDeath(Extra):
        
        def FighterDie(self, fighter):
            
            l = self._battle.GetLayer("Fighters")
            
            # Hide fighter graphic
            renpy.hide(fighter.Tag, layer=l)
            renpy.transition(Dissolve(0.5), layer=l)
            _battle.Pause(0.5, hard=True)
            
    class RPGActionBob(Extra):
        
        def __init__(self, exceptions=[]):
            self._exceptions = exceptions
        
        def FighterAct(self, fighter, skill):
            
            l = self._battle.GetLayer("Fighters")
            
            if (_preferences.battle_skip_incidental == False):
                
                for e in self._exceptions:
                    if isinstance(skill, e):
                        return
                
                fighter.Show(transforms=[BattleBob])
                
                _battle.Pause(0.2)
            
    class ActiveDisplay(Extra):

        # faction is the faction for which to display the ActiveDisplay
        # stats is a dictionary of the stats to display, each mapping to the stat name from the
        # fighter to use (e.g. stats={"HP": "Health"}).
        def __init__(self, faction, stats={}):
            self._faction = faction
            self._stats = stats
            
        def FighterStartTurn(self, fighter):
            self._battle.Show()
            
        def Show(self):
            l = self._battle.GetLayer("UI")
            
            lines = []
            priorities = []
            fighterCount = 0

            x = 0
            
            #loop through all fighters in the relevant faction
            for fighter in self._battle.FactionLists[self._faction]:
                
                if fighter.Active:
                    
                    fighterCount = fighterCount + 1
                
                    # Start each item off with the fighter's name
                    items = [Text(fighter.Name, xalign=0.0)]
                    
                    x = 1
                    
                    #loop through all relevant stats to come up with a list of Text displayables for the stats
                    for key in iter(self._stats):
                        stat = self._stats[key]
                        
                        a = fighter.GetStat(stat)
                        b = fighter.GetBaseStat(stat)
                        
                        if (a != None and b != None):
                            
                            a = int(a)
                            b = int(b)
                            
                            s = "%(stat)s: %(a)i/%(b)i" % {"stat": key, "a": a, "b": b}
                            items.append(Text(s, xalign=0.5))
                        else:
                            items.append(Null())
                        
                        x = x + 1
                
                    lines.extend(items)
                    priorities.append(Bar(100, min(100, fighter.Priority)))
                
            grid = Grid(x, fighterCount, padding=5, style="ActiveDisplayGrid",*lines)
            box = HBox(grid, Window(VBox(xmaximum=100, xalign=1.0, *priorities), xfill=True, style="ActiveDisplayBox"))
            window = Window(box, style="ActiveDisplayWindow")
            
            renpy.show("_battleActiveDisplayWindow", what=window, layer=l)
            
            _battle.Pause(0.2)
            
    
    class GridStatsDisplay(Extra):

        # faction is the faction for which to display the GridStatsDisplay
        # stats is a dictionary of the stats to display, each mapping to the stat name from the
        # fighter to use (e.g. stats={"HP": "Health"}).
        def __init__(self, faction, stats={}):
            self._faction = faction
            self._stats = stats
            
        def FighterStartTurn(self, fighter):
            self._battle.Show()
            
        def Show(self):
            l = self._battle.GetLayer("UI")
            
            lines = []
            facings = []
            fighterCount = 0

            x = 0
            
            #loop through all fighters in the relevant faction
            for fighter in self._battle.FactionLists[self._faction]:
                
                # Only show active fighters
                if fighter.Active:
                    
                    fighterCount = fighterCount + 1
                
                    # Start each item off with the fighter's name
                    items = [Text(fighter.Name, xalign=0.0)]
                    
                    x = 2 # One for the fighter's name, one for the facing
                    
                    #loop through all relevant stats to come up with a list of Text displayables for the stats
                    for key in iter(self._stats):
                        stat = self._stats[key]
                        
                        a = fighter.GetStat(stat)
                        b = fighter.GetBaseStat(stat)
                        
                        if (a != None and b != None):
                            a = int(a)
                            b = int(b)
                            
                            s = "%(stat)s: %(a)i/%(b)i" % {"stat": key, "a": a, "b": b}
                            items.append(Text(s, xalign=0.5))
                        else:
                            items.append(Null())
                            
                        
                        x = x + 1
    
                    items.append(Text(fighter.Facing.Name, xalign=0.5))
                        
                    lines.extend(items)
                
            grid = Grid(x, fighterCount, padding=5, style="GridStatsGrid",*lines)
            window = Window(grid, style="GridStatsWindow")
            
            renpy.show("_battleGridStatsWindow", what=window, layer=l)
            
            
    # Causes the battle to be over with a win for the last faction standing
    class SimpleWinCondition(Extra):            
        
        def Tick(self):
            self.CheckWin()
            
        def FighterEndTurn(self, fighter):
            self.CheckWin()
            
        def CheckWin(self):
            
            activeFactions = 0
            
            liveFaction = None
            
            for faction in self._battle.FactionLists.keys():
                activeFighters = 0
                
                for fighter in self._battle.FactionLists[faction]:
                    if fighter.Active:
                        activeFighters = activeFighters + 1
                
                if activeFighters > 0:
                    activeFactions = activeFactions + 1
                    liveFaction = faction
            
            if activeFactions <= 1:
                self._battle.End()
                
            if activeFactions == 1:
                self._battle.Win(liveFaction)
                
                
                
    class FogOfWar(Extra):
        
        def __init__(self, mask, blank, faction):
            self._mask = mask
            self._faction = faction
            self._blank = blank
            
            self._width, self._height = 800, 600#renpy.image_size(self._blank)
            self._maskWidth, self._maskHeight = renpy.image_size(self._mask)
            
        def Show(self):
            
            #maskList = []
            maskList = [(0,0), 'battle/white.jpg']
            
            list = self._battle.FactionLists[self._faction]
            for f in list:
                maskList.append( (f.Position.Transform.xpos - (self._maskWidth // 2), f.Position.Transform.ypos - (self._maskHeight // 2)) )
                maskList.append(self._mask)
            
            fogMask = im.Composite( (self._width, self._height), *maskList )
            
            fog = im.AlphaMask(self._blank, fogMask)
            
            l = self._battle.GetLayer("Effects")
            
            #TODO: include panning transform!
            renpy.show("battle_fogofwareffect", what=fog, at_list=[Transform(xpos=0, ypos=0)], layer=l)
                
    class CurrentFighterPointer(Extra):
        
        def __init__(self, disp, offset, faction=None):
            self._disp = disp
            self._offset = offset
            self._faction = faction
        
        def FighterStartTurn(self, fighter):
            
            if (self._faction == None or self._faction == fighter.Faction):
                fighter.AddEffect("CurrentFighterPointer", CurrentFighterPointerEffect(fighter, self._disp, self._offset))
                fighter.Show()
            
        def FighterEndTurn(self, fighter):
            
            if (self._faction == None or self._faction == fighter.Faction):
                fighter.RemoveEffect("CurrentFighterPointer")
            
            
    ###
    # Effect
    # Effects are things that arbitrarily apply to a fighter, e.g "OnFire" or "Shielded" or whatever.
    ###
    
    class Effect(Extra):
        
        def __init__(self, fighter):
            self._fighter = fighter
            self.SetBattle(fighter._battle)
            self._name = "Effect"

        def Show(self, transforms=[], layer=None, zorder=None):
            None
            
        def Transition(self, transition, layer=None):
            None
            
        def Hide(self):
            None
            
        def OnRetrieveStat(self, name, value):
            return value
            
        def OnSetStat(self, name, value):
            return value
            
    class CurrentFighterPointerEffect(Effect):
        
        def __init__(self, fighter, disp, offset):
            super(CurrentFighterPointerEffect, self).__init__(fighter)
            self._disp = disp
            self._offset = offset
            self._tag = self._fighter.Tag+"_battleCurrentFighterPointer"

        
        def Show(self, transforms=[], layer=None, zorder=None):
            transforms.append(self._fighter.Position.Transform)
            offset = Transform(xoffset = self._offset[0], yoffset=self._offset[1])
            transforms.append(offset)
            transforms.reverse()
            
            renpy.show(self._tag, what=self._disp, at_list=transforms, layer=self._battle.GetLayer("Effects"), zorder=zorder)

        def Transition(self, transition, layer=None):
            
            renpy.transition(transition, layer=self._battle.GetLayer("Effects"))
            
        def Hide(self):
            renpy.hide(self._tag, layer=self._battle.GetLayer("Effects"))
            
    class HasteEffect(Effect):
        
        def __init__(self, fighter, turns=2):
            # Do the default setup for an effect
            super(HasteEffect, self).__init__(fighter)
            
            # set up a starting turn-count for the haste effect to last
            self._turns = turns
            self._name = "Haste"
        
        def FighterStartTurn(self, fighter):
            
            # count down one turn at the beginning of every turn this fighter takes under this effect
            if (fighter == self._fighter and self._turns > 0):
                self._turns = self._turns - 1
            
        def FighterEndTurn(self, fighter):
            
            # If we've run out of turns, remove the effect so haste no longer applies
            if (fighter == self._fighter and self._turns == 0):
                fighter.RemoveEffect("Haste")
                _battle.Announce("Haste wears off for " + fighter.Name)
                self._turns = -1
            
        def OnRetrieveStat(self, name, value):
            if name == 'Speed':
                return value * 2
            else:
                return value
                
        def OnSetStat(self, name, value):
            if name == 'Speed':
                return int(value / 2)
            else:
                return value
    