import pygame
import os
from Projectile import *

# Superclass for all towers
class Tower(pygame.sprite.Sprite):
  
  def __init__(self, xPos, yPos, range, damage, splashDmg, cost, image):
    pygame.sprite.Sprite.__init__(self)

    self.rect = pygame.Rect(xPos, yPos, 32, 32)
    self.range = range
    self.damage = damage
    self.splashDmg = splashDmg
    self.cost = cost
    self.image = image
    self.placed = False

  # Getter / Setter methods 
  
  def getRange(self):
    return self.range
  
  def getDamage(self):
    return self.damage
  
  def hasSplashDmg(self):
    return self.splashDmg
  
  def getCost(self):  
    return self.cost
  
  # Render methods

  def draw(self, window):
    window.blit(self.image, self.rect.topleft)

  def update(self, window):
    
    if self.placed == False:
      self.updatePlacement()
    else: 
      self.defend()
    
    self.draw(window)

  # Main methods

  # Logic for the placement of tower
  def updatePlacement(self):
    pos = pygame.mouse.get_pos()
    self.rect.center = pos

    if pygame.mouse.get_pressed()[0] == 1:
      self.placed = True

  # Logic for targeting and shooting aliens
  def defend(self):
    pass

class Cannon(Tower):
  def __init__(self):
    super().__init__(5, 5, 5, 5, False, 50, pygame.image.load("assets/cannon.png"))

class BombTower(Tower):
  def __init__(self):
    super().__init__(range=3, damage=5, splashDmg=True, cost=100)
  
class TomatoLauncher(Tower):
  def __init__(self):
    super().__init__(range=5, damage=15, splashDmg=True, cost=200)

  