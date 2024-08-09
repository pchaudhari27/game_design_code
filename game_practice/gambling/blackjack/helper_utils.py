import pygame
from pygame.locals import *
import random
from itertools import product
from holder import screen, card_sprites, cardback_sprites, values, suits

# start pygame
pygame.init()

def center_blit(
        bg_surface: pygame.Surface, 
        fg_surface: pygame.Surface, 
        area: pygame.Rect=None, 
        centerx: bool = True, 
        centery: bool = True,
        override_width: int = -1,
        override_height: int = -1
    ):
    '''
    Simple function for centering and blitting a foreground surface onto a background surface.
    You can center just one of the dimensions and override the other if you need.
    '''

    area = pygame.Rect(area) if area else pygame.Rect((0,0), (fg_surface.get_width(), fg_surface.get_height()))

    if centerx:
        override_width = bg_surface.get_width()//2 - area.width//2
    if centery:
        override_height = bg_surface.get_height()//2 - area.height//2

    bg_surface.blit(fg_surface, (override_width, override_height), area)

def reshuffle_deck():
    '''
    Helper function to get a shuffled deck.
    '''
    possible_cards = list(product(values, suits))
    random.shuffle(possible_cards)
    return possible_cards