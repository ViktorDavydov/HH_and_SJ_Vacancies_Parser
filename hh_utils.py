import requests
import json
import os
import time

from abstract_classes import GetVacanciesByAPI, VacanciesJson


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


class HHVacanciesInfo(HHGetVacByAPI):

    def __init__(self, city_name, prof_name):
        super().__init__(city_name, prof_name)
        # self.title = None
        # self.url = None
        # self.salary_from = None
        # self.salary_to = None
        # self.company_name = None
        # self.description = None
        self.vacancies_list = []

    def get_vac_info(self):
        for item in self.get_vacancies()["items"]:
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


class VacanciesInJson(VacanciesJson):
    def __init__(self):
        pass

    def save_to_json(self):
        pass

    def add_to_json(self):
        pass

    def get_from_json(self):
        pass

    def delete_from_json(self):
        pass
