import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from colorama import init, Fore, Back, Style
import os
init()
product_line = {
    'Молочні продукти': [0.4, 0.6, 18, 80, 0, 10, 60],
    "М'ясні продукти": [0.5, 0.5, 30, 500, 0, 10, 60],
    'Фрукти та овочі': [0.4, 0.6, 5, 100, 0, 10, 60],
    'Солодкі напої': [0.7, 0.3, 10, 80, 1, 10, 40],
    'Алкоголь': [0.7, 0.3, 30, 1200, 1, 18, 60],
    'Солодощі': [0.35, 0.65, 15, 500, 0, 10, 50],
    'Косметика': [0.2, 0.8, 30, 1500, 2, 10, 35],
    'Інструменти': [0.8, 0.2, 50, 2000, 2, 10, 40]
}
# Загрузка данных из CSV файла в объект DataFrame
data = pd.read_csv("Data.csv", encoding='cp1251')


def result_gender_product():
    # Группировка данных по полу и товару
    grouped_data_prod = data.groupby(['Стать', 'Лінійка продукту'])

    # Подсчет количества мужчин и женщин, которые купили каждый товар
    result = grouped_data_prod.size().unstack(fill_value=0)
    pd.options.display.max_columns = len(grouped_data_prod)
    # Вывод результата

    # print(result["Молочные продукты"])
    # print(result["Молочные продукты"]["Женский"])
    # print(round(result["Молочные продукты"]["Женский"]/(result["Молочные продукты"]["Женский"] + result["Молочные продукты"]["Мужской"]), 2))
    print(Fore.BLUE + "\nПорівняння ймовірності покупки Лінійки товару щодо Статі покупця:")
    print(Style.RESET_ALL)
    for i in result:
        percent_m = round(result[i]["Чоловік"]/(result[i]["Жінка"] + result[i]["Чоловік"]), 2)
        percent_w = round(result[i]["Жінка"]/(result[i]["Жінка"] + result[i]["Чоловік"]), 2)
        print(f"{i}:\nЧоловік ===> {percent_m} ({product_line[i][0]})\nЖінка ===> {percent_w} ({product_line[i][1]})\n")


def result_age_product():
    # Группировка данных по возрасту и товару
    grouped_data_age = data.groupby(['Вік', 'Лінійка продукту'])

    # Подсчет возраста покупателей, которые купили каждый товар
    result = grouped_data_age.size().unstack(fill_value=0)
    pd.options.display.max_columns = len(grouped_data_age)

    # Функция подсчета среднего возраста покупателя относительно продукта
    def average_age(products, product_name):
        customers = products.get(product_name)
        total_customers = sum(customers.values())
        if total_customers == 0:
            return 0
        else:
            weighted_sum = sum(age * count for age, count in customers.items())
            return weighted_sum / total_customers

    print(Fore.BLUE + "Середній вік покупця щодо продукту:")
    print(Style.RESET_ALL)
    # Вывод результата
    for i in list(product_line):
        print(f"{i} ===> {round(average_age(result.to_dict(), i))} ({(product_line[i][5]+product_line[i][6])/2})")


def result_time():
    print(Fore.BLUE + "\nЗагальна сума продажу щодо години:")
    print(Style.RESET_ALL)
    # Группировка данных по количеству и времени
    grouped_data_time = data.groupby(['Кількість', 'Час'])

    # Подсчет количества покупок по времени
    result = grouped_data_time.size().unstack(fill_value=0)
    pd.options.display.max_columns = len(grouped_data_time)

    sales_dict = result.to_dict()

    # создаем словарь для хранения общего количества продаж по часам
    sales_by_hour = {}

    # проходим по всем элементам входного словаря
    for time, sales in sales_dict.items():
        # извлекаем час из ключа времени
        hour = time[:2]
        # создаем словарь, если его еще нет
        if hour not in sales_by_hour:
            sales_by_hour[hour] = {}
        # проходим по всем количествам продаж и их количествам в словаре продаж
        for quantity, count in sales.items():
            # увеличиваем счетчик продаж в этом часу и с этим количеством на соответствующее количество
            if quantity not in sales_by_hour[hour]:
                sales_by_hour[hour][quantity] = 0
            sales_by_hour[hour][quantity] += count

    # # выводим общее количество продаж по часам
    # for hour, sales in sales_by_hour.items():
    #     print(f"Час: {hour.lstrip('0')}")
    #     for quantity, count in sales.items():
    #         print(f"Количество продаж {quantity}: {count}")
    # выводим общую сумму продаж по часам
    for hour, sales in sales_by_hour.items():
        total_sales = 0
        for quantity, count in sales.items():
            total_sales += quantity * count
        print(f"Час: {hour.lstrip('0')}, Загальна сума продажу: {total_sales}")


def result_branch_sale():
    print(Fore.BLUE + "\nКількість продажів та заробіток по відділах:")
    print(Style.RESET_ALL)

    # Группировка данных по отделам и количеству продаж
    grouped_data_branch_money = data.groupby(['Загальна сума', 'Відділ'])
    grouped_data_branch = data.groupby(['Кількість', 'Відділ'])

    # Подсчет количества продаж относительно отдела
    result = grouped_data_branch_money.size().unstack(fill_value=0)
    result2 = grouped_data_branch.size().unstack(fill_value=0)

    pd.options.display.max_columns = 20


    branch_dict_money = result.to_dict()
    branch_dict_sales = result2.to_dict()

    total_cash = 0
    total_sales = 0
    for department, sales_data in branch_dict_money.items():
        print(f"Відділ {department}:")
        for key, value in sales_data.items():
            total_cash += key * value
        total_sales += sum(key * value for key, value in branch_dict_sales[department].items())
        print(f"Всього продаж: {total_sales}")
        print(f"Весь заробіток: {round((total_cash), 2)}\n")
        total_cash = 0
        total_sales = 0

    # print(f"Всего заработано:")
    # for sales_count, sales_count_value in sales_data.items():
    #     print(f"Количество продаж по {sales_count} шт.: {sales_count_value} ({sales_count_value/total_sales*100:.2f}%)")
    # print("\n")


def result_age_payment():

    # Группировка данных по возрасту и типу оплаты
    grouped_data_pay = data.groupby(['Вік', 'Тип оплати'])

    # Подсчет возраста покупателей относительно типа оплаты
    result = grouped_data_pay.size().unstack(fill_value=0)
    pd.options.display.max_columns = len(grouped_data_pay)

    # Данные для построения диаграммы
    age = range(10, 91)
    print(result.index.tolist())
    # Построение диаграммы
    plt.plot(age, result["Готівкою"], label='Готівкою')
    plt.plot(age, result["Оплата карткою"], label='Оплата карткою')
    plt.plot(age, result["Електронний гаманець"], label='Електронний гаманець')
    plt.legend()
    plt.xlabel('Вік')
    plt.ylabel('Кількість')
    plt.title('Графік типів оплати щодо віку')
    plt.show()

result_gender_product()
result_age_product()
result_time()
result_branch_sale()
result_age_payment()
