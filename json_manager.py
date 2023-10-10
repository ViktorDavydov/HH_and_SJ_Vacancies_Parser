import json
from abstract_classes import JsonManager


class JsonOperator(JsonManager):
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

    @classmethod
    def delete_from_json(cls):
        """Удаление вакансий из json"""
        with open("json_vac_info.json", "w") as file:
            pass

    def get_vacancies_by_sal(self, salary):
        """Поиск вакансии по ЗП"""
        chosen_vacancies = [item for item in self.valid_vacancies
                            if item["Зарплата от"] == salary]
        if len(chosen_vacancies) > 0:
            return chosen_vacancies
        return "Упс. Кажется не нашлось ни одной вакансии с указанной зарплатой"
