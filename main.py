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
WIDTH, HEIGHT = 1300, 800  # Window Size
FPS = 120  # Frames per second
window = pygame.display.set_mode((WIDTH, HEIGHT))  # Window
currentLevel = 1  # Current level
stateManager = StateManager(WIDTH, HEIGHT, window)  # State Manager object

# Load the map image
map_img = pygame.image.load(os.path.join('assets', 'map.png')).convert_alpha()
map_img = pygame.transform.scale(map_img, (1000, HEIGHT))  # Scale map image to fit the window

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

    events = pygame.event.get()
  
    if events != []:
      Events.updateEvents(events)

    for event in Events.getEvents():  # If the user closes the window, quit program
      if event.type == pygame.QUIT:
        run = False
      elif event.type == pygame.MOUSEBUTTONUP:
        stateManager.handleSelection(event)
        break

    draw()
  
  pygame.quit()
  sys.exit()

main()

