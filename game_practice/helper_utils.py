import pygame
from pygame.locals import *

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
    if centerx:
        override_width = bg_surface.get_width()//2 - fg_surface.get_width()//2
    if centery:
        override_height = bg_surface.get_height()//2 - fg_surface.get_height()//2

    bg_surface.blit(fg_surface, (override_width, override_height), area)