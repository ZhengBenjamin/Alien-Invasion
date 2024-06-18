import pygame
import os
from Projectile import *

# Superclass for all towers
class Tower(pygame.sprite.Sprite):
  
  def __init__(self, xPos, yPos, range, damage, splashDmg, cost):
    pygame.sprite.Sprite.__init__(self)

    self.rect = pygame.Rect(xPos, yPos, 32, 32)
    self.range = range
    self.damage = damage
    self.splashDmg = splashDmg
    self.cost = cost

  # Getter / Setter methods 
  
  def getRange(self):
    return self.range
  
  def getDamage(self):
    return self.damage
  
  def hasSplashDmg(self):
    return self.splashDmg
  
  def getCost(self):  
    return self.cost
  
  # Main methods
  
  def attack(self, alien):
    CannonProj(500, 500, alien)
    

class BombTower(Tower):
  def __init__(self):
    super().__init__(range=3, damage=5, splashDmg=True, cost=100)

class Cannon(Tower):
  def __init__(self):
    super().__init__(range=5, damage=5, splashDmg=False, cost=150)
  
class TomatoLauncher(Tower):
  def __init__(self):
    super().__init__(range=5, damage=15, splashDmg=True, cost=200)

  