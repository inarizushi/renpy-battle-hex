init -10 python:
    
    ###
    # Conditions/Results
    # Condition-derived classes fire when particular conditions are met.
    # Result-derived classes do things when they're fired.
    ###
    
    class Condition(BattleAware):
        
        def __init__(self):
            
            self._results = []
            self._fired = False
            self._battle = None
            
        def AddResult(self, result):
            
            result.SetBattle(self._battle)
            self._results.append(result)
            
        def SetBattle(self, battle):
            
            self._battle = battle
            
            for r in self._results:
                r.SetBattle(battle)
            
        def getResults(self):
            return self._results
            
        def Fire(self, fighter, faction, position):
            
            if (self._fired == False):
                
                for result in self._results:
                    result.Fire(fighter, faction, position)
                    
                self._fired = True
                
    class Result:
        
        def Fire(self, fighter, faction, position):
            None
            
        def SetBattle(self, battle):
            self._battle = battle
        
            
            
    class MultiCondition(Condition):
        
        def __init__(self):
            
            self._conditions = {}
            
            super(MultiCondition, self).__init__()
            
        def SetComplete(self, condition):
            
            self._conditions[condition] = True
            
            if self.CheckFire():
                self.Fire(None, None, None)
                
        # This method needs to be overridden in descendant classes to provide the particular
        # combinatory condition
        def CheckFire(self):
            return True
                
        def SetBattle(self, battle):
            
            super(MultiCondition, self).SetBattle(battle)
            
            for c in self._conditions:
                c.SetBattle(battle)
            
        def AddCondition(self, condition):
            condition.SetBattle(self._battle)
            condition.AddResult(CallbackResult(self, condition))
            self._conditions[condition] = False
            
        def Tick(self):
            for c in self._conditions:
                c.Tick()
            
        def StartTurn(self):
            for c in self._conditions:
                c.StartTurn()
            
        def EndTurn(self):
            for c in self._conditions:
                c.EndTurn()
            
        def FighterStartTurn(self, fighter):
            for c in self._conditions:
                c.FighterStartTurn(fighter)
            
        def FighterEndTurn(self, fighter):
            for c in self._conditions:
                c.FighterEndTurn(fighter)
            
        def FighterAct(self, fighter, skill):
            for c in self._conditions:
                c.FighterAct(fighter, skill)
            
        def FighterDamage(self, fighter, damage, damager):
            for c in self._conditions:
                c.FighterDamage(fighter, damage, damager)
            
        def FighterDie(self, fighter):
            for c in self._conditions:
                c.FighterDie(fighter)
            
        def FighterKilled(self, fighter, killer):
            for c in self._conditions:
                c.FighterKilled(fighter, killer)
            
        def PointOfInterest(self, position=None, fighter=None):
            for c in self._conditions:
                c.PointOfInterest(position=None, fighter=None)
            
        def FighterStatChange(self, fighter, stat, oldValue, newValue):
            for c in self._conditions:
                c.FighterStatChange(fighter, stat, oldValue, newValue)
    
            
    class AllCondition(MultiCondition):
        
        def CheckFire(self):
            fire = True
            for c in (self._conditions.keys()):
                fire = fire and self._conditions[c]
            
            return fire
            
    class AnyCondition(MultiCondition):
        
        def CheckFire(self):
            fire = False
            for c in (self._conditions.keys()):
                fire = fire or self._conditions[c]
                
            return fire
        
            
        
    class CallbackResult(Result):
        def __init__(self, parent, condition):
            self._parent = parent
            self._condition = condition
            
        def Fire(self, fighter, faction, position):
            self._parent.SetComplete(self._condition)
    
    
    # Fires when a given fighter is killed        
    class FighterKilledCondition(Condition):
        
        def __init__(self, fighter):
            self._fighter = fighter
            
            super(FighterKilledCondition, self).__init__()
            
        def FighterKilled(self, fighter, killer):
            
            if (fighter == self._fighter):
                self.Fire(fighter, None, None)
                
    # Fires when a fighter from a particular faction ends their move within a certain area
    class AreaReachedCondition(Condition):
        
        def __init__(self, left, top, right, bottom, faction=None, fighter=None):
            
            # Make sure that even if the user specified the top/bottom or left/right
            # corners the 'wrong' way around, it still works.
            if (left <= right):
                self._left = left
                self._right = right
            else:
                self._left = right
                self._right = left
                
            if (bottom <= top):
                self._top = top
                self._bottom = bottom
            else:
                self._top = bottom
                self._bottom = top
                
            self._faction = faction
            self._fighter = fighter
            
            super(AreaReachedCondition, self).__init__()
            
        def FighterAct(self, fighter, skill):
            
            if (self._battle.On == False):
                return
            
            check = False
            
            if self._faction != None:
                check = (fighter.Faction == self._faction and self.CheckPosition(fighter.Position))
            else:
                check = (fighter == self._fighter and self.CheckPosition(fighter.Position))

            if check:
                self.Fire(fighter, fighter.Faction, fighter.Position)
                
        def CheckPosition(self, pos):
            
            if (pos.X >= self._left and pos.X <= self._right and pos.Y >= self._bottom and pos.Y <= self._top):
                return True
            else:
                return False
    
                
    # Special-case of AreaReachedCondition which only considers a single space
    class PositionReachedCondition(AreaReachedCondition):
        
        def __init__(self, x, y, faction=None, fighter=None):
            super(PositionReachedCondition, self).__init__(x, y, x, y, faction, fighter)
            
    class TimedCondition(Condition):
        
        def __init__(self, ticks):
            
            self._ticks = ticks
            self._elapsed = 0

            super(TimedCondition, self).__init__()
            
        def Tick(self):
            self._elapsed = self._elapsed + 1
            
            if (self._elapsed >= self._ticks):
                self.Fire(None, None, None)
                
    class FactionDestroyedCondition(Condition):
        
        def __init__(self, faction):
            
            self._faction = faction
            
            super(FactionDestroyedCondition, self).__init__()
            
        def FighterEndTurn(self, fighter):
            
            ended = True
            for f in fighter._battle.FactionLists[self._faction]:
                if f.Active:
                    ended = False

            if ended:
                self.Fire(None, self._faction, None)
                
    
              
                
    # In this result, the battle ends with a particular faction as the winners
    class FactionWinsResult(Result):
        
        def __init__(self, faction):
            self._faction = faction
            
        def Fire(self, fighter, faction, position):
            self._battle.End()
            self._battle.Win(self._faction)

    # In this result, a list of reinforcements are added to the given faction
    class PositionalReinforcementsResult(Result):
        
        # Expects a faction, and a list of (fighter, x, y) tuples
        def __init__(self, faction, fighters):
            self._faction = faction
            self._fighters = fighters
            
        def Fire(self, fighter, faction, position):
            
            self._battle.SetFaction(self._faction)
                
            for f in self._fighters:
                
                #TODO: Find a nearby unoccupied square if someone's in this one already...!
                self._battle.AddFighter(f[0], x=f[1], y=f[2])
                f[0].Show()

    class PlayMusicResult(Result):
        
        def __init__(self, music, channel='music', fadein=0.0, fadeout=0.0):
            self._music = music
            self._channel = channel
            self._fadein = fadein
            self._fadeout = fadeout
            
        def Fire(self, fighter, faction, position):
            
            renpy.music.play(self._music, channel=self._music, fadein=self._fadein, fadeout=self._fadeout);

    class CallLabelInNewContextResult(Result):
        
        def __init__(self, label):
            self._label = label
            
        def Fire(self, fighter, faction, position):
            renpy.call_in_new_context(self._label);
            
    class MessageResult(Result):
        
        def __init__(self, message):
            self._message = message
            
        def Fire(self, fighter, faction, position):
            self._battle.Announce(self._message)
            
    
