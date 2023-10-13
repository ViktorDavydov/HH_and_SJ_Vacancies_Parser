import requests
from abstract_classes import ApiEngine


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


def hh_vac_info_validation(hh_vac_source_list):
    """Проверка входящих данных на корректность"""
    hh_valid_vacancies = []
    for vacancies in hh_vac_source_list:
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
            hh_valid_vacancies.append(vacancies)
    return hh_valid_vacancies


def hh_data_formatting(hh_vac_valid_list):
    """Метод для преобразования json формата в читабельный формат"""
    hh_formed_vac = []
    for vacancy in hh_vac_valid_list:
        vacancies_items = {
            "Наименование вакансии": vacancy["name"],
            "Ссылка на вакансию": vacancy["alternate_url"],
            "Зарплата от": vacancy["salary"]["from"],
            "Зарплата до": vacancy["salary"]["to"],
            "Валюта": vacancy["salary"]["currency"],
            "Название компании": vacancy["employer"]["name"],
            "Требования и обязанности": f"""{vacancy["snippet"]["requirement"]}
{vacancy["snippet"]["responsibility"]}"""
        }

        hh_formed_vac.append(vacancies_items)
    return hh_formed_vac
