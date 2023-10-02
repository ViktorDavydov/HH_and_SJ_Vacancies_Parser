from hh_utils import HHUserInterface

print(f"Привет! Я программа для сбора информации о вакансиях! Приступим!\n")
while True:
    platform_input = input(f"Выбери платформу:\n1 - HeadHunter\n2 - SuperJob\n0 - Выйти\n> ")
    if platform_input == "1":
        hh_block = HHUserInterface()
        hh_block.user_interaction()

    elif platform_input == "2":
        pass

    elif platform_input == "0":
        print("Всего хорошего!")
        break

    else:
        print(f"Упс. Кажется в моей базе нет такой платформы. Попробуй еще раз!")
        print()
