from .Tower import Tower

class BombTower(Tower):
  
  def __init__(self):
    super().__init__(range=3, damage=5, splashDmg=True, cost=100)

