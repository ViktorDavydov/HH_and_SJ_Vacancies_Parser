from hh_utils import HHVacanciesInfo
from sj_utils import SJAPI
import json


city_name_input = input(f"Введите название города: ")
prof_input = input(f"Введите название профессии: ")

hh = HHVacanciesInfo(city_name_input, prof_input)
sj = SJAPI()


print(json.dumps(hh.get_vac_info(), indent=2, ensure_ascii=False))

