import pygame
import random
import time

pygame.init()

# --- Настройки ---
WIDTH, HEIGHT = 800, 600
SLOT_SIZE = 30
PARKING_ROWS = 4
SLOTS_PER_ROW = 5
TOTAL_SLOTS = PARKING_ROWS * SLOTS_PER_ROW

parking_slots = [None] * TOTAL_SLOTS

# Цвета
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Parking Simulator")
font = pygame.font.SysFont("Arial", 20)

# --- Глобальные переменные ---
incoming_car = None
last_car_time = time.time()

# --- Функции ---
def draw_parking(surface, slots):
    x_offset, y_offset = 50, 50
    for i in range(len(slots)):
        x = x_offset + (i % SLOTS_PER_ROW) * (SLOT_SIZE + 10)
        y = y_offset + (i // SLOTS_PER_ROW) * (SLOT_SIZE + 10)
        color = GREEN if slots[i] is None else RED
        pygame.draw.rect(surface, color, (x, y, SLOT_SIZE, SLOT_SIZE))

def generate_car():
    types = {
        "легковая": (1, (255, 0, 0)),
        "грузовая": (2, (0, 0, 255)),
        "электромобиль": (1, (0, 255, 0))
    }
    car_type = random.choice(list(types.keys()))
    size, color = types[car_type]
    plate = f"{random.choice('ABEKMH')}{random.randint(100,999)}{random.choice('ABEKMH')}{random.choice('ABEKMH')}"
    return {"plate": plate, "type": car_type, "size": size, "color": color}

def find_parking_slot(size):
    for i in range(len(parking_slots) - size + 1):
        if all(slot is None for slot in parking_slots[i:i+size]):
            return i
    return -1

def park_car(car):
    index = find_parking_slot(car["size"])
    if index != -1:
        for i in range(car["size"]):
            parking_slots[index + i] = car
        return True
    return False

def remove_random_car():
    occupied = [i for i, slot in enumerate(parking_slots) if slot is not None]
    if not occupied:
        return "Парковка пуста"
    i = random.choice(occupied)
    car = parking_slots[i]
    for j in range(len(parking_slots)):
        if parking_slots[j] == car:
            parking_slots[j] = None
    return f"Машина {car['plate']} уехала"

def draw_ui():
    screen.blit(font.render("Свободных мест: " + str(parking_slots.count(None)), True, BLACK), (500, 50))
    screen.blit(font.render("Занятых мест: " + str(TOTAL_SLOTS - parking_slots.count(None)), True, BLACK), (500, 80))
    pygame.draw.rect(screen, GRAY, (500, 150, 200, 40))
    screen.blit(font.render("Впустить машину", True, BLACK), (510, 160))
    pygame.draw.rect(screen, GRAY, (500, 200, 200, 40))
    screen.blit(font.render("Выпустить машину", True, BLACK), (510, 210))

    if incoming_car:
        screen.blit(font.render(f"Машина на въезде: {incoming_car['plate']}", True, BLACK), (500, 300))
        screen.blit(font.render(f"Тип: {incoming_car['type']}, Размер: {incoming_car['size']}", True, BLACK), (500, 330))

def handle_click(x, y):
    global incoming_car
    if 500 <= x <= 700 and 150 <= y <= 190 and incoming_car:
        if park_car(incoming_car):
            incoming_car = None
        else:
            print("Нет мест")
    elif 500 <= x <= 700 and 200 <= y <= 240:
        msg = remove_random_car()
        print(msg)

# --- Главный цикл ---
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    draw_parking(screen, parking_slots)
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            handle_click(x, y)

    if time.time() - last_car_time > 5 and incoming_car is None:
        incoming_car = generate_car()
        last_car_time = time.time()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
