import pygame
from pygame.locals import *
from holder import screen, card_sprites, cardback_sprites, values, suits

# start
pygame.init()

# card class
class Card:
    '''
    This class reads the cards value and suit and maps to an image of the cards
    '''
    def __init__(self, _value_ind: int, _suit_ind: int, _card_size: tuple[int, int], _cardback: pygame.Surface, _value: int = None):
        self.vind = _value_ind
        self.sind = _suit_ind
        self.card_size = _card_size
        self.cardback = _cardback

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

    def __str__(self):
        return f'{values[self.vind]}, {suits[self.sind]}, {self.value}'

    def draw_card(self, scale_size: int = 1):
        '''
        Renders image of the card from sprite sheet.
        '''
        # create card surfaces
        card_img = pygame.Surface(self.card_size)

        # suit in the background, value is the foreground
        card_img.blit(card_sprites, (0,0), pygame.Rect((self.vind*self.card_size[0], self.sind*self.card_size[1]), self.card_size))

        # scale to desired size
        card_img = pygame.transform.scale(card_img, (self.card_size[0]*scale_size, self.card_size[1]*scale_size))

        return card_img
    
    def draw_cardback(self, scale_size: int = 1):
        '''
        Renders image of the cardback from sprite sheet.
        '''
        # create card surfaces
        card_img = pygame.Surface((self.card_size[0]*scale_size, self.card_size[1]*scale_size))

        # draw cardback
        card_img.blit(pygame.transform.scale(self.cardback, (self.card_size[0]*scale_size, self.card_size[1]*scale_size)), (0,0))

        # scale to desired size
        card_img = pygame.transform.scale(card_img, (self.card_size[0]*scale_size, self.card_size[1]*scale_size))

        return card_img

    def devalue(self):
        '''
        Devalue if this card is an ace. Used for potential busts.
        '''
        if self.value == 11:
            self.value = 1

        return Card(self.vind, self.sind, self.card_size, self.cardback, self.value)

# blackjack hand classes
class BlackjackHand:
    '''
    This class stores a list of cards and stores their value for Blackjack.
    '''
    def __init__(self, _card1: Card, _card2: Card) -> None:
        '''
        Starting hand in blackjack has two cards.
        '''
        self.cards = [_card1, _card2]
        self.value = sum([c.value for c in self.cards])
    
    def __str__(self):
        ret = ''
        for c in self.cards:
            ret += c.__str__() + '\n'
        
        return ret

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
        self.cards.sort(key = lambda c: c.value, reverse = True)
        if self.value > 21:
            for c in self.cards:
                c.devalue()
                self.value = sum([c.value for c in self.cards])

                if self.value < 21:
                    return False
        
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

class BlackjackDealerHand(BlackjackHand):
    '''
    This class stores a list of cards and stores their value for Blackjack.
    '''
    def __init__(self, _card1: Card, _card2: Card) -> None:
        '''
        Starting hand in blackjack has two cards. However, dealer has to hide a card.
        '''

        self.hide = True
        BlackjackHand.__init__(self, _card1, _card2)

    # overrde draw_hand from BlackjackHand class
    def draw_hand(self, scale_size: int = 1, bg_color: pygame.Color | str = 'grey'):
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
                img.blit(card.draw_cardback(scale_size), (cardx*(scale_size+1)*i, 0))
            else:
                img.blit(card.draw_card(scale_size), (cardx*(scale_size+1)*i, 0))

        return img