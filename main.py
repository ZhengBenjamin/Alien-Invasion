import pygame
import os
import sys
from StateManager import *
from Events import *
from Menu import *
from Alien import *
from Button import *
from Tower import *
from Shop import *
from Projectile import *
from Level import *

pygame.init()
pygame.display.set_caption("Tower Defense")  # Title of window

# Global variables
WIDTH, HEIGHT = 1260, 960  # Window Size
FPS = 60  # Frames per second
window = pygame.display.set_mode((WIDTH, HEIGHT))  # Window
currentLevel = 1  # Current level
stateManager = StateManager(WIDTH, HEIGHT, window)  # State Manager object

# Load the map image
map_img = pygame.image.load(os.path.join('assets', 'map.png')).convert_alpha()

# Draws the window and updates the sprites
def draw():
  window.fill((255, 255, 255))  # Clear the window with white

  # Draw the map
  window.blit(map_img, (0, 0))

  # State manager updates the game state
  stateManager.update()

  # Update the window
  pygame.display.update()

# Main game loop
def main():
  clock = pygame.time.Clock()

  run = True
  while run:
    clock.tick_busy_loop(FPS)

    Events.updateEvents() # Update the events

    for event in Events.getEvents():  # If the user closes the window, quit program
      if event.type == pygame.QUIT:
        run = False

    draw()
  
  pygame.quit()
  sys.exit()

main()

