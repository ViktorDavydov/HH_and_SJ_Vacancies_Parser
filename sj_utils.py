import requests
import json
import os

from abstract_classes import ApiEngine, JsonManager


class SJApiEngine(ApiEngine):
    def __init__(self, city_name, prof_name):
        self.sj_api_url = "https://api.superjob.ru/2.0"
        self.SJ_API_TOKEN = os.getenv("SJ_TOKEN")
        self.headers = {
            "X-Api-App-Id": self.SJ_API_TOKEN
        }
        self.city_name = city_name
        self.prof_name = prof_name

    def get_city_id(self):
        pass

    def get_vacancies(self):
        """Получение всех вакансий выбранного города"""
        sj_vac_url = self.sj_api_url + "/vacancies"
        params = {
            "town": self.city_name,
            "keyword": self.prof_name,
            "count": 100
        }
        response = requests.get(sj_vac_url, params=params, headers=self.headers)

        if response.status_code == 200:
            vacancies = response.json()

        return vacancies["objects"]


class VacancyOperator:
    """Класс для валидации данных и сравнения вакансий по минимальной зарплате"""
    valid_vacancies_list = []

    def __init__(self, vac_list):
        """Валидация данных при инициализации"""
        self.vac_list = vac_list
        for vacancies in self.vac_list:
            if isinstance(vacancies["profession"], str):
                vacancy_name = vacancies["profession"]

            if "https://" in vacancies["link"]:
                url = vacancies["link"]

            if vacancies["payment_from"] is not None:
                if (isinstance(vacancies["payment_from"], int) and
                        vacancies["payment_from"] > 0):
                    salary_from = vacancies["payment_from"]

                else:
                    salary_from = False

                if (isinstance(vacancies["currency"], str) and
                        vacancies["currency"] == "rub"):
                    salary_currency = vacancies["currency"]

                else:
                    salary_currency = False

                if (isinstance(vacancies["payment_to"], int) and
                        vacancies["payment_to"] > 0):
                    salary_to = vacancies["payment_to"]

                else:
                    salary_to = False
            else:
                salary_from = salary_currency = salary_to = False

            if vacancies["client"] is not None:
                if ("title" in vacancies["client"]
                        and isinstance(vacancies["client"]["title"], str)):
                    employer_name = vacancies["client"]["title"]

                else:
                    employer_name = False

            if isinstance(vacancies["candidat"], str):
                requirement = vacancies["candidat"]

            if (vacancy_name and url and salary_from and salary_currency and salary_to
                    and employer_name and requirement):
                self.valid_vacancies_list.append(vacancies)

    def two_vac_comp_by_min_sal(self, first_num, second_num):
        """Метод сравнения двух вакансий по минимальной зарплате"""
        min_salary_1 = self.valid_vacancies_list[first_num - 1]["payment_from"]
        min_salary_2 = self.valid_vacancies_list[second_num - 1]["payment_from"]

        return min_salary_1 >= min_salary_2

    def get_vac_by_min_salary(self, salary_minimum):
        """Получение отфильтрованных вакансий по минимальной зарплате"""
        filtered_vac_by_min_sal = [item for item in self.valid_vacancies_list
                                   if item["payment_from"] >= salary_minimum]

        return filtered_vac_by_min_sal

    def get_top_n_vacancies_by_sal(self, vac_count):
        """Получение топ N вакансий"""
        source_list = self.valid_vacancies_list
        final_sorted = sorted(source_list,
                              key=lambda d: d["payment_from"], reverse=True)

        return final_sorted[:vac_count]

    def get_vac_by_keyword(self, keyword):
        """Получение вакансий по ключевому слову"""
        key_word_vac = [item for item in self.valid_vacancies_list if keyword
                        in item["candidat"]]

        return key_word_vac

    def get_all_valid_vacancies(self):
        """Получение всех вакансий"""
        return self.valid_vacancies_list


class VacanciesJsonOperator(JsonManager):
    """Класс для обработки вакансий в json формате, записи, фильтрации, сортировки и удаления"""

    def __init__(self, valid_vacancies):
        self.valid_vacancies = valid_vacancies

    def save_to_json(self):
        """Сохранение вакансий в json"""
        with open("json_vac_info.json", "w", encoding="utf-8") as file:
            json.dump(self.valid_vacancies, file, indent=2, ensure_ascii=False)

    def get_json(self):
        """Получение вакансий из json"""
        with open("json_vac_info.json", "r", encoding="utf-8") as file:
            vacancies_info = json.load(file)
            return vacancies_info

    def delete_from_json(self):
        """Удаление вакансий из json"""
        with open("json_vac_info.json", "w") as file:
            pass

    def get_vacancies_by_sal(self, salary):
        """Поиск вакансии по ЗП"""
        chosen_vacancies = [item for item in self.valid_vacancies
                            if item["payment_from"] == salary]
        if len(chosen_vacancies) > 0:
            return chosen_vacancies
        return "Упс. Кажется не нашлось ни одной вакансии с указанной зарплатой"


