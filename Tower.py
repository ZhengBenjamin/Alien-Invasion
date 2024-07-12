import pygame
import math
import os
from Projectile import *
from Events import *
from Sprites import *


# Superclass for all towers
class Tower(pygame.sprite.Sprite):
  
  # Constructor
  def __init__(self, xPos: int, yPos: int, cost: int, damage: int, range: int, attackSpeed: int, splashDamage: bool, levelObj, mapBoxes: list, name: str, image: str, active: bool):
    pygame.sprite.Sprite.__init__(self)
    
    self.sprites = Sprites.loadSpriteSheets("towers", name, 16, 16, False) # Loads all sprites
    self.sprite = pygame.transform.scale2x(image)

    self.rect = pygame.Rect(xPos, yPos, 32, 32)
    self.radius = range # Range of the tower
    self.cost = cost # Cost of the tower
    self.damage = damage # Damage of the tower
    self.image = pygame.transform.scale2x(image) # Image of the tower
    self.placed = False # If the tower has been placed
    self.splashDamage = splashDamage # If the tower has splash damage
    self.levelObj = levelObj # levelObj object
    self.mapBoxes = mapBoxes # Map boxes the tower can be placed on
    self.attackSpeed = attackSpeed # Attack speed of the tower
    self.active = active # If the tower is active
    self.name = name # Name of the tower
    self.clicked = 0 # If the tower has been clicked
    self.target = None # Alien target 
    self.fired = False # If tower fired. Used for fire animation 
    
    self.animationCount = 0 # Count for animation delay
    self.animationDelay = 3 # Delay between animations 
    
    if levelObj != None:
      self.level = levelObj.getLevel() # Level of the tower

    self.lastShot = pygame.time.get_ticks() # Last time the tower shot

  # Getter / Setter methods 
  
  def getRange(self):
    return self.radius
  
  def getDamage(self):
    return self.damage
  
  def getRange(self):
    return self.radius
  
  def getAttackSpeed(self):
    return self.attackSpeed
  
  def hasSplashDmg(self):
    return self.splashDamage
  
  def getName(self):
    return self.name
  
  def getCost(self):  
    return self.cost
  
  def getImage(self):
    return self.image
  
  def setPosition(self, x, y):
    self.rect.x = x
    self.rect.y = y

  def setLevelObj(self, levelObj):
    self.levelObj = levelObj
  
  # Render methods

  def draw(self, window):
    if self.placed == False and self.active == True:
      pygame.draw.circle(window, (255, 0, 0), self.rect.center, self.radius, 1)
      tempRect = self.image.get_rect(center=pygame.mouse.get_pos())
      window.blit(self.sprites[self.name + "Idle"][0], tempRect.topleft)
    window.blit(self.sprite, self.rect.topleft)

  def update(self, window):
    
    if self.placed == False:
      self.updatePlacement()
    else: 
      self.updateSprite()
      self.defend()
    
    self.draw(window) 
        
  def updateSpriteAngle(self, sprite):
    if self.target != None:
      angle = math.atan2((self.rect.x - self.target.getPos()[0]), (self.rect.y - self.target.getPos()[1]))
      return pygame.transform.rotate(sprite, angle * 180/math.pi)
    else:
      return self.sprite

  def updateSprite(self):
    if self.fired == True:
      if self.animationCount < self.animationDelay * len(self.sprites[self.name + "Fire"]):
        animationIndex = self.animationCount // self.animationDelay % len(self.name + "Fire")
        self.sprite = self.updateSpriteAngle(self.sprites[self.name + "Fire"][animationIndex])
        self.animationCount += 1 
      else:
        self.fired = False
        self.animationCount = 0
        self.sprite = self.updateSpriteAngle(self.sprites[self.name + "Idle"][0])
    else: 
      self.sprite = self.updateSpriteAngle(self.sprites[self.name + "Idle"][0])
  
  # Main methods

  # Logic for the placement of tower
  def updatePlacement(self):
    pos = pygame.mouse.get_pos()
    if self.checkPlacement(pos) == True:
      self.rect.topleft = ((pos[0] // 64) * 64 + 16, (pos[1] // 64) * 64 + 16)

    if Events.getMousePressed() == True:
      self.clicked += 1
      if self.clicked >= 2 and self.checkPlacement(pos) == True:
        self.placed = True
      pass

  def checkPlacement(self, pos):
    box = (pos[0] // 64 + 1, pos[1] // 64 + 1)
    if not (box in self.mapBoxes) and pos[0] < 960:
      return True
    return False

  # Logic for targeting and shooting aliens
  def defend(self):
    currentTime = pygame.time.get_ticks()

    if currentTime - self.lastShot > self.attackSpeed and self.active == True:
      progress = 0
      self.target = None

      for alien in self.levelObj.getAliens():
        if pygame.sprite.collide_circle(self, alien):
          if alien.getProgress() > progress and alien.getHealth() > 0:
            progress = alien.getProgress()
            self.target = alien

      if self.target != None:
        self.fired = True 
        targetX, targetY = self.target.getPos()
        spawnOffset = [0, 0]
        
        spawnOffset[0] = math.cos(math.atan2(targetY - self.rect.y, targetX - self.rect.x)) + 16
        spawnOffset[1] = math.sin(math.atan2(targetY - self.rect.y, targetX - self.rect.x)) + 16
          
        self.shoot(self.rect.x + spawnOffset[0], self.rect.y + spawnOffset[1], self.target)

      self.lastShot = currentTime

  def shoot(self, x, y, target):
    raise NotImplementedError("Must override in child method")
  

class Cannon(Tower):
  def __init__(self, levelObj, mapBoxes=None, active=True):
    super().__init__(0, 0, 100, 10, 150, 1000, False, levelObj, mapBoxes, "cannon", pygame.image.load("assets/towers/cannon/cannonIdle.png"), active)
    self.levelObj = levelObj
  
  def shoot(self, x, y, target):
    self.levelObj.addProjectile(CannonProj(x, y, target))
    
class Bomber(Tower):
  def __init__(self, levelObj, mapBoxes=None, active=True):
    super().__init__(0, 0, 100, 10, 150, 1000, False, levelObj, mapBoxes, "bomber", pygame.image.load("assets/towers/bomber.png"), active)
    self.levelObj = levelObj
  
  def shoot(self, x, y, target):
    self.levelObj.addProjectile(BomberProj(x, y, target))

class Catapult(Tower):
  def __init__(self, levelObj, mapBoxes=None, active=True):
    super().__init__(0, 0, 100, 10, 200, 1000, False, levelObj, mapBoxes, "catapult", pygame.image.load("assets/towers/catapult/catapultIdle.png"), active)
    self.levelObj = levelObj
  
  def shoot(self, x, y, target):
    self.levelObj.addProjectile(CatapultProj(x, y, target))
