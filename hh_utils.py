import requests
import json

from abstract_classes import GetVacanciesByAPI, VacanciesInJson


class HHGetVacByAPI(GetVacanciesByAPI):
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
        params = {
            "text": self.city_name
        }
        hh_areas_url = self.hh_api_url + "/suggests/areas"
        response = requests.get(hh_areas_url, params=params, headers=self.headers)

        for city in response.json()["items"]:
            if city["text"] == self.city_name:
                return city["id"]

    def get_vacancies(self):
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


class HHVacancies:

    def __init__(self, title, url, salary_from, salary_to, salary_currency,
                 company_name, description):
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.company_name = company_name
        self.description = description

    def __repr__(self):
        return (f"Данная вакансия имеет следующие параметры:"
                f"Наименование вакансии: {self.title}"
                f"Ссылка на вакансию: {self.url}"
                f"Зарплата от: {self.salary_from}"
                f"Зарплата до: {self.salary_to}"
                f"Валюта: {self.salary_currency}"
                f"Название компании: {self.company_name}"
                f"Требования: {self.description}")

    def __str__(self):
        return (f"Наименование вакансии: {self.title}"
                f"Ссылка на вакансию: {self.url}"
                f"Зарплата от: {self.salary_from}"
                f"Зарплата до: {self.salary_to}"
                f"Валюта: {self.salary_currency}"
                f"Название компании: {self.company_name}"
                f"Требования: {self.description}")

    def __ge__(self, other):
        if isinstance(self.salary_from, int):
            result = self.salary_from >= other.salary_from
        else:
            result = "Упс. Кажется в одной из вакансий не указана минимальная ЗП"

        return result


class VacanciesJson(HHGetVacByAPI, VacanciesInJson):
    def __init__(self, city_name, prof_name):
        super().__init__(city_name, prof_name)
        self.vacancies_list = []
        self.filtered_vac_by_min_sal = []
        self.top_n_vac = []

    def save_to_json(self):
        with open("json_vac_info.json", "w", encoding="utf-8") as file:
            json.dump(self.get_vacancies(), file, indent=2, ensure_ascii=False)

    def get_json(self):
        with open("json_vac_info.json", "r", encoding="utf-8") as file:
            vacancies_info = json.load(file)
            return vacancies_info

    def get_all_vac_info(self):
        for item in self.get_json()["items"]:
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

            vacancies_dict = {
                "Наименование вакансии": item["name"],
                "Ссылка на вакансию": item["alternate_url"],
                "Зарплата от: ": salary_from,
                "Зарплата до: ": salary_to,
                "Валюта": salary_currency,
                "Название компании": item["employer"]["name"],
                "Требования": item["snippet"]["requirement"],
                "Обязанности": item["snippet"]["responsibility"]
            }

            self.vacancies_list.append(vacancies_dict)

        return self.vacancies_list

    def get_vac_by_min_salary(self, salary_minimum):

        for item in self.get_json()["items"]:
            if (item["salary"] is not None
                    and item["salary"]["from"] is not None
                    and item["salary"]["from"] >= salary_minimum):
                self.filtered_vac_by_min_sal.append(item)
        return self.filtered_vac_by_min_sal

    def get_top_n_vacancies_by_sal(self, vac_count):
        for item in self.get_json()["items"]:
            if item["salary"] is not None and item["salary"]["from"] is not None:
                self.top_n_vac.append(item)

        final_sorted = sorted(self.top_n_vac, key=lambda d: d["salary"]["from"], reverse=True)

        return final_sorted[:vac_count]

    def get_vac_by_keyword(self, keyword):
        for item in self.get_json()["items"]:
            if (item["snippet"] is not None and item["snippet"]["requirement"] is not None
                    and item["snippet"]["responsibility"] is not None):
                if (keyword in item["snippet"]["requirement"] or
                        keyword in item["snippet"]["responsibility"]):
                    return item

    def delete_from_json(self):
        with open("json_vac_info.json", "w") as file:
            pass


class HHUserInterface:

    def user_interaction(self):
        print(f"Отлично! Ты выбрал платформу HeadHunter\n")
        city_name_input = input(f"Для начала узнаем в каком "
                                f"городе вы ищете вакансии, "
                                f"например, Москва или Казань:\n> ").capitalize()
        prof_input = input(
            f"А теперь мне необходимо узнать название профессии, например"
            f"Python разработчик или Визажист:\n> ").capitalize()
        hh_instance = VacanciesJson(city_name_input, prof_input)
        hh_instance.save_to_json()
        while True:
            function_input = input(f"Доступны следующие действия:\n"
                                   f"1 - Вывести весь список вакансий (не более 100)\n"
                                   f"2 - Вывести топ N вакансий (по убыванию)\n"
                                   f"3 - Отфильтровать список по зарплате "
                                   f"(указывается минимальная ЗП)\n"
                                   f"4 - Найти вакансию по ключевому слову\n> ")

            if function_input == "1":
                for vacancy in hh_instance.get_all_vac_info():
                    print(f"{json.dumps(vacancy, indent=2, ensure_ascii=False)}")

