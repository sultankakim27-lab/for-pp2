"""
Practice 11 - Snake (FINAL VERSION)

Features:
- Walls & levels
- Food with different weights (1–3)
- Food disappears after time
- Speed increases with level
- Clean comments for submission
"""

import pygame
import random
import sys

pygame.init()

# --- SETTINGS ---
CELL_SIZE = 20
COLUMNS = 30
ROWS = 30
HUD_HEIGHT = 60

WIDTH = CELL_SIZE * COLUMNS
HEIGHT = CELL_SIZE * ROWS + HUD_HEIGHT

# --- COLORS ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
GRAY = (70, 70, 70)
YELLOW = (255, 220, 0)

# --- DISPLAY ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 11")
clock = pygame.time.Clock()

# --- FONTS ---
font = pygame.font.SysFont("Verdana", 22)
game_over_font = pygame.font.SysFont("Verdana", 48)

# --- SNAKE ---
snake = [(10, 10), (9, 10), (8, 10)]
direction = (1, 0)
next_direction = (1, 0)

# --- GAME STATE ---
score = 0
level = 1
base_speed = 8

# --- FOOD ---
food = None


# --- WALLS ---
def get_walls(level):
    """Create border and level-based walls."""
    walls = set()

    # Borders
    for x in range(COLUMNS):
        walls.add((x, 0))
        walls.add((x, ROWS - 1))

    for y in range(ROWS):
        walls.add((0, y))
        walls.add((COLUMNS - 1, y))

    # Level obstacles
    if level >= 2:
        for y in range(6, 24):
            walls.add((15, y))

    if level >= 3:
        for x in range(7, 23):
            walls.add((x, 15))

    if level >= 4:
        for y in range(5, 11):
            walls.add((7, y))
            walls.add((22, y))
        for y in range(19, 25):
            walls.add((7, y))
            walls.add((22, y))

    return walls


# --- FOOD ---
def generate_food():
    """Generate food object with position, weight, and timer."""
    walls = get_walls(level)

    free = []
    for x in range(1, COLUMNS - 1):
        for y in range(1, ROWS - 1):
            pos = (x, y)
            if pos not in walls and pos not in snake:
                free.append(pos)

    return {
        "pos": random.choice(free),
        "weight": random.choice([1, 2, 3]),
        "timer": random.randint(80, 150)
    }


# --- DRAW ---
def draw_cell(pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + HUD_HEIGHT, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


def draw():
    screen.fill(BLACK)

    # HUD
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HUD_HEIGHT))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 15))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (150, 15))
    screen.blit(font.render(f"Speed: {base_speed + level}", True, WHITE), (280, 15))

    # Walls
    for wall in get_walls(level):
        draw_cell(wall, GRAY)

    # Food color depends on weight
    if food["weight"] == 1:
        color = YELLOW
    elif food["weight"] == 2:
        color = (255, 100, 0)
    else:
        color = (255, 0, 255)

    draw_cell(food["pos"], color)

    # Snake
    for i, part in enumerate(snake):
        color = GREEN if i == 0 else DARK_GREEN
        draw_cell(part, color)


# --- LOGIC ---
def change_level():
    """Level increases every 5 score."""
    global level
    level = 1 + score // 5


def handle_keys(key):
    global next_direction

    if key == pygame.K_UP and direction != (0, 1):
        next_direction = (0, -1)
    elif key == pygame.K_DOWN and direction != (0, -1):
        next_direction = (0, 1)
    elif key == pygame.K_LEFT and direction != (1, 0):
        next_direction = (-1, 0)
    elif key == pygame.K_RIGHT and direction != (-1, 0):
        next_direction = (1, 0)


def move():
    global direction, score, food

    direction = next_direction
    head = snake[0]

    new_head = (head[0] + direction[0], head[1] + direction[1])

    # Collision
    if new_head in snake or new_head in get_walls(level):
        return False

    snake.insert(0, new_head)

    # Eat food
    if new_head == food["pos"]:
        score += food["weight"]
        change_level()
        food = generate_food()
    else:
        snake.pop()

    return True


def game_over():
    screen.fill(BLACK)
    text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 40))
    pygame.display.flip()
    pygame.time.wait(2000)


# --- INIT ---
food = generate_food()

# --- MAIN LOOP ---
running = True
alive = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                handle_keys(event.key)

    if alive:
        alive = move()

        # Food timer
        food["timer"] -= 1
        if food["timer"] <= 0:
            food = generate_food()

        draw()
        pygame.display.flip()

        clock.tick(base_speed + level)

    else:
        game_over()
        running = False

pygame.quit()
sys.exit()