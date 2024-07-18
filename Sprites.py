import pygame
import os

# This class will handle spritesheets
class Sprites:
  
  @staticmethod
  def loadSpriteSheets(dir1: str, dir2: str, width: int, height: int, directional=False, scale=2):
    path = os.path.join("assets", dir1, dir2) # Path to the spritesheet
    images = [file for file in os.listdir(path) if file.endswith('.png')] # Loads all images of specific sprite
    allSprites = {} # Dictionary to store all sprites in all spritesheets key: name of sprite, value: list of sprites
    
    for image in images:
      spriteSheet = pygame.image.load(os.path.join(path, image)).convert_alpha() # Load the spritesheet
      sprites = [] # List to store all sprites in a specific spritesheet
      
      for i in range(spriteSheet.get_width() // width):
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32) # Create a surface for the sprite
        rect = pygame.Rect(i * width, 0, width, height) # Create an invidiual rectangle for each sprite in spritesheet
        surface.blit(spriteSheet, (0, 0), rect) # Blit the sprite to the surface
        sprites.append(pygame.transform.scale_by(surface, scale))
        # pygame.transform.scale_by(surface, 3)
        
      if directional:
        allSprites[image.replace(".png", "") + "Right"] = sprites # Add the sprites to the dictionary
        allSprites[image.replace(".png", "") + "Left"] = [Sprites.flip(sprite) for sprite in sprites]
      else:
        allSprites[image.replace(".png", "")] = sprites
        
    return allSprites
  
  @staticmethod
  def flip(sprite):
    return pygame.transform.flip(sprite, True, False)
    