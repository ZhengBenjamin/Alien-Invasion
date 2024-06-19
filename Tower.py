import pygame
import os
from Projectile import *

# Superclass for all towers
class Tower(pygame.sprite.Sprite):
  
  # Constructor (int, int, int, int, boolean, int, String, Level, String)
  # Level = Level object, type = Type of tower in String
  def __init__(self, xPos, yPos, range, cost, attackSpeed, level, image):
    pygame.sprite.Sprite.__init__(self)

    self.rect = pygame.Rect(xPos, yPos, 32, 32)
    self.radius = range # Range of the tower
    self.cost = cost # Cost of the tower
    self.image = image # Image of the tower
    self.placed = False # If the tower has been placed
    self.level = level # Level object
    self.attackSpeed = attackSpeed # Attack speed of the tower

    # Temp for testing. Used for timing of attacks 
    self.timer = 0
    self.lastShot = pygame.time.get_ticks()

  # Getter / Setter methods 
  
  def getRange(self):
    return self.radius
  
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
    currentTime = pygame.time.get_ticks()

    if currentTime - self.lastShot > self.attackSpeed:
      progress = 0
      target = None

      for alien in self.level.getAliens():
        if pygame.sprite.collide_circle(self, alien):
          if alien.getProgress() > progress:
            progress = alien.getProgress()
            target = alien
      
      print(target)

      if target != None:
        self.shoot(self.rect.x, self.rect.y, target)

      self.lastShot = currentTime

  def shoot(self, x, y, target):
    raise NotImplementedError("Must override in child method")
  

class Cannon(Tower):
  def __init__(self, level):
    super().__init__(5, 5, 300, 50, 250, level, pygame.image.load("assets/cannon.png"))
    self.level = level
  
  def shoot(self, x, y, target):
    self.level.addProjectile(CannonProj(x, y, target))
    
