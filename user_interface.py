from vacancy_operator import VacancyOperator
from json_manager import JsonOperator


class UserInterface:
    """Класс пользовательского интерфейса"""

    def __init__(self, vac_list):
        """Инициализация для работы с пользователем"""
        self.vac_list = vac_list

    @staticmethod
    def functions_choosing():
        """Выбор функции"""
        function_input = input(f"Доступны следующие действия:\n"
                               f"1 - Вывести весь список вакансий (не более 100)\n"
                               f"2 - Вывести топ N вакансий (по убыванию)\n"
                               f"3 - Отфильтровать список по зарплате "
                               f"(указывается минимальная ЗП)\n"
                               f"4 - Найти вакансию по ключевому слову\n"
                               f"5 - Очистить список вакансий\n"
                               f"6 - Сравнить две вакансии по зарплате\n"
                               f"0 - Вернуться к выбору платформы и вакансий (выйти)\n> ")
        return function_input

    def functions_exe(self):
        """Функционал"""
        if len(self.vac_list) > 0:
            print(f"Найденное кол-во вакансий: {len(self.vac_list)} с корректными данными.\n"
                  f"Остальные вакансии имеют не полные данные.")
            while True:
                chosen_func = self.functions_choosing()

                # Вывод полного списка вакансий
                if chosen_func == "1":
                    all_vac_inst_1 = VacancyOperator(self.vac_list)
                    all_vac = output_formatting(all_vac_inst_1.get_all_valid_vacancies())
                    for item in all_vac:
                        print(item)

                # Вывод топ N вакансий
                if chosen_func == "2":
                    n_input = int(input(f"Введите желаемое количество вакансий для "
                                        f"обработки:\n> "))
                    all_vac_inst_2 = VacancyOperator(self.vac_list)
                    top_n = output_formatting(all_vac_inst_2.get_top_n_vacancies_by_sal(n_input))
                    for item in top_n:
                        print(item)

                # Вывод отфильтрованных вакансий по минимальной зарплате
                if chosen_func == "3":
                    min_sal_input = int(input(f"Введите минимальный уровень зарплаты:\n> "))
                    all_vac_inst_3 = VacancyOperator(self.vac_list)
                    min_sal_list = output_formatting(all_vac_inst_3.get_vac_by_min_salary
                                                     (min_sal_input))
                    if len(min_sal_list) == 0:
                        print(f"Кажется у Вас слишком высокие требования :)\n"
                              f"Таких вакансий не нашлось.\n")
                    else:
                        for item in min_sal_list:
                            print(item)

                # Вывод вакансий по ключевому слову в описании
                if chosen_func == "4":
                    keyword_input = input(f"Введите ключевое слово:\n> ")
                    all_vac_inst_4 = VacancyOperator(self.vac_list)
                    key_word_list = output_formatting(all_vac_inst_4.get_vac_by_keyword
                                                      (keyword_input))
                    if len(key_word_list) > 0:
                        for item in key_word_list:
                            print(item)
                    else:
                        print(f"Упс. Кажется такого слова нет ни в одном описании найденных "
                              f"вакансии")

                # Очистка списка вакансий
                if chosen_func == "5":
                    JsonOperator.delete_from_json()
                    print(f"Список вакансий очищен! Давай сначала!")
                    break

                # Сравнение двух вакансий по минимальной зарплате
                if chosen_func == "6":
                    all_vac_inst_5 = VacancyOperator(self.vac_list)
                    all_vac = output_formatting(all_vac_inst_5.get_all_valid_vacancies())
                    for item in all_vac:
                        print(item)
                    print()
                    print("Вот весь список вакансий!")
                    while True:
                        first_vac_num_input = int(input(f"Введи порядковый "
                                                        f"номер первой вакансии:\n> "))
                        second_vac_num_input = int(input(f"Введи порядковый "
                                                         f"номер второй вакансии:\n> "))
                        if (first_vac_num_input > len(all_vac_inst_5.get_all_valid_vacancies()) or
                                second_vac_num_input > len(
                                    all_vac_inst_5.get_all_valid_vacancies())):
                            print(f"Таких вакансии нет в списке. Введите верный №.")
                        else:
                            result = all_vac_inst_5.two_vac_comp_by_min_sal(first_vac_num_input,
                                                                            second_vac_num_input)
                            break

                    if result:
                        print(f"Первая выбранная вакансия имеет наибольшую зарплату!\n")
                    else:
                        print(f"Вторая выбранная вакансия имеет наибольшую зарплату!\n")

                # Возвращение к выбору платформы
                if chosen_func == "0":
                    break

                # Защита от неверного выбора функции
                if chosen_func not in ["0", "1", "2", "3", "4", "5", "6"]:
                    print(f"Сначала выбери функцию!")
                    print()

        else:
            print("Упс. Кажется не нашлось ни одной вакансии с полными данными.")


def output_formatting(hh_vac_valid_list):
    """Метод для преобразования json формата в читабельный формат"""
    hh_formed_vac = []
    counter = 1
    for vacancy in hh_vac_valid_list:
        vacancies_items = f"""Вакансия № {counter}
Наименование вакансии: {vacancy["Наименование вакансии"]}
Ссылка на вакансию: {vacancy["Ссылка на вакансию"]}
Зарплата от: {vacancy["Зарплата от"]}
Зарплата до: {vacancy["Зарплата до"]}
Валюта: {vacancy["Валюта"]}
Название компании: {vacancy["Название компании"]}
Требования и обязанности: {vacancy["Требования и обязанности"]}\n"""

        hh_formed_vac.append(vacancies_items)
        counter += 1
    return hh_formed_vac
