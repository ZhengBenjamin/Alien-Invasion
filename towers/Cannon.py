from .Tower import Tower

class Cannon(Tower):
  
  def __init__(self):
    super().__init__(range=5, damage=5, splashDmg=False, cost=150)
  