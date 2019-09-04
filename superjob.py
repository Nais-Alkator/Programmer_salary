import requests
import os
from dotenv import load_dotenv
from secondary_functions import print_statistics_table_view, predict_salary
from terminaltables import AsciiTable
load_dotenv()

SUPERJOB_TOKEN = os.getenv("SUPERJOB_TOKEN")
URL = "https://api.superjob.ru/2.0/vacancies/"
HEADERS = {"X-Api-App-Id": SUPERJOB_TOKEN}
TOWN_ID = 4
CATALOG_OF_PROFESSION = 48
COUNT = 100


def get_global_vacancy_data(language):
    global_vacancy_data = list()
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
        global_vacancy_data.extend(page_data["objects"])
    return global_vacancy_data


def get_vacancy_processed(predicted_salaries):
    vacancy_processed = 0
    for salary in predicted_salaries:
        if salary != None:
            vacancy_processed += 1
    return vacancy_processed


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
    	global_vacancy_data = get_global_vacancy_data(language)
    	predicted_salaries = [predict_salary(salary["payment_from"], salary["payment_to"]) for salary in global_vacancy_data if salary["currency"] == "rub"]
    	statistics_for_all_languages[language] = {
                "vacancy_found": len(predicted_salaries),
                "vacancy_processed": get_vacancy_processed(predicted_salaries),
                "average_salary": get_average_salary_for_one_vacancy(predicted_salaries)
            }
    return statistics_for_all_languages


if __name__ == "__main__":
	try:
	    stat_for_langguages = get_statistics_for_languages()
	except requests.exceptions.HTTPError as error:
		exit("Can't get data from server:\n{0}".format(error))
	except requests.exceptions.HTTPError as error:
		exit("Can't get data from server:\n{0}".format(error))
	print_statistics_table_view(stat_for_langguages)
	

