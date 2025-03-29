import pygame
from pygame.locals import *
from classes import Card, BlackjackDealerHand, BlackjackHand
from helper_utils import center_blit, reshuffle_deck

def main_game(
    screen: pygame.Surface,
    card_size: tuple[int, int],
    cardback: pygame.Surface,
    ckey: pygame.Color,
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
    menu_font = pygame.font.Font(size=30)

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

    hit_pos = (W - 200, H - 200)
    stay_pos = (W - 200, H - 300)

    # create button for menu
    menu_text = menu_font.render('Back to Main Menu', True, 'black')

    # stay text is longer so make both boxes the same size
    menu_box = pygame.Surface((2*menu_text.get_width(), 4*menu_text.get_height()))

    menu_box.fill('white')
    center_blit(menu_box, menu_text)
    menu_pos = (W - menu_box.get_width() - 10, 10)

    # get clock for frame setting
    clock = pygame.time.Clock()

    # draw the deck
    card_deck = pygame.image.load('../card_deck_sprite.png')
    card_deck.set_colorkey(ckey)
    card_deck.blit(cardback, (0, 0))
    card_deck = pygame.transform.scale(card_deck, (scale_size*(card_size[0] + 3), scale_size*card_size[1]))

    deck_pos = (W - card_deck.get_width() - 100, (H - card_size[1]*scale_size - 200)//2)

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
    
    class InitialState:
        player_stay = False
        player_hit = False
        dealer_hit = False
        freeze = False
        frame_cntr = 0
        hit_animation = False
        dealer_hit_animation = False

        def reset(self):
            return self.player_stay, self.player_hit, self.dealer_hit, self.freeze, self.frame_cntr, self.hit_animation, self.dealer_hit_animation

    # main game loop
    running = True
    screen_bg = pygame.Color(53, 101, 77)
    end_bg = pygame.Color(25, 25, 25)

    setup = InitialState()

    save_screen = pygame.Surface((W, H))
    
    player_stay, player_hit, dealer_hit, freeze, frame_cntr, hit_animation, dealer_hit_animation = setup.reset()

    while running:
        for event in pygame.event.get():
            # if player clicks X then exit
            if event.type == pygame.QUIT:
                running = False

            if not player_stay and not hit_animation and event.type == pygame.MOUSEBUTTONUP:
                (x,y), left = event.pos, event.button == 1

                if left:
                    if stay_pos[0] <= x <= stay_pos[0] + stay_box.get_width() and \
                       stay_pos[1] <= y <= stay_pos[1] + stay_box.get_height():
                        # if you click on stay, then player_stay == True
                        player_stay = True

                    elif hit_pos[0] <= x <= hit_pos[0] + hit_box.get_width() and \
                         hit_pos[1] <= y <= hit_pos[1]  + hit_box.get_height():
                        # if you click on stay, then player_hit == True
                        player_hit = True
                        hit_animation = True

                        save_screen.blit(screen, (0, 0))
                        save_screen.blit(menu_box, menu_pos)

                        target = (150 + card_size[0]*(scale_size+1)*len(player.cards), H - card_size[1]*scale_size - 100)
                        fake_card = pygame.Rect(deck_pos, (card_size[0]*scale_size, card_size[1]*scale_size))

            if event.type == pygame.MOUSEBUTTONUP:
                (x,y), left = event.pos, event.button == 1

                if left:
                    if menu_pos[0] <= x <= menu_pos[0] + menu_box.get_width() and \
                       menu_pos[1] <= y <= menu_pos[1] + menu_box.get_height():
                        return "back to menu"
        
        if hit_animation:
            fake_card = fake_card.move((target[0]-deck_pos[0])/100, (target[1]-deck_pos[1])/90)
            screen.fill(screen_bg)
            
            screen.blit(save_screen, (0,0))
            screen.blit(pygame.transform.scale(cardback, fake_card.size), fake_card.topleft)
            pygame.display.flip()

            if fake_card.topleft[0] <= target[0]:
                fake_card2 = fake_card.copy()
                for i in range(20):
                    clock.tick(100)
                    screen.blit(save_screen, (0,0))
                    screen.blit(pygame.transform.scale(cardback, fake_card2.size), fake_card2.topleft)
                    fake_card2 = fake_card2.scale_by(0.85, 1)
                    pygame.display.flip()
                hit_animation = False
                screen.blit(save_screen, (0,0))
                clock.tick(200)
            clock.tick(300)
            continue

        if dealer_hit_animation:
            fake_card = fake_card.move((target[0]-deck_pos[0])/100, (target[1]-deck_pos[1])/90)
            screen.fill(screen_bg)
            
            screen.blit(save_screen, (0,0))
            screen.blit(pygame.transform.scale(cardback, fake_card.size), fake_card.topleft)
            pygame.display.flip()

            if fake_card.topleft[0] <= target[0]:
                fake_card2 = fake_card.copy()
                for i in range(20):
                    clock.tick(100)
                    screen.blit(save_screen, (0,0))
                    screen.blit(pygame.transform.scale(cardback, fake_card2.size), fake_card2.topleft)
                    fake_card2 = fake_card2.scale_by(0.85, 1)
                    pygame.display.flip()
                dealer_hit_animation = False
                dealer_hit = True
                screen.blit(save_screen, (0,0))
                clock.tick(200)
            clock.tick(300)
            continue


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
                player_stay, player_hit, dealer_hit, freeze, frame_cntr, hit_animation, dealer_hit_animation = setup.reset()


        ###############################
        # Game logic updates
        ###############################
        # ...

        # check for busts and blackjacks
        pbj = player.is_blackjack()
        dbj = dealer.is_blackjack()

        # check for blackjacks and player clicks
        if pbj or dbj:
            player_stay = True
            player_hit = False
            dealer.hide = False
        elif player_stay:
            # once you stay you can't hit anymore
            player_hit = False

            # when player stays, reveal dealer's hand
            if dealer.hide:
                dealer.hide = False
            else:
                # dealer's hand is already revealed--do the hit animation if < 17
                # add cards to dealer's hand until 17 or more
                if dealer.value < 17:
                    if dealer_hit:
                        c = deck.pop()
                        card = Card(values.index(c[0]), suits.index(c[1]), card_size, _cardback = cardback)
                        dealer.hit(card)

                        if len(deck) == 0:
                            deck = reshuffle_deck(num_decks)

                        dealer_hit = False
                    else:
                        dealer_hit_animation = True
                
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
        screen.blit(hit_box, hit_pos)
        screen.blit(stay_box, stay_pos)
        screen.blit(menu_box, menu_pos)
        screen.blit(card_deck, deck_pos)

        if (dealer.value >= 17 or player.value >= 21) and (not dealer_hit and not dealer_hit_animation):
            # display win or lost banner based on outcome of the game
            if pbj and dbj:
                tie_text = bust_font.render('Push!', True, 'white')
                tie_box = pygame.Surface((W, 3*tie_text.get_height()))
                tie_box.fill(end_bg)

                center_blit(tie_box, tie_text)
                center_blit(screen, tie_box)

                freeze = True
            elif pbj:
                win_text = bust_font.render('Blackjack! You Won!', True, pcolor)
                win_box = pygame.Surface((W, 3*win_text.get_height()))
                win_box.fill(end_bg)

                center_blit(win_box, win_text)
                center_blit(screen, win_box)

                freeze = True
            elif dbj:
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

        if dealer_hit_animation:
            save_screen.blit(screen, (0, 0))
            save_screen.blit(menu_box, menu_pos)
            target = (150 + card_size[0]*(scale_size+1)*len(dealer.cards), 100)
            fake_card = pygame.Rect(deck_pos, (card_size[0]*scale_size, card_size[1]*scale_size))


        # show renderd graphics
        pygame.display.flip()

        # limit fps to 60
        clock.tick(60)

    pygame.quit()

    return "quit"


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

    main_game(screen, (20, 28), cardback, pygame.Color(0,255,0), values, suits, 6)