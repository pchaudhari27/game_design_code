import pygame
from pygame.locals import *

def center_blit(
        bg_surface: pygame.Surface, 
        fg_surface: pygame.Surface, 
        area: pygame.Rect=None, 
        centerx: bool = True, 
        centery: bool = True,
        override_width: int = -1,
        override_height: int = -1
    ):
    '''
    Simple function for centering and blitting a foreground surface onto a background surface.
    You can center just one of the dimensions and override the other if you need.
    '''
    if centerx:
        override_width = bg_surface.get_width()//2 - fg_surface.get_width()//2
    if centery:
        override_height = bg_surface.get_height()//2 - fg_surface.get_height()//2

    bg_surface.blit(fg_surface, (override_width, override_height), area)


def home_page_loop(screen: pygame.Surface):
    # start pygame
    pygame.init()
    pygame.font.init()
    title_font = pygame.font.Font(size=150)
    selection_font = pygame.font.Font(size=40)

    W, H = screen.get_size()

    # get clock for frame setting
    clock = pygame.time.Clock()

    # write title and subtitle
    title = title_font.render('Snake', True, 'black')
    chooose_difficulty = selection_font.render('Choose Your Difficulty', True, 'black')
    loading = title_font.render('Loading...', True, 'Red')

    # user choices
    easy = selection_font.render('Easy (Big Snake, Small Enclosure)', True, 'white')
    hard = selection_font.render('Hard (Small Snake, Big Enclosure)', True, 'white')

    easy_button = pygame.Surface((4*easy.get_width()//3, 2*easy.get_height()))
    easy_button.fill('green')
    center_blit(easy_button, easy)

    hard_button = pygame.Surface((4*hard.get_width()//3, 2*hard.get_height()))
    hard_button.fill('red')
    center_blit(hard_button, hard)

    # main game loop
    running = True
    snake_sprite = None
    block_dims = None
    while running:
        for event in pygame.event.get():
            # if player clicks X then exit
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                snake_sprite = None
                block_dims = None
                break
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    x,y = event.pos

                    if W//2 - easy_button.get_width()//2 <= x <= W//2 + easy_button.get_width()//2 and \
                       H//2 <= y <= H//2 + easy_button.get_height():
                        # if on easy button, load easy sprite and block size
                        snake_sprite = pygame.image.load('./images/sprite_big_snake.png')
                        block_dims = (50, 50)
                    elif W//2 - hard_button.get_width()//2 <= x <= W//2 + hard_button.get_width()//2 and \
                       2*H//3 <= y <= 2*H//3 + hard_button.get_height():
                        # if on hard button, load hard sprite and block size
                        snake_sprite = pygame.image.load('./images/sprite_small_snake.png')
                        block_dims = (20, 20)
                    
                    # if hey select a difficulty
                    if snake_sprite and block_dims:
                        screen.fill('grey')
                        center_blit(screen, loading)
                        pygame.display.flip()
                        running = False
                        clock.tick(0.75)
                        continue
        else:
            ###############################
            # Screen updates
            ###############################
            # clear screen
            screen.fill('grey')

            # graphics changes
            center_blit(screen, title, centery = False, override_height = H//6)
            center_blit(screen, chooose_difficulty, centery = False, override_height = H//6 + title.get_height())
            center_blit(screen, easy_button, centery = False, override_height = H//2)
            center_blit(screen, hard_button, centery = False, override_height = 2*H//3)

            # show renderd graphics
            pygame.display.flip()

            # limit fps to 60
            clock.tick(60)

    return snake_sprite, block_dims

if __name__ == "__main__":
    # get screen with width and height
    W, H = 1300, 1000
    screen = pygame.display.set_mode((W, H))
    
    home_page_loop(screen)