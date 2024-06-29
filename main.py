import pygame
import os
import sys
from PIL import Image
from Alien import *
from Button import *
from Tower import *
from Shop import *
from Projectile import *
from Level import *

pygame.init()
pygame.display.set_caption("Tower Defense")  # Title of window

# Global variables
WIDTH, HEIGHT = 1300, 800  # Window Size
FPS = 120  # Frames per second
window = pygame.display.set_mode((WIDTH, HEIGHT))  # Window
currentLevel = 1  # Current level
shop = Shop()  # Shop object

# Function to load and resize GIF frames
def load_gif(filename):
    gif = Image.open(filename)
    frames = []
    try:
        while True:
            frame = gif.copy()
            frame = frame.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
            frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
            gif.seek(len(frames))  # Move to the next frame
    except EOFError:
        pass  # End of sequence
    return frames

BG_FRAMES = load_gif("assets/game_starters/Background.gif")
bg_frame_index = 0
bg_frame_count = len(BG_FRAMES)

def get_font(size):
    # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/game_starters/font.ttf", size)

def play():
    global running
    running = False

def main_menu():
    global bg_frame_index

    while True:
        window.blit(BG_FRAMES[bg_frame_index], (0, 0))
        bg_frame_index = (bg_frame_index + 1) % bg_frame_count

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 4))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/game_starters/Play Rect.png"), pos=(WIDTH // 2, HEIGHT // 2 - 50), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/game_starters/Quit Rect.png"), pos=(WIDTH // 2, HEIGHT // 2 + 50), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return  # Transition to the main game loop
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        pygame.time.delay(100)  # Adjust the delay to control GIF animation speed

# Load the map image
map_img = pygame.image.load(os.path.join('assets', 'map.png')).convert_alpha()
map_img = pygame.transform.scale(map_img, (1000, HEIGHT))  # Scale map image to fit the window

# Draws the window and updates the sprites
def draw():
    window.fill((255, 255, 255))  # Clear the window with white

    # Draw the map
    window.blit(map_img, (0, 0))

    # Draw other game elements (aliens, towers, etc.)
    shop.draw(window)

    # Update the window
    pygame.display.update()

# Main game loop
def main():
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():  # If the user closes the window, quit program
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                shop.handleSelection(event)
                break

        draw()
    
    pygame.quit()
    sys.exit()

while True:
    main_menu()
    main()
