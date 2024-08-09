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
    choose_text = basic_font.render('Choose your cardback!', True, 'white')

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

    # main game loop
    running = True
    screen_bg = pygame.Color(53, 101, 77)

    while running:
        for event in pygame.event.get():
            # if player clicks X then exit
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                (x,y), left = event.pos, event.button == 1
                
                if left:
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
                    elif W//2 - play_box.get_width()//2 <= x <= W//2 + play_box.get_width()//2 and \
                        5*H//6 <= y <= 5*H//6 + play_box.get_height():
                        # if you click on play button, then start the game
                        running = False

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
        center_blit(screen, choose_text, centery = False, override_height= H//4)
        
        center_blit(screen, pygame.transform.scale(cardback, (scale_size*cardback_size[0], scale_size*cardback_size[1])), centery = False, override_height = H//4 + 50)

        center_blit(screen, play_box, centery = False, override_height= 5*H//6)

        # draw left and right buttons for cardbacks
        pygame.draw.lines(screen, 'white', True, [(W//2 - 150, H//2 + 50), (W//2 - 150, H//2 - 50), (W//2 - 200, H//2)], width = 10)
        pygame.draw.lines(screen, 'white', True, [(W//2 + 150, H//2 + 50), (W//2 + 150, H//2 - 50), (W//2 + 200, H//2)], width = 10)

        # show renderd graphics
        pygame.display.flip()

        # limit fps to 60
        clock.tick(60)

    return cardback

if __name__ == "__main__":
    # get screen with width and height
    W, H = 1300, 800
    screen = pygame.display.set_mode((W, H))

    # card sprites
    card_sprites = pygame.image.load('../cards_sprites.png').convert()
    cardback_sprites = pygame.image.load('../cardback_sprites.png').convert()
    cardback_sprites.set_colorkey(pygame.Color(0,255,0))

    cardback = main_menu(screen, cardback_sprites, (40, 56), 6)
    pygame.quit()