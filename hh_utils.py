#imports
import requests
import json

from abstract_classes import GetVacanciesByAPI, VacanciesInFileJson


class HHGetVacByAPI(GetVacanciesByAPI):
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

        return vacancies


class VacanciesJson(HHGetVacByAPI, VacanciesInFileJson):
    """Класс для обработки вакансий в json формате, записи, фильтрации, сортировки и удаления"""
    def __init__(self, city_name, prof_name):
        super().__init__(city_name, prof_name)

    def save_to_json(self):
        """Сохранение вакансий в json"""
        with open("json_vac_info.json", "w", encoding="utf-8") as file:
            json.dump(self.get_vacancies(), file, indent=2, ensure_ascii=False)

    def get_json(self):
        """Получение вакансий из json"""
        with open("json_vac_info.json", "r", encoding="utf-8") as file:
            vacancies_info = json.load(file)
            return vacancies_info

    def get_all_vac_info(self):
        """Получение всего списка вакансий в формате json"""
        return self.get_json()["items"]

    def get_valid_vacancies_with_salary(self):
        """Получение вакансий только с указанными минимальными зарплатами"""
        valid_vacancies = []
        for item in self.get_json()["items"]:
            if item["salary"] is not None and item["salary"]["from"] is not None:
                valid_vacancies.append(item)
        return valid_vacancies

    def get_vac_by_min_salary(self, salary_minimum):
        """Получение отфильтрованных вакансий по минимальной зарплате"""
        filtered_vac_by_min_sal = []
        for item in self.get_json()["items"]:
            if (item["salary"] is not None
                    and item["salary"]["from"] is not None
                    and item["salary"]["from"] >= salary_minimum):
                filtered_vac_by_min_sal.append(item)
        return filtered_vac_by_min_sal

    def get_top_n_vacancies_by_sal(self, vac_count):
        """Получение топ N вакансий"""
        top_n_vac = []
        for item in self.get_json()["items"]:
            if item["salary"] is not None and item["salary"]["from"] is not None:
                top_n_vac.append(item)

        final_sorted = sorted(top_n_vac, key=lambda d: d["salary"]["from"], reverse=True)

        return final_sorted[:vac_count]

    def get_vac_by_keyword(self, keyword):
        """Получение вакансий по ключевому слову"""
        key_word_vac = []
        for item in self.get_json()["items"]:
            if (item["snippet"] is not None and item["snippet"]["requirement"] is not None
                    and item["snippet"]["responsibility"] is not None):
                if (keyword in item["snippet"]["requirement"] or
                        keyword in item["snippet"]["responsibility"]):
                    key_word_vac.append(item)
        return key_word_vac

    def formatting_output_data(self, input_list):
        """Метод для преобразования json формата в читабельный формат"""
        vacancies_list = []
        counter = 1
        for item in input_list:
            if item["salary"] is None:
                salary_from = salary_to = salary_currency = "Не указано"
            else:
                if item["salary"]["from"] is None:
                    salary_from = "Не указано"
                else:
                    salary_from = item["salary"]["from"]
                if item["salary"]["to"] is None:
                    salary_to = "Не указано"
                else:
                    salary_to = item["salary"]["to"]
                salary_currency = item["salary"]["currency"]

            vacancies_items = f"""Вакансия {counter}
Наименование вакансии: {item["name"]}
Ссылка на вакансию: {item["alternate_url"]}
Зарплата от: {salary_from}
Зарплата до: {salary_to}\nВалюта: {salary_currency}
Название компании: {item["employer"]["name"]}
Требования: {item["snippet"]["requirement"]}
Обязанности: {item["snippet"]["responsibility"]}\n"""

            vacancies_list.append(vacancies_items)
            counter += 1
        return vacancies_list

    def delete_from_json(self):
        """Удаление вакансий из json"""
        with open("json_vac_info.json", "w") as file:
            pass


class HHVacancies(VacanciesJson):
    """Класс для работы с вакансиями (сравнение вакансий по зарплате)"""

    def __init__(self, number_of_vacancy, city_name, prof_name):
        super().__init__(city_name, prof_name)
        super().get_valid_vacancies_with_salary()
        all_vacancies = self.get_valid_vacancies_with_salary()
        self.salary_from = all_vacancies[number_of_vacancy - 1]["salary"]["from"]

    def __ge__(self, other):
        if isinstance(self.salary_from, int):
            return self.salary_from >= other.salary_from


