import pygame
import os
from Shop import *
from Level import *
from Menu import *

class StateManger:

  def __init__(self):
    self.states = ["Menu", "LevelSelect", "Game", "Lost"] # States of the game. Refernece only
    self.currentState = 0 # Starting state of the game (Index of states)
    self.shop = Shop()
    self.level = Level(self.shop)
    
    self.startMenu = StartMenu()
    self.levelSelect = LevelSelect() 
    self.endMenu = EndMenu()
    self.stateObj = [self.startMenu, ]
    
  # Getter / Setter methods

  def getState(self):
    return self.currentState
  
  def changeState(self, state):
    self.currentState = state 

  # State Logic

  def manageStaets(self):
    if self.state == 0:
      pass
      

  

  
  