# A class that stores all events of the game

class Events:
  
  events = []
  
  @classmethod
  def getEvents(cls):
    return cls.events
  
  @classmethod
  def updateEvents(cls, events):
    cls.events = events