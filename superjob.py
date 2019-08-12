import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable, DoubleTable, SingleTable
load_dotenv()

SUPERJOB_TOKEN = os.getenv("SUPERJOB_TOKEN")
URL = "https://api.superjob.ru/2.0/vacancies/"
HEADERS = {"X-Api-App-Id": SUPERJOB_TOKEN}

def get_developers_professions():
  params = {"town": 4, "catalogues": 48}
  response = requests.get(URL, headers=HEADERS, params=params)
  response = response.json()
  data = response["objects"]
  professions = [item["profession"] for item in data]
  return professions

def get_predict_rub_salary_for_Superjob(vacancy):
	params = {"town": 4, "catalogues": 48, "keyword": "Разработчик {}".format(vacancy)}
	response = requests.get(URL, headers=HEADERS, params=params)
	response = response.json()
	data = response["objects"]
	predict_rub_salary = list()
	for salary in data:
		if salary["currency"] == "rub":
			if salary["payment_from"] == 0 and salary["payment_to"] == 0:
				average_salary = None
			elif salary["payment_from"] != 0 and salary["payment_to"] == 0:
				average_salary = salary["payment_from"] * 0.8
			elif salary["payment_from"] == 0 and salary["payment_to"] != 0:
				average_salary = salary["payment_to"] * 0.8
			elif salary["payment_from"] != 0 and salary["payment_to"] != 0:
				average_salary = (salary["payment_from"] + salary["payment_to"]) / 2
			predict_rub_salary.append(average_salary)
	return predict_rub_salary

def get_global_data(vacancy):
  global_data = list()
  page = 0
  pages_number = 1
  while page < pages_number:
  	params = {"keyword":"{}".format(vacancy), "town": 4, "catalogues": 48}
  	page_data = requests.get(URL, params=params, headers=HEADERS)
  	page_data = page_data.json()
  	pages_number = page_data['total']
  	print("{} Добавлено из {}".format(page, page_data["total"]))
  	page += 1
  	global_data.append(page_data["objects"])
  return global_data

def get_quantity_of_vacancies(vacancy):
  params = {"keyword":"Разработчик {}".format(vacancy), "town": 4, "catalogues": 48}
  response = requests.get(URL, headers=HEADERS, params=params)
  response = response.json()
  quantity_of_vacancies = response["total"]
  return quantity_of_vacancies

def get_vacancy_processed(vacancy):
  predict_salary = get_predict_rub_salary_for_Superjob(vacancy)
  vacancy_prosecced = 0
  for salary in predict_salary:
  	if salary != None:
  		vacancy_prosecced += 1
  return vacancy_prosecced

def get_average_salary_for_one_vacancy(vacancy):
  predict_salary = get_predict_rub_salary_for_Superjob(vacancy)
  average_salaries_for_count = list()
  for salary in predict_salary:
  	if salary != None:
  		salary = int(salary)
  		average_salaries_for_count.append(salary)
  if len(average_salaries_for_count) != 0:
  	final_average_salary = sum(average_salaries_for_count) / len(average_salaries_for_count)
  else:
  	final_average_salary = 0
  return int(final_average_salary)

def get_statistics_for_languages_from_Superjob():
  top_10_programming_languages = ["Javascript", "Java", "Python", "Ruby", "PHP", "C++", "C#", "C", "Go", "Scala"]
  statistics_for_all_languages = {}
  for language in top_10_programming_languages:
	  statistics_for_one_language = {
		  language: {
		  "vacancy_found": get_quantity_of_vacancies(language),
		  "vacancy_processed": get_vacancy_processed(language),
		  "average_salary": get_average_salary_for_one_vacancy(language)
		  }
	  }
	  statistics_for_all_languages.update(statistics_for_one_language)
  return(statistics_for_all_languages)

def print_statistics_table_view():
  data = get_statistics_for_languages_from_Superjob()
  TABLE_DATA = [["Язык", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
  languages = data.keys()
  for language in languages:
  	row = []
  	row.append(language)
  	keys_data = data[language]
  	keys_data = keys_data.values()
  	for key in keys_data:
  		row.append(key)
  	TABLE_DATA.append(row)
  title = 'SuperJob Moscow'
  table = AsciiTable(TABLE_DATA, title)
  print(table.table)
  print()

if __name__ == "__main__":
  try: print_statistics_table_view()
  except requests.exceptions.ConnectionError as error:
    exit("Can't get data from server:\n{0}".format(error))
  except requests.exceptions.HTTPError as error:
    exit("Can't get data from server:\n{0}".format(error))
  except KeyError as error:
    exit("Неверный URL")