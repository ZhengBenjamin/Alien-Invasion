# Alien superclass, parent class for all the alien types in the game.
class Alien:
  
  def __init__(self, health, speed, reward):
    self.health = health
    self.speed = speed
    self.reward = reward

  # Getter methods
  
  def getHealth(self):
    return self.health
  
  def getSpeed(self):
    return self.speed
  
  def getReward(self):
    return self.reward
  
  # Main methods

