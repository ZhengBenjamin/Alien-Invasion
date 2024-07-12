import pygame
import math
import os 

class Projectile(pygame.sprite.Sprite):
  
  # Constructor (int, int, int, int, Alien, String)
  def __init__(self, x, y, speed, damage, target, image):
    pygame.sprite.Sprite.__init__(self)

    self.rect = pygame.Rect(x, y, 10, 10) # Rectangular hitbox
    self.speed = speed # Speed of projectile
    self.damage = damage # Damage of projectile
    self.target = target # Target of projectile
    self.collide = False # If the projectile has collided with the target
    self.image = image
    
    self.target.reduceHealth(self.damage)

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
  def __init__(self, x, y, target):
    super().__init__(x, y, 5, 10, target, pygame.image.load("assets/projectiles/cannonProj.png"))
  
class BomberProj(Projectile):
  def __init__(self, x, y, target):
    super().__init__(x, y, 8, 5, target, pygame.image.load("assets/projectiles/bomberProj.png"))

class CatapultProj(Projectile):
  def __init__(self, x, y, target):
    super().__init__(x, y, 8, 25, target, pygame.image.load("assets/projectiles/catapultProj.png"))