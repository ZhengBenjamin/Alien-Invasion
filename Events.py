# A class that stores all events of the game

import pygame

class Events:
  
  events = []
  mousePressed = False
  
  lastPressed = pygame.time.get_ticks()
  currentTime = 0
  
  @classmethod
  def updateEvents(cls):
    cls.events = pygame.event.get()
    cls.currentTime = pygame.time.get_ticks()

    for event in cls.events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        if cls.currentTime - cls.lastPressed > 1000:
          cls.mousePressed = True
          cls.lastPressed = cls.currentTime
        else:
          cls.mousePressed = False
      
      if event.type == pygame.MOUSEBUTTONUP:
        cls.mousePressed = False
        
  @classmethod
  def getEvents(cls):
    return cls.events
  
  @classmethod
  def getMousePressed(cls):
    return cls.mousePressed