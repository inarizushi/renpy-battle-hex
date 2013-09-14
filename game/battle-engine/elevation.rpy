init -9 python:

    class ElevationPosition(object):
        def __init__(self, tile, height):
            self.Tile = tile
            self.Height = height

    class ElevationGridSprite(BattlefieldSprite):
        
        def __init__(self, bg, map, origin=(0,0), spaceSize=(100,100),
                        heightStep = 100, anchor=(0.5, 0.25), *args, **properties):
            super(BattlefieldSprite, self).__init__(*args, **properties)
            
            self._bg = ImageReference(bg)
            self._xSize = map.XSize
            self._ySize = map.YSize
            self._origin = origin
            self._spaceSize = spaceSize
            self._anchor = anchor
            
            self._map = map
            self._tiles = map.Tiles
            self._heightStep = heightStep
            
        def Show(self, hiddenFactions=[]):
            
            tran = Transform(xpos=0.5, ypos=0.5, xanchor=0.5, yanchor=0.5)
            
            renpy.show("battleBackground", what=self._bg, at_list=[tran], layer=self._battle.GetLayer("BG"))
            
            bf = self._battle.Battlefield
            
            rot = int(self._battle.Rotation / 90)
            
            for x in range(self._xSize):
                for y in range(self._ySize):
                    
                    p = mat.smat(x, y)
                    p = bf.GetPresentationMatrix() * bf.GetPositionMatrix() * p
                    
                    xp = int(p[0][0])
                    yp = int(p[1][0])
                    
                    pos = self._map[x][y]
                    
                    oyp = yp
                    
                    yp = yp - int(float(pos.Height) * float(self._heightStep))
                    
                    tileParts = self._tiles[pos.Tile].GetParts(rotation=rot)
                    partIndex = 0
                    for part in tileParts:
                        offset = part[0]
                        img = part[1]
                        
                        z = 1 + (((oyp - partIndex) * 1.0) / (config.screen_height * 1.0))
                        
                        t = Transform(xanchor=self._anchor[0], yanchor=self._anchor[1], xpos = xp, ypos = yp + offset, function=BattlePanningFunction)
                        tag = "battleTile_"+str(x)+"_"+str(y)+"_"+str(partIndex)
                        
                        renpy.show(tag, what=img, at_list=[t], layer=self._battle.GetLayer("BG"), zorder=z)
                        
                        partIndex = partIndex + 1
            
            f = self._battle.All
            
            f.sort(Battle_Draw_Compare)
            
            for fighter in f:
                #TODO: something needs to go here for displaying corpses
                if (fighter.Active and (fighter.Faction in hiddenFactions) == False):
                    fighter.Show()

    class ElevationHexGridSprite(ElevationGridSprite):
        
        def __init__(self, bg, map, origin=(0,0), spaceSize=(100,100),
                        heightStep = 100, anchor=(0.5, 0.25), *args, **properties):
            super(BattlefieldSprite, self).__init__(*args, **properties)
            
            self._bg = ImageReference(bg)
            self._xSize = map.XSize
            self._ySize = map.YSize
            self._origin = origin
            self._spaceSize = spaceSize
            self._anchor = anchor
            
            self._map = map
            self._tiles = map.Tiles
            self._heightStep = heightStep
            
        def Show(self, hiddenFactions=[]):
            
            tran = Transform(xpos=0.5, ypos=0.5, xanchor=0.5, yanchor=0.5)
            
            renpy.show("battleBackground", what=self._bg, at_list=[tran], layer=self._battle.GetLayer("BG"))
            
            bf = self._battle.Battlefield
            
            rot = int(self._battle.Rotation / 60)
            
            for x in range(self._xSize):
                for y in range(self._ySize):
                    
                    if (x % 2 != 0):
                        p = mat.smat(x, y + 0.5)
                    else:
                        p = mat.smat(x, y)
                    p = bf.GetPresentationMatrix() * bf.GetPositionMatrix() * p
                    
                    xp = int(p[0][0])
                    yp = int(p[1][0])
                    
                    pos = self._map[x][y]
                    
                    oyp = yp
                    
                    yp = yp - int(float(pos.Height) * float(self._heightStep))
                    
                    tileParts = self._tiles[pos.Tile].GetParts(rotation=rot)
                    partIndex = 0
                    for part in tileParts:
                        offset = part[0]
                        img = part[1]
                        
                        z = 1 + (((oyp - partIndex) * 1.0) / (config.screen_height * 1.0))
                        
                        t = Transform(xanchor=self._anchor[0], yanchor=self._anchor[1], xpos = xp, ypos = yp + offset, function=BattlePanningFunction)
                        tag = "battleTile_"+str(x)+"_"+str(y)+"_"+str(partIndex)
                        
                        renpy.show(tag, what=img, at_list=[t], layer=self._battle.GetLayer("BG"), zorder=z)
                        
                        partIndex = partIndex + 1
            
            f = self._battle.All
            
            f.sort(Battle_Draw_Compare)
            
            for fighter in f:
                #TODO: something needs to go here for displaying corpses
                if (fighter.Active and (fighter.Faction in hiddenFactions) == False):
                    fighter.Show()


    



    class TilesetTile:
        
        def __init__(self):
            # A dict to keep a mapping of rotation-step -> graphic
            self._parts = {}
            
        def AddPart(self, offset, graphic, rotation=0):
            if (rotation in self._parts.keys()) == False:
                self._parts[rotation] = []
                
            self._parts[rotation].append( (offset, graphic) )
            
        def GetParts(self, rotation=0):
            rotation = rotation % len(self._parts.keys())
            
            return self._parts[rotation]
        
    # Tileset files define the graphics used for each tiles, in the following format:
    
    # tile X:
    #   A /image/path_1.png /image/path_2.png /image/path_3.png
    #   B /image/path_1.png /image/path_2.png /image/path_3.png
    
    # X is the tile index, which you will use later when specifying the map itself to refer to the tile.
    # A is a pixel offset downwards to display the first graphic used for that tile at.
    #   Following A are the paths to the actual image files for the first graphic for that tile.
    #   The first image will be used for 0 rotation; each subsequent image will be used for further
    #   rotation steps, looping around to the first again if insufficient steps are provided.
    # B is a pixel offset downwards to display the second graphic used for that tile at.
    #   Following B is another image path. Bear in mind that the first graphic for a tile is drawn on top,
    #   then each successive image behind the previous one. Each graphic for a single tile must have
    #   the same number of rotation steps, but different tiles may have different numbers of sprites.

    # Example tile file:
    
    # tile 0:
    #   0 /tiles/grass.png
    #   0 /tiles/earth-block.png
    #   100 /tiles/deep-earth-block.png
    #
    # tile 1:
    #   0 /tiles/rock-block.png
    #   100 /tiles/deep-rock-block.png
    #
    # tile 2:
    #   0 /tiles/grass.png
    #
    # tile 3:
    #   0 /tiles/road-n-s.png /tiles/road-e-w.png
    
    import re
    
    class TileSet(object):
        def __init__(self, manifest):
            
            self._tiles = {}
            if manifest != None:
                self.LoadTiles(manifest)
            
        def __getitem__(self, index):
            return self._tiles[index]
            
        def __setitem__(self, index, value):
            self._tiles[index] = value
        
        def LoadTiles(self, filename):
            
            file = renpy.file(filename)
            
            data = []
            
            for row in file:
                data.append(row)

            fileLength = len(data)

            # reverse the list so we can use pop because damnit.
            data.reverse()
                
            while len(data) > 0:
                
                line = data.pop().rstrip()
                
                # ignore blank lines
                if len(line) > 0:
                    indent = len(line) - len(line.lstrip())
                    
                    lineNumber = str(fileLength - len(data))
                    
                    if indent > 0:
                        raise Exception("No indentation expected - line " + lineNumber + ":\n"+line)
                        
                    matches = re.match(r"^tile\s+(\d+)\s*:\s*$", line)
                    
                    if matches:
                        tileIndex = int(matches.group(1))
                        
                        if tileIndex in self._tiles:
                            raise Exception("Tile " + str(tileIndex) + " already defined - line " + lineNumber + ":\n" + line)
                            
                        data = self.LoadTile(tileIndex, data, fileLength)
                        
                    else:
                        raise Exception("Directive not understood - line " + lineNumber + ":\n" + line)
                        
        def LoadTile(self, index, data, fileLength):
            
            
            i = 0
            parts = 0
            rotations = 0
            
            tile = TilesetTile()
            
            while len(data) > 0:
                
                line = data.pop().rstrip()
                
                
                # ignore blank lines
                if len(line) > 0:
                    
                    lineNumber = str(fileLength - len(data))                    
                    
                    indent = len(line) - len(line.lstrip())
                    
                    if i > 0 and indent > 0 and indent != i:
                        raise Exception("Indent mismatch - line " + lineNumber + ":\n" + line)
                    elif indent > 0:
                        i = indent
                    else:
                        # if indent is zero, we must have finished this tile
                        if parts == 0:
                            raise Exception("Expected block - line " + lineNumber + ":\n" + line)
                        else:
                            self._tiles[index] = tile
                        
                        data.append(line)
                        return data
                        
                    # flatten whitespace
                    line = re.sub(r"\s+", " ", line)
                    matches = re.match(r"^\s+(\-?\d+)\s+(.*)$", line)
                    
                    if matches:
                        graphic = [Image(x) for x in matches.group(2).split(' ')]
                        if (rotations != 0 and len(graphic) != rotations):
                            raise Exception("All parts of tile must have the same number of rotation sprites - line " + lineNumber + ":\n" + line)
                        else:
                            rotations = len(graphic)
                            
                        offset = int(matches.group(1))
                        
                        for x in range(len(graphic)):
                            tile.AddPart(offset, graphic[x], rotation=x)
                            
                        parts = parts + 1
                    else:
                        raise Exception("Directive not understood - line " + lineNumber + ":\n" + line)
                  
            if parts == 0:
                raise Exception("File terminated without expected block")
            else:
                self._tiles[index] = tile
                
            return []


    # TileMap files describe the layout of tiles and their heights, in the following format:
    
    # tileset /path/to/tileset/file.ts
    # size X Y
    # tiles:
    #   A B C
    #   D E F
    #   G H I
    # heights:
    #   J K L
    #   M N O
    #   P Q R
    
    # The first command, tileset, describes which tileset definition file (see above) to use for the whole map.
    # The second, size, describes the width and height of the map in tiles (X wide by Y tall)
    # The third, tiles, takes a block of values A-I which are the individual tile references of each row
    #   of tiles in the map. Each row of references must be X tiles long, and there must be Y rows.
    # The last, heights, takes a block of values J-R which are the individual heights of each space
    #   in the map, corresponding to the tiles values.
    #   A height of 1 is considered to be approximately as tall as an average person, so a waist-high 
    #   space may have a height of 0.5, and a hole deep enough for a person to stand completely in may 
    #   have a height of -1.


    # Example map file
    
    # tileset filename.ts
    # size 4 3
    # tiles:
    #   0, 0, 2, 0
    #   1, 2, 2, 2
    #   0, 0, 2, 0
    # heights:
    #   0, 0, 0, 0.25
    #   0.5, 0, 0.25, 0.5
    #   0.25, 0.5, 0.5, 0.25

    class TileMap (object):
        def __init__(self, filename):
            self._tileMap = {}
            self._tileSet = None
            self._size = None
            
            if filename != None:
                self.Load(filename)
            else:
                self._tileSet = TileSet(None)
                self._size = (0,0)
            
        # Shouldn't need to implement setitem as anyone trying to replace
        # entire rows deserves all the exceptions they get.
        def __getitem__(self, item):
            return self._tileMap[item]
            
            
        def getTiles(self):
            return self._tileSet
        Tiles = property(getTiles)
        
        def getXSize(self):
            return self._size[0]
        XSize = property(getXSize)
        
        def getYSize(self):
            return self._size[1]
        YSize = property(getYSize)
            
        def Load(self, filename):
            
            file = renpy.file(filename)
            
            data = []
            
            for row in file:
                data.append(row)
                
            fileLength = len(data)
            
            # reverse the list so we can use pop because damnit.
            data.reverse()
                
            while len(data) > 0:
                
                line = data.pop().rstrip()
                
                # ignore blank lines
                if len(line) > 0:
                    indent = len(line) - len(line.lstrip())
                    
                    lineNumber = str(fileLength - len(data))
                    
                    if indent > 0:
                        raise Exception("No indentation expected - line " + lineNumber + ":\n"+line)
                    
                    # Check for 'tileset filename.ts' lines
                    matches = re.match(r"^tileset\s+(.*)$", line)
                    
                    if matches:
                        if self._tileSet != None:
                            raise Exception("Tileset already defined - line " + lineNumber + ":\n" + line)
                        tsFile = matches.group(1)
                        self._tileSet = TileSet(tsFile)
                        continue
                        
                    # Check for 'size x y' lines
                    matches = re.match(r"^size\s+(\d+)\s+(\d+)\s*$", line)
                    
                    if matches:
                        if self._size != None:
                            raise Exception("Size already defined - line " + lineNumber + ":\n" + line)
                        xSize = int(matches.group(1))
                        ySize = int(matches.group(2))
                        self._size = (xSize, ySize)
                        continue
                        
                    # Check for 'tiles:' blocks
                    matches = re.match(r"^tiles\s*:\s*$", line)
                    
                    if matches:
                        if self._tileSet == None:
                            raise Exception("Cannot start tiles until tileset is defined - line " + lineNumber + ":\n" + line)
                        if self._size == None:
                            raise Exception("Cannot start tiles until size is defined - line " + lineNumber + ":\n" + line)
                        data = self.LoadTiles(data, fileLength)
                        continue
                    
                    # Check for 'heights' blocks
                    matches = re.match(r"^heights\s*:\s*$", line)
                    
                    if matches:
                        if self._tileMap == None:
                            raise Exception("Cannot start heights until tiles are defined - line " + lineNumber + ":\n" + line)
                        data = self.LoadHeights(data, fileLength)
                        continue
                    
                    raise Exception("Directive not understood - line " + lineNumber + ":\n" + line)
                    
            # Transpose self._tileMap so it's in an [x][y] format rather than a [y][x] format.
            # (This also involves flipping the X direction because WTF.)

            oldMap = self._tileMap
            newMap = {}
            for x in range(self.XSize):
                newMap[x] = {}
                
            for y in range(self.YSize):
                for x in range(self.XSize):
                    newMap[x][y] = oldMap[self.YSize - (y+1)][x]
                    
            self._tileMap = newMap
            
        
        def LoadTiles(self, data, fileLength):
            
            i = 0
            rows = 0
            
            while len(data) > 0:
                
                line = data.pop().rstrip()
                
                row = {}
                
                # ignore blank lines
                if len(line) > 0:
                    
                    lineNumber = str(fileLength - len(data))                    
                    
                    indent = len(line) - len(line.lstrip())
                    
                    if i > 0 and indent > 0 and indent != i:
                        raise Exception("Indent mismatch - line " + lineNumber + ":\n" + line)
                    elif indent > 0:
                        i = indent
                    else:
                        # if indent is zero, we must have finished this tile
                        if rows == 0:
                            raise Exception("Expected block - line " + lineNumber + ":\n" + line)
                        elif rows < self._size[1]:
                            raise Exception("Tiles block expected " + str(self._size[1]) + " lines - line " + lineNumber + ":\n" + line)
                        
                        data.append(line)
                        return data
                    
                    cells = line.split(",")
                    
                    if len(cells) != self._size[0]:
                        raise Exception("Tiles row expected " + str(self._size[0]) + " items - line " + lineNumber + ":\n" + line)
                    
                    item = 0
                    
                    for cell in cells:
                        row[item] = ElevationPosition(int(cell), 0)
                        item = item + 1
                        
                        
                    self._tileMap[rows] = row
                    
                    rows = rows + 1
                    
            if rows == 0:
                raise Exception("Expected block - line " + lineNumber + ":\n" + line)
            elif rows < self._size[1]:
                raise Exception("Tiles block expected " + str(self._size[1]) + " lines - line " + lineNumber + ":\n" + line)
            
            return []


        def LoadHeights(self, data, fileLength):
            
            i = 0
            rows = 0
            
            while len(data) > 0:
                
                line = data.pop().rstrip()
                
                row = self._tileMap[rows]
                
                # ignore blank lines
                if len(line) > 0:
                    
                    lineNumber = str(fileLength - len(data))                    
                    
                    indent = len(line) - len(line.lstrip())
                    
                    if i > 0 and indent > 0 and indent != i:
                        raise Exception("Indent mismatch - line " + lineNumber + ":\n" + line)
                    elif indent > 0:
                        i = indent
                    else:
                        # if indent is zero, we must have finished this tile
                        if rows == 0:
                            raise Exception("Expected block - line " + lineNumber + ":\n" + line)
                        elif rows < self._size[1]:
                            raise Exception("Heights block expected " + str(self._size[1]) + " lines - line " + lineNumber + ":\n" + line)
                        
                        data.append(line)
                        return data
                    
                    cells = line.split(",")
                    
                    if len(cells) != self._size[0]:
                        raise Exception("Heights row expected " + str(self._size[0]) + " items - line " + lineNumber + ":\n" + line)
                    
                    item = 0
                    
                    for cell in cells:
                        row[item].Height = float(cell)
                        item = item + 1
                        
                    rows = rows + 1
                
            if rows == 0:
                raise Exception("Expected block - line " + lineNumber + ":\n" + line)
            elif rows < self._size[1]:
                raise Exception("Heights block expected " + str(self._size[1]) + " lines - line " + lineNumber + ":\n" + line)
            
            return []














