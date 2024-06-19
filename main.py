import pygame as pg
import os
from Alien import *
from Tower import *
from Shop import *
from Map import *

# Initialize Pygame and set up the window
pg.init()
pg.display.set_caption("Tower Defense")  # Title of the window

# Global variables
WIDTH, HEIGHT = 1000, 800  # Window size
FPS = 120  # Frames per second

aliens = []  # List of all aliens TODO: Make sure to append aliens to this list

window = pg.display.set_mode((WIDTH, HEIGHT))  # Create the window

# This method draws the window; call draw for all objects here
def draw():
    for alien in aliens:
        alien.update(window)
    pg.display.update()  # Update the window

# This main method contains the loop of the game
def main(window):
    clock = pg.time.Clock()

    # Load images
    map_img = pg.image.load(os.path.join('assets', 'map.png')).convert_alpha()  # Ensure the correct path

    # Create a Map object
    game_map = Map(map_image=map_img)  # Pass the map image to the Map object

    run = True
    while run:
        clock.tick(FPS)

        window.fill((0, 0, 0))  # Fill the window with black before drawing
        game_map.draw(window)  # Draw the map

        for event in pg.event.get():  # Check for events
            if event.type == pg.QUIT:  # If the user closes the window, quit the program
                run = False
                break

        draw()  # Draw all game elements (aliens, towers, etc.)

    pg.quit()  # Quit Pygame when the game loop ends

# Testing
testObject = Slime(40, 40)
aliens.append(testObject)

main(window)

