import pygame
from pygame.locals import *
from blackjack_main import main_game
from blackjack_menu import main_menu
from holder import screen, card_sprites, cardback_sprites, values, suits

# start pygame 
pygame.init()

cardback = main_menu(screen, cardback_sprites, (40, 56), 6)
main_game(screen, (20, 28), cardback, values, suits, 6)