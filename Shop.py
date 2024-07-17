import pygame
import os
from Level import *
from Tower import *
from Events import *
from Toaster import *
from Button import *
from pathlib import Path

class Shop:
  
  def __init__(self):
    self.rect = pygame.Rect(960, 0, 300, 960) # Rectangle containing shop
    self.money = 200 # Starting money
    self.health = 100 # Starting health
    self.towers = pygame.sprite.Group() # List of towers
    self.selectedTower = None # Selected tower (for placement)
    self.levelObj = None # Level object
    self.level = 0 # Current level
    self.events = None # Events
    self.map = 0 # Current map
    self.occupiedBoxes = [] # List of boxes occupied by towers
    self.levelStarted = False # If the level has started

    self.towerCollection = [Cannon(None, None, False), Bomber(None, None, False), Catapult(None, None, False)]

    self.towerButtons = self.makeTowerButtons(self.towerCollection)
    
    self.titleFont = pygame.font.Font("assets/game_starters/font.ttf", 32)
    self.headerFont = pygame.font.Font("assets/game_starters/font.ttf", 18)
    self.toasterFont = pygame.font.Font("assets/game_starters/font.ttf", 16)
    self.subFont = pygame.font.Font("assets/game_starters/font.ttf", 12)
    
    self.startButton = Button((1035, 225), "Start", self.titleFont, (0, 255, 0), (255, 255, 255))
    
    self.placementToast = Toaster((985, 300), "Place your tower", 10, self.toasterFont, (255, 255, 255))
    self.noMoneyToast = Toaster((985, 300), "Not enough money", 1500, self.toasterFont, (255, 0, 0))
    
    self.toasters = [] 
    self.toasters.append(self.placementToast)
    self.toasters.append(self.noMoneyToast)

  # Helper methods for constructor 

  # Creates the buttons for each of the towers
  def makeTowerButtons(self, towerCollection):
    yPos = 400 # Starting y position for the buttons
    towerButtons = {}
    for tower in towerCollection:
      towerButtons.update({tower: pygame.Rect(self.rect.x + 15, yPos, 275, 150)})
      yPos += 175

    return towerButtons

  # Getter / Setter methods

  def addMoney(self, amount):
    self.money += amount

  def deductMoney(self, amount):
    self.money -= amount
  
  def getMoney(self):
    return self.money
  
  def getTowers(self):
    return self.towers
  
  def getLevel(self):
    return self.level
  
  def getLevelObj(self):
    return self.levelObj
  
  def getMap(self):
    return self.map
  
  def towerPlaced(self):
    self.selectedTower = None
  
  def setEvents(self, events):
    self.events = events

  def updateLevel(self, towers, health, occupiedBoxes):
    self.towers = towers
    self.health = health
    self.occupiedBoxes = occupiedBoxes
    self.levelStarted = False

  # Render methods

  # Renders the shop and the level
  def draw(self, window):
    self.update(window)
    self.levelObj.draw(window)
    self.shopGUI(window)
    self.startButton.draw(window)
    
    for toast in self.toasters:
      toast.draw(window)
  
  # Updates the shop and the level
  def update(self, window):
    if self.levelObj == None:
      self.level = 1
      self.startLevel()
    elif self.levelObj.isLost():
      self.level = 1
      self.towers = pygame.sprite.Group() # Clears player towers 
    elif self.levelObj.isComplete():
      self.level += 1
      self.startLevel()
    
    if not self.levelStarted: 
      self.handleStartButton()
    self.handleSelection()

  def shopGUI(self, window):
    # Draw the shop
    window.blit(pygame.image.load("assets/shop/shop.png"), self.rect.topleft)

    # Draw the money
    money = self.headerFont.render("Money: " + str(self.money), 1, (255, 255, 255))
    level = self.headerFont.render("Level: " + str(self.level), 1, (255, 255, 255))
    health = self.headerFont.render("Health: " + str(self.levelObj.getHealth()), 1, (255, 255, 255))
    wave = self.headerFont.render("Wave: {}/{}".format(self.levelObj.getCurrentWave() + 1, self.levelObj.getTotWave() + 1), 1, (255, 255, 255))
    shopTitle = self.titleFont.render("Shop", 1, (255, 255, 255))
    start = self.titleFont.render("Start", 1, (255, 255, 255))
    
    window.blit(money, (1010, 30))
    window.blit(level, (1010, 55))
    window.blit(health, (1010, 80))
    window.blit(wave, (1010, 105))
    window.blit(shopTitle, (1050, 350))
    
    window.blit(start, (1035, 225))
    window.blit(pygame.image.load("assets/shop/startButton.png"), (1017, 207))

    # Draw the buttons for each of the towers
    for tower in list(self.towerButtons.keys()):
      self.drawTowerButton(window, tower)
    
  # Renders the buttons to buy the towers
  def drawTowerButton(self, window, tower):
    # Draw button
    button = self.towerButtons[tower]

    window.blit(pygame.image.load("assets/shop/towerButton.png"), button.topleft)
    tower.setPosition(button.x + 20, button.y + 59)
    tower.draw(window)

    name = self.subFont.render(tower.getName().capitalize(), 1, (255, 255, 255))
    damage = self.subFont.render(str(tower.getDamage()) + " Damage", 1, (255, 255, 255))
    reload = self.subFont.render(str(tower.getAttackSpeed() / 1000) + "s Reload", 1, (255, 255, 255))
    range = self.subFont.render(str(tower.getRange()) + " Range", 1, (255, 255, 255))
    cost = self.subFont.render(str(tower.getCost()), 1, (255, 255, 255))
    
    if tower.hasSplashDmg():
      splash = self.subFont.render("Splash Damage", 1, (255, 255, 255))
      window.blit(splash, (button.x + 100, button.y + 117))
      window.blit(pygame.image.load("assets/shop/splash.png"), (button.x + 70, button.y + 115))
    
    window.blit(name, (button.x + 70, button.y + 15))
    window.blit(cost, (button.x + 100, button.y + 37))
    window.blit(damage, (button.x + 100, button.y + 57))
    window.blit(reload, (button.x + 100, button.y + 77))
    window.blit(range, (button.x + 100, button.y + 97))
    window.blit(pygame.image.load("assets/shop/cost.png"), (button.x + 70, button.y + 35))
    window.blit(pygame.image.load("assets/shop/damage.png"), (button.x + 70, button.y + 55))
    window.blit(pygame.image.load("assets/shop/reload.png"), (button.x + 70, button.y + 75))
    window.blit(pygame.image.load("assets/shop/range.png"), (button.x + 70, button.y + 95))
    
  # Main methods

  def startLevel(self):
    self.levelObj = Level(self)
    self.levelObj.updateTowers(self.towers)
    self.levelObj.setHealth(self.health)
    self.levelObj.setOccupiedBoxes(self.occupiedBoxes)
  
  def selectTower(self, tower):
    self.selectedTower = tower 
  
  def handleStartButton(self):
    self.startButton.changeColor(pygame.mouse.get_pos())
    
    if Events.getMousePressed() == True and self.startButton.checkForInput(pygame.mouse.get_pos()):
      self.levelObj.start()
      self.levelStarted = True 
  
  def handleSelection(self):
    if Events.getMousePressed() == True and self.selectedTower == None:
      pos = pygame.mouse.get_pos()
      for tower in list(self.towerButtons.keys()):
        if self.towerButtons.get(tower).collidepoint(pos):
          if self.money >= tower.getCost():
            self.selectTower(tower)
            self.deductMoney(tower.getCost())
            self.addTower(self.selectedTower)
          else:
            self.noMoneyToast.update()
    if self.selectedTower != None:
      self.placementToast.update()

  # Adds tower object to level
  def addTower(self, tower):
    if tower.getName() == "cannon":
      self.levelObj.addTower(Cannon(self.levelObj, self.levelObj.getMapBoxes()))
    elif tower.getName() == "bomber":
      self.levelObj.addTower(Bomber(self.levelObj, self.levelObj.getMapBoxes()))
    elif tower.getName() == "catapult":
      self.levelObj.addTower(Catapult(self.levelObj, self.levelObj.getMapBoxes()))
  
    

  