# Level object that manages all entities
import pygame
import os
from Alien import *
from Tower import *
from Projectile import *

class Level:
  
  def __init__(self, shop):
  
    self.shop = shop
    self.level = shop.getLevel()
    self.health = 100

    # Sprite Groups / Count
    self.aliens = pygame.sprite.Group()
    self.projectiles = pygame.sprite.Group()
    self.towers = pygame.sprite.Group()
    self.spawned = [0, 0, 0, 0] # Count of aliens spawned [easy, med, hard, boss]

    # Game State
    self.lost = False 
    self.complete = False

    # Maps
    # Map layout: [[start], [verticies]]: [[startingDirection], [x, y, nextDirection]]
    self.maps = []
    self.maps.append([[864, 0, "down"], [864, 96, "left"], [96, 96, "down"], [96, 223, "right"], [864, 223, "down"], [864, 736, "left"], [544, 736, "up"], [544, 414, "left"], [96, 414, "down"], [96, 735, "right"], [288, 735, "down"], [288, 864, "right"]])
    self.maps.append([[100, 200, "right"], [400, 200, "down"], [400, 600, "right"], [800, 600, "up"]])
    
    # Timing of spawns
    self.lastSpawnEasy = pygame.time.get_ticks()
    self.lastSpawnMed = pygame.time.get_ticks()
    self.spawnRateEasy = 300
    self.spawnRateMed = 500

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
  
  def getHealth(self):
    return self.health

  def isComplete(self):
    return self.complete
  
  def isLost(self):
    return self.lost

  def setHealth(self, health):
    self.health = health

  def addMoney(self, amount):
    self.shop.addMoney(amount)

  def addTower(self, tower):
    self.towers.add(tower)

  def addProjectile(self, projectile):
    self.projectiles.add(projectile)

  def updateTowers(self, towers):
    self.towers = towers
    for tower in towers:
      tower.setLevel(self)

  def deductHealth(self, amount):
    self.health -= amount
    if self.health <= 0:
      self.lost = True
      print("Game Over")

  def checkDone(self):
    if len(self.aliens.sprites()) == 0:
      self.shop.updateLevel(self.towers, self.health)
      self.complete = True
      print("Level Complete")

  # Draws the window and updates the sprites
  def draw(self, window):
    if self.complete == False and self.lost == False:
      self.update(window)

  # Updates the game state
  def update(self, window):

    if self.health <= 0:
      self.lost = True

    self.spawn()
    self.aliens.update(window)
    self.towers.update(window)
    self.projectiles.update(window)

  # Spawning logic for each level 
  def spawn(self):
    currentTime = pygame.time.get_ticks()

    if self.level <= 10 and self.spawned[0] < 5 + self.level * 5: # Spawning logic for first 5 levels
      if currentTime - self.lastSpawnEasy > self.spawnRateEasy:
        self.aliens.add(Slime(self.maps[0], self))
        self.lastSpawnEasy = currentTime
        self.spawned[0] += 1

    if self.level >= 5 and self.level <= 10 and self.spawned[1] < 10: # Spawning logic for levels 6-10
      if currentTime - self.lastSpawnMed > self.spawnRateMed:
        self.aliens.add(BobaAlien(self.maps[0], self))
        self.lastSpawnMed = currentTime
        self.spawned[1] += 1
    


