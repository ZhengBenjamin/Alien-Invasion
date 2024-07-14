import pygame
import os
from Level import *
from Tower import *
from Events import *
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

    self.towerCollection = [Cannon(None, None, False), Bomber(None, None, False), Catapult(None, None, False)]
    self.towerButtons = self.makeTowerButtons(self.towerCollection)
    
    self.headerFont = pygame.font.Font("assets/game_starters/font.ttf", 18)
    self.subFont = pygame.font.Font("assets/game_starters/font.ttf", 12)

  # Helper methods for constructor 

  # Creates the buttons for each of the towers
  def makeTowerButtons(self, towerCollection):
    yPos = 400 # Starting y position for the buttons
    towerButtons = {}
    for tower in towerCollection:
      towerButtons.update({tower: pygame.Rect(self.rect.x + 15, yPos, 275, 100)})
      yPos += 150

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
  
  def getMap(self):
    return self.map
  
  def setEvents(self, events):
    self.events = events

  def updateLevel(self, towers, health):
    self.towers = towers
    self.health = health

  # Render methods

  # Renders the shop and the level
  def draw(self, window):
    self.update()
    self.levelObj.draw(window)
    self.shopGUI(window)
  
  # Updates the shop and the level
  def update(self):
    if self.levelObj == None:
      self.level = 1
      self.startLevel()
    elif self.levelObj.isLost():
      self.level = 1
      self.towers = pygame.sprite.Group() # Clears player towers 
    elif self.levelObj.isComplete():
      print("Level Complete")
      self.level += 1
      self.startLevel()
    self.handleSelection()

  def shopGUI(self, window):
    # Draw the shop
    window.blit(pygame.image.load("assets/shop/shop.png"), self.rect.topleft)

    # Draw the money
    money = self.headerFont.render("Money: " + str(self.money), 1, (255, 255, 255))
    level = self.headerFont.render("Level: " + str(self.level), 1, (255, 255, 255))
    health = self.headerFont.render("Health: " + str(self.levelObj.getHealth()), 1, (255, 255, 255))
    window.blit(money, (1010, 30))
    window.blit(level, (1010, 55))
    window.blit(health, (1010, 80))

    # Draw the buttons for each of the towers
    for tower in list(self.towerButtons.keys()):
      self.drawTowerButton(window, tower)
    
  # Renders the buttons to buy the towers
  def drawTowerButton(self, window, tower):
    # Draw button
    button = self.towerButtons[tower]

    window.blit(pygame.image.load("assets/shop/towerButton.png"), button.topleft)
    tower.setPosition(button.x + 20, button.y + 35)
    tower.draw(window)

    name = self.subFont.render(tower.getName().capitalize(), 1, (255, 255, 255))
    damage = self.subFont.render(str(tower.getDamage()) + " Damage", 1, (255, 255, 255))
    reload = self.subFont.render(str(tower.getAttackSpeed() / 1000) + "s Reload", 1, (255, 255, 255))
    range = self.subFont.render(str(tower.getRange()) + " Range", 1, (255, 255, 255))
    cost = self.subFont.render(str(tower.getCost()), 1, (255, 255, 255))
    
    if tower.hasSplashDmg():
      splash = self.subFont.render("Splash Damage", 1, (255, 255, 255))
      window.blit(splash, (button.x + 80, button.y + 50))
    
    window.blit(name, (button.x + 80, button.y + 15))
    window.blit(damage, (button.x + 100, button.y + 37))
    window.blit(reload, (button.x + 100, button.y + 57))
    window.blit(range, (button.x + 100, button.y + 77))
    window.blit(cost, (button.x + 100, button.y + 10))
    window.blit(pygame.image.load("assets/shop/damage.png"), (button.x + 70, button.y + 35))
    window.blit(pygame.image.load("assets/shop/reload.png"), (button.x + 70, button.y + 55))
    window.blit(pygame.image.load("assets/shop/range.png"), (button.x + 70, button.y + 75))
    
  # Main methods

  def startLevel(self):
    self.levelObj = Level(self)
    self.levelObj.updateTowers(self.towers)
    self.levelObj.setHealth(self.health)
    print("Starting level " + str(self.level))
  
  def selectTower(self, tower):
    self.selectedTower = tower 
  
  def handleSelection(self):
    if Events.getMousePressed() == True:
      pos = pygame.mouse.get_pos()
      for tower in list(self.towerButtons.keys()):
        if self.towerButtons.get(tower).collidepoint(pos):
          if self.money >= tower.getCost():
            self.selectTower(tower)
            self.deductMoney(tower.getCost())
            self.addTower(tower)
          else:
            print("Not enough money")

  # Adds tower object to level
  def addTower(self, tower):
    if tower.getName() == "cannon":
      self.levelObj.addTower(Cannon(self.levelObj, self.levelObj.getMapBoxes()))
    elif tower.getName() == "bomber":
      self.levelObj.addTower(Bomber(self.levelObj, self.levelObj.getMapBoxes()))
    elif tower.getName() == "catapult":
      self.levelObj.addTower(Catapult(self.levelObj, self.levelObj.getMapBoxes()))
  
    

  