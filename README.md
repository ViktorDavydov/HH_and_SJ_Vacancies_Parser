# Парсер вакансий на платформах HeadHunter и SuperJob

### Установка:
- Убедитесь, что у вас установлен python 3.11 или более новая версия<br>
- Склонировать репозиторий<br>
- Создать и активировать виртуальное окружение```python -m venv ваша_папка_для_виртуального_окружения```<br>
- Установить зависимости командой ```pip install -r requirements.txt```<br>

### Используемые библиотеки:
- requests<br>

### Логика работы системы:
После запуска программы необходимо выбрать платформу для сбора вакансий или ввести "0" для выхода:<br>
- 1 - HeadHunter
- 2 - SuperJob
- 0 - Выход

Далее ввести наименование города в котором необходимо найти вакансии, затем ввести название вакансии.

После поиска будет выведена информация о количестве найденных вакансий. Если не найдено ни одной 
вакансии, производится возврат на этап выбора платформы.

Если вакансии найдены, будет выведено контекстное меню со следующим функционалом:<br>
- 1 - Вывести весь список вакансий (не более 100)
- 2 - Вывести топ N вакансий (по убыванию)
- 3 - Отфильтровать список по зарплате (указывается минимальная ЗП)
- 4 - Найти вакансию по ключевому слову
- 5 - Очистить список вакансий
- 6 - Сравнить две вакансии по зарплате
- 0 - Вернуться к выбору платформы и вакансий (выйти)

Для выбора функционала необходимо ввести его порядковый номер.
Данным функционалом предусмотрено:

1 - Вывод всего списка найденных вакансий (не более 100).
***
2 - Вывод топ N вакансий по убыванию. N - число вакансий для вывода, указывается пользователем.
    Вакансии выводятся по убыванию по минимальной указанной зарплате. 
***
3 - Вывод отфильтрованного списка вакансий по минимальной зарплате. Сумма минимальной зарплаты
    указывается пользователем.
***
4 - Вывод вакансии/вакансий по ключевому слову, указанному в описании, требованиях или обязанностях.
    Ключевое слово указывается пользователем.
***
5 - Очистка списка вакансий. После выбора функции происходит возврат к выбору платформы.
***
6 - Вывод результата сравнения двух вакансий по минимальной зарплате. Вакансии, в которых
    не указана минимальная зарплата учтены не будут. Пользователь вводит порядковые номера первой
    и второй вакансий для сравнения. Выводится информация о том в какой выбранной вакансии 
    наибольшая зарплата (в первой или во второй).
***
0 - Выход из контекстного меню функций. Возврат к выбору платформы.
