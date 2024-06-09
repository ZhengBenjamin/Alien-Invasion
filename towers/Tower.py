# Superclass for all towers
class Tower:
  
  def __init__(self, range, damage, splashDmg, cost):
    self.range = range
    self.damage = damage
    self.splashDmg = splashDmg
    self.cost = cost

  # Getter methods 
  
  def getRange(self):
    return self.range
  
  def getDamage(self):
    return self.damage
  
  def hasSplashDmg(self):
    return self.splashDmg
  
  def getCost(self):  
    return self.cost
  
  # Main methods
  
  def attack(self):
    pass

  