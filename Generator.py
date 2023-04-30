import pandas as pd
import random
import datetime

# Список лінійок товарів з ймовірностями їх вибору щодо статі
# [%Чол, %Жін, МінЦена, МаксЦена, Відділ, МінВік, МаксВік]
# МінВік і МаксВік позначають лише бажане значення
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
seasons = ["Весна", "Літо", "Осінь", "Зима"]  # Сезони
percent_seasons = [0.10, 0, 0.10, 0.20]
payment_types = ['Оплата карткою', 'Готівкою', 'Електронний гаманець']  # Типи оплати
branches = ['A', 'B', 'C']  # Список відділів
gender_list = ['Чоловік', 'Жінка']  # Стать
percent = 0.06  # Податок
max_sales = 10  # Максимальна кількість продажів

# Для генерації випадкової дати в межах 2023 року від 1 до 3 місяців
start_date = datetime.date(2023, 1, 1)  # Початок
end_date = datetime.date(2023, 3, 31)  # Кінець
time_between_dates = end_date - start_date  # Рахуємо час між датами
days_between_dates = time_between_dates.days  # Перекладаємо у дні


def generate_price(lower_range, upper_range):

    # Визначення діапазону цін, які ми хочемо згенерувати
    prices = range(lower_range, upper_range+1)

    # Визначення ймовірностей кожної ціни в діапазоні
    probabilities = [1/(price-lower_range+1) for price in prices]

    # Нормалізація ймовірностей, щоб вони підсумовувалися до 1
    probabilities_sum = sum(probabilities)
    probabilities = [probability/probabilities_sum for probability in probabilities]

    # Використання ймовірностей для випадкового вибору ціни з діапазону
    price = random.choices(list(prices), weights=probabilities)[0]

    return price


def fix_age(list_):

    # згенерувати випадкове число від 0 до 1
    p = random.random()
    if p < 0.85:
        # вибрати число з діапазону list
        return random.randint(list_[0], list_[1])
    else:
        # вибрати число з діапазону list[1], 100
        return random.randint(list_[1], 90)


def fix_pay(age):

    # згенерувати випадкове число від 0 до 1
    p = random.random()
    if age <= 60:
        return random.choice(payment_types)
    else:
        if p < 0.70:
            return payment_types[1]
        else:
            return random.choice(payment_types)


def generate_date():

    random_number_of_days = random.randrange(days_between_dates)
    # Додаємо випадкову кількість днів до початкової дати
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


def generate_transaction_number():

    num1 = str(random.randint(100, 999))
    num2 = str(random.randint(10, 99))
    num3 = str(random.randint(1000, 9999))
    return f"{num1}-{num2}-{num3}"


def generate_base():
    # Создаем пустой DataFrame и генерируем данные
    sales_data = pd.DataFrame(
        columns=['Відділ', 'Номер угоди', 'Лінійка продукту', 'Стать', 'Вік', 'Ціна',
                 'Кількість', 'Податок 6%', 'Сезон', 'Загальна сума', 'Дата', 'Час', 'Тип оплати'])
    for i in range(5000):  # Количество сделок, которые мы хотим сгенерировать
        # Корректируем время продаж
        p = random.random() * 100
        if p <= 70:
            open_ = 12
            close_ = 20
        elif p >= 90:
            open_ = 8
            close_ = 11
        else:
            open_ = 20
            close_ = 22
        transaction_num = generate_transaction_number()  # Номер угоди
        product_line_choice = random.choice(list(product_line))  # Назва лінійки
        values = product_line.get(product_line_choice, [0.5, 0.5])  # % Чоловіків та Жінок
        quantity = random.randint(1, max_sales)  # Випадкова кількість продажів від 1 до 10
        # price = round(random.uniform(weights[2:][0], weights[2:][1]), 2)
        # price = round(sum([round(random.uniform(weights[2], weights[3]), 2) for _ in range(quantity)]), 2)
        date = generate_date()  # Генерируем дату
        season = seasons[(int(str(date).split('-')[1].lstrip("0"))-1)//3]  # Визначаємо сезон
        # Ціна з 2 знаками після коми у проміжку
        price = round(sum([generate_price(values[2], values[3]) for _ in range(quantity)]) + random.random(), 2)
        tax = round(price * percent, 2)  # Рахуємо % податку
        season_tax = percent_seasons[seasons.index(season)]# Рахуємо вплив сезону на ціну
        # Коригуємо залежно від сезону та рахуємо підсумкову суму
        total_amount = round(price + tax + price * season_tax, 2)  # Рахуємо підсумкову суму
        time = datetime.time(hour=random.randint(open_, close_),
                             minute=random.randint(0, 59), second=random.randint(0, 59))
        gender = random.choices(gender_list, weights=values[:2])[0]  # Випадково визначити стать
        age = fix_age(values[5:])  # Визначаємо вік
        payment_type = fix_pay(age)  # Визначаємо тип оплати
        branch = branches[values[4]]  # Визначаємо відділ

        # Додаємо рядок у DataFrame
        sales_data.loc[i] = [branch, transaction_num, product_line_choice, gender, age, price,
                             quantity, tax, season, total_amount, date, time, payment_type]
    return sales_data


default = generate_base()
# Змінюємо обмеження на виведення кількості стовпців на 11
pd.options.display.max_columns = len(product_line)
# Виводимо результат
print(default)
# Вносимо базу в csv файл
default.to_csv('Data.csv', encoding='cp1251', index=False)

# Тенденція за статтю покупця +
# Тенденція за віком покупця +
# Тенденція за типом оплати +
# У кожної лінійки продуктів свій відділ
# Для кожної лінійки продуктів своя ціна
# Ціни більш реальні, за рахунок ймовірності, що зменшується, для більш високих цін
# Ціна залежить від сезону
# Вранці та ввечері продаж менше ніж протягом дня +
