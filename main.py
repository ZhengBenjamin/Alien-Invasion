import pygame
import os
from Alien import *
from Tower import *
from Shop import *

pygame.init()
pygame.display.set_caption("Tower Defense") # Title of window

# Global variables
WIDTH, HEIGHT = 1000, 800 # Window Size
FPS = 120 # Frames per second

level = [] # List of all levels
towers = [] # List of all towers TODO: Make sure to append towers to this list
aliens = [] # List of all aliens TODO: Make sure to append aliens to this list

level.append([0, 100, "right"], [400, 100, "down"], [400, 500, "right"], [800, 500, "up"], [800, 0, "end"])

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

# Testing
testObject = Slime(40, 40)
aliens.append(testObject)

main(window)

