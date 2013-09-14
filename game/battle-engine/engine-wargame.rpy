init python:
            
    class WargameSchema(SimpleTurnSchema):
                    
        def SetUpFighter(self, fighter, **properties):
            fighter.RegisterStat("Attack", 1)
            fighter.RegisterStat("Move", 1)
            
        def GetMechanic(self):
            return WargameMechanic(self._battle)
            
        def GetAttackResolver(self):
            return WargameAttackResolver()
            
        def GetUIProvider(self):
            return WargameUIProvider(self._battle)
    
    class WargameUIProvider(UIProvider):

        def PickFighter(self, fighters):
            
            l = self._battle.GetLayer("UI")

            endText = Text("End Turn", slow=False, style='EndTurnPickTargetFighterText')
            endButton = Button(endText, clicked=ui.returns(-1), style='EndTurnPickTargetFighterButton')
            renpy.show("UI_PickFighter_EndTurnButton", what=endButton, layer=l)
                                    
            hideList = ["UI_PickFighter_EndTurnButton"]

            x = 0
            
            for fighter in fighters:

                buttonText = Text(" ", slow=False, style='PickTargetFighterText')
                fButton = Button(buttonText, clicked=ui.returns(x), style='PickTargetFighterButton')
                tag = "UI_PickTargetFighter_FighterButton_"+fighter.Tag
                offset = Transform(xoffset=fighter.PlaceMark[0], yoffset=fighter.PlaceMark[1], xanchor=0.5, yanchor=0.5)
                renpy.show(tag, what=fButton, at_list=[fighter.Position.Transform, offset], layer=l)
                hideList.append(tag)
                x = x + 1

            
            result = self.Interact()

            for d in hideList:
                renpy.hide(d, layer=l)

            if (result == -1):
                return None
            else:
                return fighters[result]

    class WargameAttackResolver(AttackResolver):
        
        def SetUpFighter(self, fighter):
            fighter.RegisterStat("Defence", 1)
        
        def ResolveAttack(self, attacker, attack, attributes, target, range=1, **parameters):
            
            # Here we use a very simple CRT to determine battle results:
            
            #         1-3  1-2  1-1  2-1  3-1
            #   1     AD   AD   AD   SM    SM
            #   2     AD   AD   SM   SM    DD
            #   3     AD   SM   SM   DD    DD
            #   4     SM   SM   DD   DD   DD
            
            # We'll represent the odds as a number between -2 and 2, being the number of rows in the 1-1
            # column to shift up or down.
            
            odds = 0
            
            defend = target.Stats.Defence
            
            if (attack > defend):
                if (defend == 0):
                    ratio = 3
                else:
                    ratio = (attack - (attack % defend)) / defend
                if (ratio > 3):
                    ratio = 3
                    
                _battle.Announce("Ratio: " + str(ratio) + ":1")
                odds = ratio - 1
            else:
                if (attack == 0):
                    ratio = 3
                else:
                    ratio = (defend - (defend % attack)) / attack
                if (ratio > 3):
                    ratio = 3
                    
                _battle.Announce("Ratio: 1:" + str(ratio))
                odds = (ratio - 1) * -1
            
            result = odds + renpy.random.choice([1, 2, 3 ,4])
            
            if (result > 3):
                _battle.Announce("Defender Destroyed!")
                self.kill(target, attacker)
            elif (result < 2):
                if (range == 1):
                    _battle.Announce("Attacker Destroyed!")
                    self.kill(attacker, target)
                else:
                    # Attacker cannot be destroyed if it's a ranged attack
                    _battle.Announce("No Effect.")
            else:
                if (range == 1):
                    _battle.Announce("Stalemate - no casualties.")
                else:
                    _battle.Announce("No casualties.")


        def kill(self, victim, killer):
            _battle.FighterKilled(victim, killer)
            victim.Die()
            
    
    class WargameSkill(Skill):
        def __init__(self):
            self._name = "WargameSkill"
            self._command = [self._name]
            
        def FilterTargets(self, fighter, targets):
            
            # This method will receive target positions in the form:
            # {Position:(<range>, <path taken as Position list>)}
            
            # The targeting option for this Skill will give us all the empty squares we can move to;
            # we need to amend that list to include all the squares with enemy fighters in that we
            # can move to in a single step.
            
            # First, loop through all positions in the current target list, looking for one which is
            # at least one shy of move allowance
            for p1 in targets.keys()[:]:
                
                # If the range to this position isn't too far...:
                if targets[p1][0] < fighter.Stats.Move:
                    # ... loop through all adjacent positions looking for potential attack targets.
                    for p2 in p1.Joins:
                        
                        # Only proceed if the new position isn't already in the big list for
                        # an equal or lesser range
                        if ((p2 in targets.keys()) == False) or (targets[p2][0] > (targets[p1][0] + 1)):
                            
                            # Check the occupants of the space - we're looking for a space where
                            # none of the occupants are invulnerable (so we can attack it) or
                            # on our side.
                            o = _battle.Battlefield.GetOccupants(p2)
                            
                            good = True
                            for f in o:
                                if f.Invulnerable or (f.Faction == fighter.Faction):
                                    good = False
                                    break
                            
                            # If we've found a candidate attack spot, then add it to the list.
                            if good:
                                range = targets[p1][0] + 1
                                path = targets[p1][1][:]
                                path.append(p1)
                                targets[p2] = (range, path)

            return targets
                        
        def GetTargets(self, fighter):
            return TargetData.TargetPositionsNoLos(range=fighter.Stats.Move, ignoreFaction=[fighter.Faction])
            
        # TODO: Either a filter to remove squares with friendly fighters in, or a stacking enforcement to prevent too many friendlies in the same square at once...
            
        def PerformAction(self, fighter, target):
            if (target != None):
                
                path = target[1][1][1:]
                
                for step in path:
                    fighter.Position = step
                    fighter.Transition(battlemove)
                    fighter.Show()
                    _battle.Pause(0.5)
                    
                o = _battle.Battlefield.GetOccupants(target[0])
                
                if (len(o) > 0):
                    if (o[0].Faction != fighter.Faction):
                        fighter._battle.Attack(fighter, fighter.Stats.Attack, ["melee"], o[0], 1)
                        fighter.EndTurn()
                    
                if (len(o) == 0 or o[0].Active == False) and fighter.Active:
                        fighter.Position = target[0]
                        fighter.Transition(battlemove)
                        fighter.Show()
                        _battle.Pause(0.5)
    
        
    class WargameMechanic(TurnBattleMechanic):
        
        def RunFighterTurn(self, fighter):
            fighter.StartTurn()
            self._battle.FighterStartTurn(fighter)
            # Instead of the usual give-the-fighter-a-choice, we force acting with WargameSkill
            # - which handles movement and basic close combat
            # (If the fighter can't move, then WargameSkill is useless)
            skill = WargameSkill()
            if (fighter.Stats.Move > 0):
                targets = _battle.GetTargetPositions(fighter, fighter.Position, range=fighter.Stats.Move, los=False, ignoreFactions=[fighter.Faction], skill=skill)
                target = _battle.UI.PickTargetPosition(fighter, targets)
                if (target != None):
                    _battle.FighterAct(fighter, skill)
                    skill.PerformAction(fighter, target)
                else:
                    return
                    
            #Next check whether the fighter has any skills of their own that they may want to
            # use - which are also available - and present a menu if appropriate.
            
            if fighter.TurnComplete == False:
                skills = fighter.GetSkillList()
                # skills is a list of tuples (skill-handler, available-flag). Skill handler is an instance
                # of Skill; available-flag is a True/False bool value that describes whether that
                # particular skill can be used by that fighter right now.
                while fighter.TurnComplete == False and len([x for x in skills if x[1]]) > 0:
                    skill = fighter.PickSkill(includeCancel = True)
                    if (skill == None):
                        fighter.EndTurn()
                    else:
                        fighter.PerformAction(skill)

            fighter.EndTurn()
            self._battle.FighterEndTurn(fighter)
