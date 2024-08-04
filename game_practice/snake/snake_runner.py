import pygame
from pygame.locals import *

from snake_home import home_page_loop
from snake_main import main_game_loop

pygame.init()

# get screen with width and height
all_desktop_dims = pygame.display.get_desktop_sizes()
W, H = 5*min(all_desktop_dims)[0]//6, 5*min(all_desktop_dims, key = lambda a: (a[1],a[0]))[1]//6
screen = pygame.display.set_mode((W, H))

# main game loop
user_quit = False
while not user_quit:
    snake_sprite, block_dims = home_page_loop(screen)

    if not snake_sprite or not block_dims:
        break
    
    user_quit = main_game_loop(screen, snake_sprite, block_dims)

pygame.quit()