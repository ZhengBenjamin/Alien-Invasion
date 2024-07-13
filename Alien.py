# Alien superclass, parent class for al lthe alien types in the game 
import pygame
import random
import os
from Sprites import *

class Alien(pygame.sprite.Sprite):
  
  def __init__ (self, health, speed, reward, path, level, name, scale=2): 
    pygame.sprite.Sprite.__init__(self)
    
    self.sprites = Sprites.loadSpriteSheets("aliens", name, 16, 16, False, scale) # Load the spritesheet
    self.sprites["{}RunLeft".format(name)] = [Sprites.flip(sprite) for sprite in self.sprites["{}RunRight".format(name)]] # Flip the sprites for left movement
    self.sprites["{}RunLeftHit".format(name)] = [Sprites.flip(sprite) for sprite in self.sprites["{}RunRightHit".format(name)]] 
    self.sprite = None # Current sprite

    self.xOffset, self.yOffset = random.randrange(-8, 8), random.randrange(-8, 8) # Random offset
    self.randomOffset = 0 # Random offset for turns 
    self.lastRandom = pygame.time.get_ticks() # Last time the random offset was generated

    self.name = name # Name type of alien
    self.rect = pygame.Rect(path[0][0] + self.xOffset, path[0][1] + self.yOffset, 32, 32) # Rectangular Hitbox 
    self.health = health # Health of the alien
    self.speed = speed # Speed of the alien
    self.reward = reward # Reward for killing the alien
    self.path = path # Path the alien will follow
    self.level = level # Level object
    self.velocity = [0, 0] # Starting velocity of the alien
    self.turn = 0 # Turn number on path
    self.currentDirection = path[0][2] # Current direction of the alien
    self.progress = 0 # Progress on the path
    self.hit = False # If projectile collided with alien
    self.lastDistance = [9999, 9999] # Last distance from the next point on the path (Starting with arbitrarily large number)
    self.animationCount = 0 # Count for animation delay
    self.animationDelay = 3 # Delay between animations
    self.hitAnimationCount = 0 # Hit animation frames remaining

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
  
  # Called by projectile as soon as it spawns
  def reduceHealth(self, damage):
    self.health -= damage
  
  # Called when projectile collides with alien 
  def collideProj(self):
    self.hit = True

  # Render Methods

  def draw(self, window):
    window.blit(self.sprite, (self.rect.x, self.rect.y))

  def update(self, window):
    # Checks if alien goes outside the map
    if self.rect.x > 980 or self.rect.x < -20 or self.rect.y > 980 or self.rect.y < -20:
        self.kill()
        self.level.deductHealth(1)
        self.level.checkDone()
    
    # Updates movement 
    self.progress += self.speed
    self.updatePath()
    self.move(self.velocity[0], self.velocity[1])
    self.updateSprite()
    self.draw(window)
    
    # Checks if alien is dead
    if self.health > 0:
      self.hit = False
    else: 
      if self.hit == True: # Only kills itself when projectile collides
        self.level.addMoney(self.reward)
        self.kill()
        self.level.checkDone()

  def updateSprite(self):
    spriteSheet = self.name + "Run" + self.currentDirection.capitalize()
    animationIndex = self.animationCount // self.animationDelay % len(self.sprites[spriteSheet])
    self.sprite = self.sprites[spriteSheet][animationIndex]
    if self.hit == True:
      self.hitAnimationCount = 10
    if self.hitAnimationCount > 0: 
      self.sprite = self.sprites[self.name + "Run" + self.currentDirection.capitalize() + "Hit"][animationIndex]
      self.hitAnimationCount -= 1
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
      self.randomOffset = random.randrange(-8, 8)
      self.lastRandom = currentTime


# Alien subclasses

class Slime(Alien):
  def __init__(self, path, level):
    super().__init__(15, 1, 2, path, level, "slime")

class BobaAlien(Alien):
  def __init__(self, path, level):
    super().__init__(30, 1, 5, path, level, "boba")

class BigDaddyBen(Alien):
  def __init__(self, path, level):
    super().__init__(20, 1, 40, path, level, "bigDaddyBen")

class SkateboardAlien(Alien):
  def __init__(self, path, level):
    super().__init__(45, 3, 7, path, level, "skateboard", 2.5)

