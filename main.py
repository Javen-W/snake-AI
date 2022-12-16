import sys
from time import sleep
import pygame
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
    'north': [0, BLOCK_SIZE],
    'south': [0, -BLOCK_SIZE],
    'north-west': [BLOCK_SIZE, -BLOCK_SIZE],
    'north-east': [-BLOCK_SIZE, -BLOCK_SIZE],
    'south-west': [BLOCK_SIZE, BLOCK_SIZE],
    'south-east': [-BLOCK_SIZE, BLOCK_SIZE],
}

# game vars
frame = 0
velocity = VELOCITIES['south-west']
screen = pygame.display.set_mode(SCREEN_SIZE)
snake_rect = pygame.Rect(START_COORDS, (BLOCK_SIZE, BLOCK_SIZE))

# play
while frame < 100:
    print("Frame: {} | Left: {} | Right: {} | Top: {} | Bottom: {}".format(
        frame, snake_rect.left, snake_rect.right, snake_rect.top, snake_rect.bottom)
    )

    # draw & display current frame
    screen.fill(COLOR_BLACK)
    pygame.draw.rect(screen, COLOR_WHITE, snake_rect)
    pygame.display.flip()

    # event listeners
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # move snake
    snake_rect = snake_rect.move(velocity)
    if snake_rect.left <= 0 or snake_rect.right >= SCREEN_WIDTH:
        velocity[0] = -velocity[0]
    if snake_rect.top <= 0 or snake_rect.bottom >= SCREEN_HEIGHT:
        velocity[1] = -velocity[1]

    # advance frame
    frame += 1
    sleep(1/10)

