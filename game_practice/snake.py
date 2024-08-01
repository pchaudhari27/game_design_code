import pygame
from pygame.locals import *
import random

class SnakeBlock:
    def __init__(self, _pos, _parent, _dims=(20,20), _curr_dir=1) -> None:
        '''
        SnakeBlock class takes in a current position and a parent SnakeBlock to follow.
        '''
        self.pos = _pos
        self.parent = _parent
        self.dims = _dims

        # set cardinal directions--start by moving right
        #   0=N, 1=E, 2=S, 3=W
        self.curr_dir = _curr_dir

        # calculate distance from head if there is a parent
        self.dist_from_head = 0 if not self.parent else self.parent.dist_from_head + 1

        self.box = pygame.Rect(self.pos, self.dims)
    
    def follow(self, speed):
        if self.parent:
            x1, y1 = self.pos
            x2, y2 = self.parent.pos

            if self.curr_dir % 2:
                # if moving left or right, change direction 
                # only if your parent is directly up or down
                if (y2 - y1) // self.dims[1] == 1:
                    self.curr_dir = 2
                elif (y1- y2) // self.dims[1] == 1:
                    self.curr_dir = 0
            else:
                # if moving up or down, change direction 
                # only if your parent is directly up or down
                if (x2 - x1) // self.dims[0] == 1:
                    self.curr_dir = 1
                elif (x1 - x2) // self.dims[0] == 1:
                    self.curr_dir = 3

        # move block
        match self.curr_dir:
            case 0:
                self.pos = self.pos[0], self.pos[1] - speed[1]
            case 1:
                self.pos = self.pos[0] + speed[0], self.pos[1]
            case 2:
                self.pos = self.pos[0], self.pos[1] + speed[1]
            case 3:
                self.pos = self.pos[0] - speed[0], self.pos[1]

    
    def draw(self, surf):
        self.box = pygame.draw.rect(surf, 'green' if self.parent else 'red', pygame.Rect(self.pos, self.dims))

def gcd(a,b):
    while b:
        a,b = b, a%b
    return a

def lcm(a,b):
    return a*b//gcd(a,b)    

# start pygame
pygame.init()
pygame.font.init()
title_font = pygame.font.Font(size = 50)
game_font = pygame.font.Font(size=30)

# get screen with width and height
W, H = 1300, 1000
screen = pygame.display.set_mode((W, H))

# get clock for frame setting
clock = pygame.time.Clock()

# write title
title = title_font.render('Snake', True, 'black')

# write instructions
instructions = game_font.render('Move with WASD. Collect fruit. Become long.', True, 'blue')

# write fruit counter
length = 5
length_tracker = game_font.render(f'Current Length: {length}', True, 'blue')

# collect all text in a list
texts = [title, instructions, length_tracker]

