import sys
from time import sleep
import pygame
pygame.init()

# constants
COLOR_BLACK = 0, 0, 0
COLOR_WHITE = 255, 255, 255
BLOCK_SIZE = 30
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600

# game vars
frame = 0
velocity = [BLOCK_SIZE, BLOCK_SIZE]
screen = pygame.display.set_mode(SCREEN_SIZE)
snake_rect = pygame.Rect(120, 120, BLOCK_SIZE, BLOCK_SIZE)

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
    sleep(0.25)

