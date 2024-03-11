import pygame
import random
import sys
import time

from snake import Snake
from food import Food
from scoreboard import Scoreboard
from enemy_snake import EnemySnake
from events import PLAYER_EATS_FOOD

pygame.init()

# Define custom events
PLAYER_EATS_FOOD = pygame.USEREVENT + 1

# Define the game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SNAKE_SIZE = 10
FOOD_SIZE = 10

# Define the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load sounds
try:
    game_over_sound = pygame.mixer.Sound("game_over.wav")
    game_start_sound = pygame.mixer.Sound("game_start.wav")
    pellet_eat_sound = pygame.mixer.Sound("pellet_eat.wav")
except pygame.error as e:
    print("Error loading sound files:", e)
    sys.exit()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Play the game start sound
game_start_sound.play()

# Pause the game for a few seconds
time.sleep(2)

# Create the snake, food, and scoreboard
snake = Snake()
food = Food(RED, FOOD_SIZE, FOOD_SIZE)
scoreboard = Scoreboard(snake)

# Create a clock object
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    screen.fill(BLACK)

    enemy_snakes = []  # Define the enemy_snakes list

    # Handle the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.up()
            elif event.key == pygame.K_DOWN:
                snake.down()
            elif event.key == pygame.K_LEFT:
                snake.left()
            elif event.key == pygame.K_RIGHT:
                snake.right()

        elif event.type == PLAYER_EATS_FOOD:
            scoreboard.handle_event(event)  # Handle the event in the scoreboard
            print("Player eats food")

    # Spawn a new enemy snake with a 10% chance
    if random.randint(1, 100) <= 10:
        color = (255, 0, 0)  # Red color
        speed = random.randint(1, 3)
        behavior = random.choice(["chase_player", "chase_food", "random", "chase_enemy"])

        enemy_snake = EnemySnake(color, speed, snake, behavior)
        enemy_snakes.append(enemy_snake)

    # Draw the game elements
    snake.draw(screen)
    food.draw(screen)
    for enemy_snake in enemy_snakes:
        enemy_snake.draw(screen)

    # Move the enemy snakes
    for enemy_snake in enemy_snakes:
        enemy_snake.move(food, enemy_snakes)

    # Update the snake and food
    snake.update(SCREEN_WIDTH, SCREEN_HEIGHT, food)
    if food.update(snake):
        scoreboard.score.increase()
        pellet_eat_sound.play()

    scoreboard.draw_scoreboard(screen)  # Draw the scoreboard

    # Update the display
    pygame.display.flip()

    # Check for collisions
    if snake.head.rect.left < 0 or snake.head.rect.right > SCREEN_WIDTH or \
            snake.head.rect.top < 0 or snake.head.rect.bottom > SCREEN_HEIGHT:
        running = False
        game_over_sound.play()

    # Check for collisions with the enemy snakes
    flat_segments = list(snake.segments.sprites())[1:]
    if pygame.sprite.spritecollide(snake.head, pygame.sprite.Group(*flat_segments), False):
        running = False
        game_over_sound.play()

    clock.tick(10)

# Game over
pygame.quit()
sys.exit()