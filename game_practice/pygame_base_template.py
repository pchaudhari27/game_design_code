import pygame
from pygame.locals import *

# start pygame
pygame.init()

# get screen with width and height
W, H = 1000, 800
screen = pygame.display.set_mode((W, H))

# get clock for frame setting
clock = pygame.time.Clock()

# main game loop
running = True
while running:
    for event in pygame.event.get():
        # if player clicks X then exit
        if event.type == pygame.QUIT:
            running = False
    
    ###############################
    # Game logic updates
    ###############################
    # ...

    ###############################
    # Screen updates
    ###############################
    # clear screen
    screen.fill('black')

    # graphics changes
    # ....

    # show renderd graphics
    pygame.display.flip()

    # limit fps to 60
    clock.tick(60)

pygame.quit()