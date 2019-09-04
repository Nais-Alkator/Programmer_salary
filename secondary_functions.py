from terminaltables import AsciiTable


def print_statistics_table_view(stat_for_langguages):
    table_data = [["Язык",
                   "Вакансий найдено",
                   "Вакансий обработано",
                   "Средняя зарплата"]]
    for language in stat_for_langguages:
        row = [language]
        language_keys = stat_for_langguages[language]
        vacancy_found = language_keys["vacancy_found"]
        row.append(str(vacancy_found))
        vacancy_processed = language_keys["vacancy_processed"]
        row.append(str(vacancy_processed))
        average_salary = language_keys["average_salary"]
        row.append(str(average_salary))
        table_data.append(row)
    title = 'SuperJob Moscow'
    table = AsciiTable(table_data, title)
    print(table.table)
    print()


def predict_salary(salary_from, salary_to):
    if salary_from is None and salary_to is None:
        predict_salary = 0
    elif salary_from == 0 and salary_to == 0:
        predict_salary = None
    elif salary_from is not None and salary_to is None:
        predict_salary = salary_from * 1.2
        predict_salary = int(predict_salary)
    elif salary_from != 0 and salary_to == 0:
        predict_salary = salary_from * 0.8
    elif salary_from is None and (salary_to) is not None:
        predict_salary = salary_to * 0.8
        predict_salary = int(predict_salary)
    elif salary_from == 0 and salary_to != 0:
        predict_salary = salary_to * 0.8
    elif salary_from is not None and salary_to is not None:
        predict_salary = (salary_from + salary_to) / 2
        predict_salary = int(predict_salary)
    elif salary_from != 0 and salary_to != 0:
        predict_salary = (salary_from + salary_to) / 2
    return predict_salary