import os

def clear_screen():
    # Очищает консоль (работает и на Windows, и на Linux/Mac)
    os.system('cls' if os.name == 'nt' else 'clear')

def print_field(field):
    print()
    print(f" {field[0]} | {field[1]} | {field[2]}")
    print("---+---+---")
    print(f" {field[3]} | {field[4]} | {field[5]}")
    print("---+---+---")
    print(f" {field[6]} | {field[7]} | {field[8]}")
    print()

def check_win(field, symbol):
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # строки
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # столбцы
        [0, 4, 8], [2, 4, 6]              # диагонали
    ]
    for combo in win_combinations:
        if all(field[i] == symbol for i in combo):
            return True
    return False

def play_game():
    field = [str(i) for i in range(1, 10)]
    current_player = 'X'
    moves = 0

    while True:
        clear_screen()
        print_field(field)

        try:
            move = int(input(f"Игрок {current_player}, введите номер клетки (1-9): "))
        except ValueError:
            print("Ошибка: введите число от 1 до 9.")
            continue

        if move < 1 or move > 9:
            print("Ошибка: число должно быть от 1 до 9.")
            continue

        if field[move - 1] in ['X', 'O']:
            print("Эта клетка уже занята. Попробуйте другую.")
            continue

        field[move - 1] = current_player
        moves += 1

        if check_win(field, current_player):
            clear_screen()
            print_field(field)
            print(f"Поздравляем! Игрок {current_player} победил!\n")
            break

        if moves == 9:
            clear_screen()
            print_field(field)
            print("Ничья! Все клетки заняты.\n")
            break

        current_player = 'O' if current_player == 'X' else 'X'

def main():
    while True:
        play_game()
        again = input("Сыграть ещё раз? (Y/N): ").strip().lower()
        if again != 'y':
            print("Спасибо за игру!")
            break


if __name__ == "__main__":
    main()        