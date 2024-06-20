import pygame
import os
from Level import *
from Tower import *
from pathlib import Path

class Shop:
  
  def __init__(self):
    self.rect = pygame.Rect(1000, 0, 300, 800) # Rectangle containing shop
    self.money = 100 # Starting money
    self.towers = pygame.sprite.Group() # List of towers
    self.selectedTower = None # Selected tower (for placement)
    self.levelObj = None # Level object
    self.level = 1 # Current level

  # Getter / Setter methods

  def addMoney(self, amount):
    self.money += amount

  def deductMoney(self, amount):
    self.money -= amount

  def setTowers(self, towers):
    self.towers = towers
  
  def getMoney(self):
    return self.money
  
  def getTowers(self):
    return self.towers
  
  def getLevel(self):
    return self.level
  
  # Render methods

  def draw(self, window):
    if self.levelObj == None: # Start the game 
      self.startLevel()
    elif self.levelObj.isComplete(): # Logic when player complets the level
      if self.levelObj.isLost():
        self.level = 1
        self.towers = pygame.sprite.Group()
      else: 
        self.towers = self.levelObj.getTowers() # Stores the level so they can be rendered in the next level
        self.level += 1
        self.startLevel()
    
    #self.handleShop(self, window)
    self.levelObj.draw(window)
    self.shopGUI(window)
  
  def shopGUI(self, window):
    yPos = 200 # Starting y position for the buttons

    # Draw the shop
    window.blit(pygame.image.load("assets/shop.png"), self.rect.topleft)

    # Draw the money
    font = pygame.font.Font(None, 36)
    text = font.render("Money: " + str(self.money), 1, (255, 255, 255))
    window.blit(text, (10, 10))

    # Draw the buttons for each of the towers
    for imageFile in os.listdir("assets/towers"):
      name = Path(os.path.join("assets/towers", imageFile)).stem
      image = pygame.image.load(os.path.join("assets/towers", imageFile))
      self.drawTowerButton(window, image, name, yPos)
      yPos += 150
    
  # Renders the buttons to buy the towers
  def drawTowerButton(self, window, image, name, yPos):
    window.blit(image, (self.rect.x + 50, yPos))
    font = pygame.font.Font(None, 36)
    name = font.render(name, 1, (255, 255, 255))
    window.blit(name, (self.rect.x + 100, yPos))

  # Main methods

  def startLevel(self):
    self.levelObj = Level(self, self.towers)
  
  def selectTower(self, tower):
    self.selectedTower = tower 
  
  def handleShop(self, window):
    pass

    