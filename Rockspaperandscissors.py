import pygame
import random
import sys

# Инициализация
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Камень, Ножницы, Бумага")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Переменные игры
choices = ['Камень', 'Бумага', 'Ножницы']
player_choice = None
computer_choice = None
result = "Сделайте свой выбор!"
game_active = True

# Кнопки
rock_btn = pygame.Rect(50, 150, 150, 50)
paper_btn = pygame.Rect(225, 150, 150, 50)
scissors_btn = pygame.Rect(400, 150, 150, 50)

def draw_text(text, x, y):
    rendered = font.render(text, True, BLACK)
    screen.blit(rendered, (x, y))

def determine_winner(player, computer):
    if player == computer:
        return "Ничья!"
    elif (player == 'Камень' and computer == 'Ножницы') or \
         (player == 'Бумага' and computer == 'Камень') or \
         (player == 'Ножницы' and computer == 'Бумага'):
        return "Вы выиграли!"
    else:
        return "Вы проиграли!"

# Основной цикл
running = True
while running:
    screen.fill(WHITE)
    draw_text("Камень Ножницы Бумага!", 180, 30)
    draw_text("Выберите свой ход:", 200, 80)

    # Рисуем кнопки
    pygame.draw.rect(screen, GRAY, rock_btn)
    pygame.draw.rect(screen, GRAY, paper_btn)
    pygame.draw.rect(screen, GRAY, scissors_btn)
    draw_text("Камень (R)", rock_btn.x + 20, rock_btn.y + 10)
    draw_text("Бумага (P)", paper_btn.x + 20, paper_btn.y + 10)
    draw_text("Ножницы (S)", scissors_btn.x + 10, scissors_btn.y + 10)

    # Показываем выборы и результат
    if player_choice and computer_choice:
        draw_text(f"Вы выбрали: {player_choice}", 50, 250)
        draw_text(f"Компьютер выбрал: {computer_choice}", 300, 250)
        draw_text(result, 200, 300)
        draw_text("Нажмите ПРОБЕЛ, чтобы сыграть снова", 120, 340)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_active:
                if event.key == pygame.K_r:
                    player_choice = 'Камень'
                elif event.key == pygame.K_p:
                    player_choice = 'Бумага'
                elif event.key == pygame.K_s:
                    player_choice = 'Ножницы'
                else:
                    continue
                computer_choice = random.choice(choices)
                result = determine_winner(player_choice, computer_choice)
                game_active = False
            elif event.key == pygame.K_SPACE:
                player_choice = None
                computer_choice = None
                result = "Сделайте свой выбор!"
                game_active = True

        elif event.type == pygame.MOUSEBUTTONDOWN and game_active:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if rock_btn.collidepoint(mouse_pos):
                    player_choice = 'Камень'
                elif paper_btn.collidepoint(mouse_pos):
                    player_choice = 'Бумага'
                elif scissors_btn.collidepoint(mouse_pos):
                    player_choice = 'Ножницы'
                else:
                    continue
                computer_choice = random.choice(choices)
                result = determine_winner(player_choice, computer_choice)
                game_active = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()