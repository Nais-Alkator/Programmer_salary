import requests
from terminaltables import AsciiTable, DoubleTable, SingleTable

URL = "https://api.hh.ru/vacancies/"
HEADERS = {"User-Agent":"User-Agent"}
def get_quantity_of_vacancies(vacancy):
  params = {"text":"Разработчик {}".format(vacancy), "area":"1", "period":"30"}
  response = requests.get(URL, params=params, headers=HEADERS)
  response.ok
  response = response.json()
  quantity_of_vacancy = response["found"]
  return quantity_of_vacancy

def get_salaries_of_developers(vacancy):
  global_data = get_global_vacancy_data(vacancy)
  salaries_in_rub = []
  salaries = []
  for page in global_data:
    for item in page:
      item = item["salary"]
      salaries.append(item)
  for salary in salaries:
    if salary["currency"] != "RUR":
      salary = {"from": None, "to": None}
    else: 
      salary = salary
    salaries_in_rub.append(salary)
  return salaries_in_rub

def get_predict_rub_salary(vacancy):
  salaries = get_salaries_of_developers(vacancy)
  predict_salary = list()
  for salary in salaries:
  	salary_from = salary["from"]
  	salary_to = salary["to"]
  	if salary_from is None and salary_to is None:
  		average_salary = 0
  	elif salary_from != None and salary_to is None:
  		average_salary = salary_from * 1.2
  		average_salary = int(average_salary)
  	elif salary_from is None and (salary_to) != None:
  		average_salary = salary_to * 0.8
  		average_salary = int(average_salary)
  	elif salary_from != None and salary_to != None:
  		average_salary = (salary_from + salary_to) / 2
  		average_salary = int(average_salary)
  	predict_salary.append(average_salary)
  return predict_salary

def get_vacancy_processed(vacancy):
  predict_salary = get_predict_rub_salary(vacancy)
  vacancy_prosecced = 0
  for salary in predict_salary:
  	if salary != 0:
  		vacancy_prosecced += 1
  return vacancy_prosecced

def get_average_salary_for_one_vacancy(vacancy):
  average_salary_for_one_vacancy = sum(get_predict_rub_salary(vacancy)) / get_vacancy_processed(vacancy)
  return int(average_salary_for_one_vacancy)

def get_statistics_for_languages_from_HeadHunter():
  top_10_programming_languages = ["Javascript", "Java", "Python", "Ruby", "PHP", "C++", "C#", "C", "Go", "Scala"]
  statistics_for_all_languages = dict()
  for language in top_10_programming_languages:
	  statistics_for_one_language = {
		  language: {
		  "vacancy_found": get_quantity_of_vacancies(language),
		  "vacancy_processed": get_vacancy_processed(language),
		  "average_salary": get_average_salary_for_one_vacancy(language)
		  }
	  }
	  statistics_for_all_languages.update(statistics_for_one_language)
  return statistics_for_all_languages

def get_global_vacancy_data(vacancy):
  global_data = list()
  page = 0
  pages_number = 1
  while page < pages_number:
      params = {"text":"{}".format(vacancy), "area":"1", "period":"30", "only_with_salary":"True", "page": page}
      page_data = requests.get(URL, params=params, headers=HEADERS)
      page_data = page_data.json()
      pages_number = page_data['pages']
      print("{} Добавлено из {}".format(page, page_data["pages"]))
      page += 1
      global_data.append(page_data["items"])
  return global_data

def print_statistics_table_view():
  data = get_statistics_for_languages_from_HeadHunter()
  TABLE_DATA = [["Язык", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
  languages = data.keys()
  for language in languages:
  	row = list()
  	row.append(language)
  	keys_data = data[language]
  	keys_data = keys_data.values()
  	for item in keys_data:
  		row.append(item)
  	TABLE_DATA.append(row)
  title = 'HeadHunter Moscow'
  table = AsciiTable(TABLE_DATA, title)
  print(table.table)
  print()

if __name__ == "__main__":
  try: print_statistics_table_view()
  except requests.exceptions.ConnectionError as error:
    exit("Can't get data from server:\n{0}".format(error))
  except requests.exceptions.HTTPError as error:
    exit("Can't get data from server:\n{0}".format(error))
