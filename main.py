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

maps = [] # List of all maps
towers = [] # List of all towers TODO: Make sure to append towers to this list
aliens = [] # List of all aliens TODO: Make sure to append aliens to this list
projectiles = [] # List of all projectiles TODO: Make sure to append projectiles to this list

# Level layout: [[start], [verticies]]: [[startingDirection], [x, y, nextDirection]]
maps.append([[100, 200, "right"], [400, 200, "down"], [400, 600, "right"], [800, 600, "up"]])

window = pygame.display.set_mode((WIDTH, HEIGHT)) # Window

# This method draws the window; Call draw for all objects here
def draw():
  for alien in aliens:
    alien.update(window) 

  for projectile in projectiles:
    projectile.update(window)

  pygame.display.update() # Update the window


# This main method contains the loop of the game
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
    
    #startSpawn(1)
    draw()

# Spawning aliens

def startSpawn(level):
  time = 1000
  nextTime = 0
  # Easy aliens

  currTime = pygame.time.get_ticks()
  if currTime > nextTime:
    nextTime += time
    aliens.append(Slime(maps[0]))

  # Med aliens 

  # Hard aliens 

aliens.append(Slime(maps[0]))
projectiles.append(CannonProj(50, 50, aliens[0]))
main(window)


