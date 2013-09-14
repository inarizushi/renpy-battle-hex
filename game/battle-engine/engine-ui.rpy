init -10 python:
    
    ###
    # UIProvider
    # UiProviders are responsible for providing any UI elements necessary for the battle, e.g. picking targets or skills
    ###
        
    class UIProvider(object):
            
        def __init__(self, battle):
            self._battle = battle
            
        # The next two methods should be called before and after any interaction that requires the user to do
        # or wait for something in the UIProvider - otherwise, you may encounter random pauses when the battle
        # is redrawn. This is because of the asynchronous-pause functionality, which needs to know when pauses
        # are taken so as to decrease the pending-pause time.
        # For example, if a magic attack is made which has a two-second animation, and then immediately after
        # the "pick next fighter to use" display is shown, there will still be a two-second pause pending. If the
        # UI is up for more than two seconds, the animation will be finished... but the pause will still be carried
        # out unless these methods are used to ensure it isn't.
        def StartInteraction(self):
            self._startTime = renpy.get_game_runtime()
            
        def EndInteraction(self):
            now = renpy.get_game_runtime()
            diff = now - self._startTime
            self._battle.DecreasePause(diff)
            
        # This method is a replacement for ui.interact which automatically includes the asynch-pause-handling code.
        def Interact(self):
            self.StartInteraction()
            result = ui.interact()
            self.EndInteraction()
            return result
            
        # This method doesn't return anything - just shows the user whatever it's told to show them.
        # In this implementation we're cheating a little, and ignoring the style parameter in favour of just using the narrator.
        # Custom implementations may use style to decorate the announcement differently or even position/pause/forward differently.
        # The pause parameter expects the Announce method to auto-forward after that many seconds, but of course custom
        # implementations are free to ignore that.
        def Announce(self, text, speaker=announcer, pause=3):
            
            self.StartInteraction()
            renpy.say(speaker, text + "{fast}{w="+str(pause)+"}{nw}")
            self.EndInteraction()

        # This method takes a list of strings (faction names) and is expected to return a single string (the picked faction name).            
        def PickTargetFaction(self, source, targets):
            
            l = self._battle.GetLayer("UI")
            
            cancelText = Text("Cancel", slow=False, style='CancelPickTargetFactionText')
            cancelButton = Button(cancelText, clicked=ui.returns(-1), style='CancelPickTargetFactionButton')
            renpy.show("UI_PickTargetFaction_CancelButton", what=cancelButton, layer=l)
            
            buttons=[]
            
            for target in targets:
                fText = Text(target, slow=False, style='PickTargetFactionText')
                fButton = Button(fText, clicked=ui.returns(target), style='PickTargetFactionButton')
                buttons.append(fButton)

            fBox = VBox(style='PickTargetFactionMenu', *buttons)
            fWindow = Window(fBox, style='PickTargetFactionMenuWindow')
            
            renpy.show("UI_PickTargetFaction_Menu", what=fWindow, layer=l)
            
            result = self.Interact()
            
            renpy.hide("UI_PickTargetFaction_CancelButton", layer=l)
            renpy.hide("UI_PickTargetFaction_Menu", layer=l)
            
            if result == -1:
                return None
            else:
                return result

        # This method takes a list of tuples. Each tuple is of the form (<target fighter>, <range to target>).
        # It is expected to return either a single similar tuple for the selected target, or None if no target is selected.
        def PickTargetFighter(self, source, targets):
            
            l = self._battle.GetLayer("UI")
            
            # We have to construct our own displayables, and handle the teardown later (with hideList), because we need to be able to
            # display the UI elements on the battle's 'UI' layer.
            cancelText = Text("Cancel", slow=False, style='CancelPickTargetFighterText')
            cancelButton = Button(cancelText, clicked=ui.returns(-1), style='CancelPickTargetFighterButton')
            renpy.show("UI_PickTargetFighter_CancelButton", what=cancelButton, layer=l)
            
            hideList = ["UI_PickTargetFighter_CancelButton"]
            
            x = 0
            for target in targets.keys():
                
                buttonText = Text(" ", slow=False, style='PickTargetFighterText')
                fButton = Button(buttonText, clicked=ui.returns(x), style='PickTargetFighterButton')
                tag = "UI_PickTargetFighter_FighterButton_"+target.Tag
                offset = Transform(xoffset=target.PlaceMark[0], yoffset=target.PlaceMark[1], xanchor=0.5, yanchor=0.5)
                renpy.show(tag, what=fButton, at_list=[target.Position.Transform, offset], layer=l)
                hideList.append(tag)
                x = x + 1
            
            result = self.Interact()
            
            for item in hideList:
                renpy.hide(item, layer=l)

            if result >= 0:
                t = targets.keys()[result]
                target = (t, targets[t])
            else:
                target = None
            
            return target
            
        # This method takes a list of tuples. Each tuple is of the form (<target position>, <range to target>).
        # It is expected to return either a single similar tuple for the selected target, or None if no target is selected.
        def PickTargetPosition(self, source, targets):
            
            l = self._battle.GetLayer("UI")
            
            # We have to construct our own displayables, and handle the teardown later (with hideList), because we need to be able to
            # display the UI elements on the battle's 'UI' layer.
            cancelText = Text("Cancel", slow=False, style='CancelPickTargetPositionText')
            cancelButton = Button(cancelText, clicked=ui.returns(-1), style='CancelPickTargetPositionButton')
            renpy.show("UI_PickTargetPosition_CancelButton", what=cancelButton, at_list=[Transform(xalign=0.0, yalign=0.0)], layer=l)
            
            hideList = ["UI_PickTargetPosition_CancelButton"]
            
            x = 0
            for target in targets.keys():
                buttonText = Text(" ", slow=False, style='PickTargetPositionText')
                posButton = Button(buttonText, clicked=ui.returns(x), style='PickTargetPositionButton')
                tag = "UI_PickTargetPosition_PositionButton_"+str(target.X)+"_"+str(target.Y)
                renpy.show(tag, what=posButton, at_list=[target.Transform], layer=l)
                hideList.append(tag)
                x = x + 1
                
            result = self.Interact()
            
            for item in hideList:
                renpy.hide(item, layer=l)

                
            if result >= 0:
                t = targets.keys()[result]
                target = (t, targets[t])
            else:
                target = None
                
                
            return target
            

        # This method expects a list of tuples (skill-name-string, skill-available-bool), and will present them as a list of options to the user.
        # It will return the name of the picked skill
        def PickSkill(self, source, options):

            l = self._battle.GetLayer("UI")
            
            titleText = Text(source.Name, slow=False, style=style.PickSkillMenuTitle)
            
            buttons=[]
            available=[]
            
            for item in options:
                returns = None
                if (item[1] == True):
                    available.append(item[0])
                    returns = ui.returns(item[0])
                    
                sText = Text(item[0], slow=False, style=style.PickSkillText[item[0]])
                sButton = Button(sText, clicked=returns, style=style.PickSkillButton[item[0]])
                buttons.append(sButton)
                #buttons.append(sText)

            if _preferences.battle_automatic_skill == True and len(available) == 1:
                return available[0]
                
            sBox = VBox(titleText, style=style.PickSkillMenu, *buttons)
            sWindow = Window(sBox, style=style.PickSkillMenuWindow)
            
            renpy.show("UI_PickSkill_Menu", what=sWindow, at_list=[Transform(xalign=0.5, yalign=0.5)], layer=l)
            
            result = self.Interact()
            
            renpy.hide("UI_PickSkill_Menu", layer=l)
                        
            return result
            
        # This method expects a list of tuples (skill-name-string, skill-available-bool), and will present them as a list of options to the user.
        # It will return the name of the picked skill, or -1 to go back up the skill tree.
        def PickSubSkill(self, source, options):
            
            l = self._battle.GetLayer("UI")
            buttons=[]
            
            sText = Text("Back", slow=False, style=style.PickSubSkillText['Back'])
            sButton = Button(sText, clicked=ui.returns(-1), style=style.PickSubSkillButton['Back'])
            buttons.append(sButton)

            
            for item in options:
                returns = None
                if (item[1] == True):
                    returns = ui.returns(item[0])
                    
                sText = Text(item[0], slow=False, style=style.PickSkillText[item[0]])
                sButton = Button(sText, clicked=returns, style=style.PickSkillButton[item[0]])
                buttons.append(sButton)

            sBox = VBox(style='PickSubSkillMenu', *buttons)
            sWindow = Window(sBox, style='PickSubSkillMenuWindow')
            
            renpy.show("UI_PickSubSkill_Menu", what=sWindow, at_list=[Transform(xalign=0.5, yalign=0.5)], layer=l)
            
            result = self.Interact()
            
            renpy.hide("UI_PickSubSkill_Menu", layer=l)
                        
            return result
            
            
        # This method expects a list of fighters, and is expected to return the single fighter that is picked.
        # 'None' is returned to signal the end of the turn instead.
        def PickFighter(self, fighters):
            
            l = self._battle.GetLayer("UI")
            
            endText = Text("End Turn", slow=False, style='EndTurnPickFighterText')
            endButton = Button(endText, clicked=ui.returns(-1), style='EndTurnPickFighterButton')
            renpy.show("UI_PickFighter_EndTurnButton", what=endButton, layer=l)
            
            buttons=[]
            
            
            x = 0
            
            for fighter in fighters:
                if fighter.Active:
                    fText = Text(fighter.Name, slow=False, style=style.PickFighterText[fighter.Name])
                    fButton = Button(fText, clicked=ui.returns(x), style=style.PickFighterButton[fighter.Name])
                    buttons.append(fButton)
                x = x + 1

            fBox = VBox(style='PickFighterMenu', *buttons)
            fWindow = Window(fBox, style='PickFighterMenuWindow')
            
            #TODO: take Transform out, use style instead
            renpy.show("UI_PickFighter_Menu", what=fWindow, at_list=[Transform(xalign=0.5, yalign=0.5)], layer=l)
            
            result = self.Interact()
            
            renpy.hide("UI_PickFighter_Menu", layer=l)
            renpy.hide("UI_PickFighter_EndTurnButton", layer=l)
            
            if result == -1:
                return None
            else:
                return fighters[result]
            
        # Expects to be working with a list of tuples (name, quantity, item-instance)
        def PickItem(self, items):
            
            l = self._battle.GetLayer("UI")
            buttons = []
            
            cancelText = Text("Cancel", slow=False, style='CancelPickItemText')
            cancelButton = Button(cancelText, clicked=ui.returns(-1), style='CancelPickItemButton')
            renpy.show("UI_PickItem_CancelButton", what=cancelButton, at_list=[Transform(xalign=0.0, yalign=0.0)], layer=l)
            
            x = 0
            
            for i in items:
                name = i[0]
                quantity = i[1]
                
                iText = Text("%(n)s (%(q)s)" % {'n': name, 'q': quantity}, slow=False, style=style.PickItemText[name])
                iButton = Button(iText, clicked=ui.returns(x), style=style.PickItemButton[name])
                buttons.append(iButton)
                x = x + 1
                
            if (x == 0):
                iText = Text("(none)", slow=False, style=style.PickItemText["none"])
                iButton = Button(iText, clicked=None, style=style.PickItemButton["none"])
                buttons.append(iButton)
                
            iBox = VBox(style='PickItemMenu', *buttons)
            iWindow = Window(iBox, style='PickItemMenuWindow')
            
            #TODO: take Transform out, use style instead
            renpy.show('UI_PickItem_Menu', what=iWindow, at_list=[Transform(xalign=0.5, yalign=0.5)], layer=l)
            
            result = self.Interact()
            
            renpy.hide('UI_PickItem_Menu', layer=l)
            renpy.hide('UI_PickItem_CancelButton', layer=l)

            if (result == -1):
                return None
            else:
                return items[result][2]
                
                
                
    ###
    # TileUIProvider
    # TileUIProvider differs from the regular UI provider in two regards:
    # - It intends to highlight the positions for target positions appropriately, in place on the tiles, using a configurable highlight graphic
    # - It adds rotation controls to several UI interactions to allow the user to rotate the tilemap by a configurable degree.
    #   (Unicode characters used for rotation: ↺ for rotate-left, ↻ for rotate-right.)
    ###
        
    class TileUIProvider(UIProvider):
            
        def __init__(self, highlight=None, highlightHover=None, rotation=90):
            self._highlight = highlight
            self._highlightHover = highlightHover
            self._rotation = rotation
            
        def __call__(self, battle):
            self._battle = battle
            return self
            
        # This method takes a list of tuples. Each tuple is of the form (<target fighter>, <range to target>).
        # It is expected to return either a single similar tuple for the selected target, or None if no target is selected.
        def PickTargetFighter(self, source, targets):
            
            l = self._battle.GetLayer("UI")
            
            # We have to construct our own displayables, and handle the teardown later (with hideList), because we need to be able to
            # display the UI elements on the battle's 'UI' layer.
            cancelText = Text("Cancel", slow=False, style='CancelPickTargetFighterText')
            cancelButton = Button(cancelText, clicked=ui.returns(-1), style='CancelPickTargetFighterButton')
            renpy.show("UI_PickTargetFighter_CancelButton", what=cancelButton, layer=l)
            
            rotateLeftButtonText = Text(u"↺", slow=False, style='RotateButtonText')
            rotateLeftButton = Button(rotateLeftButtonText, clicked=ui.returns(-2), style="RotateButton")
            renpy.show("UI_PickTargetFighter_RotateLeftButton", what=rotateLeftButton, at_list=[Transform(xalign=0.0, yalign=0.5)], layer=l)
            
            rotateRightButtonText = Text(u"↻", slow=False, style='RotateButtonText')
            rotateRightButton = Button(rotateRightButtonText, clicked=ui.returns(-3), style="RotateButton")
            renpy.show("UI_PickTargetFighter_RotateRightButton", what=rotateRightButton, at_list=[Transform(xalign=1.0, yalign=0.5)], layer=l)
            
            
            hideList = ["UI_PickTargetFighter_CancelButton", "UI_PickTargetFighter_RotateLeftButton", "UI_PickTargetFighter_RotateRightButton"]
            
            x = 0
            for target in targets.keys():
                
                buttonText = Text(" ", slow=False, style='PickTargetFighterText')
                fButton = Button(buttonText, clicked=ui.returns(x), style='PickTargetFighterButton')
                tag = "UI_PickTargetFighter_FighterButton_"+target.Tag
                offset = Transform(xoffset=target.PlaceMark[0], yoffset=target.PlaceMark[1], xanchor=0.5, yanchor=0.5)
                renpy.show(tag, what=fButton, at_list=[target.Position.Transform, offset], layer=l)
                hideList.append(tag)
                x = x + 1
            
            result = self.Interact()
            
            for item in hideList:
                renpy.hide(item, layer=l)

            if result >= 0:
                t = targets.keys()[result]
                target = (t, targets[t])
            elif result == -1:
                target = None
            elif result == -2:
                self._battle.Rotate(-1 * self._rotation, source.Position)
                self._battle.Battlefield.Show()
                return self.PickTargetFighter(source, targets)
            elif result == -3:
                self._battle.Rotate(self._rotation, source.Position)
                self._battle.Battlefield.Show()
                return self.PickTargetFighter(source, targets)
            
            return target
            
        # This method takes a list of tuples. Each tuple is of the form (<target position>, <range to target>).
        # It is expected to return either a single similar tuple for the selected target, or None if no target is selected.
        def PickTargetPosition(self, source, targets):
            
            l = self._battle.GetLayer("Fighters")
            
            cancelText = Text("Cancel", slow=False, style='CancelPickTargetPositionText')
            cancelButton = Button(cancelText, clicked=ui.returns(-1), style='CancelPickTargetPositionButton')
            renpy.show("UI_PickTargetPosition_CancelButton", what=cancelButton, at_list=[Transform(xalign=0.0, yalign=0.0)], layer=self._battle.GetLayer("UI"))
            
            
            
            rotateLeftButtonText = Text(u"↺", slow=False, style='RotateButtonText')
            rotateLeftButton = Button(rotateLeftButtonText, clicked=ui.returns(-2), style="RotateButton")
            renpy.show("UI_PickTargetPosition_RotateLeftButton", what=rotateLeftButton, at_list=[Transform(xalign=0.0, yalign=0.5)], layer=self._battle.GetLayer("UI"))
            
            rotateRightButtonText = Text(u"↻", slow=False, style='RotateButtonText')
            rotateRightButton = Button(rotateRightButtonText, clicked=ui.returns(-3), style="RotateButton")
            renpy.show("UI_PickTargetPosition_RotateRightButton", what=rotateRightButton, at_list=[Transform(xalign=1.0, yalign=0.5)], layer=self._battle.GetLayer("UI"))
            
            

            hideList = []

            # Here we loop through all the potential targets and draw buttons for them on the screen, with
            # each button returning the index in the list.
            x = 0
            for target in targets.keys():
                
                buttonImage = self._highlight
                posButton = Button(buttonImage, clicked=ui.returns(x), style='PickElevationTargetPositionButton')
                
                tag = "UI_PickTargetPosition_PositionButton_"+str(target.X)+"_"+str(target.Y)
                renpy.show(tag, what=posButton, at_list=[target.Transform], layer=l, zorder=target.Z)
                hideList.append(tag)
                x = x + 1
                
            result = self.Interact()
            
            for item in hideList:
                renpy.hide(item, layer=l)
            renpy.hide("UI_PickTargetPosition_CancelButton", layer=self._battle.GetLayer("UI"))
            renpy.hide("UI_PickTargetPosition_RotateLeftButton", layer=self._battle.GetLayer("UI"))
            renpy.hide("UI_PickTargetPosition_RotateRightButton", layer=self._battle.GetLayer("UI"))

            # If the result was equal or greater than zero, it means the user picked a position, so
            # we return the tuple for that position
            if result >= 0:
                t = targets.keys()[result]
                target = (t, targets[t])
            # If the result was less than zero, it means the user picked Cancel or one of the rotation buttons, so we return None.
            else:
                if result == -1:
                    return None
                elif result == -2:
                    self._battle.Rotate(-1 * self._rotation, source.Position)
                    self._battle.Battlefield.Show()
                    return self.PickTargetPosition(source, targets)
                elif result == -3:
                    self._battle.Rotate(self._rotation, source.Position)
                    self._battle.Battlefield.Show()
                    return self.PickTargetPosition(source, targets)
                
            return target
            

        # This method expects a list of fighters, and is expected to return the single fighter that is picked.
        # 'None' is returned to signal the end of the turn instead.
        def PickFighter(self, fighters):
            
            l = self._battle.GetLayer("UI")
            
            endText = Text("End Turn", slow=False, style='EndTurnPickFighterText')
            endButton = Button(endText, clicked=ui.returns(-1), style='EndTurnPickFighterButton')
            renpy.show("UI_PickFighter_EndTurnButton", what=endButton, layer=l)
            
            rotateLeftButtonText = Text(u"↺", slow=False, style='RotateButtonText')
            rotateLeftButton = Button(rotateLeftButtonText, clicked=ui.returns(-2), style="RotateButton")
            renpy.show("UI_PickFighter_RotateLeftButton", what=rotateLeftButton, at_list=[Transform(xalign=0.0, yalign=0.5)], layer=l)
            
            rotateRightButtonText = Text(u"↻", slow=False, style='RotateButtonText')
            rotateRightButton = Button(rotateRightButtonText, clicked=ui.returns(-3), style="RotateButton")
            renpy.show("UI_PickFighter_RotateRightButton", what=rotateRightButton, at_list=[Transform(xalign=1.0, yalign=0.5)], layer=l)
            

            buttons=[]
            
            
            x = 0
            
            for fighter in fighters:
                if fighter.Active:
                    fText = Text(fighter.Name, slow=False, style=style.PickFighterText[fighter.Name])
                    fButton = Button(fText, clicked=ui.returns(x), style=style.PickFighterButton[fighter.Name])
                    buttons.append(fButton)
                x = x + 1

            fBox = VBox(style='PickFighterMenu', *buttons)
            fWindow = Window(fBox, style='PickFighterMenuWindow')
            
            #TODO: take Transform out, use style instead
            renpy.show("UI_PickFighter_Menu", what=fWindow, at_list=[Transform(xalign=0.5, yalign=0.5)], layer=l)
            
            result = self.Interact()
            
            renpy.hide("UI_PickFighter_Menu", layer=l)
            renpy.hide("UI_PickFighter_EndTurnButton", layer=l)
            renpy.hide("UI_PickFighter_RotateLeftButton", layer=l)
            renpy.hide("UI_PickFighter_RotateRightButton", layer=l)
            
            if result < 0:
                if result == -1:
                    return None
                elif result == -2:
                    self._battle.Rotate(-1 * self._rotation, source.Position)
                    self._battle.Battlefield.Show()
                    return self.PickFighter(fighters)
                elif result == -3:
                    self._battle.Rotate(self._rotation, source.Position)
                    self._battle.Battlefield.Show()
                    return self.PickFighter(fighters)
            else:
                return fighters[result]
            
        
                

