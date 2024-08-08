import pygame
from pygame.locals import *

# set card locations from card_sprites
card_size = (20, 28)

# suit locations in sprite
suit_locs = {
    'S': (0*card_size[0], 0*card_size[1]), 
    'C': (1*card_size[0], 0*card_size[1]), 
    'H': (2*card_size[0], 0*card_size[0]), 
    'D': (3*card_size[0], 0*card_size[0])
}

# suit locations in sprite
value_locs = {
    'A':  (0*card_size[0], 1*card_size[1]), 
    'K':  (1*card_size[0], 1*card_size[1]), 
    'Q':  (2*card_size[0], 1*card_size[1]), 
    'J':  (3*card_size[0], 1*card_size[1]),
    '10': (0*card_size[0], 2*card_size[1]), 
    '9':  (1*card_size[0], 2*card_size[1]), 
    '8':  (2*card_size[0], 2*card_size[1]), 
    '7':  (3*card_size[0], 2*card_size[1]),
    '6':  (0*card_size[0], 3*card_size[1]), 
    '5':  (1*card_size[0], 3*card_size[1]), 
    '4':  (2*card_size[0], 3*card_size[1]), 
    '3':  (3*card_size[0], 3*card_size[1]),
    '2':  (0*card_size[0], 4*card_size[1])
}

# get screen with width and height
W, H = 1000, 800
screen = pygame.display.set_mode((W, H))

# get card_sprites.png
sprites = pygame.image.load('./card_part_sprites.png').convert()
suits = list(suit_locs.keys())
values = list(value_locs.keys())

# card class
class CardCreation:
    def __init__(self, _value: str | int, _suit: str, _card_size: tuple[int, int]):
        if str(_value) not in value_locs:
            raise ValueError(f'Value must be in {list(value_locs.keys())}')
        
        if _suit not in suit_locs:
            raise ValueError(f'Suit must be in {list(suit_locs.keys())}')
        
        self.value = str(_value)
        self.suit = _suit
        self.card_size = _card_size

    def get_card(self, scale_size: int = 1):
        # create card surfaces
        suit_img = pygame.Surface(self.card_size)
        value_img = pygame.Surface(self.card_size)

        # set transparency color
        value_img.set_colorkey(pygame.Color(0, 255, 0))

        # suit in the background, value is the foreground
        suit_img.blit(sprites, (0,0), pygame.Rect(suit_locs[self.suit], self.card_size))
        value_img.blit(sprites, (0,0), pygame.Rect(value_locs[self.value], self.card_size))

        # blit value onto suit
        suit_img.blit(value_img, (0,0))

        # scale to desired size
        suit_img = pygame.transform.scale(suit_img, (self.card_size[0]*scale_size, self.card_size[1]*scale_size))

        return suit_img

# get clock for frame setting
clock = pygame.time.Clock()

sind = 0
vind = 0

cards = pygame.Surface((len(value_locs)*card_size[0], len(suit_locs)*card_size[1]))


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
    card = CardCreation(values[vind], suits[sind], card_size)
    cards.blit(card.get_card(card_size), (vind*card_size[0], sind*card_size[1]))

    ###############################
    # Screen updates
    ###############################
    # clear screen
    screen.fill('white')

    # graphics changes
    # ....
    screen.blit(card.get_card((200, 280)), (300, 300))

    # show renderd graphics
    pygame.display.flip()

    if vind == 12 and sind == 3:
        vind = 0
        sind = 0

        screen.blit(cards, (100, 100))
        pygame.display.flip()
        clock.tick(0.5)
        break
    elif vind == 12:
        vind = 0
        sind += 1
    else:
        vind += 1

    # limit fps to 60
    clock.tick(3)

pygame.image.save(cards, './cards_sprites.png')

pygame.quit()