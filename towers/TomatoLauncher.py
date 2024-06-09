from .Tower import Tower

class TomatoLauncher(Tower):
  
  def __init__(self):
    super().__init__(range=5, damage=15, splashDmg=True, cost=200)
  