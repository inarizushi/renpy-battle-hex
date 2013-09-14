init -20 python:
    
    class BattleFacing(object):
        def __init__(self, name, start, end):
            self._name = name
            
            # Normalise both angles
            start = start % 360
            end = end % 360
            
            # If the start point is greater than the end point, then the arc probably straddles 0,
            # e.g. -45 to 45 may be given as 315 to 45. So fix it to be negative in this case so
            # it's easier to make checks against.
            if start > end:
                start = start - 360
            
            self._start = start
            self._end = end
        
        def getName(self):
            return self._name
        Name = property(getName)
        
        def getStart(self):
            return self._start
        Start = property(getStart)
        
        def getEnd(self):
            return self._end
        End = property(getEnd)
        
        def Contains(self, angle):
            # Normalise...
            angle = angle % 360
            
            # normal case
            if (angle >= self._start and angle <= self._end):
                return True
            # case where start and end straddle the 0 mark... for example, N = -45 to 45
            # A check of 330 would fail the above check, but here would be checked against
            # 315 and 405, and pass.
            elif (angle >= (self._start + 360) and angle <= (self._end + 360)):
                return True
            else:
                return False
    
init -10 python:
    
    ###
    # Battlefield
    # A class to represent the battlefield upon which the Fighters fight, providing all battlefield-related features (e.g. position, targeting, etc.)
    ###
    
    class Battlefield(BattleAware):
        
        def __init__(self, facings={}):
            self._facings = {}
            
            if facings == {}:
                facings = {"default": (0,360)}
            self.LoadFacings(facings)
            
        # Accessors
        
        def getFacings(self):
            return self._facings
        Facings = property(getFacings)
        
        def GetPositionMatrix(self):
            return mat.sidentity()
            
        def GetPresentationMatrix(self):
            return mat.sidentity()
        
        # Setup methods
        
        def SetBattle(self, battle):
            self._battle = battle
            
        def RegisterFighter(self, fighter, **properties):
            None
            
        def RegisterScenery(self, scenery, **properties):
            None
            
        # The battlefield expects a dictionary of facings in the form of a string facing name (e.g. 'N') which maps to
        # a tuple of two angles, start and end.
        # Facings must cover all angles between 0 and 360 or the world ends in a cataclysm of fire, brimstone and over-cooked broccoli.
        def LoadFacings(self, facings):
            
            newFacings = {}
            
            # First check that the data we've been given fills the whole 360
            items = facings.values()
            items.sort()

            start = items[0][0] % 360
            end = items[len(items) - 1][1] % 360
            
            if (start != end):
                raise Exception("Facings must not have gaps or overlaps: facing end " + str(end) + " and start " + str(start) + " do not match.")
            
            last = items[0][0] % 360
            total = 0
            
            for item in items:
                start = item[0] % 360
                end = item[1] % 360

                if (item[0] % 360) != last:
                    raise Exception("Facings must not have gaps or overlaps: facing end " + str(last) + " and start " + str(start) + " do not match.")
                last = (item[1] % 360)
                
                if (end <= start):
                    end = end + 360
                total = total + (end - start)
            
            if total != 360:
                raise Exception("Facings must all add up to 360; actual total: " + str(total))
            
            # Next, convert all those facings into BattleFacing instances and save them away
            for item in facings.keys():
                if item in newFacings.keys():
                    raise Exception("Facing " + str(item) + " defined more than once.")
                else:
                    newFacings[item] = BattleFacing(item, facings[item][0], facings[item][1])
                    
            self._facings = newFacings
            
            
        # Functional Methods
        
        def Show(self):
            None
            
            
        # Utility Methods
            
        def GetTargetFactions(self, source, targeting=None):
            
            enemy = True
            friendly = False
            
            if targeting != None:
                enemy = targeting.Enemy
                friendly = targeting.Friendly
                
            targets = []
            for target in self._battle.Factions:
                if target != source.Faction and enemy:
                    targets.append(target)
                elif target == source.Faction and friendly:
                    targets.append(target)

            return targets
        
        def GetTargetFighters(self, source, targeting=None, range=1, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[], los=True, callback=None):
            return {}
            
        def GetTargetPositions(self, source, targeting=None, range=1, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[], los=False, callback=None):
            return {}
            
        def GetOccupants(self, position):
            
            checks = self._battle.All

            results = []
            
            for fighter in checks:
                #TODO: Consider whether dead fighters should block - maybe a schema thing?
                if (fighter.Position == position) and fighter.Active:
                    results.append(fighter)
            
            return results
    
        def CheckLoS(self, pos, target, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[]):
            return 1
            
        def GetRange(self, pos1, pos2, callback=None):
            return 0
            
        def GetPathLength(self, pos1, pos2, callback=None):
            return self.GetRange(pos1, pos2, callback=callback)
            
        def GetPositionsInRadius(self, start, radius=1, callback=None):
            return [start]
            
        def GetPositionsInLine(self, start, end, callback=None):
            return [start, end]
            
        def GetPositionsInRect(self, start, end):
            return [start, end]
            
        # Here, we work out the facing based on the X and Y of the positions passed in.
        # Child classes may want to override this to do facings however makes the most sense in that child class.
        def GetFacing(self, source, target):
            a = math.atan2(target.X-source.X, target.Y-source.Y)
            a = ((a * 360) / (math.pi * 2)) % 360
            
            return self.GetFacingFromAngle(a)
            
        def GetFacingFromAngle(self, angle):
            
            facing = None
            
            for k in self._facings.keys():
                f = self._facings[k]
                
                if f.Contains(angle + self._battle.Rotation):
                    facing = k
                    break
            
            return facing

        def GetAngleFromFacing(self, facing):
            
            f = self._facings[facing]
            
            if (f == None):
                raise exception("Cannot find facing " + str(facing))
                
            else:
                a = ((float(f.End - f.Start) / 2.0) + f.Start)
                return a - self._battle.Rotation
                
        # Method to rotate the battlefield, which needs to be overriden in child classes which support rotation
        
        def Rotate(self, degree):
            self._battle.Rotation = self._battle.Rotation + degree
    ###
    # SimpleBattlefield
    # A Battlefield which just has a plain image backdrop, two lines of fighters on each side of the screen
    # (SimpleBattlefield does not support more than two factions; it's simple!)
    ###
    
    class SimpleBattlefield(Battlefield):
        
        def __init__(self, disp, facings={'E': (0, 180), 'W': (180, 360)}):
            self._disp = disp
            
            if isinstance(self._disp, BattlefieldSprite) == False:
                self._disp = BattlefieldSprite(self._disp)
                
            super(SimpleBattlefield, self).__init__(facings)
            
        def SetBattle(self, battle):
            self._battle = battle
            self._disp.SetBattle(battle)
            
        def RegisterFighter(self, fighter, **properties):
            # Dole out fighters in an offset line by faction
            
            faction = self._battle.Factions.index(fighter.Faction)
            count = len(self._battle.FactionLists[fighter.Faction])
            
            if (faction == 0):
                start = (150, 225)
                end = (75, 450)
                offset = (-25, 75)
            elif (faction == 1):
                start = (650, 225)
                end = (725, 450)
                offset = (25, 75)
            
            if (count * offset[1]) + start[1] > end[1]:
                # If there are too many fighters to space them at the desired spacing, then we need to adjust the spacing:
                offset[0] = (end[0] - start[0]) / count
                offset[1] = (end[1] - start[1]) / count
            else:
                # Otherwise, we need to adjust the start and end so that the column of fighters is centred in the desired space.
                width = offset[0] * count
                height = offset[1] * count
                remainderWidth = end[0] - start[0] - width
                remainderHeight = end[1] - start[1] - height
                
                end = (end[0] - (remainderWidth / 2),end[1] - (remainderHeight / 2)) 
                start = (start[0] + (remainderWidth / 2),start[1] + (remainderHeight / 2))


            # Next, having ascertained the correct parameters, we need to lay the whole faction out in a line.
            # We need to re-do everyone 'cause new fighters shuffle everyone else around.

            f = 0
            
            for fighter in self._battle.FactionLists[fighter.Faction]:
                
                x, y = start[0] + (f * offset[0]), start[1] + (f * offset[1])
                
                pos = BattlePosition(x, y, 0)
                pos.SetBattle(self._battle)
                fighter.Position = pos
                
                f = f + 1
            
            
        def GetTargetFighters(self, source, targeting=None, range=1, los=True, callback=None):
            
            friendly = False
            enemy = True
            live = True
            dead = False
            
            if targeting != None:
                range = targeting.Range
                los = targeting.Los
                friendly = targeting.Friendly
                enemy = targeting.Enemy
                live = targeting.Live
                dead = targeting.Dead
                callback = targeting.Callback
                
            
            targets = {}
            
            for fighter in self._battle.Fighters:
                if ((fighter.Active and live) or ((fighter.Active == False) and dead)):
                    if enemy and fighter.Faction != source.Faction:
                        targets[fighter] = 0
                    if friendly and fighter.Faction == source.Faction:
                        targets[fighter] = 0
            
            return targets
            
        
        def Show(self):
            self._disp.Show()
            
            
    ###
    # FacingBattlefield
    # A battlefield where the enemy faces 'out' from the screen and we only see
    # portraits of the fighters
    ###
    
    class FacingBattlefield(SimpleBattlefield):
        
        def __init__(self, disp):
            super(FacingBattlefield, self).__init__(disp, facings={'U':(-90, 90), 'D':(90, 270)})
             
        def RegisterFighter(self, fighter, **properties):
            self.PositionFighters()
            
        def PositionFighters(self):
            
            if len(self._battle.Factions) > 0:
                playerFaction = self._battle.Factions[0]
                
                x = len(self._battle.FactionLists[playerFaction])
                
                spacing = (float)(config.screen_width) / (x + 1)
                
                x = 1
                
                for f in self._battle.FactionLists[playerFaction]:
                    pos = BattlePosition((int)(x * spacing), 0.8)
                    pos.SetBattle(self._battle)
                    f._position = pos
                    
                    x = x + 1

            if len(self._battle.Factions) > 1:
                enemyFaction = self._battle.Factions[1]
                
                x = len(self._battle.FactionLists[enemyFaction])
                
                spacing = (float)(config.screen_width) / (x + 2)
                
                x = 1.5
                y = round(config.screen_height * 0.45)
                
                for f in self._battle.FactionLists[enemyFaction]:
                    pos = BattlePosition((int)(x * spacing), (int)(y))
                    pos.SetBattle(self._battle)
                    f._position = pos
                    
                    x = x + 1
                    
            nullPos = BattlePosition(400, 300)
            nullPos.SetBattle(self._battle)
            
            s = ""
            
            for f in self._battle.All:
                s = s + f.Name + " " + str(f.Position.X) + ", " + str(f.Position.Y) + "\n"
                
            #self._battle.Announce(s)
            
        def Show(self):
            self._disp.Show() #hiddenFactions=[self._battle.Factions[0]]
            
    ###
    # PathBattlefield
    # A Battlefield which consists of various arbitrary paths which Fighters traverse.
    ###
    
    class PathBattlefield(Battlefield):
        
        def __init__(self, disp, facings={}):
            self._positions = []
            self._disp = disp
            
            self._rangeCache = {}
            self._pathCache = {}
            
            super(PathBattlefield, self).__init__(facings)

        
        def SetBattle(self, battle):
            self._battle = battle
            self._disp.SetBattle(battle)
        
        def AddPosition(self, pos):
            pos.SetBattle(self._battle)
            self._positions.append(pos)
            
        def AddPositions(self, positions):
            for pos in positions:
                pos.SetBattle(self._battle)
            self._positions.extend(positions)
            
        def AddJoin(self, pos1, pos2):
            pos1.AddJoin(pos2)
        
        def AddOneWay(self, pos1, pos2):
            pos1.AddOneWay(pos2)
            
        def RegisterFighter(self, fighter, position=None, facing=None, **properties):
            if (position == None):
                raise Exception("When adding a Fighter to this kind of Battlefield, you must specify a position with the 'position' parameter.")
                
            if (position in self._positions) == False:
                raise Exception("The position specified does not exist in this Battlefield.")

            if (facing == None):
                facing = self._facings.keys()[0]
                
            fighter.Position = position
            fighter.Facing = facing

        # Returns a list of positions within X spaces of the start point
        def GetPositionsInRadius(self, start, radius=1, callback=None):
            return self.GetPositionsWithinRange(start, radius, fightersImpede=False, sceneryImpedes=False, callback=callback)
            
        # Returns a list of positions between the start and end points inclusive
        def GetPositionsInLine(self, start, end, callback=None):
            range = self.GetRange(start, end, callback=callback)
            positions = self.GetPositionsWithinRange(start, range, fightersImpede=False, sceneryImpedes=False, callback=callback)
            if end in positions:
                return positions[end][1]
            else:
                return [start, end]
        
        # Returns a list of positions in a rectangle between opposite start and end corners.
        def GetPositionsInRect(self, start, end):
            minX = min([start.xpos, end.xpos])
            minY = min([start.ypos, end.ypos])
            maxX = max([start.xpos, end.xpos])
            maxY = max([start.ypos, end.ypos])
            
            results = []
            
            for pos in self._positions:
                if (pos.xpos >= minX) and (pos.xpos <= maxX) and (pos.ypos >= minY) and (pos.ypos <= maxY):
                    results.append(pos)
            
            return results

            
        # Returns a dict of type <fighter> => (range, path taken)
        def GetTargetFighters(self, source, targeting=None, range=1, los=True, callback=None):
            
            friendly = False
            enemy = True
            live = True
            dead = False
            
            if targeting != None:
                range = targeting.Range
                los = targeting.Los
                friendly = targeting.Friendly
                enemy = targeting.Enemy
                live = targeting.Live
                dead = targeting.Dead
                callback = targeting.Callback

            startPos = source.Position
            # Only want the list of positions, don't care about the costs (right now)
            positions = self.GetPositionsWithinRange(startPos, range, fightersImpede=False, sceneryImpedes=False, callback=callback)
            
            targets = {}
            # check all fighters to see if anyone is in these positions; add to list if they are
            for fighter in self._battle.Fighters:
                if ((fighter.Active and live) or ((fighter.Active == False) and dead)) and (fighter.Position in positions.keys()):
                    if enemy and fighter.Faction != source.Faction:
                        targets[fighter] = positions[fighter.Position]
                    if friendly and fighter.Faction == source.Faction:
                        targets[fighter] = positions[fighter.Position]
            
            return targets

        # Returns a dict of type <position> => (range, path taken)
        def GetTargetPositions(self, source, targeting=None, range=1, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[], los=False, callback=None):
            
            if targeting != None:
                range = targeting.Range
                los = targeting.Los
                fightersImpede = targeting.FightersImpede
                sceneryImpedes = targeting.SceneryImpedes
                ignoreFactions = targeting.IgnoreFactions
                callback = targeting.Callback
            
            if range <= 0:
                return {}
            else:
                check = self.GetPositionsWithinRange(source, range, fightersImpede=fightersImpede, sceneryImpedes=sceneryImpedes, ignoreFactions=ignoreFactions, callback=callback)
                
                if (los):
                
                    results = {}
                    for pos in check.keys():
                        losThreshold = _battle.GetLoSThreshold()
                        if losThreshold <= self.CheckLoS(source, pos, fightersImpede=fightersImpede, sceneryImpedes=sceneryImpedes, ignoreFactions=ignoreFactions):
                            results[pos] = check[pos]
                
                    return results
                else:
                    return check
            
        # Returns a dict of type <position> => (range, path taken)
        def GetPositionsWithinRange(self, pos, range, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[], callback=None):
            
            visited = {}
            visited[pos] = (0, [])
            self.innerGetPositionsWithinRange(visited, range, fightersImpede, sceneryImpedes, ignoreFactions, callback=callback)
            
            return visited
            
        # Warning: recursion ahead!
        #TODO: consider 'type' param allowing different types of movement/whatever to have different costs
        
        # Returns a dict of type <position> => (range, path taken)
        def innerGetPositionsWithinRange(self, visited, range, fightersImpede, sceneryImpedes, ignoreFactions, callback=None):

            firstCount = len(visited)

            for pos in visited.keys()[:]:
                
                dist = visited[pos][0]
                
                if callback == None:
                    joins = {}
                    for item in pos.Joins:
                        joins[item] = 1
                else:
                    joins = callback(pos, self)
                    
                for next in joins.keys():
                    
                    valid = True
                
                    if (fightersImpede or sceneryImpedes):
                        o = self.GetOccupants(next)
                        
                        # check all fighters to see if anyone is in this position; return empty set if anyone is in the way.
                        for item in o:
                            if (item.Faction in ignoreFactions) == False:
                                if (fightersImpede and isinstance(item, Fighter) == True and isinstance(item, Scenery) == False):
                                    if item.BlocksPosition:
                                        valid = False
                                elif (sceneryImpedes and isinstance(item, Scenery)):
                                    if item.BlocksPosition:
                                        valid = False
                    
                    stepCost = joins[next]
                        
                    nextDist = dist + stepCost
                    
                    if round(nextDist*1000) > round(range*1000):
                        valid = False
                     
                    if valid and (((next in visited.keys()) == False) or nextDist < visited[next][0]):
                        nextPath = visited[pos][1][:]
                        nextPath.append(pos)
                        
                        visited[next] = (nextDist, nextPath)
                    

                         
            if len(visited) > firstCount:
                self.innerGetPositionsWithinRange(visited, range, fightersImpede, sceneryImpedes, ignoreFactions, callback=callback)
                    
            return
                    
            
        def GetRange(self, pos1, pos2, callback=None):
            
            rangeKey = (pos1, pos2)
            invRangeKey = (pos2, pos1)
            
            if ( rangeKey in self._rangeCache.keys() ):
                return self._rangeCache[ rangeKey ]
            
            visited = {}
            visited[pos1] = 0
            self.InnerGetRange(visited, callback=callback)
            if pos2 in visited.keys():
                
                self._rangeCache[ rangeKey ] = visited[pos2]
                self._rangeCache[ invRangeKey ] = visited[pos2]
                
            else:

                self._rangeCache[ rangeKey ] = -1
                self._rangeCache[ invRangeKey ] = -1
                
            return self._rangeCache[ rangeKey ]
            

        # Breadth-first span of position graph to find shortest routes around the network
        # TODO: include costed transitions (solution in comments below won't work with negative cost transitions - should be banned anyway!)
        def InnerGetRange(self, visited, callback=None):
            
            recurse = False
            
            newEntries = {}
            
            for pos in visited:
                
                dist = visited[pos]
                
                joins = {}
                
                if callback == None:
                    for item in pos.Joins:
                        joins[item] = 1
                else:
                    joins = callback(pos, self)
                
                for next in joins.keys():
                    
                    stepCost = joins[next]
                    
                    #TODO: use cost when using costed transitions
                    nextDist = dist + 1
                    
                    #TODO: check dist as well as existence once using costed transitions
                    if (next in visited.keys()) == False and (next in newEntries.keys()) == False:
                        newEntries[next] = nextDist
                        recurse = True

                        
            for item in newEntries.keys():
                visited[item] = newEntries[item]
                
            if recurse:
                self.InnerGetRange(visited, callback=callback)

        def GetPathLength(self, pos1, pos2, breakPoint=None, callback=None):

            # Check to see if we should fall back on range instead of path length 
            if (breakPoint != None):
                range = self.GetRange(pos1, pos2, callback=callback)
                if range >= breakPoint:
                    return int(round(1.5 * range))
            
            key = (pos1, pos2)
            iKey = (pos2, pos1)
            
            if key in self._pathCache:
                return self._pathCache[key]
            elif iKey in self._pathCache:
                return self._pathCache[iKey]
                
                
            open = {}
            closed = {}
            
            r = self.GetRange(pos1, pos2, callback=callback)
            open[pos1] = (None, 0, r, r)
            
            #for n in pos1.Joins:
            #    empty = True
            #    o = self.GetOccupants(n)
            #    for s in o:
            #        if isinstance(s, Scenery):
            #            empty = False
            #    
            #    if empty:
            #        r = self.GetRange(n, pos2, callback=callback)
            #        open[n] = (pos1, 1, r, r+1)
            
            self.InnerGetPathLength(pos1, pos2, open, closed, callback=callback)
            
            if key in self._pathCache:
                #_battle.Announce("Returning: " + str(self._pathCache[key]))
                return self._pathCache[key]
            elif iKey in self._pathCache:
                #_battle.Announce("Returning: " + str(self._pathCache[iKey]))
                return self._pathCache[iKey]
            else:
                #_battle.Announce("No joy")
                return -1
                
        # tuple: (previous-position, path-length, heuristic-length, total-length)
        # The 'heuristic-length' is the best-guess at how long it would take from this node to the target; presently it defaults to a simple linear-distance check ignoring scenery.
        # The 'path-length' is the total length of the path to this node so far, and the 'total-length' is the estimated total length to the target of this path.
        # The previous-position is maintained so as to allow the path to be traced back.
        # TODO: Turn this into a GetPath rather than GetPathLength method, and write the latter based on the former.
        # Everybody loves A*
        def InnerGetPathLength(self, pos1, pos2, open, closed, callback=None):
            
            count = 0;
            maxCount = 100;
            
            while (pos2 in closed.keys()) == False:
                
                vis = False
                if vis:
                    # Begin visualisation
                    hideList = ["UI_PickFighter_EndTurnButton"]
                    x = 0
                    
                    for pp in closed.keys():
                        
                        tx = str(closed[pp][1]) + ' ' + str(closed[pp][2]) + '\n' + str(closed[pp][3])
                        
                        buttonText = Text(tx, slow=False, style='PickFighterText')
                        fButton = Button(buttonText, clicked=ui.returns(x), style='PickFighterButton')
                        tag = "weightvis_"+str(x)
                        renpy.show(tag, what=fButton, at_list=[pp.Transform], layer=_battle.GetLayer('UI'))
                        hideList.append(tag)
                        x = x + 1
                        
                    for pp in open.keys():
                        
                        tx = str(open[pp][1]) + ' ' + str(open[pp][2]) + '\n' + str(open[pp][3])

                        buttonText = Text(tx, slow=False, style='PickTargetFighterText')
                        fButton = Button(buttonText, clicked=ui.returns(x), style='PickTargetFighterButton')
                        tag = "weightvis_"+str(x)
                        renpy.show(tag, what=fButton, at_list=[pp.Transform], layer=_battle.GetLayer('UI'))
                        hideList.append(tag)
                        x = x + 1
                        
                    buttonText = Text('T', slow=False, style='PickFighterText')
                    fButton = Button(buttonText, clicked=ui.returns(x), style='PickFighterButton')
                    tag = "weightvis_"+str(x)
                    renpy.show(tag, what=fButton, at_list=[pos2.Transform], layer=_battle.GetLayer('UI'))
                    hideList.append(tag)
                    
                    ui.interact()
                    
                    for item in hideList:
                        renpy.hide(item, layer=_battle.GetLayer('UI'))
                    
                    
                    
                    # end visualisation
                
                smallest = None
                # Find smallest open heuristic length and retry
                for x in open.keys():
                    if (smallest == None) or (open[smallest][3] > open[x][3]):
                        smallest = x

                if smallest == None:
                    break
                
                # If we've been going on for too long - say, a hundred squares - give up and give it your best shot for performance reasons.
                count = count + 1
                if (count > maxCount):
                    self._pathCache[(pos1, pos2)] = open[smallest][1]
                    break
                    
                closed[smallest] = open[smallest]
                del open[smallest]
                
                self._pathCache[(pos1, smallest)] = closed[smallest][1]
                
                joins = {}
                if callback == None:
                    for item in smallest.Joins:
                        joins[item] = 1
                else:
                    joins = callback(smallest, self)
                
                for x in joins.keys():
                    empty = True
                    
                    o = self.GetOccupants(x)
                    for s in o:
                        if isinstance(s, Scenery):
                            empty=False

                    if empty:
                        
                        stepCost = joins[x]
                        
                        # TODO: alter this when weighted movement is done
                        l = closed[smallest][1] + stepCost
                        
                        # Check the path cache, and if the node isn't in it, resort to a simple linear-distance. There's no harm in having an accurate figure!
                        if ( (smallest, pos2) in self._pathCache.keys() ):
                            h  = self._pathCache[(smallest, pos2)]
                        else:
                            # TODO: Actually, a simple pythagorean approach would probably make a better heuristic...
                            h = self.GetRange(x, pos2, callback=callback)
                        
                        if (x in closed.keys()) == False:
                            if ((x in open.keys()) == False) or (open[x][3] > (l+h)):
                                open[x] = (smallest, l, h, l+h)
                

        def Show(self, move=True):
            self._disp.Show()
            if move:
                renpy.transition(MoveTransition(0.5))
            
    
    class GridBattlefield(PathBattlefield):
        
        def __init__(self, disp, origin=(0,0), gridSize=(1,1), spaceSize=(100,100),
                diagonals=False, facings={'N':(-45, 45), 'E': (45, 135), 'S':(135, 225), 'W':(225, 315)},
                map=None, heightStep=100, isometric=False):
            self._origin = origin
            self._gridSize = gridSize
            self._spaceSize = spaceSize
            self._diagonals = diagonals
            
            self._map = map
            self._positionMatrix = None
            
            self._grid = BattleGridController(self, self._origin, self._gridSize, self._spaceSize, self._diagonals, map=map, heightStep=heightStep, isometric=isometric)
            
            super(GridBattlefield, self).__init__(disp, facings)
            
            self._battle = None
            
            
        # TODO: Some errors maybe about trying to use a Battlefield before it's had SetBattle called?
        def SetBattle(self, battle):
            self._battle = battle
            self._grid.SetBattle(battle)
            self._disp.SetBattle(battle)
            
        def getPositions(self):
            return self._grid.Positions
        Positions = property(getPositions)
        
        def GetOccupants(self, position):
            
            return self._grid.GetOccupants(position)
        
        def GetPositionMatrix(self):
            
