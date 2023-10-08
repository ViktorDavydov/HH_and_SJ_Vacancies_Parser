from hh_utils import HHUserInterface
from sj_utils import SJUserInterface


if __name__ == "__main__":
    print(f"Привет! Я программа для сбора информации о вакансиях! Приступим!\n")
    while True:
        platform_input = input(f"Выбери платформу:\n1 - HeadHunter\n2 - SuperJob\n0 - Выйти\n> ")
        if platform_input == "1":
            hh_block = HHUserInterface()
            hh_block.functions_exe()

        elif platform_input == "2":
            sj_block = SJUserInterface()
            sj_block.functions_exe()

        elif platform_input == "0":
            print("Всего хорошего!")
            break

        else:
            print(f"Упс. Кажется в моей базе нет такой платформы. Попробуй еще раз!")
            print()

#
# ["payment_from"]
# ["payment_to"]
# ["currency"]
# ["client"]["title"]
# Наименование вакансии: {item["profession"]}
# Ссылка на вакансию: {item["link"]}
# Зарплата от: {payment_from}
# Зарплата до: {payment_to}\nВалюта: {currency}
# Название компании: {item["client"]["title"]}