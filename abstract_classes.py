from abc import ABC, abstractmethod


class ApiEngine(ABC):

    @abstractmethod
    def get_city_id(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class JsonManager(ABC):

    @abstractmethod
    def save_to_json(self):
        pass

    @abstractmethod
    def get_json(self):
        pass

    @abstractmethod
    def delete_from_json(self):
        pass



