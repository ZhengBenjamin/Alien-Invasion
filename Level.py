# Level object that manages all entities
import pygame
import os
from Alien import *
from Tower import *
from Projectile import *

class Level:
  
  def __init__(self, shop, towers=pygame.sprite.Group()):
  
    self.shop = shop
    self.level = shop.getLevel()
    self.health = 100

    # Sprite Groups
    self.aliens = pygame.sprite.Group()
    self.projectiles = pygame.sprite.Group()
    self.towers = towers

    # Game State
    self.lost = False 
    self.complete = False

    # Maps
    # Map layout: [[start], [verticies]]: [[startingDirection], [x, y, nextDirection]]
    self.maps = []
    self.maps.append([[200, 200, "right"], [400, 200, "down"], [400, 600, "right"], [800, 600, "up"]])
    
    # Temp for testing. Used for timing of spawns
    self.timer = 0
    self.lastSpawn = pygame.time.get_ticks()
    self.spawnRate = 650

  # Getter / Setter methods
  
  def getNumAliens(self):
    return len(self.aliens.sprites())
  
  def getNumProjectiles(self):
    return len(self.projectiles.sprites())
  
  def getNumTowers(self):
    return len(self.towers.sprites())
  
  def getTowers(self):
    return self.towers
  
  def getAliens(self):
    return self.aliens
  
  def isComplete(self):
    return self.complete
  
  def isLost(self):
    return self.lost

  def addMoney(self, amount):
    self.shop.addMoney(amount)

  def addTower(self, tower):
    self.towers.add(tower)

  def addProjectile(self, projectile):
    self.projectiles.add(projectile)

  # Draws the window and updates the sprites
  def draw(self, window):
    self.startSpawn()
    self.aliens.update(window)
    self.towers.update(window)
    self.projectiles.update(window)

  # Spawning logic for each level 
  def startSpawn(self):
    currentTime = pygame.time.get_ticks()
    spawned = [0, 0, 0, 0] # Count of aliens spawned [easy, med, hard, boss]

    if self.level < 5: # Spawning logic for first 5 levels 
      while spawned[0] < 3 + self.level * 2:
        if currentTime - self.lastSpawn > self.spawnRate:
          self.aliens.add(Slime(self.maps[0], self))
          self.lastSpawn = currentTime
          spawned[0] += 1

    if self.level > 5 and self.level < 10: # Spawning logic for levels 6-10
      while spawned[1] < 10:
        if currentTime - self.lastSpawn > self.spawnRate:
          self.aliens.add(BobaAlien(self.maps[0], self))
          self.lastSpawn = currentTime
          spawned[1] += 1



