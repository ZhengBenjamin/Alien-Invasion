import pygame
import os
import random
from Alien import *
from Tower import *
from Shop import *
from Projectile import *
from Level import *

pygame.init()
pygame.display.set_caption("Tower Defense") # Title of window

# Global variables
WIDTH, HEIGHT = 1000, 800 # Window Size
FPS = 120 # Frames per second
window = pygame.display.set_mode((WIDTH, HEIGHT)) # Window
currentLevel = 1 # Current level
level = Level(currentLevel) # Level object

# Maps
# Map layout: [[start], [verticies]]: [[startingDirection], [x, y, nextDirection]]
maps = [] # List of all maps
maps.append([[200, 200, "right"], [400, 200, "down"], [400, 600, "right"], [800, 600, "up"]])

# Draws the window and updates the sprites
def draw():
  level.draw(window)
  pygame.display.update() # Update the window


# Main game loop
def main(window):
  clock = pygame.time.Clock()

  run = True
  while run:
    clock.tick(FPS)

    window.fill((255, 255, 255))

    for event in pygame.event.get(): # If the user closes the window, quit program
      if event.type == pygame.QUIT:
        run = False
        break

    draw()
    
main(window)


