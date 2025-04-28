import random

def initialize_data():
    heroes = [
        "смелый рыцарь",
        "хитрый вор",
        "волшебник",
        "отважный пират",
        "дерзкий исследователь"
    ]
    
    places = [
        "в далёком королевстве",
        "на заброшенной фабрике",
        "в густом лесу",
        "на просторах космоса",
        "у подножия гор"
    ]
    
    events = [
        "победил дракона",
        "обнаружил сокровища",
        "выиграл битву",
        "устроил бал",
        "раскрыл древнюю тайну"
    ]
    
    details = [
        "с волшебным мечом",
        "на летающем ковре",
        "под звуки волшебной музыки",
        "с удивительной силой",
        "в сопровождении магического существа"
    ]
    
    return heroes, places, events, details

def generate_story(heroes, places, events, details):
    hero = random.choice(heroes)
    place = random.choice(places)
    event = random.choice(events)
    detail = random.choice(details)
    story = f"{hero} {place} {event} {detail}."
    return story

def save_story(story):
    try:
        with open("stories.txt", "a", encoding="utf-8") as file:
            file.write(story + "\n")
    except IOError:
        print("Ошибка при сохранении истории!")

def main():
    heroes, places, events, details = initialize_data()
    
    while True:
        input("\nНажмите Enter, чтобы сгенерировать новую историю...")
        story = generate_story(heroes, places, events, details)
        
        print("\n=== НОВАЯ ИСТОРИЯ ===")
        print(story)
        print("=====================")
        
        save = input("\nХотите сохранить эту историю? (да/нет): ").strip().lower()
        if save == 'да':
            save_story(story)
            print("История сохранена в файл stories.txt.")
        
        again = input("\nХотите сыграть ещё раз? (да/нет): ").strip().lower()
        if again != 'да':
            print("\nСпасибо за игру! До встречи!")
            break

if __name__ == "__main__":
    main()