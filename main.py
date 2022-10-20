import os

import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv


def search_job_hh(language):
    page = 1
    pages = 2
    vacancies_processed = 0
    average_salary = 0
    location = 1
    salaries = []
    while page < pages:
        payload = {
            "area": location,
            "text": f"програмист {language}",
            "page": page
        }
        response = requests.get('https://api.hh.ru/vacancies', params=payload)
        response.raise_for_status()
        response_payload = response.json()
        pages = response_payload['pages']
        page += 1
        for vacancy in response_payload["items"]:
            if not vacancy["salary"]:
                continue
            predicted_salary = predict_rub_salary(
                vacancy["salary"]["from"],
                vacancy["salary"]["to"],
                vacancy["salary"]["currency"]
            )
            if predicted_salary:
                salaries.append(predicted_salary)
                vacancies_processed += 1
    if vacancies_processed:
        average_salary = sum(salaries)/len(salaries)
    return{
        "vacancies_found": response_payload['found'],
        "vacancies_processed": vacancies_processed,
        "average_salary": int(average_salary)
    }


def search_job_superjob(language, superjob_key):
    salaries = []
    vacancies_processed = 0
    average_salary = 0
    headers = {
        'X-Api-App-Id': superjob_key,
    }
    payload = {
        "town": "Москва",
        "keyword": f"програмист {language}",
    }
    response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=payload)
    response.raise_for_status()
    response_payload = response.json()
    for vacancy in response_payload["objects"]:
        predicted_salary = predict_rub_salary(
            vacancy["payment_from"],
            vacancy["payment_to"],
            vacancy["currency"]
        )
        if predicted_salary:
            salaries.append(predicted_salary)
            vacancies_processed += 1
    if vacancies_processed:
        average_salary = sum(salaries)/len(salaries)
    return{
        "vacancies_found": response_payload['total'],
        "vacancies_processed": vacancies_processed,
        "average_salary": int(average_salary)
    }


def predict_rub_salary(payment_from, payment_to, currency):
    if not currency == "RUR" and not currency == "rub":
        return
    if payment_from and payment_to:
        return (payment_from + payment_to) / 2
    elif payment_from:
        return payment_from * 1.2
    elif payment_to:
        return payment_to * 0.8


def create_table(language_information):
    table_pyload = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for language, language_pyload in language_information.items():
        table_row = [language, language_pyload["vacancies_found"], language_pyload["vacancies_processed"], language_pyload["average_salary"]]
        table_pyload.append(table_row)
    return table_pyload


if __name__ == "__main__":
    load_dotenv()
    superjob_key = os.environ["SJ_KEY"]
    programming_languages = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "CSS", "C#", "C", "Go" ]
    language_information_hh = {}
    language_information_superjob = {}
    for language in programming_languages:
        language_information_hh[language]=search_job_hh(language)
        language_information_superjob[language]=search_job_superjob(language, superjob_key)
    finished_table_hh = AsciiTable(create_table(language_information_hh), "API_hh")
    finished_table_superjob = AsciiTable(create_table(language_information_superjob), "API_superjob")
    print(finished_table_hh.table)
    print(finished_table_superjob.table)
