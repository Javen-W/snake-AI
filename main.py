import sys
from time import sleep

import pygame
pygame.init()

COLOR_BLACK = 0, 0, 0
COLOR_WHITE = 255, 255, 255

size = width, height = 600, 600
speed = [30, 0]
frame = 0

screen = pygame.display.set_mode(size)
snake_rect = pygame.Rect(120, 120, 30, 30)

while frame < 100:
    print("Frame: {} | Left: {} | Right: {} | Top: {} | Bottom: {}".format(
        frame, snake_rect.left, snake_rect.right, snake_rect.top, snake_rect.bottom)
    )

    # display current frame
    screen.fill(COLOR_BLACK)
    pygame.draw.rect(screen, COLOR_WHITE, snake_rect)
    pygame.display.flip()

    # event listeners
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # move
    snake_rect = snake_rect.move(speed)
    if snake_rect.left <= 0 or snake_rect.right >= width:
        speed[0] = -speed[0]
    if snake_rect.top <= 0 or snake_rect.bottom >= height:
        speed[1] = -speed[1]

    # advance frame
    frame += 1
    sleep(0.5)

