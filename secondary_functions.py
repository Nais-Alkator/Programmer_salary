from terminaltables import AsciiTable


def print_statistics_table_view(stat_for_languages):

    table_data = [["Язык",
                   "Вакансий найдено",
                   "Вакансий обработано",
                   "Средняя зарплата"]]
    for language in stat_for_languages:
        row = [
            language,
            stat_for_languages[language]["vacancy_found"],
            stat_for_languages[language]["vacancy_processed"],
            stat_for_languages[language]["average_salary"]]
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
    elif salary_from is not 0 and salary_to == 0:
        predict_salary = salary_from * 0.8
    elif salary_from is None and (salary_to) is not None:
        predict_salary = salary_to * 0.8
        predict_salary = int(predict_salary)
    elif salary_from == 0 and salary_to is not 0:
        predict_salary = salary_to * 0.8
    elif salary_from is not None and salary_to is not None:
        predict_salary = (salary_from + salary_to) / 2
        predict_salary = int(predict_salary)
    elif salary_from is not 0 and salary_to is not 0:
        predict_salary = (salary_from + salary_to) / 2
    return predict_salary
