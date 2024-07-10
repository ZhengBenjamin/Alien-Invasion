# Alien superclass, parent class for al lthe alien types in the game 
import pygame
import random
import os
from Sprites import *

class Alien(pygame.sprite.Sprite):
  
  def __init__ (self, health, speed, reward, path, level, name): 
    pygame.sprite.Sprite.__init__(self)
    
    self.sprites = Sprites.loadSpriteSheets("aliens", name, 16, 16, False) # Load the spritesheet
    self.sprites["{}RunLeft".format(name)] = [Sprites.flip(sprite) for sprite in self.sprites["{}RunRight".format(name)]] # Flip the sprites for the left direction
    self.sprite = None # Current sprite

    self.xOffset, self.yOffset = random.randrange(-8, 8), random.randrange(-8, 8) # Random offset
    self.randomOffset = 0 # Random offset for turns 
    self.lastRandom = pygame.time.get_ticks() # Last time the random offset was generated

    self.name = name # Name type of alien
    self.rect = pygame.Rect(path[0][0] + self.xOffset, path[0][1] + self.yOffset, 16, 16) # Rectangular Hitbox 
    self.health = health # Health of the alien
    self.speed = speed # Speed of the alien
    self.reward = reward # Reward for killing the alien
    self.path = path # Path the alien will follow
    self.level = level # Level object
    self.velocity = [0, 0] # Starting velocity of the alien
    self.turn = 0 # Turn number on path
    self.currentDirection = path[0][2] # Current direction of the alien
    self.progress = 0 # Progress on the path
    self.lastDistance = [9999, 9999] # Last distance from the next point on the path (Starting with arbitrarily large number)
    self.animationCount = 0 # Count for animation delay
    self.animationDelay = 3 # Delay between animations

  # Getter / Setter methods

  def getHealth(self):
    return self.health
  
  def getSpeed(self):
    return self.speed
  
  def getReward(self):
    return self.reward
  
  def getPath(self):
    return self.path
  
  def getVelocity(self):
    return self.velocity
  
  def getPos(self):
    return self.rect.center
  
  def getRect(self):
    return self.rect
  
  def getProgress(self):
    return self.progress
  
  def hit(self, damage):
    self.health -= damage

  # Render Methods

  def draw(self, window):
    window.blit(self.sprite, (self.rect.x, self.rect.y))

  def update(self, window):
    if self.health > 0:
      if self.rect.x > 980 or self.rect.x < -20 or self.rect.y > 980 or self.rect.y < -20:
        self.kill()
        self.level.deductHealth(1)
        self.level.checkDone()
      self.progress += self.speed
      self.updatePath()
      self.move(self.velocity[0], self.velocity[1])
      self.updateSprite()
      self.draw(window)
    else: 
      self.level.addMoney(self.reward)
      self.kill()
      self.level.checkDone()
      
  def updateSprite(self):
    spriteSheet = self.name + "Run" + self.currentDirection.capitalize()
    animationIndex = self.animationCount // self.animationDelay % len(self.sprites[spriteSheet])
    self.sprite = self.sprites[spriteSheet][animationIndex]
    self.animationCount += 1

  # Movement Methods

  def move(self, x, y):
    self.rect.x += x
    self.rect.y += y

  def moveRight(self):
    self.velocity[0] = self.speed

  def moveLeft(self):
    self.velocity[0] = -self.speed

  def moveUp(self):
    self.velocity[1] = -self.speed

  def moveDown(self):
    self.velocity[1] = self.speed

  def updatePath(self):
    # Starting Direction
    if self.turn == 0:
      match self.path[0][2]:
        case "right":
          self.moveRight()
        case "left":
          self.moveLeft()
        case "up":
          self.moveUp()
        case "down":
          self.moveDown()
        case _:
          pass
      self.turn += 1

    # Remaining Paths
    if self.turn < len(self.path):
      if self.currentDirection == "left":
        if (self.rect.centerx - self.path[self.turn][0]) < self.randomOffset:
          self.calcNextPath()
          self.turn += 1
      if self.currentDirection == "right":
        if (self.path[self.turn][0] - self.rect.centerx) < self.randomOffset:
          self.calcNextPath()
          self.turn += 1
      if self.currentDirection == "up":
        if (self.rect.centery - self.path[self.turn][1]) < self.randomOffset:
          self.calcNextPath()
          self.turn += 1
      if self.currentDirection == "down":
        self.generateRandom()
        if (self.path[self.turn][1] - self.rect.centery) < self.randomOffset:
          self.calcNextPath()
          self.turn += 1

  # Helper method to calculate the next path
  def calcNextPath(self):
    self.lastDistance = [9999,9999]
    self.velocity = [0,0]
    nextDirection = self.path[self.turn][2]
    match nextDirection:
      case "right":
        self.moveRight()
        self.currentDirection = "right"
      case "left":
        self.moveLeft()
        self.currentDirection = "left"
      case "up":
        self.moveUp()
        self.currentDirection = "up"
      case "down":
        self.moveDown()
        self.currentDirection = "down"
    return
  
  # Helper method generates the random offsets for turns 
  def generateRandom(self):
    currentTime = pygame.time.get_ticks()
    
    if currentTime - self.lastRandom > random.randrange(500, 1500):
      self.randomOffset = random.randrange(-22, 22)
      self.lastRandom = currentTime


# Alien subclasses

class Slime(Alien):
  def __init__(self, path, level):
    super().__init__(15, 1, 10, path, level, "slime")

class BobaAlien(Alien):
  def __init__(self, path, level):
    super().__init__(10, 1, 20, path, level, "boba")

class BigDaddyBen(Alien):
  def __init__(self, path, level):
    super().__init__(20, 1, 40, path, level, "bigDaddyBen")

class SkateboardAlien(Alien):
  def __init__(self, path):
    super().__init__(15, 3, 30, path, "skateboardAlien")

