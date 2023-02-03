import sys
import numpy as np
import pygame
import random

# Initialize the game
pygame.init()

# Set up the window
block_size = 30
width = height = 20 * block_size
map_blocks = (width * height) / block_size
window = pygame.display.set_mode((width, height))

# Set up the clock
clock = pygame.time.Clock()

# Define colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Q-Learning parameters
state_space = map_blocks * map_blocks  # possible states: head position, fruit position, body positions
action_space = 4  # left, right, up, down
alpha = 0.1  # learning rate
gamma = 0.9  # discount factor
epsilon = 0.1  # exploration rate
max_iterations = 1000  # max number of moves?
q_table = np.zeros((state_space, action_space))  # state-action table


def get_current_state(snake, fruit):
    # Get the current position of the snake's head
    head_x, head_y = snake.x, snake.y

    # Get the position of the fruit
    fruit_x, fruit_y = fruit.x, fruit.y

    # Get the positions of the rest of the snake body
    body_positions = snake.body[1:]

    # Convert the head, fruit, and body positions to state indices
    head_state = head_x // block_size + head_y // block_size * 20
    fruit_state = fruit_x // block_size + fruit_y // block_size * 20
    body_states = [pos[0] // block_size + pos[1] // block_size * 20 for pos in body_positions]

    # Concatenate the head, fruit, and body state indices to form the current state
    state = (head_state, fruit_state, tuple(body_states))

    return state


# Define the Snake class
class Snake:
    def __init__(self):
        self.x = 5 * block_size
        self.y = 5 * block_size
        self.velocity = block_size
        self.direction = "right"
        self.body = [(self.x, self.y)]
        self.is_alive = True
        self.size = 1
        self.score = 0

    def move(self):
        if self.direction == "right":
            self.x += self.velocity
        elif self.direction == "left":
            self.x -= self.velocity
        elif self.direction == "up":
            self.y -= self.velocity
        elif self.direction == "down":
            self.y += self.velocity

        if self.x >= width or self.x < 0 or self.y >= height or self.y < 0:
            # Snake died because it went out of bounds
            self.is_alive = False
            return

        if (self.x, self.y) in self.body[:-1]:
            # Snake died because it collided with itself
            self.is_alive = False
            return

        self.body.insert(0, (self.x, self.y))
        if len(self.body) > self.size:
            self.body.pop()

    def draw(self, window):
        for segment in self.body:
            pygame.draw.rect(window, green, (segment[0], segment[1], block_size, block_size))


# define the food class
class Food:
    def __init__(self, snake):
        self.snake = snake
        self.generate_food()

    def generate_food(self):
        while True:
            self.x = random.randint(0, width - block_size) // block_size * block_size
            self.y = random.randint(0, height - block_size) // block_size * block_size
            if (self.x, self.y) not in self.snake.body:
                break

    def draw(self, window):
        pygame.draw.rect(window, red, (self.x, self.y, block_size, block_size))


# Create the snake and food objects
snake = Snake()
food = Food(snake=snake)

# Main game loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # key events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake.direction = "left"
    if keys[pygame.K_RIGHT]:
        snake.direction = "right"
    if keys[pygame.K_UP]:
        snake.direction = "up"
    if keys[pygame.K_DOWN]:
        snake.direction = "down"

    # end the game if the snake died
    if not snake.is_alive:
        break

    # check for collision with food
    if snake.x == food.x and snake.y == food.y:
        snake.size += 1
        snake.score = snake.size
        food = Food(snake=snake)

    # draw
    window.fill(black)
    food.draw(window)
    snake.move()
    snake.draw(window)
    font = pygame.font.Font(None, 30)
    score_text = font.render("Score: " + str(snake.score), True, white)
    window.blit(score_text, (0, 0))
    pygame.display.update()
    clock.tick(10)

# End the game if the snake is not alive
print("You lost!")
pygame.quit()
sys.exit()
