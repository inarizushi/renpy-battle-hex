init python:
    
    class ExperienceBonus(object):
        def Apply(self, fighter):
            None
            
        def UnApply(self, fighter):
            None
    
    class ExperiencePlan(object):
        
        def __init__(self, fighter, backwards=False):
            self._fighter = fighter
            # List of ((string threshold_stat, int threshold_value), (ExperienceBonus))
            self._pendingGains = []
            self._passedGains = []
            self._backwards = backwards
            
        def getFighter(self):
            return self._fighter
        Fighter = property(getFighter)
        
        def StatChange(self, stat, oldValue, newValue):
            if newValue > oldValue:
                # We're dealing with a stat increase, so look at pendingGains
                gains = [x for x in self._pendingGains if (x[0][0] == stat)]
                
                for item in gains:
                    if newValue >= item[0][1]:
                        item[1].Apply(self.Fighter)
                        self._pendingGains.remove(item)
                        self._passedGains.append(item)
                        
                # If any changes have been made to stats, we should re-show battlefield to
                # make sure that any on-screen stat displays are keeping up.
                if len(gains) > 0:
                    self._fighter._battle.Show()
                        
            elif self._backwards and newValue < oldValue:
                
                losses = [x for x in self._passedGains if (x[0][0] == stat)]
                
                for item in losses:
                    if newValue < item[0][1]:
                        item[1].UnApply(self.Fighter)
                        self._pendingGains.append(item)
                        self._passedGains.remove(item)
            
                # If any changes have been made to stats, we should re-show battlefield to
                # make sure that any on-screen stat displays are keeping up.
                if len(losses) > 0:
                    self._fighter._battle.Show()

        def AddBonus(self, thresholdStat, thresholdValue, bonus):
            #_battle.Announce("Bonus: " + thresholdStat + " " + str(thresholdValue) + " -> " + bonus._stat + " + " + str(bonus._increase))
            self._pendingGains.append( ((thresholdStat, thresholdValue), bonus) )
    
    class ExperienceTracker(Extra):
        
        def __init__(self):
            self._plans = {}
            
        def SetPlan(self, fighter, plan):
            self._plans[fighter] = plan
            
        def GetPlan(self, fighter):
            if (fighter in self._plans):
                return self._plans[fighter]
            else:
                return None
            
        def FighterStatChange(self, fighter, stat, oldValue, newValue):
            plan = self.GetPlan(fighter)
            if (plan != None):
                plan.StatChange(stat, oldValue, newValue)
            
    class SimpleBonus(ExperienceBonus):
        
        def __init__(self, stat, increase):
            self._stat = stat
            self._increase = increase
        
        def Apply(self, fighter):
            if (hasattr(fighter.Stats, self._stat)):
                
                # Rather than modify fighter.Stats directly, we'll apply the modification to RawStats (and BaseStats).
                # The reason for this is that unlike most stat changes (which are due to external factors), level-up
                # bonuses come from within and thus shouldn't go through the usual equipment/effect/etc. filter.
                # It would be silly for a fighter with a halve-all-damage talisman to only get half the health bonus 
                # for levelling up!
                
                statValue = getattr(fighter.RawStats, self._stat)
                baseValue = getattr(fighter.BaseStats, self._stat)
                
                start = getattr(fighter.Stats, self._stat)
                
                newBaseValue = baseValue + self._increase
                proportion = (newBaseValue * 1.0) / (baseValue * 1.0)
                newStatValue = statValue * proportion
                
                setattr(fighter.RawStats, self._stat, newStatValue)
                setattr(fighter.BaseStats, self._stat, newBaseValue)
                
                end = getattr(fighter.Stats, self._stat)
                
                # If the stat has changed as a result of this bonus (probably!) then we have
                # to trigger the event manually. Normally this happens in the FighterStats
                # class whenever you modify a stat, but we're going direct to rawstats so it doesn't.
                if (start != end):
                    fighter._battle.FighterStatChange(fighter, self._stat, start, end)
                
            
        def UnApply(self, fighter):
            if (hasattr(fighter.Stats, self._stat)):
                statValue = getattr(fighter.RawStats, self._stat)
                baseValue = getattr(fighter.BaseStats, self._stat)
                
                newBaseValue = baseValue - self._increase
                proportion = (newBaseValue * 1.0) / (baseValue * 1.0)
                newStatValue = statValue * proportion
                
                setattr(fighter.RawStats, self._stat, newStatValue)
                setattr(fighter.BaseStats, self._stat, newBaseValue)
            
            
    class LevelPlan(ExperiencePlan):
        
        def __init__(self, fighter):
            super(LevelPlan, self).__init__(fighter)
            self._xp = 0
            self._levels = 1
            fighter.RegisterStat('Level', 1)
            fighter.RegisterStat('XP', 0)
        
        # gains is dictionary of {stat=>gain}
        def AddLevel(self, xp, gains):
            
            self._xp = self._xp + xp
            self._levels = self._levels + 1
            
            self.AddBonus('XP', self._xp, SimpleBonus('Level', 1))
            
            for gain in gains.keys():
                self.AddBonus('Level', self._levels, SimpleBonus(gain, gains[gain]))
        
                
    # Causes a bouncing number to appear over any fighter who gains XP
    class RPGXP(Extra):
        
        def FighterStatChange(self, fighter, stat, oldValue, newValue):
            
            # We're only interested in the 'XP' stat
            if stat.upper() != 'XP':
                return
                
            gain = int(newValue - oldValue)

            # By default, show XP gains in green - or red if it's actually a loss.
            col = "#1F1"
            
            # If the XP is less than one - that is, it's a loss - then change the colour to red
            if (gain < 0):
                col = "#F11" 
            
            num = Text("+%(xp)s XP" % {"xp":gain}, bold=True, size=15, color=col, drop_shadow=(1, 1), drop_shadow_color="#000", text_align=0.5)
       
            # base position
            
            if isinstance(fighter.Sprite, BattleDisplayable):
                a = Transform(xoffset=fighter.Sprite.PlaceMark[0], yoffset=fighter.Sprite.PlaceMark[1])
            else:
                a = Transform()
            
            p = fighter.Position.Transform
            l = self._battle.GetLayer("Effects")
            tag = "RPGXP_%(f)s_%(n)d" % {"f": fighter.Name, "n": renpy.random.random()}
            
            renpy.show(tag, what=num, at_list=[p, a, BattleBounce], layer=l, zorder=1000)
            
            # No need to hide, necessarily, since next time the battle redraws it'll clear these out anyway...
            # but we do need to request a pause of the duration of the bounce, otherwise the redraw will wipe out the bounce
            fighter._battle.RequestPause(1.5)
            
            return

    class RPGLevelUp(Extra):
        
        def FighterStatChange(self, fighter, stat, oldValue, newValue):
            
            fighter._battle.Pause(0.1)
            
            if stat.upper() != 'LEVEL':
                return
                
            levels = int(newValue - oldValue)
            
            for x in range(levels):
                self._battle.Announce(fighter.Name + " levelled up!")
                
    class DamageXPGain(Extra):
        
        def __init__(self, multiplier):
            super(DamageXPGain, self).__init__()
            self._multiplier = multiplier

        def FighterDamage(self, fighter, damage, damager):
            if hasattr(damager.Stats, "XP"):
                value = int(round(damage * self._multiplier))
                damager.Stats.XP = damager.Stats.XP + value
                
    class KillsXPGain(Extra):
        
        def FighterKilled(self, fighter, killer):
            if hasattr(fighter.Stats, "Prize") and hasattr(killer.Stats, "XP"):
                killer.Stats.XP = killer.Stats.XP + fighter.Stats.Prize
                
