# imports
import requests
import json

from abstract_classes import ApiEngine, JsonManager


class HHApiEngine(ApiEngine):
    """Класс для получения вакансий по API"""

    def __init__(self, city_name, prof_name):
        self.hh_api_url = "https://api.hh.ru"
        self.headers = {
            "User-Agent": "ViktorDavydov"
        }
        self.city_name = city_name
        self.prof_name = prof_name

    def __repr__(self):
        return (f"Указанный город: {self.city_name}"
                f"Указанная профессия: {self.prof_name}")

    def get_city_id(self):
        """Получение id города для получения в нем вакансий"""
        params = {
            "text": self.city_name
        }
        hh_areas_url = self.hh_api_url + "/suggests/areas"
        response = requests.get(hh_areas_url, params=params, headers=self.headers)

        for city in response.json()["items"]:
            if city["text"] == self.city_name:
                return city["id"]

    def get_vacancies(self):
        """Получение всех вакансий выбранного города"""
        hh_vac_url = self.hh_api_url + "/vacancies"
        params = {
            "text": self.prof_name,
            "per_page": 100,
            "area": self.get_city_id()
        }
        response = requests.get(hh_vac_url, params=params, headers=self.headers)

        if response.status_code == 200:
            vacancies = response.json()

        return vacancies["items"]


class VacancyOperator:
    """Класс для валидации данных и сравнения вакансий по минимальной зарплате"""
    valid_vacancies_list = []

    def __init__(self, vac_list):
        """Валидация данных при инициализации"""
        self.vac_list = vac_list
        for vacancies in self.vac_list:
            if isinstance(vacancies["name"], str):
                vacancy_name = vacancies["name"]

            if "https://" in vacancies["alternate_url"]:
                url = vacancies["alternate_url"]

            if vacancies["salary"] is not None:
                if (isinstance(vacancies["salary"]["from"], int) and
                        vacancies["salary"]["from"] > 0):
                    salary_from = vacancies["salary"]["from"]

                else:
                    salary_from = False

                if (isinstance(vacancies["salary"]["currency"], str) and
                        vacancies["salary"]["currency"] == "RUR"):
                    salary_currency = vacancies["salary"]["currency"]

                else:
                    salary_currency = False

                if (isinstance(vacancies["salary"]["to"], int) and
                        vacancies["salary"]["to"] > 0):
                    salary_to = vacancies["salary"]["to"]

                else:
                    salary_to = False
            else:
                salary_from = salary_currency = salary_to = False

            if isinstance(vacancies["employer"]["name"], str):
                employer_name = vacancies["employer"]["name"]

            if isinstance(vacancies["snippet"]["requirement"], str):
                requirement = vacancies["snippet"]["requirement"]

            if isinstance(vacancies["snippet"]["responsibility"], str):
                responsibility = vacancies["snippet"]["responsibility"]

            if (vacancy_name and url and salary_from and salary_currency and salary_to
                    and employer_name and requirement and responsibility):
                self.valid_vacancies_list.append(vacancies)

    def two_vac_comp_by_min_sal(self, first_num, second_num):
        """Метод сравнения двух вакансий по минимальной зарплате"""
        min_salary_1 = self.valid_vacancies_list[first_num - 1]["salary"]["from"]
        min_salary_2 = self.valid_vacancies_list[second_num - 1]["salary"]["from"]

        return min_salary_1 >= min_salary_2

    def get_vac_by_min_salary(self, salary_minimum):
        """Получение отфильтрованных вакансий по минимальной зарплате"""
        filtered_vac_by_min_sal = [item for item in self.valid_vacancies_list
                                   if item["salary"]["from"] >= salary_minimum]

        return filtered_vac_by_min_sal

    def get_top_n_vacancies_by_sal(self, vac_count):
        """Получение топ N вакансий"""
        source_list = self.valid_vacancies_list
        final_sorted = sorted(source_list,
                              key=lambda d: d["salary"]["from"], reverse=True)

        return final_sorted[:vac_count]

    def get_vac_by_keyword(self, keyword):
        """Получение вакансий по ключевому слову"""
        key_word_vac = [item for item in self.valid_vacancies_list if keyword
                        in item["snippet"]["requirement"]
                        or keyword in item["snippet"]["responsibility"]]

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
                            if item["salary"]["from"] == salary]
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
"Наименование вакансии": {vacancy["name"]}
"Ссылка на вакансию": {vacancy["alternate_url"]}
"Зарплата от": {vacancy["salary"]["from"]}
"Зарплата до": {vacancy["salary"]["to"]}
"Валюта": {vacancy["salary"]["currency"]}
"Название компании": {vacancy["employer"]["name"]}
"Требования": {vacancy["snippet"]["requirement"]}
"Обязанности": {vacancy["snippet"]["responsibility"]}\n"""

            vacancies_formatted_list.append(vacancies_items)
            counter += 1
        return vacancies_formatted_list


class HHUserInterface:
    """Класс пользовательского интерфейса"""

    def __init__(self):
        """Инициализация для работы с пользователем"""
        print(f"Отлично! Ты выбрал платформу HeadHunter\n")
        hh_inst = HHApiEngine(self.city_name_purchasing(), self.prof_purchasing())
        self.hh_source_list = hh_inst.get_vacancies()
        self.valid_vacancies = VacancyOperator(self.hh_source_list)
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
                    first_vac_num_input = int(input(f"Введи порядковый номер первой вакансии"
                                                    f":\n> "))
                    second_vac_num_input = int(input(f"Введи порядковый номер второй вакансии"
                                                     f":\n> "))
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
                else:
                    print()
                    print(f"Сначала выбери функцию!")

        else:
            print("Упс. Кажется не нашлось ни одной вакансии с полными данными.")
