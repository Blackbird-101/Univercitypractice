import sqlite3
import random
from faker import Faker
from logger import logger

def add_random_vacancies():
    ''' Функция для генерации случайных данных с вакансиями'''
    # Создаем экземпляр Faker
    # Создаем экземпляр Faker
    fake = Faker('ru_RU')  # Используем русскую локализацию для генерации данных

    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('/home/valeentin87/education/HTML_CSS/work_projects/JobLink/data/db.job_link_base_data')
    cursor = connection.cursor()

    # Создаем таблицу, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vacancies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        position TEXT NOT NULL,
        salary INTEGER NOT NULL,
        work_schedule TEXT NOT NULL,
        employment_type TEXT NOT NULL,
        experience_required TEXT NOT NULL,
        employer_guarantees TEXT,
        additional_info TEXT,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    ''')

    # Возможные значения для вакансий
    companies = ['Компания А', 'Компания Б', 'Компания В', 'Компания Г', 'Компания Д']
    positions = ['Экономист', 'Фармацевт', 'Программист', 'Психолог', 'Инженер', 'Строитель', 'Менеджер', 'Бухгалтер']
    employment_types = ['Полная', 'Удалённая', 'Частичная']
    experience_required = [
        'Не обязателен', 
        'от 1 года', 
        'от 2 лет', 
        'от 3 лет', 
        'от 4 лет', 
        'от 5 лет'
    ]
    guarantees = [
        'Помощь в аренде жилья рядом с работой, ежегодная путёвка в санаторий',
        'Медицинская страховка, корпоративные мероприятия',
        'Бонусы по результатам работы, скидки на товары компании',
        'Финансовая помощь на обучение',
        'Компенсация проезда'
    ]
    work_schedules = [
        'пн, вт, ср, чт',
        'пн-пт',
        'вт, сб',
        'вт, чт, сб',
        'пн-ср'
    ]

    # Дополнительная информация
    additional_infos = [
        'Дружный коллектив, комфортные условия труда',
        'Возможность карьерного роста, обучение',
        'Современные офисы, дружелюбная атмосфера',
        'Работа в команде профессионалов',
        'Гибкий график, возможность удаленной работы'
    ]

    # Генерация 70 вакансий
    for _ in range(70):
        company_name = random.choice(companies)
        position = random.choice(positions)
        salary = random.randint(20000, 120000)  # Зарплата в диапазоне 20000 - 120000
        work_schedule = random.choice(work_schedules)
        employment_type = random.choice(employment_types)
        experience = random.choice(experience_required)
        guarantees_text = random.choice(guarantees)
        additional_info = random.choice(additional_infos)
        email = fake.email()
        
        # Генерация случайного телефона (городские номера или сотовые операторы)
        # Пример городского телефона
        phone = fake.phone_number()
        # Приведем телефон к формату московского номера
        if random.choice([True, False]):  # Генерируем случайно, является ли он городским или сотовым номером
            phone = f"8(495){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        else:  # Генерируем сотовый номер
            operators = ['900', '901', '902', '903', '904', '905', '906', '907', '908', '909']
            phone = f"8({random.choice(operators)}){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        
        # Вставка записи в таблицу
        cursor.execute('''
        INSERT INTO vacancies (company_name, position, salary, work_schedule, employment_type, experience_required, employer_guarantees, additional_info, email, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (company_name, position, salary, work_schedule, employment_type, experience, guarantees_text, additional_info, email, phone))

    # Сохранение изменений и закрытие соединения
    connection.commit()
    connection.close()

    logger.info("Данные для 70 вакансий успешно сгенерированы и добавлены в базу данных!")

def add_random_resumes():
    '''Позволяет добавить произвольные данные в таблицу resumes базы данных'''
    fake = Faker('ru_RU')  # Используем русскую локализацию для генерации данных

    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('/home/valeentin87/education/HTML_CSS/work_projects/JobLink/data/db.job_link_base_data')
    cursor = connection.cursor()

    # Создаем таблицу, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        age INTEGER NOT NULL,
        position TEXT NOT NULL,
        experience TEXT NOT NULL,
        region TEXT NOT NULL,
        about_me TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        habits TEXT
    )
    ''')

    # Возможные значения для полей
    names_female = ['Анна', 'Елена', 'Ольга', 'Татьяна', 'Мария', 'Светлана', 'Ксения', 'Дарья']
    names_male = ['Александр', 'Дмитрий', 'Максим', 'Иван', 'Сергей', 'Михаил', 'Анатолий', 'Руслан']
    surnames_female = ['Ivanova', 'Petrova', 'Sokolova', 'Mikhailova', 'Smirnova']
    surnames_male = ['Ivanov', 'Petrov', 'Sokolov', 'Mikhailov', 'Smirnov']
    positions = ['Экономист', 'Фармацевт', 'Программист', 'Психолог', 'Инженер', 'Строитель', 'Менеджер', 'Бухгалтер']
    experience_list = ['1 год', '2 года', '3 года', '4 года', '5 лет', '6 лет', '7 лет', '8 лет', '9 лет', '10 лет', '11 лет']
    regions = [
        'Центральный АО', 'Северный АО', 'Северо-Восточный АО', 'Восточный АО',
        'Юго-Восточный АО', 'Южный', 'Юго-Западный АО', 'Западный АО', 
        'Северо-Западный АО', 'Зеленоградский АО', 'Новомосковский АО', 'Троицкий АО'
    ]

    # Генерация 30 резюме
    for _ in range(30):
        # Генерация имени и фамилии
        if random.choice([True, False]):
            name = random.choice(names_female)
            surname = random.choice(surnames_female)
        else:
            name = random.choice(names_male)
            surname = random.choice(surnames_male)

        age = random.randint(21, 43)  # Возраст от 21 до 43 лет
        position = random.choice(positions)
        experience = random.choice(experience_list)
        region = random.choice(regions)
        
        # Генерируем "Обо мне" на основе профессии
        about_me = f"Я {random.choice(['команда', 'опытный', 'ответственный', 'стремлюсь к успеху', 'полон сил'])} {position.lower()}, увлекаюсь {random.choice(['спортом', 'чтением', 'технологиями'])}."[:145]
        
        email = fake.email()
        
        # Генерация случайного телефона
        # Пример городского телефона
        phone = fake.phone_number()
        # Приведем телефон к формату московского номера
        if random.choice([True, False]):  # Генерируем случайно, является ли он городским или сотовым номером
            phone = f"8(495){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        else:  # Генерируем сотовый номер
            operators = ['900', '901', '902', '903', '904', '905', '906', '907', '908', '909']
            phone = f"8({random.choice(operators)}){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

        # Случайное добавление вредной привычки
        habits = "курение" if random.random() < 0.1 else None  # У 10% будет вредная привычка

        # Вставка записи в таблицу
        cursor.execute('''
        INSERT INTO resumes (name, surname, age, position, experience, region, about_me, email, phone, habits)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, surname, age, position, experience, region, about_me, email, phone, habits))

    # Сохранение изменений и закрытие соединения
    connection.commit()
    connection.close()

logger.info("Данные для 30 резюме успешно сгенерированы и добавлены в базу данных!")



if __name__ == '__main__':
    add_random_resumes()