# create initial snake
block_dims = (20,20)
start_position = (block_dims[0]*(W//(2*block_dims[0])), block_dims[1]*(H//(2*block_dims[1])))
head = SnakeBlock(start_position, None, block_dims)
mid = SnakeBlock((start_position[0] - block_dims[0], start_position[1]), head, block_dims)
mid1 = SnakeBlock((start_position[0] - 2*block_dims[0], start_position[1]), mid, block_dims)
mid2 = SnakeBlock((start_position[0] - 3*block_dims[0], start_position[1]), mid1, block_dims)
tail = SnakeBlock((start_position[0] - 4*block_dims[0], start_position[1]), mid2, block_dims)


# create fruits
fruit_timer = 10**9
fruits_available = 0
fruits = []

# set movement parameters
speed = [4,4]
last_key_pressed = []

# set movable area with enclosure
thic = lcm(block_dims[0], block_dims[1])
offset = max(texts, key = lambda a: a.get_height()).get_height() + 30
movable_area = pygame.Surface((W, H - offset))
pygame.draw.rect(movable_area, 'white', movable_area.get_rect(), width = thic)

# main game loop
running = True
fps = 60
lost = False
freeze_frames = 0
extra_message = ''
while running:
    # if player clicks X then exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if you get really long, you win, freeze for a bit and give a fun message
    if length >= (W//block_dims[0] - 5)*(H//block_dims[1] - 5):
        extra_message = 'you won! You are one long snake!'

        # game over screen
        game_over_font = pygame.font.Font(size = 50)
        game_over = game_over_font.render(f'Game over, {extra_message}', True, 'blue')
        game_over_background = pygame.Surface((W, 2*game_over.get_height()))
        game_over_rect = game_over_background.fill('white')

        game_over_background.blit(game_over, (game_over_rect.width//2 - game_over.get_width()//2, game_over_rect.height//2 - game_over.get_height()//2))
        screen.blit(game_over_background, (0, H//2 - game_over.get_height()))
        pygame.display.flip()

        freeze_frames += 1

        if freeze_frames > 5000:
            running = False

        continue

    # if you lose, freeze for a bit and give a fun message
    if lost:
        # game over screen
        game_over_font = pygame.font.Font(size = 50)
        game_over = game_over_font.render(f'Game over, {extra_message}', True, 'blue')
        game_over_background = pygame.Surface((W, 2*game_over.get_height()))
        game_over_rect = game_over_background.fill('white')

        game_over_background.blit(game_over, (game_over_rect.width//2 - game_over.get_width()//2, game_over_rect.height//2 - game_over.get_height()//2))
        screen.blit(game_over_background, (0, H//2 - game_over.get_height()))
        pygame.display.flip()

        freeze_frames += 1

        if freeze_frames > 5000:
            running = False

        continue
    
    ###############################
    # Game logic updates
    ###############################
    # when player clicks keys, save new direction of movement
    keys = pygame.key.get_pressed()
    to_check = head.curr_dir if not last_key_pressed else last_key_pressed[-1]

    # save the last key press for next direction change
    if to_check % 2:
    # if moving in the left or right direction
    # can only change to up or down
        if keys[pygame.K_w]:
            last_key_pressed.append(0)
        elif keys[pygame.K_s]:
            last_key_pressed.append(2)
    else:
        # else if moving in the up or down direction
        # can only change to left or right
        if keys[pygame.K_d]:
            last_key_pressed.append(1)
        elif keys[pygame.K_a]:
            last_key_pressed.append(3)

    # if there was a key pressed, apply it at the next possible time
    if last_key_pressed:
        if (last_key_pressed[0] % 2 == 1 and (head.pos[1]//block_dims[1] == head.pos[1]/block_dims[1])) or \
           (last_key_pressed[0] % 2 == 0 and (head.pos[0]//block_dims[0] == head.pos[0]/block_dims[0])):
            # if there was a last key pressed, then time the next move appropriately
            head.curr_dir = last_key_pressed.pop(0)

    # truncate last_key_pressed to not take too much space
    last_key_pressed = last_key_pressed[:5]

    # check if your about to move off screen to end the game
    if (head.curr_dir == 0 and head.pos[1] <= thic) or \
       (head.curr_dir == 1 and head.pos[0] >= W - block_dims[0] - thic) or \
       (head.curr_dir == 2 and head.pos[1] >= H - block_dims[1] - thic - offset) or \
       (head.curr_dir == 3 and head.pos[0] <= thic):
        extra_message = 'you fell off the edge of the world!'
        print('\nGame Over! You ate yourself!')

        lost = True

    # generate fruits randomly every 3 seconds
    fruit_timer += 1
    if fruit_timer >= fps*3:
        # create a maximum of 5 fruits
        if fruits_available < 5:
            # make a fruit at a random location with the same dimensions as SnakeBlock
            # make sure fruits go on exact locations
            while True:
                new_fruit = pygame.Rect(
                    random.randint(3, ((W - block_dims[0] - thic)//block_dims[0]) - 3)*block_dims[0] + block_dims[0]//10, 
                    random.randint(3, ((H - block_dims[1] - thic - offset)//block_dims[1]) - 3)*block_dims[1] + block_dims[1]//10, 
                    block_dims[0] - block_dims[0]//10,
                    block_dims[1] - block_dims[1]//10
                )
                
                # if new fruit is on top of another fruit then redo
                if new_fruit.collidelist(fruits) >= 0:
                    continue
                
                break

            fruits.append(new_fruit)
            fruits_available += 1

            # reset fruit timer
            fruit_timer = 0

    # if head collided with a fruit add a new block
    fruit_collected = head.box.collidelist(fruits)
    if fruit_collected >= 0:
        # remove fruit from board
        fruits.pop(fruit_collected)

        # create a new SnakeBlock before the tail
        new_mid = SnakeBlock(tail.pos, tail.parent, tail.dims, tail.curr_dir)
        match new_mid.curr_dir:
            case 0:
                tail.pos = new_mid.pos[0], new_mid.pos[1] + block_dims[1]
            case 1:
                tail.pos = new_mid.pos[0] - block_dims[0], new_mid.pos[1]
            case 2:
                tail.pos = new_mid.pos[0], new_mid.pos[1] - block_dims[1]
            case 3:
                tail.pos = new_mid.pos[0] + block_dims[0], new_mid.pos[1]
            case _:
                raise AssertionError("Current direction of newly created block is not valid. Fatal Error")

        # make sure to keep the tail at the end
        tail.parent = new_mid
        tail.curr_dir = new_mid.curr_dir

        # increase length of snake by 1 and reduce number of available fruis by 1
        length += 1
        fruits_available -= 1


    ###############################
    # Screen updates
    ###############################
    # clear screen
    screen.fill('white')
    movable_area.fill('black')

    # move tail first, then parent, until you get to the head
    curr = tail
    while curr:
        curr.follow(speed)
        curr.draw(movable_area)

        # if some part of tail passes close enough to head, then game will end
        if curr.dist_from_head >= 4 and abs(curr.pos[0]-head.pos[0]) < 1.5*speed[0] and abs(curr.pos[1]-head.pos[1]) < 1.5*speed[1]:
            print('\nGame Over! You ate yourself!')
            extra_message = 'you ate yourself!'

            lost = True

        curr = curr.parent

    # draw fruits if they are there to be collected
    for fruit in fruits:
        pygame.draw.rect(movable_area, 'white', fruit)

    # write the title
    screen.blit(title, (W//2 - title.get_width()//2, title.get_height()//2))
    # write the instructions
    screen.blit(instructions, (20, title.get_height()//2))
    # write the length tracker
    length_tracker = game_font.render(f'Current Length: {length}', True, 'blue')
    screen.blit(length_tracker, (W-length_tracker.get_width()-20, title.get_height()//2))

    # draw encloure for the player
    pygame.draw.rect(movable_area, 'white', movable_area.get_rect(), width = thic)

    # draw movable area for player
    screen.blit(movable_area, (0, offset))

    # show renderd graphics
    pygame.display.flip()

    # limit fps
    clock.tick(fps)

pygame.quit()