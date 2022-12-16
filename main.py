import sys
from time import sleep
import pygame
import random
pygame.init()


class Snake:
    def __init__(self, start_coords, head_snake):
        self.rect = pygame.Rect(start_coords, (BLOCK_SIZE, BLOCK_SIZE))
        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        self.head_snake = head_snake
        self.tail_snake = None
        self.prev_dir = None  # TODO replace this with just prev_coords
        self.prev_coords = None

    def grow(self):
        if self.tail_snake:
            # this is not the last snake; relay to next tail snake
            self.tail_snake.grow()
        else:
            # this is the last snake
            self.tail_snake = Snake(start_coords=self.prev_coords, head_snake=self)

    def move(self, direction):
        if direction:
            self.prev_coords = (self.rect.left, self.rect.top)
            self.rect = self.rect.move(VELOCITIES[direction])
            if self.tail_snake:
                self.tail_snake.move(self.prev_dir)
            self.prev_dir = direction

    def print(self):
        text = "<>~"
        if self.tail_snake:
            text += self.tail_snake.print()
        if not self.head_snake:
            text = "~8~" + text
            print(text)
        return text

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.tail_snake:
            self.tail_snake.draw()

    def size(self):
        if self.tail_snake:
            return 1 + self.tail_snake.size()
        return 1

    def on_self(self, head_coords=None):
        if not head_coords:
            head_coords = (self.rect.left, self.rect.top)
        if self.tail_snake:
            tail_coords = (self.tail_snake.rect.left, self.tail_snake.rect.top)
            return (head_coords == tail_coords) or self.tail_snake.on_self(head_coords=head_coords)
        return False

    def on_wall(self):
        return self.rect.left < 0 or \
            self.rect.right > SCREEN_WIDTH or \
            self.rect.top < 0 or \
            self.rect.bottom > SCREEN_HEIGHT


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
screen = pygame.display.set_mode(SCREEN_SIZE)
snake = Snake(start_coords=START_COORDS, head_snake=None)
is_alive = True
next_dir = 'south-west'

# play
while frame < 1000:
    snake.print()
    print("Frame: {} | Size: {} | On-self: {} | Next direction: {} | Coords: ({}, {}, {}, {})".format(
        frame, snake.size(), snake.on_self(), next_dir, snake.rect.left, snake.rect.right, snake.rect.top, snake.rect.bottom)
    )

    # draw & display current frame
    screen.fill(COLOR_BLACK)
    snake.draw()
    pygame.display.flip()

    # event listeners
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # move snake
    snake.move(direction=next_dir)

    # did the snake collide with itself?
    if snake.on_self() or snake.on_wall():
        is_alive = False
        break

    # eat & grow
    if frame % 10 == 0:
        snake.grow()

    # decide next direction
    if snake.rect.left <= 0:
        next_dir = random.choice(['south-west', 'north-west', 'west'])
    if snake.rect.right >= SCREEN_WIDTH:
        next_dir = random.choice(['south-east', 'north-east', 'east'])
    if snake.rect.top <= 0:
        next_dir = random.choice(['south-west', 'south-east', 'south'])
    if snake.rect.bottom >= SCREEN_HEIGHT:
        next_dir = random.choice(['north-west', 'north-east', 'north'])

    # advance frame
    frame += 1
    sleep(1/10)

