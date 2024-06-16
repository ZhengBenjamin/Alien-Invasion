# Alien superclass, parent class for all the alien types in the game.
import pygame
import os
class Alien:
  
  # Constructor (int, int, int, int, List, String)
  def __init__(self, health, speed, reward, path, img):
    self.rect = pygame.Rect(0, 0, 32, 32) # Rectangular hitbox
    self.health = health # Health of the alien
    self.speed = speed # Speed of the alien
    self.reward = reward # Reward for killing the alien
    self.x = path[1][0]
    self.y = path[1][1] 
    self.width = 32
    self.height = 32 
    self.img = img # Image of the alien
    self.velocity = [0, 0] # Initial velocity
    self.turn = 0 # Current turn in the path
    self.path = path # Path of the alien
    self.currentDirection = path[0][2] # Current direction of the alien

  # Getter methods
  
  def getHealth(self):
    return self.health
  
  def getSpeed(self):
    return self.speed
  
  def getReward(self):
    return self.reward
  
  def getPath(self):
    return self.path
  
  def getPos(self):
    return self.x, self.y

  # Render methods

  def draw(self, window): # Draw the alien
    window.blit(pygame.transform.scale(self.img, (self.width, self.height)), (self.x - self.width/2, self.y-self.height/2))

  def update(self, window):
    self.updatePath()
    self.move(self.velocity[0], self.velocity[1])
    self.draw(window)

  # Movement methods

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
        if self.x == self.path[self.turn][0]:
          self.calcNextPath()
          self.turn += 1
      elif self.currentDirection in ["up", "down"]:
        if self.y == self.path[self.turn][1]:
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
  def __init__(self, path):
    super().__init__(5, 2, 10, path, pygame.image.load("assets/slime.png"))

class BobaAlien(Alien):
  def __init__(self, path):
    super().__init__(10, 1, 20, path, pygame.image.load("assets/boba.png"))

class BigDaddyBen(Alien):
  def __init__(self, path):
    super().__init__(20, 1, 40, path, pygame.image.load("assets/bigDaddyBen.png"))

class SkateboardAlien(Alien):
  def __init__(self, path):
    super().__init__(15, 3, 30, path, pygame.image.load("assets/skateboardAlien.png"))

class Healer(Alien):
  def __init__(self, path):
    super().__init__(10, 1, 20, path, pygame.image.load("assets/healer.png"))