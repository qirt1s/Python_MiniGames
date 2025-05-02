import random
import os

# Очищаем экран
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Класс персонажа
class Character:
    def __init__(self, name, health, attack, defence):
        self.name = name
        self.health = health
        self.attack = attack
        self.defence = defence

    def attack_target(self, other):
        damage = max(self.attack - other.defence + random.randint(-2, 2), 0)
        other.health -= damage
        print(f"{self.name} атакует {other.name} и наносит {damage} урона!")

# Отображение состояния
def print_status(hero, monster):
    print("\n--- Состояние боя ---")
    print(f"{hero.name}: здоровье {hero.health}, атака {hero.attack}, защита {hero.defence}")
    print(f"{monster.name}: здоровье {monster.health}, атака {monster.attack}, защита {monster.defence}")
    print("----------------------\n")

# Ход игрока
def player_turn(player, enemy):
    while True:
        print("Ваш ход:")
        print("1. Атаковать")
        print("2. Пропустить ход")
        choice = input("Выберите действие (1 или 2): ")

        if choice == '1':
            player.attack_target(enemy)
            break
        elif choice == '2':
            print(f"{player.name} пропускает ход.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

# Ход монстра
def monster_turn(monster, player):
    if random.choice([True, False]):
        monster.attack_target(player)
    else:
        print(f"{monster.name} пропускает ход.")

# Основной игровой цикл
def battle():
    clear()
    hero = Character("Герой", 30, 10, 3)
    monster = Character("Монстр", 25, 8, 2)

    while hero.health > 0 and monster.health > 0:
        print_status(hero, monster)
        player_turn(hero, monster)
        if monster.health <= 0:
            break
        monster_turn(monster, hero)

    print_status(hero, monster)

    if hero.health > 0:
        print("🎉 Победа! Вы победили монстра!\n")
    else:
        print("💀 Поражение! Монстр оказался сильнее...\n")

# Запуск игры с повтором
def main():
    while True:
        battle()
        again = input("Сыграть снова? (y/n): ").lower()
        if again != 'y':
            print("Спасибо за игру!")
            break

if __name__ == "__main__":
    main()
