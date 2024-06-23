import pygame
import os 

class Projectile(pygame.sprite.Sprite):
  
  # Constructor (int, int, int, int, Alien, String)
  def __init__(self, x, y, speed, damage, target, image):
    pygame.sprite.Sprite.__init__(self)

    self.rect = pygame.Rect(x, y, 10, 10) # Rectangular hitbox
    self.speed = speed # Speed of projectile
    self.damage = damage # Damage of projectile
    self.target = target # Target of projectile
    self.velocity = [0, 0] # Initial velocity
    self.collide = False # If the projectile has collided with the target
    self.image = image

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
    self.rect.x += dx
    self.rect.y += dy
  
  def moveRight(self):
    self.velocity[0] = self.speed

  def moveLeft(self):
    self.velocity[0] = -self.speed

  def moveUp(self):
    self.velocity[1] = -self.speed

  def moveDown(self):
    self.velocity[1] = self.speed

  # Render methods: 

  def draw(self, window):
    window.blit(self.image, self.rect.topleft)

  def update(self, window):
    self.checkCollide()

    if self.collide == False: 
      self.updatePath()
      self.move(self.velocity[0], self.velocity[1])
      self.draw(window)
    else: 
      self.target.hit(self.damage)
      self.kill()

  # TODO: Projectile pathfinding is dookie :D fix later 
  def updatePath(self):
    targetX, targetY = self.target.getPos()
    if targetX > self.rect.x:
      self.moveRight()
    if targetX < self.rect.x:
      self.moveLeft()
    if targetY > self.rect.y:
      self.moveDown()
    if targetY < self.rect.y:
      self.moveUp()
    
  def checkCollide(self):
    self.collide = self.rect.colliderect(self.target.getRect())
    

# Projectile subclasses

class CannonProj(Projectile):
  def __init__(self, x, y, target):
    super().__init__(x, y, 8, 5, target, pygame.image.load("assets/projectiles/cannonProj.png"))
  
class BomberProj(Projectile):
  def __init__(self, x, y, target):
    super().__init__(x, y, 8, 5, target, pygame.image.load("assets/projectiles/bomberProj.png"))

class CatapultProj(Projectile):
  def __init__(self, x, y, target):
    super().__init__(x, y, 8, 5, target, pygame.image.load("assets/projectiles/catapultProj.png"))