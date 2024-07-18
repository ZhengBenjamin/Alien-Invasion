import pygame
from Shop import *
from Level import *
from Menu import *

class StateManager:

  def __init__(self, width: int, height: int, window: pygame.Surface):
    
    self.width = width
    self.height = height
    self.window = window 
    
    self.states = ["StartMenu", "Game", "Lost"] # States of the game. Refernece only
    self.currentState = 0 # Starting state of the game (Index of states)
    
    self.startMenu = Start()
    self.shop = Shop()
    self.lost = Lost()
    
    self.currentLevel = 0 # Current level of the game
    
  # Getter / Setter methods

  def getState(self):
    return self.states[self.currentState]
  
  def changeState(self, state: str):
    try:
      self.currentState = self.states.index(state)
    except ValueError:
      print(f"State {state} not found")

  def update(self):
    self.manageStates()

  # State Logic

  # Router for states
  def manageStates(self):
    match self.states[self.currentState]:
      case "StartMenu":
        self.handleStartMenu()
      case "Game":
        self.handleGame()
      case "Lost":
        self.handleLost()
      case _:
        self.currentState = self.states.index("StartMenu")
      
  def handleStartMenu(self):
    self.startMenu.update(self.window)
    if self.startMenu.getStartStatus():
      self.changeState("Game")
  
  def handleGame(self):
    self.shop.draw(self.window)
    if self.shop.getLevelObj().isLost():
      self.changeState("Lost")
  
  def handleLost(self):
    self.lost.update(self.window)
    if self.lost.getRestartStatus():
      self.changeState("StartMenu")
  
  def handleSelection(self, event):
    self.shop.handleSelection(event)

  
  