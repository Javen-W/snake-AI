import math
import sys
from time import sleep
import numpy.random
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


def manhatten_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Brain:
    def __init__(self, n_input: int, n_hidden: int, n_output: int):
        self.w_input_hidden = numpy.random.uniform(low=-1.0, high=1.0, size=(n_hidden, n_input + 1))
        self.w_hidden_hidden = numpy.random.uniform(low=-1.0, high=1.0, size=(n_hidden, n_hidden + 1))
        self.w_hidden_output = numpy.random.uniform(low=-1.0, high=1.0, size=(n_output, n_hidden + 1))

    @staticmethod
    def sigmoid(x: float):
        return 1 / (1 + pow(math.e, -x))

    @staticmethod
    def activate(n):
        return [[Brain.sigmoid(col) for col in row] for row in n]

    def nn_process(self, v_input):
        # add bias to and transpose input vector
        v_input.append(1)
        v_input = numpy.transpose(numpy.atleast_2d(v_input))

        # results of layer-1 weights and input vector
        v_input_hidden = self.w_input_hidden.dot(v_input)
        v_input_hidden = self.activate(v_input_hidden)
        v_input_hidden.append([1])

        # results of layer-2 weights and layer-1 output
        v_hidden_hidden = self.w_hidden_hidden.dot(v_input_hidden)
        v_hidden_hidden = self.activate(v_hidden_hidden)
        v_hidden_hidden.append([1])

        # results of layer-3 weights and layer-2 output
        v_hidden_output = self.w_hidden_output.dot(v_hidden_hidden)
        v_hidden_output = self.activate(v_hidden_output)

        return v_hidden_output

    def decide(self):
        # the 24 input nodes
        nn_inputs = []

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

        nn_output = self.nn_process(nn_inputs)
        highest_node = nn_output.index(max([row[0] for row in nn_output]))
        if highest_node == 0:
            return 'west'
        elif highest_node == 1:
            return 'east'
        elif highest_node == 2:
            return 'north'
        elif highest_node == 3:
            return 'south'


class Snake:
    def __init__(self, start_coords, head_snake=None, color=None, brain=None):
        self.rect = pygame.Rect(start_coords, (BLOCK_SIZE, BLOCK_SIZE))
        self.head_snake = head_snake
        self.brain = brain
        self.color = color
        
        self.tail_snake = None
        self.prev_dir = None  # TODO replace this with just prev_coords
        self.prev_coords = None
        self.time_lived = 0
        self.tol = 200

        if not color:
            self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        if not head_snake and not brain:
            self.brain = Brain(n_input=24, n_hidden=18, n_output=4)

    def grow(self):
        if self.tail_snake:
            # this is not the last snake; relay to next tail snake
            self.tail_snake.grow()
        else:
            # this is the last snake
            self.tail_snake = Snake(start_coords=self.prev_coords, head_snake=self, color=self.color, brain=None)

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

    def fitness(self):
        return self.size()

    def breed(self, partner_snake):
        return self


# constants
COLOR_BLACK = 0, 0, 0
COLOR_WHITE = 255, 255, 255
BLOCK_SIZE = 30
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
START_COORDS = (BLOCK_SIZE * 6, BLOCK_SIZE * 5)
POPULATION_SIZE = 100
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
generation = 0
screen = pygame.display.set_mode(SCREEN_SIZE)
snakes = [Snake(start_coords=START_COORDS, head_snake=None) for i in range(POPULATION_SIZE)]  # initial snake gen

# play
while generation < 100:
    # new generation
    generation += 1
    print("Generation: {}".format(generation))

    # natural selection of the snakes - test their survival
    for snake in snakes:
        # event listeners
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        fruit = Fruit()
        while snake.tol > 0:
            # draw & display current frame
            screen.fill(COLOR_BLACK)
            snake.draw()
            fruit.draw()
            pygame.display.flip()

            # move snake
            snake.move(direction=snake.brain.decide())

            # did the snake collide with itself?
            if snake.on_self() or snake.on_wall():
                is_alive = False
                break

            # did the snake eat the fruit?
            if snake.on_fruit():
                snake.grow()
                fruit = Fruit()
                snake.tol = 200

            # advance frame
            snake.time_lived += 1
            snake.tol -= 1
            sleep(1/10)

    # breed the most fit snakes
    fittest_snakes = sorted({snake: snake.fitness() for snake in snakes}.items(), key=lambda kv: kv[1])[0:POPULATION_SIZE * 0.20]
    alpha_snake = fittest_snakes[0][0]
    snakes = [alpha_snake.breed(random.choice(fittest_snakes)[0]) for i in range(POPULATION_SIZE)]
    print("The alpha snake of gen {}: fitness={}, size={}, color={}".format(
        generation, alpha_snake.fitness(), alpha_snake.size(), alpha_snake.color
    ))
