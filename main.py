import sys
from time import sleep
import pygame
import random
pygame.init()

# constants
COLOR_BLACK = 0, 0, 0
COLOR_WHITE = 255, 255, 255
BLOCK_SIZE = 30
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
START_COORDS = (BLOCK_SIZE * 6, BLOCK_SIZE * 5)
VELOCITIES = {
    'west': [BLOCK_SIZE, 0],
    'east': [-BLOCK_SIZE, 0],
    'north': [0, -BLOCK_SIZE],
    'south': [0, BLOCK_SIZE],
    'north-west': [BLOCK_SIZE, -BLOCK_SIZE],
    'north-east': [-BLOCK_SIZE, -BLOCK_SIZE],
    'south-west': [BLOCK_SIZE, BLOCK_SIZE],
    'south-east': [-BLOCK_SIZE, BLOCK_SIZE],
}

# game vars
frame = 0
direction = 'south-west'
screen = pygame.display.set_mode(SCREEN_SIZE)
snake_rect = pygame.Rect(START_COORDS, (BLOCK_SIZE, BLOCK_SIZE))

# play
while frame < 1000:
    print("Frame: {} | Next direction: {} | Coords: ({}, {}, {}, {})".format(
        frame, direction, snake_rect.left, snake_rect.right, snake_rect.top, snake_rect.bottom)
    )

    # draw & display current frame
    screen.fill(COLOR_BLACK)
    pygame.draw.rect(screen, COLOR_WHITE, snake_rect)
    pygame.display.flip()

    # event listeners
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # move snake
    snake_rect = snake_rect.move(VELOCITIES[direction])

    # decide next direction
    if snake_rect.left <= 0:
        direction = random.choice(['south-west', 'north-west', 'west'])
    if snake_rect.right >= SCREEN_WIDTH:
        direction = random.choice(['south-east', 'north-east', 'east'])
    if snake_rect.top <= 0:
        direction = random.choice(['south-west', 'south-east', 'south'])
    if snake_rect.bottom >= SCREEN_HEIGHT:
        direction = random.choice(['north-west', 'north-east', 'north'])

    # advance frame
    frame += 1
    sleep(1/10)

