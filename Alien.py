# Alien superclass, parent class for all the alien types in the game.
class Alien:
  
  def __init__(self, health, speed, reward):
    self.health = health
    self.speed = speed
    self.reward = reward
    self.xVel = 0
    self.yVel = 0

  # Getter methods
  
  def getHealth(self):
    return self.health
  
  def getSpeed(self):
    return self.speed
  
  def getReward(self):
    return self.reward
  
  # Movement methods

  def move(self, dx, dy):
    self.rect.x += dx
    self.rect.y += dy

  def moveLeft(self, vel):
    self.xVel = -vel

  def moveRight(self, vel):
    self.yVel = vel

