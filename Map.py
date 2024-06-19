# Map.py

import pygame as pg

class Map:
    def __init__(self, map_image):
        self.map_image = map_image
    
    def draw(self, window):
        window.blit(self.map_image, (0, 0))  # Draw the map image at (0, 0) position