#            if (None == self._positionMatrix or _battle.Rotation == 0):
#                self._positionMatrix = self._grid.GetPositionMatrix();

            return mat.srotate(_battle.Rotation) * self._grid.GetPositionMatrix()
            
        def GetPresentationMatrix(self):
            return self._grid.GetPresentationMatrix()
            
        def Rotate(self, degree):
            
            super(GridBattlefield, self).Rotate(degree)
            
#            x = self._battle.CameraX + (config.screen_width / 2)
#            y = self._battle.CameraY + (config.screen_height / 2)

#            pos = mat.smat(x, y)

#            inverse = mat.sinvert(self.GetPresentationMatrix() * self.GetPositionMatrix())
            
#            pos = inverse * pos
            
#            newX = pos[0][0]
#            newY = pos[1][0]
            
#            newX = round(newX*100)/100
#            newY = round(newY*100)/100
            
#            self._positionMatrix = mat.srotatearound(newX, newY, degree) * self._positionMatrix
            
            
            
            
        
        def AddRect(self, start, end, height=0):
            if (self._battle == None):
                raise Exception("You must have called SetBattlefield on the Battle instance before calling this method.")
            self._grid.AddRect(start, end, height=height)
        
        def RemoveRect(self, start, end):
            if (self._battle == None):
                raise Exception("You must have called SetBattlefield on the Battle instance before calling this method.")
            self._grid.RemoveRect(start, end)
            
        def AddSpace(self, space, height=0):
            if (self._battle == None):
                raise Exception("You must have called SetBattlefield on the Battle instance before calling this method.")
            self._grid.AddRect(space, space, height=height)
            
        def RemoveSpace(self, space):
            if (self._battle == None):
                raise Exception("You must have called SetBattlefield on the Battle instance before calling this method.")
            self._grid.RemoveRect(space, space)
        
        def RegisterFighter(self, fighter, x=0, y=0, facing=None, **properties):

            inside = True
            if (x in self.Positions) == False:
                inside = False
            if (y in self.Positions[x]) == False:
                inside = False
                
            if inside == False:
                raise Exception("Position ("+ str(x) +", "+ str(y) +") not inside grid.")
            
            fighter.Position = self.Positions[x][y]
            
            if (facing == None):
                facing = self._facings.keys()[0]
            
            fighter.Facing = facing
            
            # Lastly, default the fighter's Height and Density to 1 if it's not been previously set.
            
            fighter.RegisterStat("Height", 1)
            fighter.RegisterStat("Density", 1)
            
        def RegisterScenery(self, scenery, **properties):
            self._grid.RegisterScenery(scenery, **properties)

            # Lastly, default the scenery's Height and Density to 1 if it's not been previously set.
            
            scenery.RegisterStat("Height", 1)
            scenery.RegisterStat("Density", 1)
            
        def GetPositionsInRadius(self, start, radius=1, useHeight=True, callback=None):
            return self._grid.GetPositionsInRadius(start, radius, useHeight=useHeight, callback=callback)
        def GetPositionsInLine(self, start, end, callback=None):
            return self._grid.GetPositionsInLine(start, end, callback=callback)
        def GetPositionsInRect(self, start, end):
            return self._grid.GetPositionsInRect

        def GetRange(self, pos1, pos2, callback=None, useHeight=True):
            return self._grid.GetRange(pos1, pos2, callback=callback, useHeight=useHeight)
        
        def CheckLoS(self, pos, target, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[]):
            
            return self._grid.CheckLoS(pos, target, fightersImpede, sceneryImpedes, ignoreFactions)
        
        #TODO: Amend for targeting scenery?
        def GetTargetFighters(self, source, targeting=None, range=1, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[], los=True, callback=None):
            
            friendly = False
            enemy = True
            live = True
            dead = False
            
            if targeting != None:
                range = targeting.Range
                los = targeting.Los
                friendly = targeting.Friendly
                enemy = targeting.Enemy
                live = targeting.Live
                dead = targeting.Dead
                fightersImpede = targeting.FightersImpede
                sceneryImpedes = targeting.SceneryImpedes
                callback = targeting.Callback

            results = self.GetPositionsWithinRange(source.Position, range, fightersImpede=False, sceneryImpedes=False, callback=callback)
            
            losResults = {}

            for fighter in self._battle.Fighters:
                if ((fighter.Active and live) or ((fighter.Active == False) and dead)) and (fighter.Position in results.keys()):
                    valid = False
                    
                    if los:
                        if _battle.GetLoSThreshold() <= self.CheckLoS(source.Position, fighter.Position, fightersImpede, sceneryImpedes, ignoreFactions):
                            valid = True
                    else:
                        valid = True
                        
                    if valid and ((enemy and fighter.Faction != source.Faction) or (friendly and fighter.Faction == source.Faction)):
                        losResults[fighter] = results[fighter.Position]

                            
            return losResults
    
            
    ###
    # BattlePosition
    # This class describes a position in a battlefield
    ###
    
    class BattlePosition(object):
        
        # This expects the X and Y position of the BattlePosition on the screen
        def __init__(self, x, y, height=0, heightStep=100):
            self._pos = (x, y, height)
            self._heightStep = 100;
            
            #TODO: consider moving to a property for form's sake?
            self._joins = []
            
            self._z = 1 + ((y * 1.0) / (config.screen_height * 1.0))
            
        def SetBattle(self, battle):
            self._battle = battle

        def getJoins(self):
            return self._joins
        Joins = property(getJoins)
            
        # Transform
        
        def getTransform(self):
            
            # First, modify the stored x and y values of the position by the current
            # position and presentation transformation matrices.
            pos = mat.smat(self._pos[0], self._pos[1])
            
            bf = self._battle.Battlefield
            
            pos = bf.GetPresentationMatrix() * bf.GetPositionMatrix() * pos
            
            x = pos[0][0]
            y = pos[1][0]
            
            height = self._pos[2]
            
            # Then build a Transform which represents the BattlePosition's final position on the screen.
            # (We have to use int xpos and ypos to avoid Ren'Py interpreting it as a fraction of screen width.)
            return Transform(xanchor=0.5, yanchor=0.5, xpos = int(x), ypos = int(y - (height * float(self._heightStep))), function=BattlePanningFunction)
        Transform = property(getTransform)
            
        # Joins
        def AddJoin(self, position):
            self.AddOneWay(position)
            position.AddOneWay(self)
        
        def AddOneWay(self, position):
            if (position in self.Joins) == False:
                self.Joins.append(position)

        def IsJoined(self, position):
            return position in self.Joins
            
        def RemoveJoin(self, position):
            position.RemoveOneWay(self)
            self.RemoveOneWay(position)
        
        def RemoveOneWay(self, position):
            if (position in self.Joins):
                self._joins.remove(position)
            
            
        # Accessors
        def getX(self):
            return self._pos[0]
        def getY(self):
            return self._pos[1]
        def getHeight(self):
            return self._pos[2]
        def getPosition(self):
            return self._pos
        X = property(getX)
        Y = property(getY)
        Height = property(getHeight)
        Position = property(getPosition)
        
        def getZ(self):
            return self._z
        def setZ(self, value):
            self._z = value
        Z = property(getZ, setZ)

    # BattleGridController maintains the collection of positions in a particular grid, and relates their position in the grid
    # to a position on-screen
    class BattleGridController(object):
        
        def __init__(self, battlefield, origin, gridSize, spaceSize, diagonals, map=None, heightStep=100, isometric=False):
            self._battlefield = battlefield
            self._origin = origin
            self._gridSize = gridSize
            self._spaceSize = spaceSize
            self._diagonals = diagonals
            self._map = map
            self._heightStep = heightStep
            self._isometric = isometric
            
            self._positions = {}
            
            self._genGrid()
            
            # Set heights based on map
            if (map != None):
                for x in range(self.XSize):
                    for y in range(self.YSize):
                        self._positions[x][y].Height = map[x][y].Height
                        
            
            # These two fields describe whether the X and Y axes increase in value
            # as they go 'back' into the screen (1) or decrease (0).
            # This is used to help determine draw order with rectangular scenery.
            self._behindX = 1
            self._behindY = 1
            
