from abc import ABC


class GetVacanciesByAPI(ABC):
    pass

    def get_city_id(self):
        pass

    def get_vacancies(self):
        pass


class VacanciesJson(ABC):
    pass

    def save_to_json(self):
        pass

    def add_to_json(self):
        pass

    def get_from_json(self):
        pass

    def delete_from_json(self):
        pass
