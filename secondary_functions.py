from terminaltables import AsciiTable


def print_statistics_table_view(STAT_FOR_LANGUAGES):

    table_data = [["Язык",
                   "Вакансий найдено",
                   "Вакансий обработано",
                   "Средняя зарплата"]]
    for language in STAT_FOR_LANGUAGES:
        row = [language]
        language_keys = STAT_FOR_LANGUAGES[language]
        vacancy_found = language_keys["vacancy_found"]
        row.append(str(vacancy_found))
        vacancy_processed = language_keys["vacancy_processed"]
        row.append(str(vacancy_processed))
        average_salary = language_keys["average_salary"]
        row.append(str(average_salary))
        #language_values = language_keys.values()
        table_data.append(row)
    title = 'SuperJob Moscow'
    table = AsciiTable(table_data, title)
    print(table.table)
    print()