import pygame
import os

for file in os.listdir("towers"):
  from file import *


pygame.init()

pygame.display.set_caption("Tower Defense") # Title of window

# Global variables
WIDTH, HEIGHT = 1000, 800 # Window Size
FPS = 120 # Frames per second

window = pygame.display.set_mode((WIDTH, HEIGHT)) # Window

# This method draws the window; Call draw for all objects here
def draw():


  pygame.display.update() # Update the window


# This main method contains the loop of the game
def main(window):
  clock = pygame.time.Clock()
  
  run = True
  while run:
    clock.tick(FPS)

    for event in pygame.event.get(): # If the user closes the window, quit program
      if event.type == pygame.QUIT:
        run = False
        break
    
    draw()


main(window)