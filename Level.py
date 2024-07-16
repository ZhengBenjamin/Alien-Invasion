# Level object that manages all entities
import pygame
import os
from Alien import *
from Tower import *
from Projectile import *

class Level:
  
  def __init__(self, shop):
  
    self.shop = shop # Shop object
    self.level = shop.getLevel() # Level of the game
    self.map = shop.getMap() # Map of the game
    self.health = 100 # Health of the player

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
    self.mapBoxes = []
    self.maps.append([[864, 0, "down"], [864, 96, "left"], [96, 96, "down"], [96, 223, "right"], [864, 223, "down"], [864, 736, "left"], [544, 736, "up"], [544, 414, "left"], [96, 414, "down"], [96, 735, "right"], [288, 735, "down"], [288, 864, "right"]])
    self.mapBoxes.append([(14,1), (14,2), (13,2), (12,2), (11,2), (10,2), (9,2), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2,3), (2,4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4), (14,5),(14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12),(13, 12), (12, 12), (11, 12), (10, 12), (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (8, 7), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (3, 12), (4, 12), (5, 12), (5, 13), (5, 14), (6,14),(7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14)])
    
    self.occupiedBoxes = [] # List of boxes occupied by towers
    
    # Timing of spawns
    self.totWave = self.level // 5 # Total number of waves
    self.currentWave = 0 # Current wave
    self.waveCooldown = 5000  # Cooldown between waves
    self.lastSpanwed = pygame.time.get_ticks() # Last time an alien was spawned
    
    self.lastSpawnEasy = pygame.time.get_ticks() # Last time an easy alien was spawned
    self.lastSpawnMed = pygame.time.get_ticks() # Last time a medium alien was spawned
    self.lastSpawnHard = pygame.time.get_ticks() # Last time a hard alien was spawned
    self.spawnRateEasy = 600 
    self.spawnRateMed = 1000
    self.spawnRateHard = 1500

  # Getter / Setter methods
  
  def getNumAliens(self):
    return len(self.aliens.sprites())
  
  def getNumProjectiles(self):
    return len(self.projectiles.sprites())
  
  def getNumTowers(self):
    return len(self.towers.sprites())
  
  def getMap(self):
    return self.maps[self.map]
  
  def getMapBoxes(self):
    return self.mapBoxes[self.map]
  
  def getOccupiedBoxes(self):
    return self.occupiedBoxes
  
  def getTowers(self):
    return self.towers
  
  def getAliens(self):
    return self.aliens
  
  def getHealth(self):
    return self.health
  
  def getLevel(self):
    return self.level

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
    
  def addOccupiedBox(self, box):
    self.occupiedBoxes.append(box)

  def addProjectile(self, projectile):
    self.projectiles.add(projectile)

  def updateTowers(self, towers):
    self.towers = towers
    for tower in towers:
      tower.setLevelObj(self)

  def deductHealth(self, amount):
    self.health -= amount
    if self.health <= 0:
      self.lost = True
      print("Game Over")

  def checkDone(self):
    if self.currentWave > self.totWave and len(self.aliens.sprites()) == 0:
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

    self.spawnHandler()
    self.aliens.update(window)
    self.towers.update(window)
    self.projectiles.update(window)

  # Spawning logic for each level 
  def spawnHandler(self):
    currentTime = pygame.time.get_ticks()
    
    # Spawn limits per wave based on level
    easySpawnLimit = 1 + int(math.log(self.level + 1) * 13)
    medSpawnLimit = 0
    hardSpawnLimit = 0
    
    if self.level >= 5 and self.level < 10:
      medSpawnLimit = 1 + int(math.log(self.level + 1) * 3)
    elif self.level >= 10: 
      medSpawnLimit = 1 + int(math.log(self.level + 1) * 10)
    
    if self.level >= 10 and self.level < 15:
      hardSpawnLimit = 1 + int(math.log(self.level + 1) * 3)
    elif self.level >= 15:
      hardSpawnLimit = 1 + int(math.log(self.level + 1) * 10)
    
    # Possible alien spawns, will be updated as levels progresses
    easyAliens = ["slime"]
    medAliens = ["boba"]
    hardAliens = ["skateboard"]
    
    # Spawning logic for each wave
    # There will be 3 waves, each with different difficultes 
    if self.currentWave <= self.totWave:
      if self.currentWave % 3 == 0: # Easy wave
        if self.spawned[0] < easySpawnLimit:
          self.spawn(easyAliens, "easy")
        if self.spawned[1] < medSpawnLimit // 2: 
          self.spawn(medAliens, "med")
        if self.spawned[0] >= easySpawnLimit and self.spawned[1] >= medSpawnLimit // 2 and currentTime - self.lastSpanwed > self.waveCooldown:
          self.currentWave += 1
          self.spawned = [0, 0, 0, 0]
      
      if self.currentWave % 3 == 1: # Medium wave
        if self.spawned[0] < easySpawnLimit // 2:
          self.spawn(easyAliens, "easy")
        if self.spawned[1] < medSpawnLimit:
          self.spawn(medAliens, "med")
        if self.spawned[2] < hardSpawnLimit // 2:
          self.spawn(hardAliens, "hard")
        if self.spawned[0] >= medSpawnLimit // 2 and self.spawned[1] >= medSpawnLimit and self.spawned[2] >= hardSpawnLimit // 2 and currentTime - self.lastSpanwed > self.waveCooldown:
          self.currentWave += 1
          self.spawned = [0, 0, 0, 0]
          
      if self.currentWave % 3 == 2: # Hard wave
        if self.spawned[0] < easySpawnLimit:
          self.spawn(easyAliens, "easy")
        if self.spawned[1] < medSpawnLimit:
          self.spawn(medAliens, "med")
        if self.spawned[2] < hardSpawnLimit:
          self.spawn(hardAliens, "hard")
        if self.spawned[0] >= easySpawnLimit and self.spawned[1] >= medSpawnLimit and self.spawned[2] >= hardSpawnLimit and currentTime - self.lastSpanwed > self.waveCooldown:
          self.currentWave += 1
          self.spawned = [0, 0, 0, 0]
          
  def spawn(self, possibleSpawn: list, difficulty: str):
    currentTime = pygame.time.get_ticks()
    self.lastSpanwed = pygame.time.get_ticks()
    
    match difficulty:
      case "easy":
        if currentTime - self.lastSpawnEasy > self.spawnRateEasy:
          match possibleSpawn[random.randint(0, len(possibleSpawn) - 1)]: 
            case "slime":
              self.aliens.add(Slime(self.getMap(), self))
          self.lastSpawnEasy = currentTime
          self.spawned[0] += 1
      case "med":
        if currentTime - self.lastSpawnMed > self.spawnRateMed:
          match possibleSpawn[random.randint(0, len(possibleSpawn) - 1)]: 
            case "boba":
              self.aliens.add(BobaAlien(self.getMap(), self))
          self.lastSpawnMed = currentTime
          self.spawned[1] += 1
      case "hard":
        if currentTime - self.lastSpawnHard > self.spawnRateHard:
          match possibleSpawn[random.randint(0, len(possibleSpawn) - 1)]: 
            case "skateboard":
              self.aliens.add(SkateboardAlien(self.getMap(), self))
          self.lastSpawnHard = currentTime
          self.spawned[2] += 1


