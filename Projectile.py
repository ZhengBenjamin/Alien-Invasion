import pygame
import math
import os 

class Projectile(pygame.sprite.Sprite):
  
  # Constructor (int, int, int, int, Alien, String)
  def __init__(self, x, y, levelObj, speed, damage, target, image, splashRange = 0):
    pygame.sprite.Sprite.__init__(self)

    self.rect = pygame.Rect(x, y, 10, 10) # Rectangular hitbox
    self.levelObj = levelObj # Level object (Optional for non splash damage projectiles)
    self.speed = speed # Speed of projectile
    self.damage = damage # Damage of projectile
    self.target = target # Target of projectile
    self.collide = False # If the projectile has collided with the target
    self.range = splashRange # Range of splash damage
    self.image = image
    self.splashTargets = [] # List of aliens hit by splash damage
    
    if self.range == 0:
      self.target.reduceHealth(self.damage)
    else:
      for alien in self.levelObj.getAliens():
        if math.sqrt((alien.getPos()[0] - self.target.getPos()[0]) ** 2 + (alien.getPos()[1] - self.target.getPos()[1]) ** 2) <= self.range:
          alien.reduceHealth(self.damage)
          self.splashTargets.append(alien)

  # Getter methods:

  def getPos(self):
    return self.x, self.y
  
  def getSpeed(self):
    return self.speed
  
  def getDamage(self):
    return self.damage
  
  def getTarget(self):
    return self.target

  # Movement methods:

  def move(self, dx, dy):
    self.rect.x = self.rect.x + dx
    self.rect.y = self.rect.y + dy

  # Render methods: 

  def draw(self, window):
    window.blit(self.image, self.rect.topleft)

  def update(self, window):
    self.checkCollide()
    
    if self.collide == False: 
      dx, dy = self.updatePath()
      self.move(dx, dy)
      self.draw(window)
    else: 
      self.kill()
      if self.range != 0: # If range != 0, check for splash damage
        for alien in self.splashTargets:
          alien.collideProj()
      else: 
        self.target.collideProj()

  # TODO: Projectile pathfinding is dookie :D fix later 
  def updatePath(self):
    targetX, targetY = self.target.getPos()
    angle = math.atan2(targetY - self.rect.y, targetX - self.rect.x)
    dx = math.cos(angle) * self.speed
    dy = math.sin(angle) * self.speed
    return dx, dy
    
  def checkCollide(self):
    self.collide = self.rect.colliderect(self.target.getRect())
    

# Projectile subclasses

class CannonProj(Projectile):
  def __init__(self, x, y, target, levelObj=None):
    super().__init__(x, y, levelObj, 6, 10, target, pygame.image.load("assets/projectiles/cannonProj.png"))
  
class BomberProj(Projectile):
  def __init__(self, x, y, target, levelObj):
    super().__init__(x, y, levelObj, 8, 15, target, pygame.transform.scale2x(pygame.image.load("assets/projectiles/bomberProj.png")), 20)

class CatapultProj(Projectile):
  def __init__(self, x, y, target, levelObj=None):
    super().__init__(x, y, levelObj, 8, 25, target, pygame.image.load("assets/projectiles/catapultProj.png"))