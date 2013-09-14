init -5 python:
    
    class PotionItem(BattleItem):
        def __init__(self, name="Potion", gain=50, cost=10):
            BattleItem.__init__(self, name, cost=cost)
            self._gain = gain
            self._targets = TargetData(friendly=True, enemy=False, range=1)
            
        def PerformAction(self, fighter, target):
            #TODO: Consider AttackResolver instead?
            target[0].Damage(self._gain * -1, fighter) # heal by 50

    class ElixirItem(BattleItem):
        def __init__(self, name = "Elixir", gain=10, cost=10):
            BattleItem.__init__(self, name, cost=cost)
            self._gain = gain
            self._targets = TargetData(friendly=True, enemy=False, range=1)
            
        def PerformAction(self, fighter, target):

            if hasattr(target[0].Stats, "MP"):
                gain = min(self._gain, target[0].BaseStats.MP - target[0].Stats.MP)
                target[0].Stats.MP = target[0].Stats.MP + gain
            
            
            
            
    #####
    ### Equipment
    #####
 
    
    ###
    # StatBonusEquipment
    # This class provides a base class for any kind of equipment which provides a simple +X bonus
    # to a stat or set of stats.
    ###
    
    class StatBonusEquipment(BattleEquipment):
        def __init__(self, name='Equipment', bonuses={}, attributes=[], weight=0, cost=10):
            BattleEquipment.__init__(self, weight=weight, attributes=attributes, cost=cost)
            self._attributes = attributes
            self._bonuses = bonuses
            self._name = name
            
        def OnRetrieveStat(self, name, value):
            
            for b in self._bonuses.keys():
                if name == b:
                    return value + self._bonuses[b]
            
            return value
            
        def OnSetStat(self, name, value):
            
            for b in self._bonuses.keys():
                if name == b:
                    return value - self._bonuses[b]
                    
            return value
            
    ###
    # StatMultiplierEquipment
    # This class provides a base class for any kind of equipment which provides a straight xX multiplier
    # to a stat or set of stats
    ###
            
    class StatMultiplierEquipment(BattleEquipment):
        def __init__(self, name='Equipment', multipliers={}, attributes=[], weight=0, cost=10):
            BattleEquipment.__init__(self, weight=weight, attributes=attributes, cost=cost)
            self._attributes = attributes
            self._multipliers = multipliers
            self._name = name
            
        def OnRetrieveStat(self, name, value):
            
            for m in self._multipliers.keys():
                if name == m:
                    return value * self._multipliers[m]
            
            return value
            
        def OnSetStat(self, name, value):
            
            for m in self._multipliers.keys():
                if name == m:
                    return value / self._multipliers[m]
                    
            return value
            
    

    class Weapon(StatBonusEquipment):
        def __init__(self, name="Sword", hands=1, attack=10, attributes=[], weight=0, cost=10):

            attributes = ['weapon'] + (['hand'] * hands) + attributes
            bonuses = {"Attack": attack}

            StatBonusEquipment.__init__(self, name, bonuses, attributes, weight=weight, cost=cost)
                
    
    class Armour(StatBonusEquipment):
        def __init__(self, name='Armour', defence=10, attributes=[], weight=0, cost=10):

            attributes = ['armour'] + attributes
            bonuses = {"Defence": defence}

            StatBonusEquipment.__init__(self, name, bonuses, attributes, weight=weight, cost=cost)
                
    
    class Shield(StatBonusEquipment):
        def __init__(self, name='Shield', hands=1, defence=5, attributes=[], weight=0, cost=10):

            attributes = ['shield'] + (['hand'] * hands) + attributes
            bonuses = {"Defence": defence}

            StatBonusEquipment.__init__(self, name, bonuses, attributes, weight=weight, cost=cost)

    class Helmet(StatBonusEquipment):
        def __init__(self, name='Helmet', defence=2, attributes=[], weight=0, cost=10):

            attributes = ['helmet'] + attributes
            bonuses = {"Defence": defence}

            StatBonusEquipment.__init__(self, name, bonuses, attributes, weight=weight, cost=cost)



    # Example multiplier equipment classes
    class HealthAmulet(StatMultiplierEquipment):
        def __init__(self, name="Health Amulet", multipliers={"Health":1.2}, attributes=[], weight=0, cost=10):
            StatMultiplierEquipment.__init__(self, name=name, multipliers=multipliers, attributes=attributes, weight=weight, cost=cost)
                
    class AttackAmulet(StatMultiplierEquipment):
        def __init__(self, name="Attack Amulet", multipliers={"Attack":1.2}, attributes=[], weight=0, cost=10):
            StatMultiplierEquipment.__init__(self, name=name, multipliers=multipliers, attributes=attributes, weight=weight, cost=cost)


