from typing import List, Dict, Tuple
import re

from app.models import Resume
from logger import logger

# словарь соответствии названий компаний их файлам с логотипом

associate_courses = {
    "courses_from_employers":"Курсы от работодателей",
    "online_schools":"Онлайн-школы",
    "education_in_universities":"Обучение в ВУЗах"
}


associate_logo = {
    "СБЕРБАНК":"logo-sber.png", # Экономист, Бухгалтер
    "Tinkoff": "logo-tbank.png", # Бухгалтер, Экономист
    "МЕДИАФАРМ": "media-farm.png",  # Фармацевт
    "Р-ФАРМ": "r-far-logo.jpg",  # Фармацевт
    "АВЕ-МЕДИКО": "ave-mediko.jpeg", # Психолог
    "НИТЬ-АРИАДНЫ": "ariadna.jpg", # Психолог
    "Аlgoritm-arhitect": "algoritm-arhitect.png", # Программист
    "Астра": "astra.png", # Программист
    "ДОБРЫЙ-КОЛА": "logo-dobriy-cola.png", # Менеджер
    "РУССКИЙ ХИТ": "logo-russkiy-hit.png", # Менеджер
    "СОЛНЦЕ": "logo-solnce.png", # Строитель, Инженер
    "КИР-СТРОЙ": "kir-stroy.jpg", # Строитель
    "БАКОР": "bacor.jpeg", # Инженер
}


def translate_days(short_days: str) -> str:
    """Переводит сокращенные названия дней недели в полные с правильными окончаниями.
    
    Args:
        short_days (str): Строка с сокращенными названиями дней недели.
        
    Returns:
        str: Полные названия дней недели или диапазоны с правильными окончаниями.
        
    Raises:
        ValueError: Если ввод содержит недопустимые сокращения.
    """
    
    try:
        day_mapping = {
            "пн": "понедельник",
            "вт": "вторник",
            "ср": "среда",
            "чт": "четверг",
            "пт": "пятница",
            "сб": "суббота",
            "вс": "воскресенье"
        }

        day_list = [day.strip() for day in short_days.split(',')]
        logger.info(f'{day_list=}')
        
        for day in day_list:
            if all([day not in day_mapping, day != 'пн-пт']):
                raise ValueError(f"Недопустимое сокращение дня недели: {day}")
        
        if len(day_list) == 1 and '-' in day_list[0]:
            logger.info('попали на пн-пт')
            start, end = day_list[0].split('-')
            return f'с {day_mapping[start]} по {day_mapping[end]}'
        
        days_indices = [list(day_mapping.keys()).index(day) for day in day_list]
        
        # Проверка на поочередность
        if days_indices == list(range(min(days_indices), max(days_indices) + 1)):
            start_day = day_mapping[day_list[0]]
            end_day = day_mapping[day_list[-1]]
            
            # Пунктуация для единственного дня
            if day_list[0] == day_list[-1]:
                return f'{start_day}'
            
            # Пунктуация для нескольких дней
            return f'с {start_day} по {end_day}'
        
        full_days = [day_mapping[day] for day in day_list]
        
        # Правильные окончания (по 1/2/5 и т.д.)
        if len(full_days) == 1:
            return full_days[0]
        elif len(full_days) == 2:
            return f'{full_days[0]} и {full_days[1]}'
        else:
            return ', '.join(full_days[:-1]) + ' и ' + full_days[-1]
    except ValueError as e:
        logger.error(f"Произошла ошибка {e}")



def transliterate(text: str) -> str:
    """
    Функция транслитерации русского текста в английский алфавит
    """
    # Словарь соответствий букв
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
        'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'y', 'э': 'e', 'ю': 'yu',
        'я': 'ya', 'ь': '', 'ъ': ''
    }
    
    # Приводим текст к нижнему регистру и транслитерируем
    result = ''.join([translit_dict.get(char, char) for char in text.lower()])
    
    # Делаем первую букву заглавной
    return result.capitalize()