#            if (self._offsets[1] > 0):
#                    self._behindX = -1
                    
            if (self._spaceSize[1] > 0):
                    self._behindY = -1
           
        
        def getXSize(self):
            return self._gridSize[0]
        XSize = property(getXSize)
        
        def getYSize(self):
            return self._gridSize[1]
        YSize = property(getYSize)
        
        def getHeightStep(self):
            return self._heightStep
        HeightStep = property(getHeightStep)
        
        def getPositions(self):
            return self._positions
        Positions = property(getPositions)
        
        def GetOccupants(self, position):
            
            checks = self._battle.All

            results = []
            
            for fighter in checks:
                #TODO: Consider whether dead fighters should block - maybe a schema thing?
                if isinstance(fighter, AreaScenery):
                    if (position.X < (fighter.Position.X + fighter.Area[0]) and
                            position.X >= fighter.Position.X and
                            position.Y < (fighter.Position.Y + fighter.Area[1]) and
                            position.Y >= fighter.Position.Y):
                        results.append(fighter)
                else:
                    if (fighter.Position == position) and fighter.Active:
                        results.append(fighter)
            
            return results
        
        def GetPositionMatrix(self):
            return mat.sidentity()
            
        def GetPresentationMatrix(self):
            
            if (self._isometric):
                # To project the point-positions of the grid spaces onto the display, we need to:
                # - rotate by 45 degrees.
                # - scale such that the stepsize given is created between points on a unit grid.
                #   (bearing in mind that the height/width step will start at sqrt(1/2), not 1.)
                # - translate to adjust the origin to the given position on screen.
                
                tran = mat.srotate(-45)
                
                d = math.sqrt(0.5)
                
                xscale = (float(self._spaceSize[0]) / d)
                yscale = (float(self._spaceSize[1]) / d)
                
                tran = mat.sscale(xscale, yscale) * tran
                
                tran = mat.stranslate(self._origin[0], self._origin[1]) * tran
            
                return tran
                
            else:
                # If not isometric, then we simply need to scale the grid such that the gap between
                # each space is equal to the space size in that dimension, then translate to the origin.
                
                tran = mat.sscale(self._spaceSize[0], self._spaceSize[1])
                
                tran = mat.stranslate(self._origin[0], self._origin[1]) * tran
                
                return tran
        
        def GetTransform(self, position):
            
            x = position.X
            y = position.Y
            
            # Modify the stored x and y values of the position by the current
            # position and presentation transformation matrices.
            pos = mat.smat(x, y)
            
            bf = self._battlefield
            
            pos = bf.GetPresentationMatrix() * bf.GetPositionMatrix() * pos
            
            x = pos[0][0]
            y = pos[1][0]
            
            # Adjust y value for height, because height is independent of rotation, projection etc.
            y = y - int(float(position.Height) * float(self._heightStep))

            #TODO: Come 6.11, remove xanchor from this and allow it to be set in style instead.
            return Transform(xanchor=0.5, yanchor=0.5, xpos = int(x), ypos = int(y), function=BattlePanningFunction)
            
        def GetZ(self, position):
            
            x = position.X
            y = position.Y
            
            pos = mat.smat(x, y)
            
            bf = self._battlefield
            
            pos = bf.GetPresentationMatrix() * bf.GetPositionMatrix() * pos
            
            y = pos[1][0]
            #y = self._origin[1] + (y * self._spaceSize[1]) + (x * self._offsets[1])
            
            z = 1 + ((y * 1.0) / (config.screen_height * 1.0))

            return z
            
        def _genGrid(self):
            self.AddRect((0,0), (self.XSize - 1, self.YSize - 1))
            
        def SetBattle(self, battle):
            self._battle = battle
            
            for x in self._positions.keys():
                for y in self._positions[x].keys():
                    self._positions[x][y].SetBattle(battle)
                    
        def RegisterScenery(self, scenery, **properties):
            if isinstance(scenery, AreaScenery):
                for x in self._positions.keys():
                    for y in self._positions[x].keys():
                        dx = x - scenery.Position.X
                        
                        behindX = False
                        behindY = False
                        
                        if (math.copysign(1.0, dx) == self._behindX) or (dx==0):
                            behindX = True
                        dy = y - scenery.Position.Y
                        if (math.copysign(1.0, dy) == self._behindY) or (dy==0):
                            behindY = True
                        
                        if (behindX == False or behindY == False):
                            self._positions[x][y].Z = self._positions[x][y].Z + 1
                        

            
        def AddRect(self, start, end, height=0):
            positions = self._positions
            # This keeps track of the positions we've added in this method
            newPositions = []
            
            startX = min(start[0], end[0])
            endX = max(start[0], end[0])
            startY = min(start[1], end[1])
            endY = max(start[1], end[1])
            
            xSize = endX - startX + 1
            ySize = endY - startY + 1
            
            for xa in range(xSize):
                x = startX + xa
                
                if (x in positions) == False:
                    positions[x] = {}
                
                for ya in range(ySize):
                    y = startY + ya
                    
                    if (y in positions[x]) == False:
                        
                        pos = BattleGridPosition(x, y, height, self)
                        
                        positions[x][y] = pos
                        
                        newPositions.append(pos)
            
            # Next, join up positions
            
            for xa in range(xSize):
                
                x = startX + xa
                
                for ya in range(ySize):
                    
                    y = startY + ya
                    
                    pos = positions[x][y]
                    
                    if (pos in newPositions):
                    
                        self.TryJoin(pos, x + 1, y)
                        self.TryJoin(pos, x - 1, y)
                        self.TryJoin(pos, x, y + 1)
                        self.TryJoin(pos, x, y - 1)
                        
                        if self._diagonals:
                            self.TryJoin(pos, x + 1, y + 1)
                            self.TryJoin(pos, x - 1, y + 1)
                            self.TryJoin(pos, x + 1, y - 1)
                            self.TryJoin(pos, x - 1, y - 1)

        def RemoveRect(self, start, end):
            
            positions = self._positions
            
            startX = min(start[0], end[0])
            endX = max(start[0], end[0])
            startY = min(start[1], end[1])
            endY = max(start[1], end[1])
            
            xSize = endX - startX + 1
            ySize = endY - startY + 1
            
            for xa in range(xSize):
                x = startX + xa
                
                if (x in positions) == False:
                    positions[x] = {}
                
                for ya in range(ySize):
                    y = startY + ya
                    
                    if (y in positions[x]):
                        pos = positions[x][y]
                        
                        self.RemoveJoins(pos)
                        del positions[x][y]
            
            
        def TryJoin(self, pos, x, y):
            if x in self._positions:
                if y in self._positions[x]:
                    if (pos in self._positions[x][y].Joins) == False:
                        pos.AddJoin(self._positions[x][y])
                        
        def RemoveJoins(self, pos):
            for xa in range(3):
                x = pos.X - xa + 1
                
                if x in self._positions:
                    for ya in range(3):
                        y = pos.Y - ya + 1
                        
                        if y in self._positions[x]:
                            
                            self._positions[x][y].RemoveJoin(pos)
                            
        def HasPosition(self, x, y):
            if x in self._positions:
                return y in self._positions[x]
            else:
                return False
                    

        def GetPositionsInRadius(self, start, radius=1, useHeight=True, callback=None):
            
            #TODO: use callback to get true range to positions?
            
            results = []
            
            startHeight = start.Height
            
            for x in range(start.X - radius, start.X + radius + 1): # +1 because range includes lower but notupper bound
                for y in range(start.Y - radius, start.Y + radius +1):
                    dx = startX - x
                    dy = startY - y
                    dist = pow(pow(dx, 2) + pow(dy, 2), 0.5)
                    
                    if dist <= radius:
                        if self.HasPosition(x, y):
                            p = self._positions[x][y]
                            
                            if (useHeight == True):
                                dh = p.Height - start.Height
                                dist = pow(pow(dist, 1) + pow(dh, 2), 0.5)
                                
                                if dist <= radius:
                                    results.append(p)
                            else:
                                results.append(p)
            return results
            
        def GetPositionsInLine(self, start, end, callback=None):
            
            xDiff = end.X - start.X
            yDiff = end.Y - start.Y
            
            x = start.X
            y = start.Y
            
            xStep = 1
            yStep = 1
            
            
            if xDiff < 0:
                xStep = -1
            if yDiff < 0:
                yStep = -1
            
            if xDiff == 0:
                xStep = 0
            if yDiff == 0:
                yStep = 0
            
            if (abs(xDiff) > abs(yDiff)):
                if yStep != 0:
                    yStep = float(yDiff) / float(abs(xDiff))
            else:
                if xStep != 0:
                    xStep = float(xDiff) / float(abs(yDiff))

            results = []
                    
            while ((int(round(x)) == end.X) and (int(round(y)) == end.Y)) == False: # Haven't reached the endpoint yet
                x = x + xStep
                y = y + yStep
                
                posX = int(round(x))
                posY = int(round(y))

                #print ('Step: ' + str(posX) + ', ' + str(posY))
            
                if self.HasPosition(posX, posY):
                    results.append(self._positions[posX][posY])

            return results
            
        def GetPositionsInRect(self, start, end):
            results = []
            for x in range(start.X - radius, start.X + radius + 1): # +1 because range includes lower but notupper bound
                for y in range(start.Y - radius, start.Y + radius +1):
                    if self.HasPosition(x, y):
                        results.append(self._positions[x][y])
            return results
            
        def GetRange(self, pos1, pos2, callback=None, useHeight=True):
            
            #TODO: use callback to count the actual cost of intervening squares?
            
            dX = max(pos1.X, pos2.X) - min(pos1.X, pos2.X)
            dY = max(pos1.Y, pos2.Y) - min(pos1.Y, pos2.Y)
            
            if (self._diagonals):
                dist = max(dX, dY)
            else:
                dist = dX + dY
                
            if useHeight:
                dist = dist + math.fabs(pos1.Height - pos2.Height)
                
            return dist
            

        def CheckLoS(self, pos, target, fightersImpede=True, sceneryImpedes=True, ignoreFactions=[]):
            
            steps = self.GetPositionsInLine(pos, target)
            
            if len(steps) == 0:
                return 1.0
            
            sourceFighterHeight = float(self.getPosFighterHeight(pos))
            targetFighterHeight = float(self.getPosFighterHeight(target))
            
            # We'll use these two variables to track a ray to the target fighter's head (top)
            # and feet (bottom) in the case of a fighter in the target square - otherwise
            # they'll both be the same for a position target.
            bottom = float(pos.Height + sourceFighterHeight)
            top = bottom
            
            # These track the difference that needs to be applied to each of those
            # to meet the target point on the final step
            dhb = ((target.Height) - bottom) / len(steps)
            dht = ((target.Height + targetFighterHeight) - bottom) / len(steps)
            
            # We track the maximum percentage of the target area that we can see in
            # a separate variable. Essentially, if the height of a square in a step
            # obscures up to one third between bottom and top, we remember that as 0.6(6)
            # visible
            
            visible = 1.0
            
            # Next we step through all the positions between source and target checking the
            # heights against each step
            
            for step in steps:
                
                # If the current step is actually the target step we can stop.
                if (step != target):
                    
                    bottom = bottom + dhb
                    top = top + dht
                    
                    stepHeight = step.Height
                    
                    # Get all the blocking occupants of the current step
                    o = self._battlefield.GetOccupants(step)
                    o = [item for item in o if item.BlocksLoS]
                    
                    occupantHeight = 0
                    
                    if len(o) > 0:
                        for f in o:
                            if isinstance(f, Scenery):
                                if (sceneryImpedes and f.Active):
                                    occupantHeight = max(occupantHeight, f.Stats.Height)
                            elif isinstance(f, Fighter):
                                if (fightersImpede and f.Active):
                                    occupantHeight = max(occupantHeight, f.Stats.Height)
                                
                    stepHeight = stepHeight + occupantHeight
                    
                    # floating point 'numbers' are annoying:
                    if round(stepHeight * 1000) > round(top * 1000):
                        return 0
                        
                    #print str(step.X) + "," + str(step.Y) + " - t: " + str(top) + " b: " + str(bottom) + " sH: " + str(stepHeight)
                    
                    # finally, work out what the current maximum visibility is
                    if round(stepHeight * 1000) > round(bottom * 1000):
                        window = top - stepHeight
                        total = top - bottom
                        
                        if (total > 0):
                            visible = min(visible, (window/total))
                        else:
                            # Shouldn't ever happen!
                            visible = 0
                        
            # If we somehow manage to exit the loop without having seen the target square once:
            # TODO: consider exception.
            return visible
            
        def getPosFighterHeight(self, position):
            
            o = self._battlefield.GetOccupants(position)
            
            if len(o) == 0:
                return 0
            
            height = 0
            count = 0
            
            for f in o:
                height = height + f.Stats.Height
                count = count + 1
                
            return height / count
        
    class BattleGridPosition(BattlePosition):
        
        def __init__(self, x, y, height, controller):
            self._controller = controller
            super(BattleGridPosition, self).__init__(x, y, height=height, heightStep=controller.HeightStep)
            
            self._z = None
        
        
        def getTransform(self):
            return self._controller.GetTransform(self)
        Transform = property(getTransform)
    
        def getZ(self):
            if (self._z == None):
                return self._controller.GetZ(self)
            else:
                return self._z
        def setZ(self, value):
            self._z = value
        Z = property(getZ, setZ)
        
        def getHeight(self):
            return self._pos[2]
        def setHeight(self, value):
            self._pos = (self.X, self.Y, value)
        Height = property(getHeight, setHeight)
        
        
        
    class HexGridBattlefield(GridBattlefield):
        def __init__(self, disp, origin=(0,0), gridSize=(1,1), spaceSize=(100, 100),
                facings={'N':(-30, 30), 'NE':(30, 90), 'SE':(90, 150), 'S':(150, 210), 'SW':(210, 270), 'NW':(270, 330)},
                map=None, heightStep=100):
            self._origin = origin
            self._gridSize = gridSize
            self._spaceSize = spaceSize
            self._diagonals = False
            
            self._map = map
            self._positionMatrix = None
            
            self._grid = BattleHexGridController(self, self._origin, self._gridSize, self._spaceSize, map=map, heightStep=100)
            
            super(GridBattlefield, self).__init__(disp, facings)
            
            self._battle = None
                    
        def GetPositionsInRadius(self, start, radius=1, callback=None):
            # For this, we're actually better off using the PathBattlefield implementation
            # than the parent GridBattlefield implementation.
            
            PathBattlefield.GetPositionsInRadius(self, start, radius=radius, callback=callback)

        def GetFacing(self, source, target):
            
            tx = target.X
            ty = target.Y
            
            if (tx % 2) != 0:
                ty = ty + 0.5
                
            sx = source.X
            sy = source.Y
            
            if (sx % 2) != 0:
                sy = sy + 0.5
            
            
            a = math.atan2(tx-sx, ty-sy)
            a = ((a * 360) / (math.pi * 2)) % 360
            
            return self.GetFacingFromAngle(a)
            
            
    class BattleHexGridController(BattleGridController):
        
        def __init__(self, battlefield, origin, gridSize, spaceSize, map=None, heightStep=100):
            super(BattleHexGridController, self).__init__(battlefield, origin, gridSize, spaceSize, False, map=map, heightStep=heightStep)
        
        def GetPositionMatrix(self):
            
            # The distance between hex centres horizontally - need to match it vertically to avoid alignment issues when rotating
            a = math.sqrt(1.25)
            
            return mat.sscale(1, a)
            
        def GetPresentationMatrix(self):
            # To project the point-positions of the grid spaces onto the display, we need to:
            # - scale such that the stepsize given is created between points on a unit grid.
            # - translate to adjust the origin to the given position on screen.
            
            tran = mat.sidentity()
            
            a = math.sqrt(1.25)
            
            xscale = float(self._spaceSize[0])
            yscale = float(self._spaceSize[1]) / a # countering the stretch we put into the position matrix, so that the tile sprites line up properly
            
            tran = mat.sscale(xscale, yscale) * tran
            
            tran = mat.stranslate(self._origin[0], self._origin[1]) * tran
            
            return tran
            
        def GetTransform(self, position):
            
            x = position.X
            y = position.Y
            
            if (x % 2 != 0):
                y = y + 0.5
            
            # Modify the stored x and y values of the position by the current
            # position and presentation transformation matrices.
            pos = mat.smat(x, y)
            
            bf = self._battlefield
            
            pos = bf.GetPresentationMatrix() * bf.GetPositionMatrix() * pos
            
            x = pos[0][0]
            y = pos[1][0]
            
            # Adjust y value for height, because height is independent of rotation, projection etc.
            y = y - int(float(position.Height) * float(self._heightStep))

            #TODO: Come 6.11, remove xanchor from this and allow it to be set in style instead.
            return Transform(xanchor=0.5, yanchor=0.5, xpos = int(x), ypos = int(y), function=BattlePanningFunction)
        
        def GetZ(self, position):
            
            x = position.X
            y = position.Y
            
            if (x % 2 != 0):
                y = y + 0.5
            
            
            pos = mat.smat(x, y)
            
            bf = self._battlefield
            
            pos = bf.GetPresentationMatrix() * bf.GetPositionMatrix() * pos
            
            y = pos[1][0]
            #y = self._origin[1] + (y * self._spaceSize[1]) + (x * self._offsets[1])
            
            z = 1 + ((y * 1.0) / (config.screen_height * 1.0))

            return z
           
        def AddRect(self, start, end, height=0):
            positions = self._positions
            # This keeps track of the positions we've added in this method
            newPositions = []
            
            startX = min(start[0], end[0])
            endX = max(start[0], end[0])
            startY = min(start[1], end[1])
            endY = max(start[1], end[1])
            
            xSize = endX - startX + 1
            ySize = endY - startY + 1
            
            for xa in range(xSize):
                x = startX + xa
                
                if (x in positions) == False:
                    positions[x] = {}
                
                for ya in range(ySize):
                    y = startY + ya
                    
                    if (y in positions[x]) == False:
                        pos = BattleGridPosition(x, y, height, self)
                        
                        positions[x][y] = pos
                        
                        newPositions.append(pos)
            
            # Next, join up positions
            
            for xa in range(xSize):
                
                x = startX + xa
                
                for ya in range(ySize):
                    
                    y = startY + ya
                    
                    pos = positions[x][y]
                    
                    if (pos in newPositions):
                    
                        self.TryJoin(pos, x + 1, y)
                        self.TryJoin(pos, x - 1, y)
                        self.TryJoin(pos, x, y + 1)
                        self.TryJoin(pos, x, y - 1)
                        
                        # Check x % 2 and add up-diagonal or down-diagonal joins as appropriate
                        if (x % 2) != 0:
                            # On an odd row, we need to add a link to y+1 on the prev and next rows
                            self.TryJoin(pos, x-1, y+1)
                            self.TryJoin(pos, x+1, y+1)
                        else:
                            # On an even row, we need to add a link to y-1 on the prev and next rows
                            self.TryJoin(pos, x-1, y-1)
                            self.TryJoin(pos, x+1, y-1)

        def RemoveRect(self, start, end):
            
            positions = self._positions
            
            startX = min(start[0], end[0])
            endX = max(start[0], end[0])
            startY = min(start[1], end[1])
            endY = max(start[1], end[1])
            
            xSize = endX - startX + 1
            ySize = endY - startY + 1
            
            for xa in range(xSize):
                x = startX + xa
                
                if (x in positions) == False:
                    positions[x] = {}
                
                for ya in range(ySize):
                    y = startY + ya
                    
                    if (y in positions[x]):
                        pos = positions[x][y]
                        
                        self.RemoveJoins(pos)
                        del positions[x][y]
                        
        def GetRange(self, pos1, pos2, callback=None, useHeight=True):
            
            #TODO: Use callback to count the actual cost of intervening hexes?
            dX = max(pos1.X, pos2.X) - min(pos1.X, pos2.X)
            dY = max(pos1.Y, pos2.Y) - min(pos1.Y, pos2.Y)

            range = max(dX, dY)
            
            if useHeight:
                dZ = math.fabs(pos1.Height - pos2.Height)
                range = math.sqrt((range * range) + (dZ * dZ))

            return range
            
        def GetPositionsInLine(self, start, end, callback=None):
            
            # The approach we shall use is to treat the hex grid like a grid of rectangles
            # equally wide (x-axis) and twice as tall (y-axis) as it is as hexes. We then
            # scan through these rectangles the same way we do for the regular rectangular
            # grid, and at each step look up the hex at (x, y/2).
            # for this to work, we need to start and end in the upper half of the hex for
            # lines which proceed upwards, and the lower half for lines which proceed
            # downwards.
            
            # This method is therefore similar - but not identical to - the corresponding
            # method on BattleGridController.
            
            startX = start.X
            startY = start.Y * 2 + (startX % 2)
            
            endX = end.X
            endY = end.Y * 2 + (endX % 2)
            
            dx = endX - startX
            dy = endY - startY
            
            xStep = 1
            yStep = 1
            
            
            if dx < 0:
                xStep = -1
            if dy < 0:
                yStep = -1
            
            if dx == 0:
                xStep = 0
            if dy == 0:
                yStep = 0
                
            if dy > 0:
                startY = startY + 1
                endY = endY + 1
                
            
            if (abs(dx) > abs(dy)):
                if yStep != 0:
                    yStep = float(dy) / float(abs(dx))
            else:
                if xStep != 0:
                    xStep = float(dx) / float(abs(dy))

            results = []
            
            x = startX
            y = startY
            
            posX = start.X
            posY = start.Y

            while ((round(x) == endX) and (round(y) == endY)) == False: # Haven't reached the endpoint yet

                x = x + xStep
                y = y + yStep
                
                posX = int(round(x))
                posY = int(round(math.floor(round(y-(posX%2))/2)))
                
                if self.HasPosition(posX, posY):
                    pos = self._positions[posX][posY]
                    if (pos in results) == False:
                        if (pos == start) == False:
                            results.append(pos)

            return results
            

