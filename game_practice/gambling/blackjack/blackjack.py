import pygame
from pygame.locals import *
from itertools import product
import random

# start pygame
pygame.init()
pygame.font.init()

# get screen with width and height
W, H = 1300, 800
screen = pygame.display.set_mode((W, H))

# card sprites
sprites = pygame.image.load('../cards_sprites.png').convert()

# card deck parameters
values = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
suits = ['S', 'C', 'H', 'D']

# card class
class Card:
    '''
    This class reads the cards value and suit and maps to an image of the cards
    '''
    def __init__(self, _value_ind: int, _suit_ind: int, _card_size: tuple[int, int], _value: int = None):
        self.vind = _value_ind
        self.sind = _suit_ind
        self.card_size = _card_size

        if _value:
            self.value = _value
        else:
            self.value = -1
            match self.vind:
                # not a face card
                case self.vind if self.vind > 3:
                    self.value = int(values[self.vind])
                # face card
                case self.vind if self.vind > 0:
                    self.value = 10
                # ace
                case _:
                    self.value = 11

    def draw_card(self, scale_size: int = 1):
        '''
        Renders image of the card from sprite sheet.
        '''
        # create card surfaces
        card_img = pygame.Surface(self.card_size)

        # suit in the background, value is the foreground
        card_img.blit(sprites, (0,0), pygame.Rect((self.vind*self.card_size[0], self.sind*self.card_size[1]), self.card_size))

        # scale to desired size
        card_img = pygame.transform.scale(card_img, (self.card_size[0]*scale_size, self.card_size[1]*scale_size))

        return card_img
    
    def draw_cardback(self, scale_size: int = 1, cardback_choice: tuple[int,int] = (0,0)):
        '''
        Renders image of the cardback from sprite sheet.
        '''
        # create card surfaces
        card_img = pygame.Surface(self.card_size)

        # suit in the background, value is the foreground
        cardback = pygame.Surface((20,28))
        cardback.fill('green')
        card_img.blit(cardback, (0,0), pygame.Rect(cardback_choice, card_size))

        # scale to desired size
        card_img = pygame.transform.scale(card_img, (self.card_size[0]*scale_size, self.card_size[1]*scale_size))

        return card_img

    def devalue(self):
        '''
        Devalue if this card is an ace. Used for potential busts.
        '''
        if self.value == 11:
            self.value = 1

        return Card(self.vind, self.sind, self.card_size, self.value)

# blackjack hand classes
class BlackjackDealerHand:
    '''
    This class stores a list of cards and stores their value for Blackjack.
    '''
    def __init__(self, _card1: Card, _card2: Card) -> None:
        '''
        Starting hand in blackjack has two cards.
        '''
        self.cards = [_card1, _card2]
        self.value = sum([c.value for c in self.cards])
        self.hide = True
    
    def hit(self, _card: Card):
        '''
        Add another card to the list.
        '''
        self.cards.append(_card)
        self.value += _card.value
    
    def is_bust(self):
        '''
        Checks if value is over 21, and devalues aces if possible.
        '''
        # if you bust, then devalue all cards
        if self.value > 21:
            self.cards = [c.devalue() for c in self.cards]
            self.value = sum([c.value for c in self.cards])
        
        # if you bust after devaluing, then you lose
        if self.value > 21:
            return True
        
        return False
    
    def is_blackjack(self):
        '''
        Checks if value is 21.
        '''

        return self.value == 21 and len(self.cards) == 2

    def draw_hand(self, scale_size: int = 1, cardback_choice: tuple[int,int] = (0,0), bg_color: pygame.Color | str = 'grey'):
        '''
        Helper function to draw the blackjack hand for the dealer
        '''
        cardx, cardy = self.cards[0].card_size
        img = pygame.Surface((cardx*(scale_size+1)*len(self.cards), cardy*scale_size))
        img.fill(bg_color)

        for i, card in enumerate(self.cards):
            if i == 0:
                img.blit(card.draw_card(scale_size), (0,0))
                continue
            
            if self.hide:
                img.blit(card.draw_cardback(scale_size, cardback_choice), (cardx*(scale_size+1)*i, 0))
            else:
                img.blit(card.draw_card(scale_size), (cardx*(scale_size+1)*i, 0))

        return img

class BlackjackPlayerHand:
    '''
    This class stores a list of cards and stores their value for Blackjack.
    '''
    def __init__(self, _card1: Card, _card2: Card) -> None:
        '''
        Starting hand in blackjack has two cards.
        '''
        self.cards = [_card1, _card2]
        self.value = sum([c.value for c in self.cards])
    
    def hit(self, _card: Card):
        '''
        Add another card to the list.
        '''
        self.cards.append(_card)
        self.value += _card.value
    
    def is_bust(self):
        '''
        Checks if value is over 21, and devalues aces if possible.
        '''
        # if you bust, then devalue all cards
        if self.value > 21:
            self.cards = [c.devalue() for c in self.cards]
            self.value = sum([c.value for c in self.cards])
        
        # if you bust after devaluing, then you lose
        if self.value > 21:
            return True
        
        return False
    
    def is_blackjack(self):
        '''
        Checks if value is 21.
        '''

        return self.value == 21 and len(self.cards) == 2

    def draw_hand(self, scale_size: int = 1, bg_color: pygame.Color | str = 'grey'):
        '''
        Helper function to draw the blackjack hand for the player
        '''
        cardx, cardy = self.cards[0].card_size
        img = pygame.Surface((cardx*(scale_size+1)*len(self.cards), cardy*scale_size))
        img.fill(bg_color)

        for i, card in enumerate(self.cards):
            img.blit(card.draw_card(scale_size), (cardx*(scale_size+1)*i, 0))

        return img

def reshuffle_deck():
    '''
    Helper function to get a shuffled deck.
    '''
    possible_cards = list(product(values, suits))
    random.shuffle(possible_cards)
    return possible_cards

# display parameters for cards
card_size = (20, 28)
scale_size = 3

# display text for Dealer and Player
basic_font = pygame.font.Font(size=30)
dtext = basic_font.render('Dealer', True, 'red')
ptext = basic_font.render('Player', True, 'blue')

# get clock for frame setting
clock = pygame.time.Clock()

# test deck and displaying of dealer and player cards
deck = reshuffle_deck()

cs = []
for i in range(4):
    c = deck.pop()
    cs.append(Card(values.index(c[0]), suits.index(c[1]), card_size))

dealer = BlackjackDealerHand(cs[0], cs[1])
player = BlackjackPlayerHand(cs[2], cs[3])

frame_cntr = 0

# main game loop
running = True
bg = 'grey'
while running:
    # if player clicks X then exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ###############################
    # Game logic updates
    ###############################
    # ...
    frame_cntr += 1
    if frame_cntr == 100:
        c = deck.pop()
        player.hit(Card(values.index(c[0]), suits.index(c[1]), card_size))
    
    if frame_cntr == 300:
        c = deck.pop()
        player.hit(Card(values.index(c[0]), suits.index(c[1]), card_size))

    if frame_cntr == 500:
        dealer.hide = False

    ###############################
    # Screen updates
    ###############################
    # clear screen
    screen.fill(bg)

    # graphics changes
    # ....
    screen.blit(dtext, (100, 50))
    screen.blit(ptext, (100, 600))
    screen.blit(dealer.draw_hand(scale_size, (0,0), bg), (100, 100))
    screen.blit(player.draw_hand(scale_size, bg), (100, 650))

    # show renderd graphics
    pygame.display.flip()

    # limit fps to 60
    clock.tick(60)

pygame.quit()