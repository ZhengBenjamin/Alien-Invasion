import pygame
import os
import sys
from PIL import Image
from Events import *
from Button import *

class StartMenu: 
  
  def __init__(self, width: int, height: int, window: pygame.Surface):
    
    self.WIDTH = width
    self.HEIGHT = height
    self.window = window
    self.start = False # Flag to start the game
    
    self.BG_FRAMES = self.load_gif("assets/game_starters/Background.gif")
    self.bg_frame_index = 0
    self.bg_frame_count = len(self.BG_FRAMES)
    
    self.MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
    self.MENU_RECT = self.MENU_TEXT.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4))
    self.MENU_MOUSE_POS = pygame.mouse.get_pos()

    self.PLAY_BUTTON = Button(image=pygame.image.load("assets/game_starters/Play Rect.png"), pos=(self.WIDTH // 2, self.HEIGHT // 2 - 50), 
                        text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
    self.QUIT_BUTTON = Button(image=pygame.image.load("assets/game_starters/Quit Rect.png"), pos=(self.WIDTH // 2, self.HEIGHT // 2 + 50), 
                        text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
  
  # Getter Methods
  
  def getStartStatus(self):
    return self.start
  
  def get_font(self, size):
    # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/game_starters/font.ttf", size)
    
  # Function to load and resize GIF frames
  def load_gif(self, filename):
    gif = Image.open(filename)
    frames = []
    try:
      while True:
        frame = gif.copy()
        frame = frame.resize((self.WIDTH, self.HEIGHT), Image.Resampling.LANCZOS)
        frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
        gif.seek(len(frames))  # Move to the next frame
    except EOFError:
        pass  # End of sequence
    return frames
  
  def main_menu(self, window):
    window.blit(self.BG_FRAMES[self.bg_frame_index], (0, 0))
    self.bg_frame_index = (self.bg_frame_index + 1) % self.bg_frame_count

    self.MENU_MOUSE_POS = pygame.mouse.get_pos()

    window.blit(self.MENU_TEXT, self.MENU_RECT)

    for button in [self.PLAY_BUTTON, self.QUIT_BUTTON]:
      button.changeColor(self.MENU_MOUSE_POS)
      button.update(window)

    if Events.getMousePressed() == True:
      if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):
        self.start = True  # Transition to the main game loop
        return
      if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
        pygame.quit()
        sys.exit()
    
  
