import pygame
from pygame.locals import *
from helper_utils import center_blit, reshuffle_deck

def main_menu(
    screen: pygame.Surface,
    cardback_sprites: pygame.Surface,
    cardback_size: tuple[int, int], 
    scale_size: int = 6
):
    # start pygame 
    pygame.init()
    pygame.font.init()
    
    W, H = screen.get_width(), screen.get_height()

    # display text for Dealer and Player
    title_font = pygame.font.Font(size=50)
    basic_font = pygame.font.Font(size=30)

    # create text for menu
    title_text = title_font.render('Blackjack', True, 'white')
    cardback_prompt = basic_font.render('Choose your cardback!', True, 'white')
    num_decks_prompt = basic_font.render('Choose your number of decks!', True, 'white')

    next_text = basic_font.render('Next', True, 'black')
    next_box = pygame.Surface((2*next_text.get_width(), 4*next_text.get_height()))
    next_box.fill('white')
    center_blit(next_box, next_text)

    play_text = basic_font.render('Play', True, 'black')
    play_box = pygame.Surface((2*play_text.get_width(), 4*play_text.get_height()))
    play_box.fill('white')
    center_blit(play_box, play_text)

    # get clock for frame setting
    clock = pygame.time.Clock()

    # display card back designs one by one
    last_cardback = cardback_sprites.get_width() - cardback_size[0], cardback_sprites.get_height() - cardback_size[1]
    curr_cardback = (0,0)
    colors = [
        pygame.Color(16, 19, 86),
        pygame.Color(229, 48, 41),
        pygame.Color(129, 95, 67)
    ]
    curr_color = 0

    # save number of decks the person wants to play with
    num_decks = 4

    # main game loop
    running = True
    player_quit = False
    screen_bg = pygame.Color(53, 101, 77)

    cardback_chosen = False

    while running:
        for event in pygame.event.get():
            # if player clicks X then exit
            if event.type == pygame.QUIT:
                running = False
                player_quit = True

            if event.type == pygame.MOUSEBUTTONUP:
                (x,y), left = event.pos, event.button == 1

                if left:
                    if cardback_chosen:
                        # once you've chosen a cardback, select number of decks to play with
                        if H//4 + 125 <= y <= H//4 + 150 and \
                           -y + H//4 + 125 + W//2 <= x <= y - H//4 - 125 + W//2:
                            # if in the top triangle, then increase number of decks (max of 8)
                            num_decks = min(num_decks+1, 8)
                        elif H//4 + 250 <= y <= H//4 + 275 and \
                             y - H//4 - 275 + W//2 <= x <= -y + H//4 + 275 + W//2:
                            # if in the bottom triangle, then decrease number of decks (min of 1)
                            num_decks = max(num_decks-1, 1)
                        elif W//2 - play_box.get_width()//2 <= x <= W//2 + play_box.get_width()//2 and \
                             5*H//6 <= y <= 5*H//6 + play_box.get_height():
                            # if you click on play button, then start the game
                            running = False
                    else:
                        if W//2 - 200 <= x <= W//2 - 150 and \
                           -x + W//2 - 200 + H//2 <= y <= x - W//2 + 200 + H//2:
                            # if in the left triangle, shift cardback backward
                            if curr_cardback == (0,0):
                                curr_color -= 1
                                curr_cardback = last_cardback
                            else:
                                curr_cardback = curr_cardback[0] - cardback_size[0], curr_cardback[1]
                        elif W//2 + 150 <= x <= W//2 + 200 and \
                             x - W//2 - 200 + H//2 <= y <= -x + W//2 + 200 + H//2:
                            # if in the right triangle, shift cardback forward
                            if curr_cardback == last_cardback:
                                curr_color += 1
                                curr_cardback = (0,0)
                            else:
                                curr_cardback = curr_cardback[0] + cardback_size[0], curr_cardback[1]
                        elif W//2 - next_box.get_width()//2 <= x <= W//2 + next_box.get_width()//2 and \
                             5*H//6 <= y <= 5*H//6 + play_box.get_height():
                                cardback_chosen = True

                        curr_color %= len(colors)



        ###############################
        # Game logic updates
        ###############################
        # ...
        cardback = pygame.Surface(cardback_size)
        cardback.fill(colors[curr_color])
        center_blit(cardback, cardback_sprites, pygame.Rect(curr_cardback, cardback_size))
        
        ###############################
        # Screen updates
        ###############################
        # clear screen
        screen.fill(screen_bg)

        center_blit(screen, title_text, centery = False, override_height= H//6)

        if cardback_chosen:
            center_blit(screen, num_decks_prompt, centery = False, override_height= H//4)

            # show number of decks for choosing on screen
            num_text = title_font.render(f'{num_decks}', True, 'white')
            center_blit(screen, num_text, centery = False, override_height = H//4 + 200 - num_text.get_height()//2)

            # up and down buttons for number of decks
            pygame.draw.polygon(screen, 'white', [(W//2 - 25, H//4 + 150), (W//2 + 25, H//4 + 150), (W//2, H//4 + 125)], width = 0)
            pygame.draw.polygon(screen, 'white', [(W//2 - 25, H//4 + 250), (W//2 + 25, H//4 + 250), (W//2, H//4 + 275)], width = 0)

            center_blit(screen, play_box, centery = False, override_height= 5*H//6)
        else:
            center_blit(screen, cardback_prompt, centery = False, override_height= H//4)

            # draw cardback design
            center_blit(screen, pygame.transform.scale(cardback, (scale_size*cardback_size[0], scale_size*cardback_size[1])), centery = False, override_height = H//4 + 50)

            # draw left and right buttons for cardbacks
            pygame.draw.polygon(screen, 'white', [(W//2 - 150, H//2 + 50), (W//2 - 150, H//2 - 50), (W//2 - 200, H//2)], width = 0)
            pygame.draw.polygon(screen, 'white', [(W//2 + 150, H//2 + 50), (W//2 + 150, H//2 - 50), (W//2 + 200, H//2)], width = 0)

            center_blit(screen, next_box, centery = False, override_height= 5*H//6)

        # show renderd graphics
        pygame.display.flip()

        # limit fps to 60
        clock.tick(60)

    if player_quit:
        return None, None

    return cardback, num_decks

if __name__ == "__main__":
    # get screen with width and height
    W, H = 1300, 800
    screen = pygame.display.set_mode((W, H))

    # card sprites
    card_sprites = pygame.image.load('../cards_sprites.png').convert()
    cardback_sprites = pygame.image.load('../cardback_sprites.png').convert()
    cardback_sprites.set_colorkey(pygame.Color(0,255,0))

    cardback, num_decks = main_menu(screen, cardback_sprites, (40, 56), 6)
    pygame.quit()