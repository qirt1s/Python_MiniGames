import random

secret_number = random.randint(1, 100)
attempts = 0
max_attempts = 10

print("Я загадал число от 1 до 100.")
print("У вас есть 10 попыток.")

while attempts < max_attempts:
        try:
            guess = int(input("Введите ваше число: "))
        except ValueError:
            print("Пожалуйста, введите целое число!")
            continue

        if guess < 1 or guess > 100:
            print("Число должно быть от 1 до 100!")
            continue

        attempts += 1

        if guess < secret_number:
            print("Загаданное число больше.")
        elif guess > secret_number:
            print("Загаданное число меньше.")
        else:
            print(f"\nПоздравляем! Вы угадали число {secret_number} за {attempts} попыток!")
            break
else:
        print(f"\nВы не угадали. Загаданное число было {secret_number}.")