import pygame
import os

# Start menu allows player to start the game 
class StartMenu:
  def __init__(self):
    self.startButton = pygame.Rect(200, 600, 300, 100)

  def update(self, window, events): 

    self.draw(window)

    for event in events:
      if event.type == pygame.MOUSEBUTTONUP: 
        if self.startButton.collidepoint(event.pos):
          return "Start"
  
  def draw(self, window):
    window.blit(pygame.image.load("assets/menu/startButton.png"), self.startButton.topleft)
    

class LevelSelect:
  def __init__(self):
    pass

class EndMenu:
  def __init__(self):
    pass