class HHUserInterface:
    """Класс пользовательского интерфейса"""

    @staticmethod
    def user_interaction():
        """Функция работы с пользователем"""
        print(f"Отлично! Ты выбрал платформу HeadHunter\n")
        city_name_input = input(f"Для начала узнаем в каком "
                                f"городе необходимо найти вакансии, "
                                f"например, Санкт-Петербург или Казань:\n"
                                f"(Только вводи существующий город, иначе получишь кулебяку)"
                                f"\n> ").capitalize()
        prof_input = input(
            f"А теперь мне необходимо узнать название профессии, например "
            f"Python разработчик или Визажист:\n> ").capitalize()
        hh_instance = VacanciesJson(city_name_input, prof_input)
        hh_instance.save_to_json()
        print()
        if len(hh_instance.get_all_vac_info()) == 0:
            print(f"Упс. Кажется не нашлось ни одной вакансии! Давай сначала!")
        else:
            print(f"Найденное количество вакансий: {len(hh_instance.get_all_vac_info())}")
            print()
            while True:
                print()
                function_input = input(f"Доступны следующие действия:\n"
                                       f"1 - Вывести весь список вакансий (не более 100)\n"
                                       f"2 - Вывести топ N вакансий (по убыванию)\n"
                                       f"3 - Отфильтровать список по зарплате "
                                       f"(указывается минимальная ЗП)\n"
                                       f"4 - Найти вакансию по ключевому слову\n"
                                       f"5 - Очистить список вакансий\n"
                                       f"6 - Сравнить две вакансии по зарплате\n"
                                       f"0 - Вернуться к выбору платформы и вакансий (выйти)\n> ")

                # Вывод полного списка вакансий
                if function_input == "1":
                    all_vacancies = hh_instance.get_all_vac_info()
                    for item in hh_instance.formatting_output_data(all_vacancies):
                        print(item)

                # Вывод топ N вакансий
                elif function_input == "2":
                    n_input = int(input(f"Введите желаемое количество вакансий для "
                                        f"обработки:\n> "))
                    top_n_vacancies = hh_instance.get_top_n_vacancies_by_sal(n_input)
                    for item in hh_instance.formatting_output_data(top_n_vacancies):
                        print(item)

                # Вывод отфильтрованных вакансий по минимальной зарплате
                elif function_input == "3":
                    n_input = int(input(f"Введите минимальный уровень зарплаты:\n> "))
                    vac_by_min_salary = hh_instance.get_vac_by_min_salary(n_input)
                    for item in hh_instance.formatting_output_data(vac_by_min_salary):
                        print(item)

                # Вывод вакансий по ключевому слову в описании
                elif function_input == "4":
                    keyword_input = input(f"Введите ключевое слово:\n> ")
                    key_word_filtered_list = hh_instance.get_vac_by_keyword(keyword_input)
                    if len(key_word_filtered_list) > 0:

                        for item in hh_instance.formatting_output_data(key_word_filtered_list):
                            print(item)
                    else:
                        print(f"Упс. Кажется такого слова нет ни в одном описании найденных "
                              f"вакансии")

                # Очистка списка вакансий
                elif function_input == "5":
                    hh_instance.delete_from_json()
                    print(f"Список вакансий очищен! Давай сначала!")
                    break

                # Сравнение двух вакансий по минимальной зарплате
                elif function_input == "6":
                    all_vacancies = hh_instance.get_valid_vacancies_with_salary()
                    for item in hh_instance.formatting_output_data(all_vacancies):
                        print(item)
                    print(f"Вот вакансии доступные для сравнения. В других не указана "
                          f"зарплата.\n")
                    first_vac_num_input = int(input(f"Введи порядковый номер первой "
                                                    f"вакансии:\n> "))
                    hh_inst_1 = HHVacancies(first_vac_num_input, None, None)
                    second_vac_num_input = int(input(f"Введи порядковый номер второй "
                                                     f"вакансии:\n> "))
                    hh_inst_2 = HHVacancies(second_vac_num_input, None, None)

                    if hh_inst_1 >= hh_inst_2:
                        print(f"Первая выбранная вакансия имеет наибольшую зарплату!")
                    else:
                        print(f"Вторая выбранная вакансия имеет наибольшую зарплату!")

                # Возвращение к выбору платформы
                elif function_input == "0":
                    break

                # Защита от неверного выбора функции
                else:
                    print()
                    print(f"Сначала выбери функцию!")
