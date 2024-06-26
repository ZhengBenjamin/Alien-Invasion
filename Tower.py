import pygame
import os
from Projectile import *
from typing import Type

# Superclass for all towers
class Tower(pygame.sprite.Sprite):
  
  # Constructor
  def __init__(self, xPos: int, yPos: int, cost: int, damage: int, range: int, attackSpeed: int, splashDamage: bool, level, name: str, image: str, active: bool):
    pygame.sprite.Sprite.__init__(self)

    self.rect = pygame.Rect(xPos, yPos, 32, 32)
    self.radius = range # Range of the tower
    self.cost = cost # Cost of the tower
    self.damage = damage # Damage of the tower
    self.image = image # Image of the tower
    self.placed = False # If the tower has been placed
    self.splashDamage = splashDamage # If the tower has splash damage
    self.level = level # Level object
    self.attackSpeed = attackSpeed # Attack speed of the tower
    self.active = active # If the tower is active
    self.name = name # Name of the tower

    self.lastShot = pygame.time.get_ticks() # Last time the tower shot

  # Getter / Setter methods 
  
  def getRange(self):
    return self.radius
  
  def getDamage(self):
    return self.damage
  
  def getRange(self):
    return self.radius
  
  def getAttackSpeed(self):
    return self.attackSpeed
  
  def hasSplashDmg(self):
    return self.splashDamage
  
  def getName(self):
    return self.name
  
  def getCost(self):  
    return self.cost
  
  def getImage(self):
    return self.image
  
  def setPosition(self, x, y):
    self.rect.x = x
    self.rect.y = y
  
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
    currentTime = pygame.time.get_ticks()

    if currentTime - self.lastShot > self.attackSpeed and self.active == True:
      progress = 0
      target = None

      for alien in self.level.getAliens():
        if pygame.sprite.collide_circle(self, alien):
          if alien.getProgress() > progress:
            progress = alien.getProgress()
            target = alien

      if target != None:
        self.shoot(self.rect.x, self.rect.y, target)

      self.lastShot = currentTime

  def shoot(self, x, y, target):
    raise NotImplementedError("Must override in child method")
  

class Cannon(Tower):
  def __init__(self, level, active=True):
    super().__init__(0, 0, 100, 10, 150, 500, False, level, "Cannon", pygame.image.load("assets/towers/cannon.png"), active)
    self.level = level
  
  def shoot(self, x, y, target):
    self.level.addProjectile(CannonProj(x, y, target))
    
class Bomber(Tower):
  def __init__(self, level, active=True):
    super().__init__(0, 0, 100, 10, 150, 1000, False, level, "Bomber", pygame.image.load("assets/towers/bomber.png"), active)
    self.level = level
  
  def shoot(self, x, y, target):
    self.level.addProjectile(BomberProj(x, y, target))

class Catapult(Tower):
  def __init__(self, level, active=True):
    super().__init__(0, 0, 100, 10, 150, 1000, False, level, "Catapult", pygame.image.load("assets/towers/catapult.png"), active)
    self.level = level
  
  def shoot(self, x, y, target):
    self.level.addProjectile(CatapultProj(x, y, target))
