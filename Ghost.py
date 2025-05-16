import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Поймай Призрака!")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# Шрифты
font = pygame.font.SysFont("arial", 32)
big_font = pygame.font.SysFont("arial", 48)

# Загрузка изображения призрака
ghost_image = pygame.Surface((60, 60), pygame.SRCALPHA)
pygame.draw.circle(ghost_image, (200, 200, 255), (30, 30), 30)

# Переменные игры
score = 0
time_limit = 30_000  # 30 секунд
start_time = pygame.time.get_ticks()
ghost_timer = 0
ghost_lifetime = 7000   # мс
ghost_spawn_delay = random.randint(1000, 2000)

ghost_rect = ghost_image.get_rect(center=(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100)))
ghost_visible = True

def draw_text(text, x, y, font, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def reset_game():
    global score, start_time, ghost_spawn_delay, ghost_visible
    score = 0
    start_time = pygame.time.get_ticks()
    ghost_spawn_delay = random.randint(1000, 2000)
    ghost_visible = True

# Главный цикл игры
running = True
game_over = False

while running:
    screen.fill(WHITE)
    current_time = pygame.time.get_ticks()
    elapsed = current_time - start_time
    time_left = max(0, (time_limit - elapsed) // 1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and ghost_visible:
                if ghost_rect.collidepoint(event.pos):
                    score += 1
                    ghost_visible = False
                    ghost_timer = current_time
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
                game_over = False

    # Отображение призрака
    if not game_over:
        if ghost_visible:
            screen.blit(ghost_image, ghost_rect)
            if current_time - ghost_timer > ghost_lifetime:
                ghost_visible = False
                ghost_timer = current_time
        else:
            if current_time - ghost_timer > ghost_spawn_delay:
                ghost_rect.center = (random.randint(60, WIDTH - 60), random.randint(60, HEIGHT - 60))
                ghost_visible = True
                ghost_spawn_delay = random.randint(1000, 2000)

        draw_text(f"Счёт: {score}", 10, 10, font)
        draw_text(f"Время: {time_left}", WIDTH - 150, 10, font)
        draw_text("Кликай по призраку, пока не закончится время!", 200, HEIGHT - 40, font)

        if elapsed >= time_limit:
            game_over = True

    else:
        draw_text(f"Время вышло! Ваш счёт: {score}", 200, 200, big_font, RED)
        draw_text("Нажмите ПРОБЕЛ, чтобы начать заново", 180, 280, font)

    pygame.display.flip()
    clock.tick(60)
