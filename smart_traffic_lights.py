import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
ROAD_WIDTH = 300
INTERSECTION_SIZE = 50
CAR_SIZE = 20
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Traffic Lights")
clock = pygame.time.Clock()

# Состояние светофоров
traffic_light_ns = "green"  # север-юг
traffic_light_ew = "red"    # восток-запад

# Машины
cars = []
passed_cars = 0
spawn_timer = 0
auto_mode = False
switch_timer = 0

def draw_intersection():
    """Отрисовка перекрестка и дорог"""
    screen.fill(GRAY)
    
    # Вертикальная дорога (север-юг)
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 - ROAD_WIDTH // 2, 0, ROAD_WIDTH, HEIGHT))
    
    # Горизонтальная дорога (восток-запад)
    pygame.draw.rect(screen, BLACK, (0, HEIGHT // 2 - ROAD_WIDTH // 2, WIDTH, ROAD_WIDTH))
    
    # Разметка перекрестка
    pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - INTERSECTION_SIZE // 2, HEIGHT // 2 - INTERSECTION_SIZE // 2, INTERSECTION_SIZE, INTERSECTION_SIZE))

def draw_traffic_lights():
    """Отрисовка светофоров"""
    # Северный светофор
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 - 20, HEIGHT // 2 - ROAD_WIDTH // 2 + 20, 40, 80))
    pygame.draw.circle(screen, RED if traffic_light_ns == "red" else BLACK, (WIDTH // 2, HEIGHT // 2 - ROAD_WIDTH // 2 + 40), 15)
    pygame.draw.circle(screen, GREEN if traffic_light_ns == "green" else BLACK, (WIDTH // 2, HEIGHT // 2 - ROAD_WIDTH // 2 + 70), 15)
    
    # Южный светофор
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 - 20, HEIGHT // 2 + ROAD_WIDTH // 2 - 100, 40, 80))
    pygame.draw.circle(screen, RED if traffic_light_ns == "red" else BLACK, (WIDTH // 2, HEIGHT // 2 + ROAD_WIDTH // 2 - 80), 15)
    pygame.draw.circle(screen, GREEN if traffic_light_ns == "green" else BLACK, (WIDTH // 2, HEIGHT // 2 + ROAD_WIDTH // 2 - 50), 15)
    
    # Западный светофор
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 - ROAD_WIDTH // 2 + 20, HEIGHT // 2 - 20, 80, 40))
    pygame.draw.circle(screen, RED if traffic_light_ew == "red" else BLACK, (WIDTH // 2 - ROAD_WIDTH // 2 + 40, HEIGHT // 2), 15)
    pygame.draw.circle(screen, GREEN if traffic_light_ew == "green" else BLACK, (WIDTH // 2 - ROAD_WIDTH // 2 + 70, HEIGHT // 2), 15)
    
    # Восточный светофор
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 + ROAD_WIDTH // 2 - 100, HEIGHT // 2 - 20, 80, 40))
    pygame.draw.circle(screen, RED if traffic_light_ew == "red" else BLACK, (WIDTH // 2 + ROAD_WIDTH // 2 - 80, HEIGHT // 2), 15)
    pygame.draw.circle(screen, GREEN if traffic_light_ew == "green" else BLACK, (WIDTH // 2 + ROAD_WIDTH // 2 - 50, HEIGHT // 2), 15)

def spawn_car():
    """Создание новой машины на одной из 4 сторон"""
    side = random.randint(0, 3)
    
    if side == 0:  # север (движется на юг)
        return [WIDTH // 2 + random.randint(-ROAD_WIDTH // 2 + CAR_SIZE, ROAD_WIDTH // 2 - CAR_SIZE), 0, 0, 2]
    elif side == 1:  # юг (движется на север)
        return [WIDTH // 2 + random.randint(-ROAD_WIDTH // 2 + CAR_SIZE, ROAD_WIDTH // 2 - CAR_SIZE), HEIGHT, 0, -2]
    elif side == 2:  # запад (движется на восток)
        return [0, HEIGHT // 2 + random.randint(-ROAD_WIDTH // 2 + CAR_SIZE, ROAD_WIDTH // 2 - CAR_SIZE), 2, 0]
    else:  # восток (движется на запад)
        return [WIDTH, HEIGHT // 2 + random.randint(-ROAD_WIDTH // 2 + CAR_SIZE, ROAD_WIDTH // 2 - CAR_SIZE), -2, 0]

def update_cars():
    """Обновление позиций машин"""
    global passed_cars
    
    for car in cars[:]:
        car[0] += car[2]
        car[1] += car[3]
        
        # Проверка на выезд за границы экрана
        if (car[0] < -CAR_SIZE or car[0] > WIDTH + CAR_SIZE or 
            car[1] < -CAR_SIZE or car[1] > HEIGHT + CAR_SIZE):
            cars.remove(car)
            passed_cars += 1
            continue
            
        # Проверка светофора для машин, движущихся север-юг
        if car[3] != 0:  # движется по вертикали
            if traffic_light_ns == "red":
                # Остановка перед перекрестком
                if (HEIGHT // 2 - INTERSECTION_SIZE // 2 - CAR_SIZE < car[1] < HEIGHT // 2 + INTERSECTION_SIZE // 2 + CAR_SIZE):
                    car[1] -= car[3]
        
        # Проверка светофора для машин, движущихся восток-запад
        elif car[2] != 0:  # движется по горизонтали
            if traffic_light_ew == "red":
                # Остановка перед перекрестком
                if (WIDTH // 2 - INTERSECTION_SIZE // 2 - CAR_SIZE < car[0] < WIDTH // 2 + INTERSECTION_SIZE // 2 + CAR_SIZE):
                    car[0] -= car[2]

def draw_cars():
    """Отрисовка всех машин"""
    for car in cars:
        pygame.draw.rect(screen, WHITE, (car[0] - CAR_SIZE // 2, car[1] - CAR_SIZE // 2, CAR_SIZE, CAR_SIZE))

def toggle_lights():
    """Переключение светофоров"""
    global traffic_light_ns, traffic_light_ew
    if traffic_light_ns == "green":
        traffic_light_ns = "red"
        traffic_light_ew = "green"
    else:
        traffic_light_ns = "green"
        traffic_light_ew = "red"

def draw_ui():
    """Отрисовка интерфейса"""
    font = pygame.font.SysFont(None, 36)
    
    # Счетчик проехавших машин
    passed_text = font.render(f"Проехало: {passed_cars}", True, WHITE)
    screen.blit(passed_text, (10, 10))
    
    # Режим работы
    mode_text = font.render(f"Режим: {'Авто' if auto_mode else 'Ручной'}", True, WHITE)
    screen.blit(mode_text, (10, 50))
    
    # Кнопки
    pygame.draw.rect(screen, GREEN, (WIDTH - 250, 10, 240, 40))
    manual_text = font.render("Ручное переключение", True, BLACK)
    screen.blit(manual_text, (WIDTH - 245, 15))
    
    pygame.draw.rect(screen, GREEN, (WIDTH - 250, 60, 240, 40))
    auto_text = font.render("Авто режим", True, BLACK)
    screen.blit(auto_text, (WIDTH - 245, 65))

# Главный цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Проверка нажатия на кнопку "Ручное переключение"
            if WIDTH - 250 <= mouse_pos[0] <= WIDTH - 10 and 10 <= mouse_pos[1] <= 50:
                toggle_lights()
                auto_mode = False
            
            # Проверка нажатия на кнопку "Авто режим"
            if WIDTH - 250 <= mouse_pos[0] <= WIDTH - 10 and 60 <= mouse_pos[1] <= 100:
                auto_mode = not auto_mode
                switch_timer = pygame.time.get_ticks()
    
    # Автоматическое переключение светофоров
    if auto_mode and pygame.time.get_ticks() - switch_timer > 5000:  # каждые 5 секунд
        toggle_lights()
        switch_timer = pygame.time.get_ticks()
    
    # Создание новых машин
    spawn_timer += 1
    if spawn_timer >= 60:  # каждую секунду
        cars.append(spawn_car())
        spawn_timer = 0
    
    # Обновление машин
    update_cars()
    
    # Отрисовка
    draw_intersection()
    draw_traffic_lights()
    draw_cars()
    draw_ui()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()