def process_professions(professions: List[str]) -> Dict[str, Tuple[str, str]]:
    """
    Основная функция обработки списка профессий
    """
    # Словарь с описаниями профессий
    profession_descriptions: Dict[str, str] = {
    "Программист": "Создавай будущее с помощью кода и развивайся в IT-индустрии",
    "Киберспециалист": "Защищай цифровую безопасность компаний от угроз",
    "Тестировщик": "Обеспечивай качество программных продуктов",
    "Психолог": "Помогай людям находить гармонию с собой",
    "Фармацевт": "Создавай лекарства и заботься о здоровье людей",
    "Эколог": "Защищай природу и создавай устойчивое будущее",
    "Экономист": "Развивай навыки финансового прогнозирования",
    "Маркетолог": "Продвигай бренды в цифровой среде",
    "Видеограф": "Лови яркие моменты жизни на камеру",
    "Логист": "Оптимизируй цепочки поставок и экономь ресурсы",
    "Биоинформатик": "Соединяй биологию и технологии",
    "Нейрореабилитолог": "Помогай восстанавливать здоровье мозга",
    "Архитектор": "Создавай виртуальные миры будущего",
    "Робототехник": "Развивай технологии будущего",
    "Косметолог": "Помогай людям становиться красивее и увереннее в себе",
    "Электрик": "Обеспечивай надёжную работу электрических систем",
    "Сантехник": "Решай любые проблемы с водоснабжением профессионально",
    "Фотограф": "Лови яркие моменты жизни через объектив камеры",
    "Парикмахер": "Создавай стильные образы и преображай клиентов",
    "Массажист": "Помогай людям расслабиться и восстановить здоровье",
    "Бухгалтер": "Веди точный учёт финансов и отчётность",
    "Копирайтер": "Создавай продающие тексты для бизнеса",
    "Флорист": "Создавай красивые букеты и композиции",
    "Тренер": "Помогай людям достигать спортивных целей",
    "Экскурсовод": "Открывай интересные места для путешественников",
    "Сварщик": "Создавай прочные металлические конструкции",
    "Швея": "Шьёшь качественную одежду на заказ",
    "Кладовщик": "Организуй эффективное хранение товаров",
    "Администратор": "Обеспечивай комфорт посетителей и клиентов",
    "Риелтор": "Помогай в покупке и продаже недвижимости",
    "Нотариус": "Оформляй юридические документы профессионально",
    "Воспитатель": "Развивай и воспитывай будущее поколение",
    "Механик": "Обслуживай и ремонтируй различную технику",
    "Токарь": "Изготавливай детали с высокой точностью",
    "Фрезеровщик": "Создавай сложные детали на фрезерном станке",
    "Инженер": "Реализуй сложные технические проекты с нуля",
    "Строитель": "Реализуй масштабные строительные проекты",
    "Менеджер": "Развивай карьеру в сфере современного менеджмента"
    }
    
    result: Dict[str, Tuple[str, str]] = {}
    
    try:
        for profession in professions:
            # Проверяем наличие описания профессии
            if profession not in profession_descriptions:
                raise ValueError(f"Описание для профессии '{profession}' не найдено")
                
            # Транслитерируем название профессии
            transliterated_name = transliterate(profession)
            
            # Получаем описание профессии
            description = profession_descriptions[profession]
            
            # Добавляем в результат
            result[profession] = (transliterated_name, description)
            
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        return {}
        
    return result


def get_info_of_resumes(all_resumes:List[Dict], position:str):
    '''Возвращает информацию в виде кортежа:
    первый элемент - профессия,
    второй элемент - количество резюме по переданной в аргументе position профессии
    третий элемент - минимальный возраст соискателя,
    четвёртый элемент - максимальный возраст соискателя '''
    try:
        #print(f'get_info_of_resumes {position=}')
        #print(f'get_info_of_resumes {all_resumes=}')
        resumes_from_position:List[Dict] = []
        for resume in all_resumes:
            #print(f'{resume=}')
            if resume.position == position:
                #print('get_info_of_resumes Добавляем в список resumes_from_position')
                resumes_from_position.append(resume)



        #resumes_from_position:List[Dict] = [resume for resume in all_resumes if resume['position'] == position]
        #print(f'Кличество резюме в профессии {position} равно {len(resumes_from_position)}')
        resume_counts = len(resumes_from_position)
        

        min_age = min((resume.age for resume in resumes_from_position), default=None)
        max_age = max((resume.age for resume in resumes_from_position), default=None)

        #print(f'{position=} {resume_counts=} {min_age=} {max_age=}')

        return position, resume_counts, min_age, max_age

    except Exception as e:
        logger.error(f'Произошла ошибка {e}')


def get_age_string(number: int, case: str) -> str:
    """
    Возвращает строку с правильным склонением числительного и слова 'лет'/'года'
    
    :param number: число лет
    :param case: падеж ('nominative' или 'genitive')
    :return: строка с правильным склонением
    """
    # Проверяем корректность падежа
    if case not in ('nominative', 'genitive'):
        raise ValueError("Неверный падеж. Используйте 'nominative' или 'genitive'")
    
    # Получаем последнюю цифру числа
    #print(f'{number=}')
    last_digit = number % 10
    last_two_digits = number % 100
    
    # Определяем форму слова в зависимости от падежа
    if case == 'nominative':
        if 11 <= last_two_digits <= 14:
            return f"{number} лет"
        elif last_digit == 1:
            return f"{number} год"
        elif 2 <= last_digit <= 4:
            return f"{number} года"
        else:
            return f"{number} лет"
    else:  # genitive падеж
        if 11 <= last_two_digits <= 14:
            return f"{number} лет"
        elif last_digit == 1:
            return f"{number} года"
        else:
            return f"{number} лет"



if __name__ == '__main__':
    professions = ['Экономист', 'Фармацевт', 'Программист', 'Строитель', "Бухгалтер", "Инженер", "Менеджер", "Психолог"]

    result = process_professions(professions)
    logger.info(result)
