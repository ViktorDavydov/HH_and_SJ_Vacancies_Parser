import requests
import json
import os

from abstract_classes import GetVacanciesByAPI, VacanciesInFileJson


class SJGetVacByAPI(GetVacanciesByAPI):
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

        return vacancies


class VacanciesJson(SJGetVacByAPI, VacanciesInFileJson):
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
        return self.get_json()["objects"]

    def get_valid_vacancies_with_salary(self):
        """Получение вакансий только с указанными минимальными зарплатами"""
        valid_vacancies = []
        for item in self.get_json()["objects"]:
            if item["payment_from"] != 0:
                valid_vacancies.append(item)
        return valid_vacancies

    def get_vac_by_min_salary(self, salary_minimum):
        """Получение отфильтрованных вакансий по минимальной зарплате"""
        filtered_vac_by_min_sal = []
        for item in self.get_json()["objects"]:
            if item["payment_from"] != 0 and item["payment_from"] >= salary_minimum:
                filtered_vac_by_min_sal.append(item)
        return filtered_vac_by_min_sal

    def get_top_n_vacancies_by_sal(self, vac_count):
        """Получение топ N вакансий"""
        top_n_vac = []
        for item in self.get_json()["objects"]:
            if item["payment_from"] != 0:
                top_n_vac.append(item)

        final_sorted = sorted(top_n_vac, key=lambda d: d["payment_from"], reverse=True)

        return final_sorted[:vac_count]

    def get_vac_by_keyword(self, keyword):
        """Получение вакансий по ключевому слову"""
        key_word_vac = []
        for item in self.get_json()["objects"]:
            if item["candidat"] is not None:
                if keyword in item["candidat"]:
                    key_word_vac.append(item)
        return key_word_vac

    def formatting_output_data(self, input_list):
        """Метод для преобразования json формата в читабельный формат"""
        vacancies_list = []
        counter = 1
        for item in input_list:
            if item["payment_from"] == item["payment_to"] == 0:
                payment_from = payment_to = currency = "Не указано"
            else:
                if item["payment_from"] == 0:
                    payment_from = "Не указано"
                else:
                    payment_from = item["payment_from"]
                if item["payment_to"] == 0:
                    payment_to = "Не указано"
                else:
                    payment_to = item["payment_to"]
                currency = item["currency"]

            vacancies_items = f"""Вакансия {counter}
Наименование вакансии: {item["profession"]}
Ссылка на вакансию: {item["link"]}
Зарплата от: {payment_from}
Зарплата до: {payment_to}\nВалюта: {currency}
Название компании: {item["client"]["title"]}
Описание вакансии: {item["candidat"]}\n"""

            vacancies_list.append(vacancies_items)
            counter += 1
        return vacancies_list

    def delete_from_json(self):
        """Удаление вакансий из json"""
        with open("json_vac_info.json", "w") as file:
            pass


class SJVacancies(VacanciesJson):
    """Класс для работы с вакансиями (сравнение вакансий по зарплате)"""

    def __init__(self, number_of_vacancy, city_name, prof_name):
        super().__init__(city_name, prof_name)
        super().get_valid_vacancies_with_salary()
        all_vacancies = self.get_valid_vacancies_with_salary()
        self.salary_from = all_vacancies[number_of_vacancy - 1]["payment_from"]

    def __ge__(self, other):
        if isinstance(self.salary_from, int):
            return self.salary_from >= other.salary_from


class SJUserInterface:
    """Класс пользовательского интерфейса"""

    @staticmethod
    def user_interaction():
        """Функция работы с пользователем"""
        print(f"Отлично! Ты выбрал платформу SuperJob\n")
        city_name_input = input(f"Для начала узнаем в каком "
                                f"городе необходимо найти вакансии, "
                                f"например, Санкт-Петербург или Казань:\n"
                                f"(Только вводи существующий город, иначе получишь кулебяку)"
                                f"\n> ").capitalize()
        prof_input = input(
            f"А теперь мне необходимо узнать название профессии, например "
            f"Python разработчик или Визажист:\n> ").capitalize()
        sj_instance = VacanciesJson(city_name_input, prof_input)
        sj_instance.save_to_json()
        print()
        if len(sj_instance.get_all_vac_info()) == 0:
            print(f"Упс. Кажется не нашлось ни одной вакансии! Давай сначала!")
        else:
            print(f"Найденное количество вакансий: {len(sj_instance.get_all_vac_info())}\n")
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
                    all_vacancies = sj_instance.get_all_vac_info()
                    for item in sj_instance.formatting_output_data(all_vacancies):
                        print(item)

                # Вывод топ N вакансий
                elif function_input == "2":
                    n_input = int(input(f"Введите желаемое количество вакансий для обработки:"
                                        f"\n> "))
                    top_n_vacancies = sj_instance.get_top_n_vacancies_by_sal(n_input)
                    for item in sj_instance.formatting_output_data(top_n_vacancies):
                        print(item)

                # Вывод отфильтрованных вакансий по минимальной зарплате
                elif function_input == "3":
                    n_input = int(input(f"Введите минимальный уровень зарплаты:\n> "))
                    vac_by_min_salary = sj_instance.get_vac_by_min_salary(n_input)
                    for item in sj_instance.formatting_output_data(vac_by_min_salary):
                        print(item)

                # Вывод вакансий по ключевому слову в описании
                elif function_input == "4":
                    keyword_input = input(f"Введите ключевое слово:\n> ")
                    key_word_filtered_list = sj_instance.get_vac_by_keyword(keyword_input)
                    if len(key_word_filtered_list) > 0:

                        for item in sj_instance.formatting_output_data(key_word_filtered_list):
                            print(item)
                    else:
                        print(f"Упс. Кажется такого слова нет ни в одном описании найденных "
                              f"вакансии")

                # Очистка списка вакансий
                elif function_input == "5":
                    sj_instance.delete_from_json()
                    print(f"Список вакансий очищен! Давай сначала!")
                    break

                # Сравнение двух вакансий по минимальной зарплате
                elif function_input == "6":
                    all_vacancies = sj_instance.get_valid_vacancies_with_salary()
                    for item in sj_instance.formatting_output_data(all_vacancies):
                        print(item)
                    print(f"Вот вакансии доступные для сравнения. В других не указана "
                          f"зарплата.\n")
                    first_vac_num_input = int(input(f"Введи порядковый номер первой "
                                                    f"вакансии:\n> "))
                    sj_inst_1 = SJVacancies(first_vac_num_input, None, None)
                    second_vac_num_input = int(input(f"Введи порядковый номер второй "
                                                     f"вакансии:\n> "))
                    sj_inst_2 = SJVacancies(second_vac_num_input, None, None)

                    if sj_inst_1 >= sj_inst_2:
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
