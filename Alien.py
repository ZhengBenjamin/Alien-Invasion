# Alien superclass, parent class for al lthe alien types in the game 
import pygame
import os

class Alien(pygame.sprite.Sprite):
  
  def __init__ (self, health, speed, reward, path, level, image): 
    pygame.sprite.Sprite.__init__(self)

    self.rect = pygame.Rect(path[0][0], path[0][1], 32, 32) # Rectangular Hitbox 
    self.health = health # Health of the alien
    self.speed = speed # Speed of the alien
    self.reward = reward # Reward for killing the alien
    self.path = path # Path the alien will follow
    self.image = image # Image of the alien
    self.level = level # Level object
    self.velocity = [0, 0] # Starting velocity of the alien
    self.turn = 0 # Turn number on path
    self.currentDirection = path[0][2] # Current direction of the alien
    self.progress = 0 # Progress on the path

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
    window.blit(self.image, self.rect.topleft)

  def update(self, window):
    if self.health > 0:
      if self.rect.x == 1000 or self.rect.x == 0 or self.rect.y == 800 or self.rect.y == 0:
        self.kill()
        self.level.deductHealth(1)
        self.level.checkDone()
      self.progress += self.speed
      self.updatePath()
      self.move(self.velocity[0], self.velocity[1])
      self.draw(window)
    else: 
      self.level.addMoney(self.reward)
      self.kill()
      self.level.checkDone()

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
      if self.currentDirection in ["left", "right"]:
        if self.rect.x == self.path[self.turn][0]:
          self.calcNextPath()
          self.turn += 1
      elif self.currentDirection in ["up", "down"]:
        if self.rect.y == self.path[self.turn][1]:
          self.calcNextPath()
          self.turn += 1

  def calcNextPath(self):
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


# Alien subclasses

class Slime(Alien):
  def __init__(self, path, level):
    super().__init__(15, 2, 10, path, level, pygame.image.load("assets/aliens/slime.png"))

class BobaAlien(Alien):
  def __init__(self, path, level):
    super().__init__(10, 1, 20, path, level, pygame.image.load("assets/aliens/boba.png"))

class BigDaddyBen(Alien):
  def __init__(self, path, level):
    super().__init__(20, 1, 40, path, level, pygame.image.load("assets/aliens/bigDaddyBen.png"))

class SkateboardAlien(Alien):
  def __init__(self, path):
    super().__init__(15, 3, 30, path, pygame.image.load("assets/aliens/skateboard.png"))

