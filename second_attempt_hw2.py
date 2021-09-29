import csv
import json
import pandas as pd


file_ = []
with open('Corp_Summary.csv', encoding='utf-8') as File:
    reader = csv.DictReader(File, delimiter=';')
    for row in reader:
        file_.append(row)
df = pd.read_csv('Corp_Summary.csv')
list_col = sorted(' '.join([str(elem) for elem in list(df.columns)]).split(';'))


def department(file_: list):
    dep = {}
    for row in file_:
        if row[f'{list_col[0]}'] not in dep:
            dep[row[f'{list_col[0]}']] = {'Численность': 1, 'Мин. оклад': float(row[f'{list_col[2]}']), 'Макс. оклад': float(row[f'{list_col[2]}']), 'Ср. оклад': float(row[f'{list_col[2]}'])}
        else:
            dep[row[f'{list_col[0]}']]['Ср. оклад'] = (dep[row[f'{list_col[0]}']]['Ср. оклад'] * dep[row[f'{list_col[0]}']]['Численность'] + float(row[f'{list_col[2]}'])) / (1 + dep[row[f'{list_col[0]}']]['Численность'])
            dep[row[f'{list_col[0]}']]['Численность'] += 1
            dep[row[f'{list_col[0]}']]['Мин. оклад'] = min(dep[row[f'{list_col[0]}']]['Мин. оклад'], float(row[f'{list_col[2]}']))
            dep[row[f'{list_col[0]}']]['Макс. оклад'] = max(dep[row[f'{list_col[0]}']]['Макс. оклад'], float(row[f'{list_col[2]}']))
    print(json.dumps(dep, indent=1, ensure_ascii=False))
    return dep


def hierarchy(file_: list):
    hierarchy = {}
    for row in file_:
        if row[f'{list_col[0]}'] not in hierarchy:
            hierarchy[row[f'{list_col[0]}']] = [row[f'{list_col[3]}']]
        elif row[f'{list_col[3]}'] not in hierarchy[row[f'{list_col[0]}']]:
            hierarchy[row[f'{list_col[0]}']].append(row[f'{list_col[3]}'])
    print(json.dumps(hierarchy, indent=1, ensure_ascii=False))
    return hierarchy


def to_csv(dict_: dict):
    list_for_csv = [['Департамент', 'Мин. оклад', 'Макс. оклад', 'Ср. оклад']]
    for department in dict_:
        department_list = list(dict_[department].values())
        department_list.insert(0, department)
        list_for_csv.append(department_list)
    csv_ = open('result.csv', 'w', encoding='utf-8')
    with csv_:
        writer = csv.writer(csv_)
        writer.writerows(list_for_csv)
    print(list_for_csv)
    return list_for_csv


def step1():
    print(
        '1 : Иерархия команд, т.е. департамент и все команды, которые входят в него\n'
        '2 : Сводный отчёт по департаментам: название, численность, "вилка" зарплат в виде мин – макс, среднюю зарплату\n'
        '3 : Второй пункт в csv'
    )
    option = ''
    options = {'1': 1, '2': 2, '3': 3}
    while option not in options:
        print('Выберите: {} или {} или {}'.format(*options))
        option = input()

    if options[option] == 1:
        return hierarchy(file_)
    if options[option] == 2:
        return department(file_)
    if options[option] == 3:
        return to_csv(department(file_))
step1()
