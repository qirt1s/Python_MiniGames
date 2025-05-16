import pygame
import sys
from enum import Enum

# Инициализация Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Пиццерия: Симулятор заказа")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# Состояния программы
class GameState(Enum):
    MENU = 1
    PIZZA_CUSTOMIZATION = 2
    ORDER_REVIEW = 3

current_state = GameState.MENU

# Базовый класс для элементов меню
class MenuItem:
    def __init__(self, name, base_price):
        self.name = name
        self.base_price = base_price

    def calculate_price(self):
        return self.base_price

    def display(self, x, y):
        font = pygame.font.SysFont('Arial', 30)
        text = font.render(f"{self.name} - ${self.base_price:.2f}", True, BLACK)
        screen.blit(text, (x, y))

# Класс Пицца
class Pizza(MenuItem):
    def __init__(self, name, base_price):
        super().__init__(name, base_price)
        self.size = "Medium"
        self.toppings = []
        self.base_image = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.circle(self.base_image, (255, 200, 150), (100, 100), 100)

    def calculate_price(self):
        price = self.base_price
        price += len(self.toppings) * 1.5
        return price

    def draw_preview(self, x, y):
        screen.blit(self.base_image, (x, y))
        for i, topping in enumerate(self.toppings):
            if topping.name == "Сыр":
                pygame.draw.circle(screen, (255, 255, 0), (x + 100, y + 100), 90, 5)
            elif topping.name == "Пепперони":
                for j in range(8):
                    angle = j * 45
                    px = x + 100 + 70 * pygame.math.Vector2(1, 0).rotate(angle).x
                    py = y + 100 + 70 * pygame.math.Vector2(1, 0).rotate(angle).y
                    pygame.draw.circle(screen, RED, (int(px), int(py)), 15)
            elif topping.name == "Грибы":
                for j in range(5):
                    angle = j * 72 + 18
                    px = x + 100 + 60 * pygame.math.Vector2(1, 0).rotate(angle).x
                    py = y + 100 + 60 * pygame.math.Vector2(1, 0).rotate(angle).y
                    pygame.draw.ellipse(screen, (200, 200, 200), (px-10, py-5, 20, 10))

