import pygame
import os
from Level import *
from Tower import *
from pathlib import Path

class Shop:
  
  def __init__(self):
    self.rect = pygame.Rect(1000, 0, 300, 800) # Rectangle containing shop
    self.money = 200 # Starting money
    self.health = 100 # Starting health
    self.towers = pygame.sprite.Group() # List of towers
    self.selectedTower = None # Selected tower (for placement)
    self.levelObj = None # Level object
    self.level = 0 # Current level
    self.events = None # Events

    self.towerCollection = [Cannon(None, False), Bomber(None, False), Catapult(None, False)]
    self.towerButtons = self.makeTowerButtons(self.towerCollection)

  # Helper methods for constructor 

  # Creates the buttons for each of the towers
  def makeTowerButtons(self, towerCollection):
    yPos = 200 # Starting y position for the buttons
    towerButtons = {}
    for tower in towerCollection:
      towerButtons.update({tower: pygame.Rect(self.rect.x + 10, yPos, 275, 100)})
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
      print("Game Started")
    elif self.levelObj.isLost():
      self.level = 1
      self.towers = pygame.sprite.Group() # Clears player towers 
    elif self.levelObj.isComplete():
      self.level += 1
      print("Update Method Tower: " + str(self.towers))
      self.startLevel()

  def shopGUI(self, window):
    yPos = 200 # Starting y position for the buttons

    # Draw the shop
    window.blit(pygame.image.load("assets/shop/shop.png"), self.rect.topleft)

    # Draw the money
    font = pygame.font.Font(None, 36)
    money = font.render("Money: " + str(self.money), 1, (255, 255, 255))
    level = font.render("Level: " + str(self.level), 1, (255, 255, 255))
    health = font.render("Health: " + str(self.levelObj.getHealth()), 1, (255, 255, 255))
    window.blit(money, (10, 10))
    window.blit(level, (10, 30))
    window.blit(health, (10, 50))

    # Draw the buttons for each of the towers
    for tower in list(self.towerButtons.keys()):
      self.drawTowerButton(window, tower, yPos)
      yPos += 150  # Adjust yPos for the next button
    
  # Renders the buttons to buy the towers
  def drawTowerButton(self, window, tower, yPos):
    # Draw button
    button = self.towerButtons[tower]

    # Load tower button image and frame it
    button_image = pygame.image.load("assets/shop/towerButton.png")
    button_rect = button_image.get_rect()
    button_rect.topleft = button.topleft
    window.blit(button_image, button_rect)

    # Adjust tower position within the button
    tower.setPosition(button.x + 10, button.y + 24)
    tower.draw(window)

    # Render tower details text centered left within the button frame
    font = pygame.font.Font(None, 18)
    name = tower.getName()
    damage = "Damage: {}".format(tower.getDamage())
    range_ = "Range: {}".format(tower.getRange())
    cooldown = "Cooldown: {:.2f}s".format(tower.getAttackSpeed() / 1000)
    cost = "Cost: {}".format(tower.getCost())

    text_lines = [name, damage, range_, cooldown, cost]
    text_y = button_rect.centery - font.get_linesize() * len(text_lines) // 2

    for line in text_lines:
      text_surface = font.render(line, True, (255, 255, 255))
      text_rect = text_surface.get_rect()
      text_rect.topleft = (button_rect.centerx + 20, text_y)
      window.blit(text_surface, text_rect)
      text_y += font.get_linesize()
    
  # Main methods

  def startLevel(self):
    self.levelObj = Level(self)
    self.levelObj.updateTowers(self.towers)
    self.levelObj.setHealth(self.health)
    print("Starting level " + str(self.level))
  
  def selectTower(self, tower):
    self.selectedTower = tower 
  
  def handleSelection(self, event):
    if event.type == pygame.MOUSEBUTTONUP:
      pos = pygame.mouse.get_pos()
      for tower in list(self.towerButtons.keys()):
        if self.towerButtons.get(tower).collidepoint(pos):
          if self.money >= tower.getCost():
            self.selectTower(tower)
            self.deductMoney(tower.getCost())
            self.addTower(tower)
          else:
            print("Not enough money")

  def addTower(self, tower):
    if tower.getName() == "Cannon":
      self.levelObj.addTower(Cannon(self.levelObj))
    elif tower.getName() == "Bomber":
      self.levelObj.addTower(Bomber(self.levelObj))
    elif tower.getName() == "Catapult":
      self.levelObj.addTower(Catapult(self.levelObj))
    else:
      pass
