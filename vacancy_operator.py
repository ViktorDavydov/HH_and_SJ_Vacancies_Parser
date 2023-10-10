class VacancyOperator:
    """Класс для валидации данных и сравнения вакансий по минимальной зарплате"""

    def __init__(self, valid_vacancies_list):
        self.valid_vacancies_list = valid_vacancies_list

    def two_vac_comp_by_min_sal(self, first_num, second_num):
        """Метод сравнения двух вакансий по минимальной зарплате"""
        min_salary_1 = self.valid_vacancies_list[first_num - 1]["Зарплата от"]
        min_salary_2 = self.valid_vacancies_list[second_num - 1]["Зарплата от"]

        return min_salary_1 >= min_salary_2

    def get_vac_by_min_salary(self, salary_minimum):
        """Получение отфильтрованных вакансий по минимальной зарплате"""
        filtered_vac_by_min_sal = [item for item in self.valid_vacancies_list
                                   if item["Зарплата от"] >= salary_minimum]

        return filtered_vac_by_min_sal

    def get_top_n_vacancies_by_sal(self, vac_count):
        """Получение топ N вакансий"""
        source_list = self.valid_vacancies_list
        final_sorted = sorted(source_list,
                              key=lambda d: d["Зарплата от"], reverse=True)

        return final_sorted[:vac_count]

    def get_vac_by_keyword(self, keyword):
        """Получение вакансий по ключевому слову"""
        key_word_vac = [item for item in self.valid_vacancies_list if keyword
                        in item["Требования и обязанности"]]

        return key_word_vac

    def get_all_valid_vacancies(self):
        """Получение всех вакансий"""
        return self.valid_vacancies_list
