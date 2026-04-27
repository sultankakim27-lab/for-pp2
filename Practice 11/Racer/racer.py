# Imports
import os
import random
import sys
import time

import pygame
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

# Enemy speed is separate so we can increase it by coins
ENEMY_SPEED = 5

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYER_IMAGE = os.path.join(BASE_DIR, "Player.png")
ENEMY_IMAGE = os.path.join(BASE_DIR, "Enemy.png")
COIN_IMAGE = os.path.join(BASE_DIR, "Coin.png")
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "AnimatedStreet.png")
CRASH_SOUND = os.path.join(BASE_DIR, "crash.wav")

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(BACKGROUND_IMAGE)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer")


class Enemy(pygame.sprite.Sprite):
    """Enemy car that moves downward. Speed increases when player collects coins."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(ENEMY_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(70, SCREEN_WIDTH - 70), 0)

    def move(self):
        global SCORE
        # Move downward using the separate ENEMY_SPEED variable
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(70, SCREEN_WIDTH - 70), 0)


class Player(pygame.sprite.Sprite):
    """Player car controlled with left and right arrow keys."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(PLAYER_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 45:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH - 45:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    """
    Coin with a random weight/type:
      - Bronze: common,  worth 1 point  (green circle)
      - Silver: uncommon, worth 2 points (silver circle)
      - Gold:   rare,    worth 3 points  (gold circle)
    Weight is chosen randomly when the coin spawns.
    """

    # Coin types: (label, color, value, spawn_weight)
    # spawn_weight controls how likely this type is to appear
    TYPES = [
        ("Bronze", BRONZE, 1, 60),   # 60% chance
        ("Silver", SILVER, 2, 30),   # 30% chance
        ("Gold",   GOLD,   3, 10),   # 10% chance
    ]

    def __init__(self):
        super().__init__()

        # Pick a coin type based on spawn weights
        labels   = [t[0] for t in self.TYPES]
        colors   = [t[1] for t in self.TYPES]
        values   = [t[2] for t in self.TYPES]
        weights  = [t[3] for t in self.TYPES]

        chosen = random.choices(range(len(self.TYPES)), weights=weights, k=1)[0]
        self.coin_value = values[chosen]
        self.coin_color = colors[chosen]
        self.coin_label = labels[chosen]

        # Draw the coin as a colored circle on a surface
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.coin_color, (15, 15), 15)

        # Draw the first letter of the type in the center
        label_surf = font_small.render(self.coin_label[0], True, BLACK)
        self.image.blit(label_surf, (15 - label_surf.get_width() // 2,
                                     15 - label_surf.get_height() // 2))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(65, SCREEN_WIDTH - 65), -20)

    def move(self):
        """Move coin downward; remove it when it leaves the screen."""
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# --- Sprites & groups ---
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# --- Timer events ---
INC_SPEED  = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2

pygame.time.set_timer(INC_SPEED,  1000)   # road speed up every second
pygame.time.set_timer(SPAWN_COIN,  900)   # try to spawn a coin every 0.9 s


def spawn_coin():
    """Randomly spawn a coin if there are fewer than 3 on screen."""
    if random.randint(1, 100) <= 45 and len(coins) < 3:
        coin = Coin()
        coins.add(coin)
        all_sprites.add(coin)


def update_enemy_speed():
    """
    Increase enemy speed every 5 coins collected.
    Each milestone adds +1 to ENEMY_SPEED.
    """
    global ENEMY_SPEED
    # milestone = how many times we've hit a multiple of 5
    milestone = COINS_COLLECTED // 5
    ENEMY_SPEED = 5 + milestone


def draw_hud():
    """Draw score, coins collected, and current enemy speed on screen."""
    score_text  = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text   = font_small.render(f"Coins: {COINS_COLLECTED}", True, GOLD)
    speed_text  = font_small.render(f"Enemy spd: {ENEMY_SPEED}", True, RED)

    DISPLAYSURF.blit(score_text,  (10, 10))
    DISPLAYSURF.blit(speed_text,  (10, 35))

    coin_rect = coin_text.get_rect()
    coin_rect.topright = (SCREEN_WIDTH - 10, 10)
    DISPLAYSURF.blit(coin_text, coin_rect)


# --- Game loop ---
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            # Increase background/road scroll speed every second
            SPEED += 0.5

        if event.type == SPAWN_COIN:
            spawn_coin()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    draw_hud()

    # Move and draw all sprites
    for entity in list(all_sprites):
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Coin collection — add the value of each collected coin
    collected = pygame.sprite.spritecollide(P1, coins, True)
    if collected:
        for coin in collected:
            COINS_COLLECTED += coin.coin_value
        # After collecting, check if enemy should speed up
        update_enemy_speed()

    # Collision with enemy → game over
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound(CRASH_SOUND).play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 220))

        final_score = font_small.render(f"Final score: {SCORE}", True, BLACK)
        final_coins = font_small.render(f"Collected coins: {COINS_COLLECTED}", True, BLACK)
        DISPLAYSURF.blit(final_score, (120, 320))
        DISPLAYSURF.blit(final_coins, (95, 350))

        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)