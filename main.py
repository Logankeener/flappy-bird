import pygame

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.score import Score

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))

pygame.display.set_caption("Flappy Bird Game v1.0.2")

img = pygame.image.load('assets/icons/red_bird.png')
pygame.display.set_icon(img)


clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False

assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()


def create_sprites():
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)

    return Bird(sprites), GameStartMessage(sprites), Score(sprites)


bird, game_start_message, score = create_sprites()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                gamestarted = True
                game_start_message.kill()
                pygame.time.set_timer(column_create_event, 1500)
            if event.key == pygame.K_ESCAPE and gameover:
                gameover = False
                gamestarted = False
                sprites.empty()
                bird, game_start_message, score = create_sprites()

        if not gameover:
            bird.handle_event(event)

    screen.fill(0)

    sprites.draw(screen)

    if gamestarted and not gameover:
        sprites.update()

    if bird.check_collision(sprites) and not gameover:
        gameover = True
        gamestarted = False
        GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, 0)
        assets.play_audio("hit")

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            assets.play_audio("point")

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit() import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 500, 800
FPS = 60
GRAVITY = 0.25
BIRD_JUMP = 7
PIPE_GAP = 200
PIPE_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PIPE_SPAWN_EVENT, 1500)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Load images
bg_img = pygame.image.load("assets/sprites/background.png").convert_alpha()
bird_img = pygame.image.load("assets/sprites/bird.png").convert_alpha()
pipe_img = pygame.image.load("assets/sprites/pipe.png").convert_alpha()
message_img = pygame.image.load("assets/sprites/message.png").convert_alpha()
shop_img = pygame.image.load("assets/sprites/shop.png").convert_alpha()

# Game variables
score = 0
game_over = False
game_started = False
shop_opened = False
coins = 0

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Game fonts
font = pygame.font.Font(None, 40)

# Game objects
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_img
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.vel_y = 0

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def jump(self):
        self.vel_y = -BIRD_JUMP

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted=False):
        super().__init__()
        self.image = pygame.transform.flip(pipe_img, False, inverted)
        self.rect = self.image.get_rect()
        if inverted:
            self.rect.y = -self.rect.height
        else:
            self.rect.y = HEIGHT - PIPE_GAP
        self.rect.x = WIDTH + 10

    def update(self):
        self.rect.x -= 3

# Groups
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Functions
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def show_menu():
    screen.blit(message_img, (WIDTH // 2 - message_img.get_width() // 2, HEIGHT // 3))
    draw_text("Press SPACE to Start", font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)

def show_shop():
    screen.blit(shop_img, (WIDTH // 2 - shop_img.get_width() // 2, HEIGHT // 3))
    draw_text(f"Coins: {coins}", font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)

# Game loop
running = True
clock = pygame.time.Clock()
bird = Bird()
all_sprites.add(bird)

while running:
    clock.tick(FPS)
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_started:
                game_started = True
            elif event.key == pygame.K_SPACE and not game_over:
                bird.jump()
            elif event.key == pygame.K_s:
                shop_opened = True
        elif event.type == PIPE_SPAWN_EVENT:
            pipe_bottom = Pipe()
            pipe_top = Pipe(inverted=True)
            all_sprites.add(pipe_bottom, pipe_top)
            pipes.add(pipe_bottom, pipe_top)

    if game_started:
        all_sprites.update()

        # Check collisions
        hits = pygame.sprite.spritecollide(bird, pipes, False)
        if hits or bird.rect.bottom >= HEIGHT:
            game_over = True

        # Remove off-screen pipes
        for pipe in pipes:
            if pipe.rect.right <= 0:
                pipes.remove(pipe)
                all_sprites.remove(pipe)
                if not game_over:
                    score += 1

        # Draw sprites
        all_sprites.draw(screen)

        # Draw score
        draw_text(f"Score: {score}", font, WHITE, WIDTH // 2, 50)

    else:
        if not shop_opened:
            show_menu()
        else:
            show_shop()

    pygame.display.flip()

pygame.quit()
