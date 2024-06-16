import pygame
import os 

class Projectile(pygame.sprite.Sprite):
  
  # Constructor (int, int, int, int, Alien, String)
  def __init__(self, x, y, speed, damage, target, img):
    pygame.sprite.Sprite.__init__(self)

    self.x = x # Position of projectile on map
    self.y = y
    self.width = 10 # Size of projectile
    self.height = 10
    self.speed = speed # Speed of projectile
    self.damage = damage # Damage of projectile
    self.target = target # Target of projectile
    self.velocity = [0, 0] # Initial velocity
    self.collide = False # If the projectile has collided with the target
    self.show = True 
    self.img = img 

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
    self.x += dx
    self.y += dy
  
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
    window.blit(pygame.transform.scale(self.img, (self.width, self.height)), (self.x - self.width/2, self.y - self.width/2))

  def update(self, window):

    #if self.collide == False: 
      self.updatePath()
      self.move(self.velocity[0], self.velocity[1])
      self.draw(window)
    #else: 
      #self.show = False

  # TODO: Projectile pathfinding is dookie :D fix later 
  def updatePath(self):
    targetX, targetY = self.target.getPos()
    if targetX > self.x:
      self.moveRight()
    if targetX < self.x:
      self.moveLeft()
    if targetY > self.y:
      self.moveDown()
    if targetY < self.y:
      self.moveUp()
    

# Alien subclasses

class CannonProj(Projectile):
  def __init__(self, x, y, target):
    super().__init__(x, y, 7, 5, target, pygame.image.load("assets/cannonBall.png"))
  