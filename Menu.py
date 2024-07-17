import pygame
import sys
import random
from Alien import *
from Tower import *
from Events import *
from Button import *

class Start:
  
  def __init__(self):
    self.start = False
    self.startMap = pygame.image.load("assets/menu/startMenu.png")

    self.towers = pygame.sprite.Group()
    self.aliens = pygame.sprite.Group()
    self.projectiles = pygame.sprite.Group()

    self.headerFont = pygame.font.Font("assets/game_starters/font.ttf", 52)
    self.subFont = pygame.font.Font("assets/game_starters/font.ttf", 40)

    self.PLAY_BUTTON = Button(pos=(120, 445), text_input="PLAY", font=self.subFont, base_color="#d7fcd4", hovering_color="White")
    self.QUIT_BUTTON = Button(pos=(120, 520), text_input="QUIT", font=self.subFont, base_color="#d7fcd4", hovering_color="White")

    self.availableAliens = ["slime", "boba", "skateboard"]
    self.lastAlienSpanwed = pygame.time.get_ticks()
    self.alienSpawnRate = 1000

    self.spawnTowers()

    self.paths = [[[900, 0, "down"]], [[965, 0, "down"]]]

  def getStartStatus(self):
    return self.start
  
  def addProjectile(self, projectile):
    self.projectiles.add(projectile)
  
  def update(self, window):
    self.draw(window)
    self.handleAliens()
    self.updateTowers()
    self.aliens.update(window)
    self.towers.update(window)
    self.projectiles.update(window)

  def draw(self, window):
    window.blit(self.startMap, (0, 0))
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    
    title = self.headerFont.render("Alien Invasion", True, "#ffffff")

    for button in [self.PLAY_BUTTON, self.QUIT_BUTTON]:
      button.changeColor(MENU_MOUSE_POS)
      button.update(window)

    if Events.getMousePressed() == True:
      if self.PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
        self.start = True  # Transition to the main game loop
        return
      if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
        pygame.quit()
        sys.exit()

    window.blit(title, (65, 350))

  def handleAliens(self):
    currentTime = pygame.time.get_ticks()
    if currentTime - self.lastAlienSpanwed > self.alienSpawnRate:
      self.spawnAlien()
      self.lastAlienSpanwed = currentTime

  def spawnAlien(self):
    randomAlien = random.choice(self.availableAliens)
    randomPath = random.choice(self.paths)

    match randomAlien:
      case "slime":
        self.aliens.add(Slime(randomPath, None))
      case "boba":
        self.aliens.add(BobaAlien(randomPath, None))
      case "skateboard":
        self.aliens.add(SkateboardAlien(randomPath, None))

  def spawnTowers(self):
    towers = [Cannon(None, None, True), Cannon(None, None, True), Catapult(None, None, True), Cannon(None, None, True), Cannon(None, None, True)]
    yVal = 50
    for tower in towers:
      tower.setPosition(1050, yVal)
      tower.setPlaced()
      tower.setMenu(self)
      yVal += 200
      self.towers.add(tower)

  def updateTowers(self):
    for tower in self.towers:
      tower.updateAliens(self.aliens)
      
class Lost:
  
  def __init__(self):
    self.restart = False
    self.gameOverMap = pygame.image.load("assets/menu/gameOverMenu.png")
    
    self.aliens = pygame.sprite.Group()
    
    self.headerFont = pygame.font.Font("assets/game_starters/font.ttf", 52)
    self.subFont = pygame.font.Font("assets/game_starters/font.ttf", 40)
    
    self.MENU_BUTTON = Button(pos=(120, 445), text_input="MAIN MENU", font=self.subFont, base_color="#d7fcd4", hovering_color="White")
    self.QUIT_BUTTON = Button(pos=(120, 520), text_input="QUIT", font=self.subFont, base_color="#d7fcd4", hovering_color="White")

    self.availableAliens = ["slime", "boba", "skateboard"]
    self.lastAlienSpanwed = pygame.time.get_ticks()
    self.alienSpawnRate = 100
    
  def getRestartStatus(self):
    return self.restart
    
  def update(self, window):
    self.draw(window)
    self.handleAliens()
    
  def draw(self, window):
    window.blit(self.gameOverMap, (0, 0))
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    
    self.aliens.update(window)
    
    title = self.headerFont.render("Game Over", True, "#ffffff")
    
    for button in [self.MENU_BUTTON, self.QUIT_BUTTON]:
      button.changeColor(MENU_MOUSE_POS)
      button.update(window)
      
    if Events.getMousePressed() == True:
      if self.MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
        self.restart = True  # Transition to the main game loop
        return
      if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
        pygame.quit()
        sys.exit()
      
    window.blit(title, (65, 350))

  def handleAliens(self):
    currentTime = pygame.time.get_ticks()
    if currentTime - self.lastAlienSpanwed > self.alienSpawnRate:
      self.spawnAlien()
      self.lastAlienSpanwed = currentTime

  def spawnAlien(self):
    randomAlien = random.choice(self.availableAliens)
    randomPath = [[0, random.randint(0, 960), "right"]]

    match randomAlien:
      case "slime":
        self.aliens.add(Slime(randomPath, None))
      case "boba":
        self.aliens.add(BobaAlien(randomPath, None))
      case "skateboard":
        self.aliens.add(SkateboardAlien(randomPath, None))
        
    for alien in self.aliens:
      alien.setMenu()
