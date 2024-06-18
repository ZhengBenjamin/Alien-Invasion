# Level object that manages all entities
import pygame
import os
from Alien import *
from Tower import *
from Shop import *
from Projectile import *

class Level:
  
  def __init__(self, level):
  
    self.level = level

    # Sprite Groups
    self.aliens = pygame.sprite.Group()
    self.towers = pygame.sprite.Group()
    self.projectiles = pygame.sprite.Group()

    # Maps
    # Level layout: [[start], [verticies]]: [[startingDirection], [x, y, nextDirection]]
    self.maps = []
    self.maps.append([[200, 200, "right"], [400, 200, "down"], [400, 600, "right"], [800, 600, "up"]])
    
    self.timer = 0
    self.lastSpawn = pygame.time.get_ticks()
    self.spawnRate = 1000


  # Draws the window and updates the sprites
  def draw(self, window):
    self.startSpawn()
    self.aliens.update(window)
    self.projectiles.update(window)

  def startSpawn(self):
    currentTime = pygame.time.get_ticks()

    if currentTime - self.lastSpawn > self.spawnRate:
      self.aliens.add(Slime(self.maps[0]))
      self.lastSpawn = currentTime