# Класс Кнопка
class Button:
    def __init__(self, x, y, width, height, text, action=None, color=GREEN, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color
        self.text_color = text_color
        self.hovered = False

    def draw(self):
        color = (min(self.color[0] + 30, 255), 
                min(self.color[1] + 30, 255), 
                min(self.color[2] + 30, 255)) if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        font = pygame.font.SysFont('Arial', 24)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

# Класс Топпинг
class Topping:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.selected = False

# Создаем элементы меню
menu_items = [
    Pizza("Маргарита", 10),
    Pizza("Пепперони", 12),
    Pizza("Гавайская", 11)
]

toppings = [
    Topping("Сыр", 1.5),
    Topping("Пепперони", 2.0),
    Topping("Грибы", 1.0)
]

# Список заказов
orders = []

# Текущая пицца для кастомизации
current_pizza = None

def set_state(state):
    global current_state, current_pizza
    current_state = state
    if state == GameState.PIZZA_CUSTOMIZATION and not current_pizza:
        current_pizza = Pizza("Маргарита", 10)

def handle_pizza_customization_events(event):
    mouse_pos = pygame.mouse.get_pos()
    
    size_buttons = [
        Button(150, 150, 200, 50, "Маленькая ($8)", lambda: set_pizza_size("Small"), 
               color=GREEN if current_pizza.size == "Small" else GRAY),
        Button(150, 220, 200, 50, "Средняя ($10)", lambda: set_pizza_size("Medium"), 
               color=GREEN if current_pizza.size == "Medium" else GRAY),
        Button(150, 290, 200, 50, "Большая ($13)", lambda: set_pizza_size("Large"), 
               color=GREEN if current_pizza.size == "Large" else GRAY)
    ]
    
    topping_buttons = []
    for i, topping in enumerate(toppings):
        topping_buttons.append(
            Button(450, 150 + i * 70, 250, 50, 
                  f"{topping.name} (+${topping.price})", 
                  lambda t=topping: toggle_topping(t),
                  color=GREEN if topping.selected else GRAY)
        )
    
    action_buttons = [
        Button(150, 450, 200, 50, "Назад", lambda: set_state(GameState.MENU), color=GRAY),
        Button(450, 450, 250, 50, "Добавить в заказ", lambda: add_to_order(), color=GREEN)
    ]
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for button in size_buttons + topping_buttons + action_buttons:
            if button.is_clicked(mouse_pos) and button.action:
                button.action()
                return True
    
    for button in size_buttons + topping_buttons + action_buttons:
        button.check_hover(mouse_pos)
    
    return False

def set_pizza_size(size):
    current_pizza.size = size
    if size == "Small":
        current_pizza.base_price = 8
    elif size == "Medium":
        current_pizza.base_price = 10
    elif size == "Large":
        current_pizza.base_price = 13

def toggle_topping(topping):
    topping.selected = not topping.selected
    if topping.selected:
        current_pizza.toppings.append(topping)
    else:
        current_pizza.toppings.remove(topping)

def add_to_order():
    global orders, current_pizza
    
    ordered_pizza = Pizza(current_pizza.name, current_pizza.base_price)
    ordered_pizza.size = current_pizza.size
    ordered_pizza.toppings = current_pizza.toppings.copy()
    
    orders.append(ordered_pizza)
    reset_pizza_customization()
    set_state(GameState.MENU)

def reset_pizza_customization():
    global current_pizza
    current_pizza = Pizza("Маргарита", 10)
    for topping in toppings:
        topping.selected = False

def draw_menu():
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    title = title_font.render("Добро пожаловать в пиццерию!", True, (50, 50, 150))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
    
    menu_buttons = [
        Button(350, 200, 300, 50, "Заказать пиццу", lambda: set_state(GameState.PIZZA_CUSTOMIZATION)),
        Button(350, 300, 300, 50, "Корзина", lambda: set_state(GameState.ORDER_REVIEW)),
        Button(350, 400, 300, 50, "Выход", lambda: sys.exit())
    ]
    
    for button in menu_buttons:
        button.draw()

def draw_pizza_customization():
    title_font = pygame.font.SysFont('Arial', 36, bold=True)
    title = title_font.render("Кастомизация пиццы", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
    
    # Размеры пиццы
    size_font = pygame.font.SysFont('Arial', 28)
    size_label = size_font.render("Выберите размер:", True, BLACK)
    screen.blit(size_label, (150, 100))
    
    # Создаем кнопки выбора размера
    size_buttons = [
        Button(150, 150, 200, 50, "Маленькая ($8)", lambda: set_pizza_size("Small"), 
               color=GREEN if current_pizza.size == "Small" else GRAY),
        Button(150, 220, 200, 50, "Средняя ($10)", lambda: set_pizza_size("Medium"), 
               color=GREEN if current_pizza.size == "Medium" else GRAY),
        Button(150, 290, 200, 50, "Большая ($13)", lambda: set_pizza_size("Large"), 
               color=GREEN if current_pizza.size == "Large" else GRAY)
    ]
    
    # Топпинги
    toppings_label = size_font.render("Добавьте топпинги:", True, BLACK)
    screen.blit(toppings_label, (450, 100))
    
    # Создаем кнопки топпингов
    topping_buttons = []
    for i, topping in enumerate(toppings):
        topping_buttons.append(
            Button(450, 150 + i * 70, 250, 50, 
                  f"{topping.name} (+${topping.price})", 
                  lambda t=topping: toggle_topping(t),
                  color=GREEN if topping.selected else GRAY)
        )
    
    # Превью пиццы
    current_pizza.draw_preview(700, 150)
    
    # Итоговая цена
    price_font = pygame.font.SysFont('Arial', 32, bold=True)
    price_text = price_font.render(f"Итого: ${current_pizza.calculate_price():.2f}", True, BLACK)
    screen.blit(price_text, (SCREEN_WIDTH//2 - price_text.get_width()//2, 400))
    
    # Кнопки действий
    action_buttons = [
        Button(150, 450, 200, 50, "Назад", lambda: set_state(GameState.MENU), color=GRAY),
        Button(450, 450, 250, 50, "Добавить в заказ", lambda: add_to_order(), color=GREEN)
    ]
    
    # Отрисовываем ВСЕ кнопки
    for button in size_buttons + topping_buttons + action_buttons:
        button.draw()

def handle_pizza_customization_events(event):
    mouse_pos = pygame.mouse.get_pos()
    
    # Создаем временные кнопки для обработки событий
    size_buttons = [
        Button(150, 150, 200, 50, "", lambda: set_pizza_size("Small")),
        Button(150, 220, 200, 50, "", lambda: set_pizza_size("Medium")),
        Button(150, 290, 200, 50, "", lambda: set_pizza_size("Large"))
    ]
    
    topping_buttons = []
    for i, topping in enumerate(toppings):
        topping_buttons.append(
            Button(450, 150 + i * 70, 250, 50, "", lambda t=topping: toggle_topping(t))
        )
    
    action_buttons = [
        Button(150, 450, 200, 50, "", lambda: set_state(GameState.MENU)),
        Button(450, 450, 250, 50, "", lambda: add_to_order())
    ]
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for button in size_buttons + topping_buttons + action_buttons:
            if button.is_clicked(mouse_pos) and button.action:
                button.action()
                return True
    return False

def draw_order_review():
    title_font = pygame.font.SysFont('Arial', 36, bold=True)
    title = title_font.render("Ваш заказ", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
    
    if not orders:
        placeholder_font = pygame.font.SysFont('Arial', 24)
        placeholder = placeholder_font.render("Ваша корзина пуста", True, GRAY)
        screen.blit(placeholder, (SCREEN_WIDTH//2 - placeholder.get_width()//2, 200))
    else:
        for i, pizza in enumerate(orders):
            pizza_info = f"{pizza.name} ({pizza.size}) - ${pizza.calculate_price():.2f}"
            if pizza.toppings:
                pizza_info += " + " + ", ".join([t.name for t in pizza.toppings])
            item_font = pygame.font.SysFont('Arial', 24)
            item_text = item_font.render(pizza_info, True, BLACK)
            screen.blit(item_text, (150, 150 + i * 40))
    
    Button(SCREEN_WIDTH//2 - 100, 500, 200, 50, "Назад", lambda: set_state(GameState.MENU)).draw()

# Главный цикл
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if current_state == GameState.PIZZA_CUSTOMIZATION:
            handle_pizza_customization_events(event)
        elif current_state == GameState.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_buttons = [
                    Button(350, 200, 300, 50, "Заказать пиццу", lambda: set_state(GameState.PIZZA_CUSTOMIZATION)),
                    Button(350, 300, 300, 50, "Корзина", lambda: set_state(GameState.ORDER_REVIEW)),
                    Button(350, 400, 300, 50, "Выход", lambda: sys.exit())
                ]
                for button in menu_buttons:
                    if button.is_clicked(mouse_pos) and button.action:
                        button.action()
        elif current_state == GameState.ORDER_REVIEW:
            if event.type == pygame.MOUSEBUTTONDOWN:
                back_button = Button(SCREEN_WIDTH//2 - 100, 500, 200, 50, "Назад", lambda: set_state(GameState.MENU))
                if back_button.is_clicked(mouse_pos) and back_button.action:
                    back_button.action()

    if current_state == GameState.MENU:
        draw_menu()
    elif current_state == GameState.PIZZA_CUSTOMIZATION:
        draw_pizza_customization()
    elif current_state == GameState.ORDER_REVIEW:
        draw_order_review()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()