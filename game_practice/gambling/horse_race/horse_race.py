import pygame
from pygame.locals import *
import random

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

# start pygame
pygame.init()
pygame.font.init()

# get screen with width and height
all_desktop_dims = pygame.display.get_desktop_sizes()
W, H = 5*min(all_desktop_dims)[0]//6, 5*min(all_desktop_dims, key = lambda a: (a[1],a[0]))[1]//6
screen = pygame.display.set_mode((W, H))

# get clock for frame setting
clock = pygame.time.Clock()

# create horses
colors = [
    pygame.Color(255,0,0), 
    pygame.Color(0,0,0), 
    pygame.Color(0,255,0), 
    pygame.Color(255,255,255), 
    pygame.Color(0,0,255)
]
color_names = [
    'red', 
    'black', 
    'green', 
    'white', 
    'blue'
]
horses = [pygame.Surface((50, 50)) for _ in colors]
horse_pos = [(W//5, (i + 1)*H//(len(colors) + 3) - 50) for i in range(len(colors))]

# create track
tracks = [[(W//5, (i + 1)*H//(len(colors) + 3)), (4*W//5, (i + 1)*H//(len(colors) + 3))] for i in range(len(colors))]

# horse speeds
speeds = [10 for _ in range(len(colors))]

# main game loop
running = True
freeze = False
winner = -1
freeze_frames = 0
while running:
    # if player clicks X then exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # winning freeze frame
    if freeze:
        # write the winner on the screen
        win_font = pygame.font.Font(size=50)
        win_text = win_font.render(f'{color_names[winner].upper()} WON!', True, colors[winner])

        # invert color for background
        win_text_background = pygame.Surface((W, win_text.get_height()*2))
        win_text_background.fill(
            pygame.Color(255 - colors[winner].r, 255 - colors[winner].g, 255 - colors[winner].b)
        )
        center_blit(win_text_background, win_text)
        center_blit(screen, win_text_background)

        pygame.display.flip()

        freeze_frames += 1
        clock.tick(60)
        if freeze_frames >= 300:
            break

        continue
    
    ###############################
    # Game logic updates
    ###############################
    # change horses speeds by a random amount
    speeds = [max(5, speeds[i] + random.randint(-5, 5)) for i in range(len(colors))]

    # move horses
    horse_pos = [(horse_pos[i][0] + speeds[i], horse_pos[i][1]) for i in range(len(colors))]

    # if any of the horses won then freeze
    for i, pos in enumerate(horse_pos):
        if pos[0]+50 >= 4*W//5:
            horse_pos[i] = (4*W//5 - 50, horse_pos[i][1])
            winner = i
            freeze = True

    ###############################
    # Screen updates
    ###############################
    # clear screen
    screen.fill('grey')

    # graphics changes
    for i in range(len(colors)):
        horses[i].fill(colors[i])
        screen.blit(horses[i], horse_pos[i])
        pygame.draw.line(screen, colors[i], tracks[i][0], tracks[i][1], 15)

    # show renderd graphics
    pygame.display.flip()

    # limit fps to 60
    clock.tick(20)

pygame.quit()