import pygame
from pygame.locals import *
from classes import Card, BlackjackDealerHand, BlackjackHand
from helper_utils import center_blit, reshuffle_deck

def main_game(
    screen: pygame.Surface,
    card_size: tuple[int, int],
    cardback: pygame.Surface, 
    values: list[str], 
    suits: list[str],
    scale_size: int = 5,
    num_decks: int = 4
):
    # start pygame 
    pygame.init()
    pygame.font.init()

    W, H = screen.get_width(), screen.get_height()

    # display text for Dealer and Player
    basic_font = pygame.font.Font(size=30)
    bust_font = pygame.font.Font(size=50)

    # create buttons for hit and stay
    hit_text = basic_font.render('Hit', True, 'black')
    stay_text = basic_font.render('Stay', True, 'black')

    # stay text is longer so make both boxes the same size
    hit_box = pygame.Surface((2*stay_text.get_width(), 4*stay_text.get_height()))
    stay_box = pygame.Surface((2*stay_text.get_width(), 4*stay_text.get_height()))

    hit_box.fill('white')
    stay_box.fill('white')

    center_blit(hit_box, hit_text)
    center_blit(stay_box, stay_text)

    # get clock for frame setting
    clock = pygame.time.Clock()

    # test deck and displaying of dealer and player cards
    deck = reshuffle_deck(num_decks)
    cs = []
    for i in range(4):
        c = deck.pop()
        cs.append(Card(values.index(c[0]), suits.index(c[1]), card_size, cardback))

    dealer = BlackjackDealerHand(cs[0], cs[1])
    player = BlackjackHand(cs[2], cs[3])

    dcolor = pygame.Color(200, 53, 53)
    pcolor = pygame.Color(238, 208, 31)
    dtext = basic_font.render(f'Dealer: ?', True, dcolor)
    ptext = basic_font.render(f'Player: {player.value}', True, pcolor)

    # main game loop
    running = True
    screen_bg = pygame.Color(53, 101, 77)
    end_bg = pygame.Color(25, 25, 25)

    player_stay = False
    player_hit = False

    freeze = False
    frame_cntr = 0

    while running:
        for event in pygame.event.get():
            # if player clicks X then exit
            if event.type == pygame.QUIT:
                running = False

            if not player_stay and event.type == pygame.MOUSEBUTTONUP:
                (x,y), left = event.pos, event.button == 1

                if left:
                    if W - 200 <= x <= W - 200 + stay_box.get_width() and \
                       200 <= y <= 200 + stay_box.get_height():
                        # if you click on stay, then player_stay == True
                        player_stay = True
                    elif W - 200 <= x <= W - 200 + hit_box.get_width() and \
                         H - 200 <= y <= H - 200 + hit_box.get_height():
                        # if you click on stay, then player_hit == True
                        player_hit = True
        
        if freeze:
            frame_cntr += 1
            clock.tick(60)

            if frame_cntr >= 60:
                # after waiting, next hand
                cs = []
                for i in range(4):
                    c = deck.pop()
                    cs.append(Card(values.index(c[0]), suits.index(c[1]), card_size, cardback))

                    if len(deck) == 0:
                        deck = reshuffle_deck(num_decks)

                dealer = BlackjackDealerHand(cs[0], cs[1])
                player = BlackjackHand(cs[2], cs[3])

                # main game loop
                running = True
                player_stay = False
                player_hit = False
                freeze = False
                frame_cntr = 0


        ###############################
        # Game logic updates
        ###############################
        # ...

        # check for busts and blackjacks
        pbust = player.is_bust()
        dbust = dealer.is_bust()
        pbj = player.is_blackjack()
        dbj = dealer.is_blackjack()

        # check for blackjacks and player clicks
        if pbj or dbj:
            player_stay = True
            player_hit = False
        elif player_stay:
            # once you stay you can't hit anymore
            player_hit = False

            # add cards to dealer's hand until 17 or more
            dealer.hide = False
            while dealer.value < 17:
                c = deck.pop()
                card = Card(values.index(c[0]), suits.index(c[1]), card_size, _cardback = cardback)
                dealer.hit(card)

                if len(deck) == 0:
                    deck = reshuffle_deck(num_decks)
        elif player_hit:
            # if player hits then add one card to their hand
            c = deck.pop()
            card = Card(values.index(c[0]), suits.index(c[1]), card_size, _cardback = cardback)
            player.hit(card)

            if len(deck) == 0:
                deck = reshuffle_deck(num_decks)
            
            player_hit = False
            player_stay = player.is_bust()


        dtext = basic_font.render(f'Dealer: {'?' if dealer.hide else dealer.value}', True, dcolor)
        ptext = basic_font.render(f'Player: {player.value}', True, pcolor)


        ###############################
        # Screen updates
        ###############################
        # clear screen
        screen.fill(screen_bg)

        # graphics changes
        # ....

        # stay and hit buttons
        screen.blit(hit_box, (W - 200, H - 200))
        screen.blit(stay_box, (W - 200, 200))

        # display win or lost banner based on outcome of the game
        if player.is_blackjack() and dealer.is_blackjack():
            tie_text = bust_font.render('Push!', True, 'white')
            tie_box = pygame.Surface((W, 3*tie_text.get_height()))
            tie_box.fill(end_bg)

            center_blit(tie_box, tie_text)
            center_blit(screen, tie_box)

            freeze = True
        elif player.is_blackjack():
            win_text = bust_font.render('Blackjack! You Won!', True, pcolor)
            win_box = pygame.Surface((W, 3*win_text.get_height()))
            win_box.fill(end_bg)

            center_blit(win_box, win_text)
            center_blit(screen, win_box)

            freeze = True
        elif dealer.is_blackjack():
            lose_text = bust_font.render('Blackjack! You Lost!', True, dcolor)
            lose_box = pygame.Surface((W, 3*lose_text.get_height()))
            lose_box.fill(end_bg)

            center_blit(lose_box, lose_text)
            center_blit(screen, lose_box)

            freeze = True
        elif player.is_bust():
            bust_text = bust_font.render('You Busted! You Lost!', True, dcolor)
            bust_box = pygame.Surface((W, 3*bust_text.get_height()))
            bust_box.fill(end_bg)
            center_blit(bust_box, bust_text)

            dealer.cards = dealer.cards[:2]
            dealer.hide = True

            center_blit(screen, bust_box)

            freeze = True
        elif dealer.is_bust():
            bust_text = bust_font.render('Dealer Busted! You Won!', True, pcolor)
            bust_box = pygame.Surface((W, 3*bust_text.get_height()))
            bust_box.fill(end_bg)

            center_blit(bust_box, bust_text)
            center_blit(screen, bust_box)

            freeze = True
        elif player_stay and player.value == dealer.value:
            tie_text = bust_font.render('Push!', True, 'white')
            tie_box = pygame.Surface((W, 3*tie_text.get_height()))
            tie_box.fill(end_bg)

            center_blit(tie_box, tie_text)
            center_blit(screen, tie_box)

            freeze = True
        elif player_stay and player.value > dealer.value:
            win_text = bust_font.render('You Won!', True, pcolor)
            win_box = pygame.Surface((W, 3*win_text.get_height()))
            win_box.fill(end_bg)

            center_blit(win_box, win_text)
            center_blit(screen, win_box)

            freeze = True
        elif player_stay and player.value < dealer.value:
            lose_text = bust_font.render('You Lost!', True, dcolor)
            lose_box = pygame.Surface((W, 3*lose_text.get_height()))
            lose_box.fill(end_bg)

            center_blit(lose_box, lose_text)
            center_blit(screen, lose_box)

            freeze = True

        # current hand
        screen.blit(dtext, (150, 50))
        screen.blit(ptext, (150, H - card_size[1]*scale_size - 150))
        screen.blit(dealer.draw_hand(scale_size, screen_bg), (150, 100))
        screen.blit(player.draw_hand(scale_size, screen_bg), (150, H - card_size[1]*scale_size - 100))


        # show renderd graphics
        pygame.display.flip()

        # limit fps to 60
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    # get screen with width and height
    W, H = 1300, 800
    screen = pygame.display.set_mode((W, H))

    # card sprites
    card_sprites = pygame.image.load('../cards_sprites.png').convert()
    cardback_sprites = pygame.image.load('../cardback_sprites.png').convert()
    cardback_sprites.set_colorkey(pygame.Color(0,255,0))

    cardback = pygame.Surface((40, 56))
    cardback.fill('pink')

    # card deck parameters
    values = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    suits = ['S', 'C', 'H', 'D']

    main_game(screen, (20, 28), cardback, values, suits, 6)