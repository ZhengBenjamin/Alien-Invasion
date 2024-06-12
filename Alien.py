# Alien superclass, parent class for all the alien types in the game.
import pygame
import os
class Alien:
  
  def __init__(self, health, speed, reward, x, y, img):
    self.rect = pygame.Rect(0, 0, 64, 64) # Rectangular hitbox
    self.health = health
    self.speed = speed
    self.reward = reward
    self.x = x
    self.y = y
    self.width = 64
    self.height = 64
    self.img = img
    self.velocity = [0, 0]

  # Getter methods
  
  def getHealth(self):
    return self.health
  
  def getSpeed(self):
    return self.speed
  
  def getReward(self):
    return self.reward
  
  # Movement methods

  def draw(self, window): # Draw the alien
    window.blit(pygame.transform.scale(self.img, (self.width, self.height)), (self.x, self.y))

  def update(self, window):
    self.x += self.velocity[0]
    self.y += self.velocity[1]
    self.draw(window)


# Alien subclasses

class Slime(Alien):
  def __init__(self, xPos, yPos):
    super().__init__(5, 2, 10, xPos, yPos, pygame.image.load("assets/slime.png"))

class BobaAlien(Alien):
  def __init__(self, xPos, yPos):
    super().__init__(10, 1, 20, xPos, yPos, pygame.image.load("assets/boba.png"))

class BigDaddyBen(Alien):
  def __init__(self, xPos, yPos):
    super().__init__(20, 1, 40, xPos, yPos, pygame.image.load("assets/bigDaddyBen.png"))

class SkateboardAlien(Alien):
  def __init__(self, xPos, yPos):
    super().__init__(15, 3, 30, xPos, yPos, pygame.image.load("assets/skateboardAlien.png"))

class Healer(Alien):
  def __init__(self, xPos, yPos):
    super().__init__(10, 1, 20, xPos, yPos, pygame.image.load("assets/healer.png"))