import pygame
from pygame.locals import *

# start pygame 
pygame.init()

# get screen with width and height
W, H = 1300, 800
screen = pygame.display.set_mode((W, H))

# card sprites
card_sprites = pygame.image.load('../cards_sprites.png').convert()
cardback_sprites = pygame.image.load('../cardback_sprites.png').convert()
cardback_sprites.set_colorkey(pygame.Color(0,255,0))

# card deck parameters
values = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
suits = ['S', 'C', 'H', 'D']