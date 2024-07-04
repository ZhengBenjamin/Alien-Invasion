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
    
    mouseDown = False
    
    for event in cls.events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouseDown = True
      
      if event.type == pygame.MOUSEBUTTONUP:
        mouseDown = False
    
    if mouseDown and cls.currentTime - cls.lastPressed > 250:
      cls.mousePressed = True
      cls.lastPressed = cls.currentTime
    else:
      cls.mousePressed = False
        
  @classmethod
  def getEvents(cls):
    return cls.events
  
  @classmethod
  def getMousePressed(cls):
    return cls.mousePressed