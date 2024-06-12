# Alien superclass, parent class for all the alien types in the game.
import pygame
import os
class Alien:
  
  def __init__(self, health, speed, reward, path, img):
    self.rect = pygame.Rect(0, 0, 64, 64) # Rectangular hitbox
    self.health = health # Health of the alien
    self.speed = speed # Speed of the alien
    self.reward = reward # Reward for killing the alien
    self.x = path[0]
    self.y = path[1] 
    self.width = 32
    self.height = 32 
    self.img = img # Image of the alien
    self.velocity = [0, 0] # Initial velocity
    self.turn = 0 # Current turn in the path

  # Getter methods
  
  def getHealth(self):
    return self.health
  
  def getSpeed(self):
    return self.speed
  
  def getReward(self):
    return self.reward
  
  # Render methods

  def draw(self, window): # Draw the alien
    window.blit(pygame.transform.scale(self.img, (self.width, self.height)), (self.x, self.y))

  def update(self, window):
    self.move(self.velocity[0], self.velocity[1])
    self.draw(window)

  # Movement methods

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

  def path(self, path):
    totTurns = len(path)
    
    while self.turn < totTurns:
      if path[self.turn][2] == "left" or "right":
        if self.x == path[self.turn][0]:
          self.turn += 1
          self.calcNextTurn(path, self.turn)
      elif path[self.turn][2] == "up" or "down":
        if self.y == path[self.turn][1]:
          self.turn += 1
          self.calcNextTurn(path, self.turn)
      else: 
        pass
        
  def calcNextTurn(self, path, turn):
    match path[turn][2]:
      case "right":
        self.moveRight()
      case "left":
        self.moveLeft()
      case "up":
        self.moveUp()
      case "down":
        self.moveDown()

    
  


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