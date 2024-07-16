import pygame

class Toaster:

  def __init__(self, pos: list, text: str, timeout: int, font: pygame.font, color: str):
    self.x_pos = pos[0]
    self.y_pos = pos[1]
    self.timeout = timeout
    self.font = font
    self.color = color
    self.text = self.font.render(text, True, self.color)
    self.rect = pygame.Rect(self.x_pos, self.y_pos, self.text.get_width(), self.text.get_height())
    self.text_rect = self.text.get_rect(topleft=(self.x_pos, self.y_pos))

    self.creationTime = pygame.time.get_ticks()

  def update(self, screen):
    while pygame.time.get_ticks() - self.creationTime < self.timeout:
      screen.blit(self.text, self.text_rect)

  
