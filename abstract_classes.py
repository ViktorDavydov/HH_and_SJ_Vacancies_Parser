from abc import ABC, abstractmethod


class GetVacanciesByAPI(ABC):

    @abstractmethod
    def get_city_id(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class VacanciesInFileJson(ABC):

    @abstractmethod
    def save_to_json(self):
        pass

    @abstractmethod
    def get_json(self):
        pass

    @abstractmethod
    def get_all_vac_info(self):
        pass

    @abstractmethod
    def get_vac_by_min_salary(self, salary_minimum):
        pass

    @abstractmethod
    def get_top_n_vacancies_by_sal(self, vac_count):
        pass

    @abstractmethod
    def get_vac_by_keyword(self, keyword):
        pass

    @abstractmethod
    def formatting_output_data(self, input_list):
        pass

    @abstractmethod
    def delete_from_json(self):
        pass
