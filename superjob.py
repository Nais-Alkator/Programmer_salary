import requests
import os
from dotenv import load_dotenv
from secondary_functions import print_statistics_table_view
from terminaltables import AsciiTable
load_dotenv()

SUPERJOB_TOKEN = os.getenv("SUPERJOB_TOKEN")
URL = "https://api.superjob.ru/2.0/vacancies/"
HEADERS = {"X-Api-App-Id": SUPERJOB_TOKEN}
TOWN_ID = 4
CATALOG_OF_PROFESSION = 48
COUNT = 100


def get_predicted_rub_salaries_for_superjob(vacancy):
    data = get_global_data(vacancy)
    predicted_rub_salaries = list()
    for item in data:
    	for salary in item:
            if salary["currency"] == "rub":
                if salary["payment_from"] == 0 and salary["payment_to"] == 0:
                    average_salary = None
                elif salary["payment_from"] != 0 and salary["payment_to"] == 0:
                    average_salary = salary["payment_from"] * 0.8
                elif salary["payment_from"] == 0 and salary["payment_to"] != 0:
                    average_salary = salary["payment_to"] * 0.8
                elif salary["payment_from"] != 0 and salary["payment_to"] != 0:
                    average_salary = (
                        salary["payment_from"] + salary["payment_to"]) / 2
                predicted_rub_salaries.append(average_salary)
    return predicted_rub_salaries


def get_global_data(language):
    global_data = list()
    page = 0
    pages_number = 1
    while page < pages_number:
        params = {
            "keyword": "Разработчик {}".format(language),
            "town": TOWN_ID,
            "catalogues": CATALOG_OF_PROFESSION, "count": COUNT}
        page_data = requests.get(URL, params=params, headers=HEADERS)
        page_data.raise_for_status()
        page_data = page_data.json()
        pages_number = page_data['total']
        print("{} Добавлено из {}".format(page, page_data["total"]))
        page += 1
        global_data.append(page_data["objects"])
    return global_data


def get_vacancy_processed(predicted_salaries):
    vacancy_prosecced = 0
    for salary in predicted_salaries:
        if salary != None:
            vacancy_prosecced += 1
    return vacancy_prosecced


def get_average_salary_for_one_vacancy(predicted_salaries):
    average_salaries_for_count = list()
    for salary in predicted_salaries:
        if salary is not None:
            salary = int(salary)
            average_salaries_for_count.append(salary)
    if len(average_salaries_for_count) != 0:
        final_average_salary = sum(
            average_salaries_for_count) / len(average_salaries_for_count)
    else:
        final_average_salary = 0
    return int(final_average_salary)


def get_statistics_for_languages():
    top_10_programming_languages = [
        "Javascript",
        "Java",
        "Python",
        "Ruby",
        "PHP",
        "C++",
        "C#",
        "C",
        "Go",
        "Scala"]
    statistics_for_all_languages = dict()
    for language in top_10_programming_languages:
        predicted_salaries = get_predicted_rub_salaries_for_superjob(language)
        statistics_for_all_languages[language] = {
                "vacancy_found": len(predicted_salaries),
                "vacancy_processed": get_vacancy_processed(predicted_salaries),
                "average_salary": get_average_salary_for_one_vacancy(predicted_salaries)
            }
    return statistics_for_all_languages


if __name__ == "__main__":
	try:
	    STAT_FOR_LANGUAGES = get_statistics_for_languages()
	except requests.exceptions.HTTPError as error:
		exit("Can't get data from server:\n{0}".format(error))
	try:
		print_statistics_table_view(STAT_FOR_LANGUAGES)
	except requests.exceptions.ConnectionError as error:
		exit("Can't get data from server:\n{0}".format(error))
	except requests.exceptions.HTTPError as error:
		exit("Can't get data from server:\n{0}".format(error))

