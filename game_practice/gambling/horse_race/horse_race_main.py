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

banner_colors = [
    pygame.Color(0,0,0),
    pygame.Color(255,255,255),
    pygame.Color(0,0,0),
    pygame.Color(0,0,0),
    pygame.Color(125,125,125)
]

color_names = [
    'red', 
    'black', 
    'green', 
    'white', 
    'blue'
]
horses = [pygame.Surface((50, 50)) for _ in colors]

# create track
tracks = [[(W//5, (i + 1)*H//(len(colors) + 3)), (4*W//5, (i + 1)*H//(len(colors) + 3))] for i in range(len(colors))]

class InitialState:
    # horse starting positions
    horse_pos = [(W//5, (i + 1)*H//(len(colors) + 3) - 50) for i in range(len(colors))]
    # horse speeds
    speeds = [10 for _ in range(len(colors))]

    # winner selected
    winner = []

    # freeze game on win
    freeze = False
    freeze_frames = 0

    def reset(self):
        return self.horse_pos, self.speeds, self.winner, self.freeze, self.freeze_frames

setup = InitialState()
hps, ss, w, f, ff = setup.reset()
w = w.copy()

# main game loop
running = True
while running:
    # if player clicks X then exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            hps, ss, w, f, ff = setup.reset()
            w = w.copy()
    
    # winning freeze frame
    if f:
        if len(w) == 1:
            # write the winner on the screen
            win_font = pygame.font.Font(size=50)
            win_text = win_font.render(f'{color_names[w[0]].upper()} WON!', True, colors[w[0]])

            # invert color for background
            win_text_background = pygame.Surface((W, win_text.get_height()*2))
            win_text_background.fill(banner_colors[w[0]])
            center_blit(win_text_background, win_text)
            center_blit(screen, win_text_background)
        else:
            tie_string = ""
            for i, tier in enumerate(w):
                tie_string += color_names[tier].upper()
                if i == len(w) - 2:
                    tie_string += ", and "
                elif i == len(w) - 1:
                    tie_string += " TIED! Photo Finish!"
                else:
                    tie_string += ", "

            # write the winner on the screen
            tie_font = pygame.font.Font(size=50)
            tie_text = tie_font.render(tie_string, True, 'white')

            # invert color for background
            tie_text_background = pygame.Surface((W, tie_text.get_height()*2))
            tie_text_background.fill(pygame.Color(50,50,50))
            center_blit(tie_text_background, tie_text)
            center_blit(screen, tie_text_background)

        pygame.display.flip()

        ff += 1
        clock.tick(60)
        if ff >= 300:
            break

        continue
    
    ###############################
    # Game logic updates
    ###############################
    # change horses speeds by a random amount
    ss = [max(5, ss[i] + random.randint(-1, 1)) for i in range(len(colors))]

    # move horses
    hps = [(hps[i][0] + ss[i], hps[i][1]) for i in range(len(colors))]

    # if any of the horses won then freeze
    for i, pos in enumerate(hps):
        if pos[0]+50 >= 4*W//5:
            hps[i] = (4*W//5 - 50, hps[i][1])
            w.append(i)
            f = True

    ###############################
    # Screen updates
    ###############################
    # clear screen
    screen.fill('grey')

    # graphics changes
    for i in range(len(colors)):
        horses[i].fill(colors[i])
        screen.blit(horses[i], hps[i])
        pygame.draw.line(screen, colors[i], tracks[i][0], tracks[i][1], 15)

    # show renderd graphics
    pygame.display.flip()

    # limit fps to 60
    clock.tick(20)

pygame.quit()