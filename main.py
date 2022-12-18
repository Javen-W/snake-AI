import sys
from time import sleep
import pygame
import random
pygame.init()


class Fruit:
    coords = None

    def __init__(self):
        Fruit.coords = (snake.rect.left, snake.rect.top)
        while snake.on_fruit():
            Fruit.coords = (
                random.randint(0, (SCREEN_WIDTH / BLOCK_SIZE) - 1) * BLOCK_SIZE,
                random.randint(0, (SCREEN_HEIGHT / BLOCK_SIZE) - 1) * BLOCK_SIZE
            )

        self.rect = pygame.Rect(Fruit.coords, (BLOCK_SIZE, BLOCK_SIZE))
        self.color = (255, 0, 0)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def dist(self, x, y):
        return manhatten_distance(
            x, y,
            self.rect.left, self.rect.top
        )


def pick_random_direction():
    if snake.rect.left <= 0:
        return random.choice(['south-west', 'north-west', 'west'])
    if snake.rect.right >= SCREEN_WIDTH:
        return random.choice(['south-east', 'north-east', 'east'])
    if snake.rect.top <= 0:
        return random.choice(['south-west', 'south-east', 'south'])
    if snake.rect.bottom >= SCREEN_HEIGHT:
        return random.choice(['north-west', 'north-east', 'north'])
    return random.choice(['north', 'south', 'west', 'east'])


def manhatten_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Brain:
    def __init__(self):
        self.is_dumb = False

    def decide(self):
        # the 24 input nodes
        nn_inputs = []

        # best choice
        best_dir = pick_random_direction()
        best_score = 999999

        # get hypothetical distances
        for direction in VELOCITIES:
            test_rect = snake.rect.move(VELOCITIES[direction])

            # fruit
            fruit_dist = fruit.dist(test_rect.left, test_rect.top)
            nn_inputs.append(fruit_dist)

            # snake
            snake_dist = snake.min_dist(test_rect.left, test_rect.top)
            nn_inputs.append(snake_dist)

            # wall
            wall_dist = min(
                abs(0 - test_rect.left),
                abs(600 - test_rect.left),
                abs(0 - test_rect.top),
                abs(600 - test_rect.top),
            )
            nn_inputs.append(wall_dist)
            print(wall_dist)

            # temp
            if fruit_dist < best_score:
                best_score = fruit_dist
                best_dir = direction

        print(nn_inputs)
        return best_dir


class Snake:
    def __init__(self, start_coords, head_snake):
        self.rect = pygame.Rect(start_coords, (BLOCK_SIZE, BLOCK_SIZE))
        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        self.head_snake = head_snake
        self.tail_snake = None
        self.prev_dir = None  # TODO replace this with just prev_coords
        self.prev_coords = None

        if not head_snake:
            self.brain = Brain()

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

    def on_fruit(self):
        fruit_coords = (Fruit.coords[0], Fruit.coords[1])
        snake_coords = (self.rect.left, self.rect.top)
        if self.tail_snake:
            return snake_coords == fruit_coords or self.tail_snake.on_fruit()
        return snake_coords == fruit_coords

    def min_dist(self, x, y):
        my_dist = manhatten_distance(x, y, self.rect.left, self.rect.top)
        if self.tail_snake:
            return min(my_dist, self.tail_snake.min_dist(x, y))
        return my_dist


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
fruit = Fruit()
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
    fruit.draw()
    pygame.display.flip()

    # event listeners
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # move snake
    snake.move(direction=next_dir)

    # did the snake collide with itself?
    if snake.on_self() or snake.on_wall():
        print("Snake died.")
        is_alive = False
        # break

    # did the snake eat the fruit?
    if snake.on_fruit():
        snake.grow()
        fruit = Fruit()

    # decide next direction
    next_dir = snake.brain.decide()

    # advance frame
    frame += 1
    sleep(1/10)

