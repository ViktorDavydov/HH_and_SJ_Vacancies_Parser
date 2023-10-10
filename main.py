from hh_vac_getter import HHApiEngine, hh_vac_info_validation, hh_data_formatting
from sj_vac_getter import SJApiEngine, sj_vac_info_validation, sj_data_formatting
from json_manager import JsonOperator
from user_interface import UserInterface

if __name__ == "__main__":
    print(f"Привет! Я программа для сбора информации о вакансиях! Приступим!\n")
    while True:
        platform_input = input(f"Выбери платформу:\n1 - HeadHunter\n2 - SuperJob\n0 - Выйти\n> ")
        if platform_input not in ["0", "1", "2"]:
            print(f"Упс. Кажется в моей базе нет такой платформы. Попробуй еще раз!")
            print()
        else:
            platform = {
                "1": "HeadHunter",
                "2": "SuperJob"
            }
            if platform_input == "0":
                print("Всего хорошего!")
                break
            else:
                print(f"Отлично! Ты выбрал платформу {platform[platform_input]}\n")
                city_name_input = input(f"Для начала узнаем в каком "
                                        f"городе необходимо найти вакансии, "
                                        f"например, Санкт-Петербург или Казань:\n"
                                        f"(Только вводи существующий город, иначе получишь "
                                        f"кулебяку)"
                                        f"\n> ").capitalize()
                prof_input = input(f"А теперь мне необходимо узнать название профессии, например "
                                   f"Python разработчик или Визажист:\n> ").capitalize()
                if platform_input == "1":
                    hh_block = HHApiEngine(city_name_input, prof_input)
                    vac_source = hh_block.get_vacancies()  # Получение вакансий с HeadHunter
                    hh_valid_vac = hh_vac_info_validation(vac_source)  # Валидация вакансий
                    fin_valid_list = hh_data_formatting(hh_valid_vac)  # Приведение к общему виду

                elif platform_input == "2":
                    sj_block = SJApiEngine(city_name_input, prof_input)
                    vac_source = sj_block.get_vacancies()  # Получение вакансий с SuperJob
                    sj_valid_vac = sj_vac_info_validation(vac_source)  # Валидация вакансий
                    fin_valid_list = sj_data_formatting(sj_valid_vac)  # Приведение к общему виду

            json_list = JsonOperator(fin_valid_list)
            json_list.save_to_json()
            work_vac_list = json_list.get_json()
            user_instance = UserInterface(work_vac_list)
            user_instance.functions_exe()
