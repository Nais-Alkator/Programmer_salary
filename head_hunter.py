import requests
from terminaltables import AsciiTable, DoubleTable, SingleTable
from secondary_functions import print_statistics_table_view, predict_salary
from terminaltables import AsciiTable

URL = "https://api.hh.ru/vacancies/"
HEADERS = {"User-Agent": "User-Agent"}
SEARCH_AREA = 1
SEARCH_PERIOD = 30


def get_quantity_of_vacancies(vacancy):
    params = {
        "text": "Разработчик {}".format(vacancy),
        "area": SEARCH_AREA,
        "period": SEARCH_PERIOD}
    response = requests.get(URL, params=params, headers=HEADERS)
    response.raise_for_status()
    response = response.json()
    quantity_of_vacancy = response["found"]
    return quantity_of_vacancy


def download_salaries(vacancy):
    vacancies = download_vacancies(vacancy)
    salaries = [salary["salary"] for salary in vacancies]
    salaries_in_rub = [salary if salary["currency"]
                       != "RUR" else salary for salary in salaries]
    return salaries_in_rub


def get_average_salary_for_one_vacancy(
        predicted_salaries,
        vacancies_processed):
    average_salary_for_one_vacancy = sum(
        predicted_salaries) / len(vacancies_processed)
    return int(average_salary_for_one_vacancy)


def download_vacancies(vacancy):
    vacancies = list()
    page = 0
    pages_number = 1
    while page < pages_number:
        params = {
            "text": "{}".format(vacancy),
            "area": SEARCH_AREA,
            "period": SEARCH_PERIOD,
            "only_with_salary": "True",
            "page": page}
        page_data = requests.get(URL, params=params, headers=HEADERS)
        page_data.raise_for_status()
        page_data = page_data.json()
        pages_number = page_data['pages']
        print("{} Добавлено из {}".format(page, page_data["pages"]))
        page += 1
        vacancies.extend(page_data["items"])
    return vacancies


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
        "Scala",
    ]
    statistics_for_all_languages = dict()
    for language in top_10_programming_languages:
        salaries = download_salaries(language)
        predicted_salaries = [
            predict_salary(
                salary["from"],
                salary["to"]) for salary in salaries]
        vacancies_processed = [
            vacancy_processed for vacancy_processed in predicted_salaries if vacancy_processed is not None]
        statistics_for_all_languages[language] = {
            "vacancy_found": get_quantity_of_vacancies(language),
            "vacancy_processed": len(vacancies_processed),
            "average_salary": get_average_salary_for_one_vacancy(
                predicted_salaries,
                vacancies_processed)}
    return statistics_for_all_languages


if __name__ == "__main__":
    try:
        stat_for_languages = get_statistics_for_languages()
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server:\n{0}".format(error))
    except requests.exceptions.ConnectionError as error:
        exit("Can't get data from server:\n{0}".format(error))
    print_statistics_table_view(stat_for_languages)
