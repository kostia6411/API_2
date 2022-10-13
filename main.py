import os

import requests
from terminaltables import AsciiTable


def job_search(language):
    page = 1
    pages = 2
    vacancies_processed = 0
    average_salary = 0
    salaries = []
    while page < pages:
        payload = {
            "area": 1,
            "text": f"програмист {language}",
            "page": page
        }
        response = requests.get('https://api.hh.ru/vacancies', params=payload)
        response.raise_for_status()
        pages = response.json()['pages']
        page += 1
        for vacancy in response.json()["items"]:
            if vacancy["salary"]:
                predicted_salary = predict_rub_salary(vacancy["salary"])
                if predicted_salary:
                    salaries.append(predicted_salary)
                    vacancies_processed += 1
    if vacancies_processed:
        average_salary = sum(salaries)/len(salaries)
    return{
        "vacancies_found": response.json()['found'],
        "vacancies_processed": vacancies_processed,
        "average_salary": int(average_salary)
    }


def superjob(language):
    salaries = []
    vacancies_processed = 0
    average_salary = 0
    superjob_key = os.environ["SJ_KEY"]
    headers = {
        'X-Api-App-Id': superjob_key,
    }
    payload = {
        "town": "Москва",
        "keyword": f"програмист {language}",
    }
    response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=payload)
    response.raise_for_status()
    for vacancy in response.json()["objects"]:
                predicted_salary = predict_rub_salary_for_superjob(vacancy)
                if predicted_salary:
                    salaries.append(predicted_salary)
                    vacancies_processed += 1
    if vacancies_processed:
        average_salary = sum(salaries)/len(salaries)
    return{
        "vacancies_found": response.json()['total'],
        "vacancies_processed": vacancies_processed,
        "average_salary": int(average_salary)
    }


def predict_rub_salary_for_superjob(salary):
    if salary["currency"] == "rub":
        if salary["payment_from"] and salary["payment_to"]:
            return (salary["payment_from"] + salary["payment_to"]) / 2
        elif salary["payment_from"]:
            return salary["payment_from"] * 1.2
        elif salary["payment_to"]:
            return salary["payment_to"] * 0.8


def predict_rub_salary(salary):
    if salary["currency"] == "RUR":
        if salary["from"] and salary["to"]:
            return (salary["from"] + salary["to"]) / 2
        elif salary["from"]:
            return salary["from"] * 1.2
        elif salary["to"]:
            return salary["to"] * 0.8


def creating_table(language_information):
    table_pyload = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for language, language_pyload in language_information.items():
        table_row = [language, language_pyload["vacancies_found"], language_pyload["vacancies_processed"], language_pyload["average_salary"]]
        table_pyload.append(table_row)
    return table_pyload


if __name__ == "__main__":
    programming_languages = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "CSS", "C#", "C", "Go" ]
    language_information_hh = {}
    language_information_superjob = {}
    for language in programming_languages:
        language_information_hh[language]=job_search(language)
        language_information_superjob[language]=superjob(language)
    finished_table_hh = AsciiTable(creating_table(language_information_hh), "API_hh")
    finished_table_superjob = AsciiTable(creating_table(language_information_superjob), "API_superjob")
    print(finished_table_hh.table)
    print(finished_table_superjob.table)
