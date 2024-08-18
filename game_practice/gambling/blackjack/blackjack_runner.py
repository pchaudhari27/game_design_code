import pygame
from pygame.locals import *
from blackjack_main import main_game
from blackjack_menu import main_menu
from holder import screen, card_sprites, cardback_sprites, values, suits, card_size, cardback_size

# start pygame 
pygame.init()

cardback, num_decks = main_menu(screen, cardback_sprites, cardback_size, 6)

if cardback and num_decks:
    while True:
        val = main_game(screen, card_size, cardback, values, suits, 6, num_decks)
        if val == "back to menu":
            cardback, num_decks = main_menu(screen, cardback_sprites, cardback_size, 6)

        if val == "quit":
            pygame.quit()
            break