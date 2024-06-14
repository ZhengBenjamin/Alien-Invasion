import pygame
import os
import random
from Alien import *
from Tower import *
from Shop import *

pygame.init()
pygame.display.set_caption("Tower Defense") # Title of window

# Global variables
WIDTH, HEIGHT = 1000, 800 # Window Size
FPS = 120 # Frames per second

maps = [] # List of all maps
towers = [] # List of all towers TODO: Make sure to append towers to this list
aliens = [] # List of all aliens TODO: Make sure to append aliens to this list

# Level layout: [[start], [verticies]]: [[startingDirection], [x, y, nextDirection]]
maps.append([[200, 200, "right"], [400, 200, "down"], [400, 600, "right"], [800, 600, "up"]])

window = pygame.display.set_mode((WIDTH, HEIGHT)) # Window

# This method draws the window; Call draw for all objects here
def draw():
  for alien in aliens:
    alien.update(window) 

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
    
    draw()

# Spawning aliens

def startSpawn(level):
  delay = 1000 # Delay between each alien spawn
  timer = 0 

  # Easy aliens 
  if level < 3: 
    for i in range(4):
      if pygame.time.get_ticks() - timer > delay:
        aliens.append(Slime(maps[0]))
        timer = pygame.time.get_ticks()

  # Med aliens 

  # Hard aliens 

main(window)
startSpawn(1)

