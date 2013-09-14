init -10 python:
    
    def BattlePanningFunction(transform, st, at):
        
        if '_battle' in globals():
            return _battle.BattlePanningFunction(transform, st, at)
        else:
            transform.xoffset = 0 - _battle.CameraX
            transform.yoffset = 0 - _battle.CameraY
            return 0.1
    
    class BattleDisplay(object):
        @staticmethod
        def GetPanningTransform(child=None):
            return Transform(child=child, function=BattlePanningFunction)
    
            
    class MoveFunction:
        
        def __init__(self, x1, y1, x2, y2, period=0.5):
            self._x1 = x1
            self._y1 = y1
            self._x2 = x2
            self._y2 = y2
            self._period = period
            
        def __call__(self, transform, st, at):
            
            if (st > self._period):
                transform.xpos = self._x2
                transform.ypos = self._y2
                return 100
            else:
                t = st/self._period
                dx = self._x2 - self._x1
                dy = self._y2 - self._y1
                
                transform.xpos = self._x1 + int(round(t * dx))
                transform.ypos = self._y1 + int(round(t * dy))
                
                return 0
            
            
    class MoveJumpFunction:
        
        def __init__(self, x1, y1, x2, y2, period=0.5, height=50):
            self._x1 = x1
            self._y1 = y1
            self._x2 = x2
            self._y2 = y2
            self._period = period
            self._height = height
            #self._sineScale = math.pi/period
            
        def __call__(self, transform, st, at):
            
            if (st > self._period):
                transform.xpos = self._x2
                transform.ypos = self._y2
                return 100
            else:
                t = st/self._period
                dx = self._x2 - self._x1
                dy = self._y2 - self._y1
                
                jumpHeight = math.sin(t*math.pi) * self._height
                
                transform.xpos = self._x1 + int(round(t * dx))
                transform.ypos = self._y1 + int(round(t * dy)) - int(jumpHeight)
                
                return 0
            
            
    ###
    # BattleDisplayable
    # BattleDisplayable is a version of Displayable ready for use in Battles, with the corresponding methods to take advantage of battle-related events
    ###
    
    class BattleDisplayable (renpy.Displayable, BattleAware):
        
        def __init__(self, anchor=(0.5, 0.5), placeMark=(0,0), *args, **properties):
            super(BattleDisplayable, self).__init__(*args, **properties)
            self._anchor = anchor
            self._placeMark = placeMark
        
        def getAnchor(self):
            return self._anchor
        Anchor = property(getAnchor)

        def getPlaceMark(self):
            return self._placeMark
        PlaceMark = property(getPlaceMark)
        
        
        # visit does nothing in default implementation, but if you subclass this class,
        # you must implement visit to supply a list of child displayables
        def visit(self):
            return []
        
        # render actually draws the BattleDisplayable... or at least, provides a Render
        # instance that can be used to draw it onto another surface later
        def render(self, width, height, st, at):
            
            render = renpy.Render(10, 10)
            return render
            
        def SetBattle(self, battle):
            self._battle = battle
            

            
            
    ###
    # BattleSprite
    # This class presents a BattleDisplayable used as a sprite for a Fighter
    ###
    
    class BattleSprite(BattleDisplayable):
        
        def __init__(self, disp, *args, **properties):
            
            # _sprites: {facing: {state-name: sprite}}
            self._sprites = {}
            # _transitions: {(from-state, facing):{(to-state, facing): sprite}}
            self._transitions = {}
            self.AddStateSprite("default", disp)
            self._currentState = "default"
            self._angle = 0
            self._battle = None
            super(BattleSprite, self).__init__(*args, **properties)
        
        def visit(self):
            sprites = []
            for facingKey in self._sprites.keys():
                for stateKey in self._sprites[facingKey].keys():
                    s = self._sprites[facingKey][stateKey]
                    if (s != None):
                        sprites.append(s)
            
            return sprites
            
        def Copy(self):
            copy = BattleSprite(self._sprites["default"], anchor=self._anchor, placeMark=self._placeMark)
            copy._sprites = self._sprites.copy()
            copy._transitions = self._transitions.copy()
            copy._currentState = "default"
            copy._facing = None
            return copy

            
        def getFacing(self):
            if (self._battle != None):
                return self._battle.GetFacingFromAngle(self._angle)
            else:
                return None
        def setFacing(self, val):
            if (isinstance(val, str) == False):
                raise Exception("Facing of BattleSprite set to something other than string.")
            if (self._battle != None):
                self._angle = self._battle.GetAngleFromFacing(val)

        Facing = property(getFacing, setFacing)
    
        def AddStateSprite(self, state, disp, facing=None):
            
            if (disp != None):
                #disp = BattleDisplay.GetPanningTransform(ImageReference(disp))
                disp = ImageReference(disp)
            
            if facing == None:
                facing = 'default'
            if (facing in self._sprites.keys()) == False:
                self._sprites[facing] = {}
            self._sprites[facing][state] = disp
            
            # If this state doesn't have a default sprite, add it to the default list as well
            if (state in self._sprites['default'].keys()) == False:
                self._sprites['default'][state] = disp

        # Meaningful Transitions are:
        # - default -> acting
        # - acting -> default
        # - default -> damage
        # - damage -> default
        # - default -> dying
        # - default -> moving
        # - moving -> moving (different facings!)
        # - moving -> default
        # - default -> melee
        # - melee -> default
        # - default -> magic
        # - magic -> default
        def AddStateTransition(self, fromState, toState, disp, duration, fromFacing=None, toFacing=None):
            #TODO: check types?
            
            if (fromFacing == None):
                fromFacing = 'default'
            if (toFacing == None):
                toFacing = 'default'

            source = (fromState, fromFacing)
            target = (toState, toFacing)

            if (source in self._transitions.keys()) == False:
                self._transitions[source] = {}
            
            #self._transitions[source][target] = (ImageReference(disp), duration)
            self._transitions[source][target] = (disp, duration)

        # Known states are:
        # - default (default!)
        # - acting (whenever this fighter performs an action)
        # - damage (taking damage)
        # - dying (upon health=0, removal from battlefield)
        # - melee
        # - moving
        # - magic
        # - leapup
        # - leapdown
        def SetState(self, state):
            if state == self._currentState:
                return
            self._currentState = state
                        
        # Allow extras and so on to check whether a state exists, in case they want to provide a default themselves.
        def HasState(self, state):
            # All states added should have at least an entry in the 'default' facing
            if state in self._sprites['default'].keys():
                return True
            else:
                return False
                
        # TODO: Take layer as a parameter to this?
        def ShowNewState(self, state, tag, position, facing=None):
            

            if facing == None:
                facing = self.Facing
            
            #TODO: Is this in fact a FighterSprite? Maybe the layer should be added to the initialiser?
            l = self._battle.GetLayer("Fighters")
            
            anchor = Transform(xanchor=self._anchor[0], yanchor=self._anchor[1])

            #check whether there's an appropriate transition
            prevState = self._currentState
            
            foundTransition = False
            tranSource = None
            tranTarget = None
            
            oldFacing = self.Facing
            newFacing = facing

            if (state == prevState and oldFacing == facing):
                return
            
            #TODO: Some better debugging mechanism
            #print("Looking for transition from " + prevState + "[" + oldFacing + "] to " + state + "[" + newFacing + "]")
            
            # check every combination of transition and facing, in order of preference
            if (prevState, oldFacing) in self._transitions.keys() and (state, newFacing) in self._transitions[(prevState, oldFacing)].keys():
                tranSource = (prevState, oldFacing)
                tranTarget = (state, newFacing)
                foundTransition = True
            elif (prevState, 'default') in self._transitions.keys() and (state, newFacing) in self._transitions[(prevState, 'default')].keys():
                tranSource = (prevState, 'default')
                tranTarget = (state, newFacing)
                foundTransition = True
            elif (prevState, oldFacing) in self._transitions.keys() and (state, 'default') in self._transitions[(prevState, oldFacing)].keys():
                tranSource = (prevState, oldFacing)
                tranTarget = (state, 'default')
                foundTransition = True
            elif (prevState, 'default') in self._transitions.keys() and (state, 'default') in self._transitions[(prevState, 'default')].keys():
                tranSource = (prevState, 'default')
                tranTarget = (state, 'default')
                foundTransition = True
            
            if foundTransition:
                #print("Found transition from " + tranSource[0] + "[" + tranSource[1] + "] to " + tranTarget[0] + "[" + tranTarget[1] + "]")

                # draw the transition
                tran = self._transitions[tranSource][tranTarget]
                
                if (tran[0] != None):
                    renpy.hide(tag, layer=l)
                    renpy.show(tag, what=tran[0], at_list=[position.Transform, anchor], layer=l, zorder=position.Z)
                
                # pause for the appropriate period
                _battle.Pause(tran[1])
            else:
                #print("No transition found.")
                None

            # draw the new state
            self.SetState(state)
            self.Facing = facing

            renpy.hide(tag, layer=l)
            renpy.show(tag, what=self, at_list=[position.Transform, anchor], layer=l, zorder=position.Z)
            #renpy.transition(Dissolve(0.1))
            
            
        def render(self, width, height, st, at):     
            
            disp = None
            
            facing = self.Facing
            
            if facing in self._sprites.keys():
            
                
                if self._currentState in self._sprites[facing].keys():

                    disp = self._sprites[facing][self._currentState]
                elif 'default' in self._sprites[facing].keys():
                    disp = self._sprites[facing]['default']
            
            if disp == None:
                if self._currentState in self._sprites['default'].keys():
                    disp = self._sprites['default'][self._currentState]
                else:
                    disp = self._sprites["default"]['default']
                
            # These next four lines relate to an issue where ATL transforms caught inside ImageReferences displayed like this
            # don't re-animate from the beginning, leading to things like the magic attack spells just consisting of a single frame
            # on second or subsequent uses.
            # If the target of the ImageReference (all things in the _sprites/state dict are ImageReference instances) is an
            # ATLTransform, then it needs to be called to reset it; thanks to PyTom for the instruction here. 
            
            if disp != None:
            
                disp.find_target()
                disp = disp.target
                
                if isinstance(disp, renpy.display.motion.ATLTransform):
                    disp = disp()
                        
                childRender = renpy.render(disp, width, height, st, at)
                
                renpy.redraw(self, 0.1)
                
                return childRender
            else:
                return renpy.Render(0, 0)
    
    class BattlefieldSprite(BattleDisplayable):
        
        def __init__(self, disp, *args, **properties):
            super(BattlefieldSprite, self).__init__(*args, **properties)
            self._disp = BattleDisplay.GetPanningTransform(ImageReference(disp))
            
        def Show(self, hiddenFactions=[]):
            
            tran = Transform(xpos=0, ypos=0, xanchor=0, yanchor=0)
            
            renpy.show("battleBackground", what=self._disp, at_list=[tran], layer=self._battle.GetLayer("BG"))
            
            f = self._battle.All
            
            f.sort(Battle_Draw_Compare)
            
            for fighter in f:
                #TODO: something needs to go here for displaying corpses
                if (fighter.Active and (fighter.Faction in hiddenFactions) == False):
                    fighter.Show()
                    
        def render(self, width, height, st, at):     
            
            disp = self._disp
            
            if disp != None:
            
                childRender = renpy.render(disp, width, height, st, at)
                
                renpy.redraw(self, 0.1)
                
                return childRender
            else:
                return renpy.Render(0, 0)
                    
