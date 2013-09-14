init -9 python:
    
    ###
    # BattleItem
    # This class is used for consumable items - things like health potions or bombs or whatever.
    # Each class should ideally be a flyweight/singleton type design, with no reference back to its 'owning' Fighter.
    ###
    
    class BattleItem(Actionable):
        
        def __init__(self, name="Item", weight=0, attributes=[], cost=10):
            self._name = name
            self._weight = weight
            self._attributes = attributes
            self._cost = cost
            
        # Weight can be used to limit the number of items a particular fighter can carry; it's not mandatory, setting it to '0'
        # should effectively be saying 'an infinite number may be carried'.
        def getWeight(self):
            return self._weight
        Weight = property(getWeight)
        
        # Attributes may be used by all kinds of things - maybe for selecting which items can or cannot be
        # carried (no earth elementals carrying flaming torches!) or limiting equipment (only one item with
        # 'armour' attribute may be equipped at once), etc.
        def getAttributes(self):
            return self._attributes
        Attributes = property(getAttributes)
        
        # Cost is the default base price for the item.
        def getCost(self):
            return self._cost
        Cost = property(getCost)
        
    ###
    # BattleEquipment
    # This class is used for equippable items - things like armour or swords.
    # Very similar to Items, but with added methods to modify stats - so a fighter's stats can be
    # affected by the gear he has equipped.
    ###
        
    #TODO: make this a shared base class between BattleEquipment and Effect.
    class BattleEquipment(BattleItem):
        
        def __init__(self, weight=0, attributes=[], cost=10):
            BattleItem.__init__(self, weight=weight, attributes=attributes, cost=cost)
        
        # By default, equipment isn't usually usable in the use-item sense, so we make it not 'available'.
        def IsAvailable(self, fighter):
            return False
        
        def OnRetrieveStat(self, name, value):
            return value
            
        def OnSetStat(self, name, value):
            return value
        
    #TODO: Is this necessary? Should we do a similar thing for skills?
    ###
    # BattleItemLibrary
    # This class stores a collection of instances of BattleItem keyed on name, providing an easy way to retrieve
    # particular items from just the name.
    ###
    
    class BattleItemLibrary(object):
        
        def __init__(self):
            self._items = {}
            
        def RegisterItem(self, item):
            if (item.Name in self._items) == False:
                self._items[item.Name] = item
            else:
                raise Exception("Item \"" + item.Name + "\" is already registered.")
                
        def GetItem(self, itemName):
            if item.Name in self._items:
                return self._items[item.Name]
            else:
                raise Exception("Item \"" + itemName + "\" not registered.")
    
    ###
    # RPGPriceList
    # This class encapsulates a selling-price or buying-price resolution, based on either the item's default
    # price or a list of pre-set selling or buying prices.
    # Pass in sellPrices or buyPrices dicts (mapping from item to price) or call SetBuyPrice or SetSellPrice
    # methods to set up prices, pass in sellExclusive or buyExclusive flags as true to force the price list to
    # only allow trading on items which explicitly have prices set for them, and pass in the 'defaultBuy'
    # param to control what percentage of the selling price the default buy price will be set at.
    ###
    
    class RPGPriceList(object):
        
        def __init__(self, sellExclusive=False, sellPrices={}, buyExclusive=False, buyPrices={}, defaultBuy=0.5):
            self._sellExclusive = sellExclusive
            self._sellPrices = sellPrices
            self._buyExclusive = buyExclusive
            self._buyPrices = buyPrices
            self._defaultBuy = defaultBuy
        
        def SetSellPrice(self, item, price):
            self._sellPrices[item] = price
            if (item in self._buyPrices.keys()) == False and self._buyExclusive == False:
                self._buyPrices[item] = price * self._defaultBuy
        
        def SetBuyPrice(self, item, price):
            self._buyPrices[item] = price
            if (item in self._sellPrices.keys()) == False and self._sellExclusive == False:
                self._sellPrices[item] = price / self._defaultBuy
            
        def CanSell(self, item):
            if (item in self._sellPrices.keys()) or self._sellExclusive == False:
                return True
            return False
            
        def GetSellPrice(self, item):
            if (item in self._sellPrices.keys()):
                return self._sellPrices[item]
            if (self._sellExclusive == False):
                return item.Cost
            return None
            
        def CanBuy(self, item):
            if (item in self._buyPrices.keys()) or self._buyExclusive == False:
                return True
            return False
            
        def GetBuyPrice(self, item):
            if (item in self._buyPrices.keys()):
                return self._buyPrices[item]
            if (self._buyExclusive == False):
                return item.Cost * self._defaultBuy
            return None
        
    ###
    # RPGMarkupPriceList
    # The MarkupPriceList functions identically to the PriceList class, but takes two additional parameters:
    # sellMarkup and buyMarkup. These should be decimals which represent the multiplier to the original prices
    # that this price list demands. For example, if you want to create a list which sells items at one and a half
    # times the normal price, but pays double the normal price to purchase them, set sellMarkup to 1.5 and
    # buyMarkup to 2
    ###
    
    class RPGMarkupPriceList(RPGPriceList):
        
        def __init__(self, sellMarkup=1.0, buyMarkup=1.0, sellExclusive=False, sellPrices={}, buyExclusive=False, buyPrices={}, defaultBuy=0.5):
            self._sellMarkup = sellMarkup
            self._buyMarkup = buyMarkup
            RPGPriceList.__init__(self, sellExclusive=sellExclusive, sellPrices=sellPrices, buyExclusive=buyExclusive, buyPrices=buyPrices, defaultBuy=defaultBuy)

        def GetSellPrice(self, item):
            return RPGPriceList.GetSellPrice(self, item) * self._sellMarkup
            
        def GetBuyPrice(self, item):
            return RPGPriceList.GetBuyPrice(self, item) * self._buyMarkup
        

    
    ###
    # BattleInventory
    # An inventory stores a collection of items, and provides management functions for said items.
    # Inventories may be shared across a faction or assigned directly to a particular fighter, or some combination thereof.
    ###
    
    class BattleInventory(object):
        
        def __init__(self, capacity=0):
            self._capacity = capacity
            self._items = {}
            self._handlers = {}
            
        def GetCount(self, item):
            if item in self._items.keys():
                return self._items[item]
            else:
                return 0
                
        def AddItem(self, item, quantity=1):
            count = self.GetCount(item)
            
            self._items[item] = count + quantity
            
            if (item in self._handlers.keys()) == False:
                self._handlers[item] = item
            
        def RemoveItem(self, item, quantity=1):
            count = self.GetCount(item)
            
            newCount = count - quantity
            
            if count < quantity:
                raise Exception(str(quantity) + " items of type \""+ item.Name + "\" removed from inventory, but inventory only contains " + str(count) + " items.")
            else:
                self._items[item] = newCount
                
            handler = self._handlers[item]
            
            if newCount <= 0: # Shouldn't ever be less than, but hey...
                del self._handlers[item]
                del self._items[item]
                
        # Returns a list of (name, quantity, item-instance) tuples.
        def GetItems(self):
            
            results = []
            
            for item in self._items:
                results.append( (item.Name, self._items[item], item) )
                
            return results
            
    
    ###
    # FighterEquipment
    # Class which represents a single fighter's equipped equipment.
    ###

    class FighterEquipment(object):
        def __init__(self, limits={'weapon':1, 'armour':1, 'helmet':1, 'shield':1}):
            self._items = []
            self._limits = limits
            
        def getAll(self):
            return self._items
        All = property(getAll)
        
        def CanBeAdded(self, item):
            
            allowed = True
            
            for limit in self._limits.keys():
                if limit in item.Attributes:
                    if self.CountAttribute(limit) >= self._limits[limit]: #Shouldn't be greater, but just in case!
                        allowed = False
            
            return allowed
            
        def CanBeRemoved(self, item):
            return (item in self._items)
        
        #TODO: do type checking?
        def Add(self, item):
            allowed = self.CanBeAdded(item)
            if allowed:
                self._items.append(item)
            return allowed
            
        def Remove(self, item):
            allowed = self.CanBeRemoved(item)
            if allowed:
                self._items.remove(item)
                
            return allowed
        
        def CountAttribute(self, attribute):
            return len(self.GetAllWithAttribute(attribute))
            
        def GetAllWithAttribute(self, attribute):
            return filter(lambda x: attribute in x.Attributes, self._items)
            
        def GetFirstWithAttribute(self, attribute):
            a = self.GetAllWithAttribute(attribute)            
            if (len(a) == 0):
                return None
            else:
                return a[0]
                
        def __contains__(self, item):
            return item in self._items
                
        # overload the index-get operation to return either the first item with that attribute - if only allowed one -
        # or the list of items if allowed more than one.
        # TODO: consider whether this is really a great idea or not!
        def __getitem__(self, index):
            if index in self._limits.keys():
                if self._limits[index] == 0:
                    return None
                if self._limits[index] == 1:
                    return self.GetFirstWithAttribute(index)

            return self.GetAllWithAttribute(index)

        #TODO: Consider doing same with __setitem__(self, index, item) ?
        # Harder to see what the correct behaviour would be, since the Add may not be allowed, the
        # item may not be the correct type, etc... could throw a lot of exceptions, silently fail, overwrite existing
        # data, etc.
        
    class HandedFighterEquipment(FighterEquipment):
        def __init__(self, hands=2, limits={'weapon':1, 'armour':1, 'helmet':1, 'shield':1}):
            super(HandedFighterEquipment, self).__init__(limits=limits)
            self._hands = 2

        def CanBeAdded(self, item):
            
            needed = len(filter(lambda x: x == 'hand', item.Attributes))

            used = 0
            
            for i in self._items:
                used = used + len(filter(lambda x: x == 'hand', i.Attributes))
                
            if (self._hands - (used + needed)) < 0:
                return False
            else:
                return super(HandedFighterEquipment, self).CanBeAdded(item)


