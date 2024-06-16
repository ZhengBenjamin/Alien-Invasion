import pygame
import os
import random
from Alien import *
from Tower import *
from Shop import *
from Projectile import *

pygame.init()
pygame.display.set_caption("Tower Defense") # Title of window

# Global variables
WIDTH, HEIGHT = 1000, 800 # Window Size
FPS = 120 # Frames per second
window = pygame.display.set_mode((WIDTH, HEIGHT)) # Window

# Sprite Groups
towers = pygame.sprite.Group() 
aliens = pygame.sprite.Group()
projectiles = pygame.sprite.Group() 

# Maps
# Level layout: [[start], [verticies]]: [[startingDirection], [x, y, nextDirection]]
maps = [] # List of all maps
maps.append([[200, 200, "right"], [400, 200, "down"], [400, 600, "right"], [800, 600, "up"]])

# Draws the window and updates the sprites
def draw():
  aliens.update(window)
  projectiles.update(window)

  pygame.display.update() # Update the window


# Main game loop
def main(window):
  clock = pygame.time.Clock()

  run = True
  while run:
    clock.tick(FPS)

    window.fill((0, 0, 0))

    for event in pygame.event.get(): # If the user closes the window, quit program
      if event.type == pygame.QUIT:
        run = False
        break
    
    draw()

# Spawning aliens

def startSpawn(level):
  pass

aliens.add(Slime(maps[0]))
projectiles.add(CannonProj(500, 500, aliens.sprites()[0]))
main(window)


