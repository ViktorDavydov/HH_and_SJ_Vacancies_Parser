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

    def get_json(self):
        pass

    def get_all_vac_info(self):
        pass

    def get_vac_by_min_salary(self, salary_minimum):
        pass

    def get_top_n_vacancies_by_sal(self, vac_count):
        pass

    def get_vac_by_keyword(self, keyword):
        pass

    def delete_from_json(self):
        pass
