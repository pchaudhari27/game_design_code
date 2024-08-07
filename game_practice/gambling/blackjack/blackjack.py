import pygame
from pygame.locals import *
from itertools import product

# start pygame
pygame.init()

# get screen with width and height
W, H = 1300, 800
screen = pygame.display.set_mode((W, H))

# card sprites
sprites = pygame.image.load('../cards_sprites.png').convert()
# card class
class Card:
    def __init__(self, _value_ind: int, _suit_ind: int, _card_size: tuple[int, int]):
        self.vind = _value_ind
        self.sind = _suit_ind
        self.card_size = _card_size

    def get_card(self, scale_size: tuple[int, int]):
        # create card surfaces
        card_img = pygame.Surface(self.card_size)

        # suit in the background, value is the foreground
        card_img.blit(sprites, (0,0), (self.vind*self.card_size[0], self.sind*self.card_size[1]))

        # scale to desired size
        card_img = pygame.transform.scale(card_img, scale_size)

        return card_img

suits = ['S', 'C', 'H', 'D']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
possible_cards = product(suits, values)

print(possible_cards)

# get clock for frame setting
clock = pygame.time.Clock()

# main game loop
running = True
while running:
    # if player clicks X then exit
    for event in pygame.event.get():
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
    screen.blit(pygame.transform.scale(sprites, (1300,560)), (0,0))

    # show renderd graphics
    pygame.display.flip()

    # limit fps to 60
    clock.tick(60)

pygame.quit()