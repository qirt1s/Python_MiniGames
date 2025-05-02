import random
import os

# Класс игрока
class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.health = 100

    def move(self, direction, size):
        if direction == 'w' and self.x > 0:
            self.x -= 1
        elif direction == 's' and self.x < size - 1:
            self.x += 1
        elif direction == 'a' and self.y > 0:
            self.y -= 1
        elif direction == 'd' and self.y < size - 1:
            self.y += 1
        else:
            print("Нельзя двигаться в этом направлении!")

# Генерация поля
def generate_field(size, traps_count):
    field = [['.' for _ in range(size)] for _ in range(size)]

    # Установка ловушек
    count = 0
    while count < traps_count:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if (x, y) != (0, 0) and field[x][y] == '.':
            field[x][y] = 'T'
            count += 1

    # Установка выхода
    while True:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if (x, y) != (0, 0) and field[x][y] == '.':
            field[x][y] = 'X'
            break

    return field

# Печать поля
def print_field(field, player):
    os.system('cls' if os.name == 'nt' else 'clear')
    size = len(field)
    for i in range(size):
        row = ""
        for j in range(size):
            if i == player.x and j == player.y:
                row += "P "
            else:
                row += field[i][j] + " "
        print(row)
    print(f"\nЗдоровье игрока: {player.health}")

# Основной игровой цикл
def play_game():
    size = 5
    traps = random.randint(3, 5)
    field = generate_field(size, traps)
    player = Player()

    while True:
        print_field(field, player)

        if field[player.x][player.y] == 'T':
            player.health -= 20
            field[player.x][player.y] = '.'
            print("Вы попали в ловушку! -20 здоровья")
        elif field[player.x][player.y] == 'X':
            print("Поздравляем! Вы нашли выход!")
            break
        elif player.health <= 0:
            print("Вы проиграли. Здоровье закончилось.")
            break

        move = input("Куда пойти? (w/a/s/d): ").lower()
        if move in ['w', 'a', 's', 'd']:
            player.move(move, size)
        else:
            print("Неверная команда. Используйте w/a/s/d.")

# Повтор игры
while True:
    play_game()
    again = input("\nСыграть снова? (y/n): ").lower()
    if again != 'y':
        print("Спасибо за игру!")
        break


if __name__ == "__main__":
    main()