class DataCorFormatOutput:
    """Класс для форматирования данных для вывода"""

    def __init__(self, filtered_vac_list):
        self.filtered_vac_list = filtered_vac_list

    def formatting_output_data(self):
        """Метод для преобразования json формата в читабельный формат"""
        vacancies_formatted_list = []
        counter = 1
        for vacancy in self.filtered_vac_list:
            vacancies_items = f""""Вакансия №": {counter}
"Наименование вакансии": {vacancy["profession"]}
"Ссылка на вакансию": {vacancy["link"]}
"Зарплата от": {vacancy["payment_from"]}
"Зарплата до": {vacancy["payment_to"]}
"Валюта": {vacancy["currency"]}
"Название компании": {vacancy["client"]["title"]}
"Описание": {vacancy["candidat"]}\n"""

            vacancies_formatted_list.append(vacancies_items)
            counter += 1
        return vacancies_formatted_list


class SJUserInterface:
    """Класс пользовательского интерфейса"""

    def __init__(self):
        """Инициализация для работы с пользователем"""
        print(f"Отлично! Ты выбрал платформу SuperJob\n")
        sj_inst = SJApiEngine(self.city_name_purchasing(), self.prof_purchasing())
        self.sj_source_list = sj_inst.get_vacancies()
        self.valid_vacancies = VacancyOperator(self.sj_source_list)
        self.vac_list = self.valid_vacancies.get_all_valid_vacancies()
        self.json_format_inst = VacanciesJsonOperator(self.vac_list)
        self.json_format_inst.save_to_json()

    @staticmethod
    def city_name_purchasing():
        """Получение названия города"""
        city_name_input = input(f"Для начала узнаем в каком "
                                f"городе необходимо найти вакансии, "
                                f"например, Санкт-Петербург или Казань:\n"
                                f"(Только вводи существующий город, иначе получишь кулебяку)"
                                f"\n> ").capitalize()
        return city_name_input

    @staticmethod
    def prof_purchasing():
        """Получение названия профессии"""
        prof_input = input(f"А теперь мне необходимо узнать название профессии, например "
                           f"Python разработчик или Визажист:\n> ").capitalize()
        return prof_input

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
        return int(function_input)

    def functions_exe(self):
        """Функционал"""
        if len(self.vac_list) > 0:
            print(f"Найденное кол-во вакансий: {len(self.vac_list)} с корректными данными.\n"
                  f"Остальные вакансии имеют не полные данные.")
            while True:
                chosen_func = self.functions_choosing()
                # Вывод полного списка вакансий
                if chosen_func == 1:
                    formed_all_vac_list = DataCorFormatOutput(
                        self.valid_vacancies.get_all_valid_vacancies())
                    all_vac = formed_all_vac_list.formatting_output_data()
                    for item in all_vac:
                        print(item)

                # Вывод топ N вакансий
                if chosen_func == 2:
                    n_input = int(input(f"Введите желаемое количество вакансий для "
                                        f"обработки:\n> "))
                    formed_top_n = DataCorFormatOutput(self.valid_vacancies.
                                                       get_top_n_vacancies_by_sal(n_input))
                    top_n = formed_top_n.formatting_output_data()
                    for item in top_n:
                        print(item)

                # Вывод отфильтрованных вакансий по минимальной зарплате
                if chosen_func == 3:
                    min_sal_input = int(input(f"Введите минимальный уровень зарплаты:\n> "))
                    formed_by_min_sal = DataCorFormatOutput(self.valid_vacancies.
                                                            get_vac_by_min_salary(min_sal_input))
                    min_sal_list = formed_by_min_sal.formatting_output_data()
                    for item in min_sal_list:
                        print(item)

                # Вывод вакансий по ключевому слову в описании
                if chosen_func == 4:
                    keyword_input = input(f"Введите ключевое слово:\n> ")
                    formed_by_key_word = DataCorFormatOutput(self.valid_vacancies.
                                                             get_vac_by_keyword(keyword_input))
                    key_word_list = formed_by_key_word.formatting_output_data()
                    if len(key_word_list) > 0:
                        for item in key_word_list:
                            print(item)
                    else:
                        print(f"Упс. Кажется такого слова нет ни в одном описании найденных "
                              f"вакансии")

                # Очистка списка вакансий
                if chosen_func == 5:
                    self.json_format_inst.delete_from_json()
                    print(f"Список вакансий очищен! Давай сначала!")
                    break

                # Сравнение двух вакансий по минимальной зарплате
                if chosen_func == 6:
                    formed_all_vac_list = DataCorFormatOutput(
                        self.valid_vacancies.get_all_valid_vacancies())
                    all_vac = formed_all_vac_list.formatting_output_data()
                    for item in all_vac:
                        print(item)
                    print()
                    print("Вот весь список вакансий!")
                    first_vac_num_input = int(
                        input(f"Введи порядковый номер первой вакансии:\n> "))
                    second_vac_num_input = int(
                        input(f"Введи порядковый номер второй вакансии:\n> "))
                    result = self.valid_vacancies.two_vac_comp_by_min_sal(first_vac_num_input,
                                                                          second_vac_num_input)

                    if result:
                        print(f"Первая выбранная вакансия имеет наибольшую зарплату!")
                    else:
                        print(f"Вторая выбранная вакансия имеет наибольшую зарплату!")

                # Возвращение к выбору платформы
                if chosen_func == 0:
                    break

                # Защита от неверного выбора функции
                if chosen_func not in [0, 1, 2, 3, 4, 5, 6]:
                    print()
                    print(f"Сначала выбери функцию!")

        else:
            print("Упс. Кажется не нашлось ни одной вакансии с полными данными.")
