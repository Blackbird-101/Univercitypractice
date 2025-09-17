import os, sys
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)

from typing import Optional, Dict, List


from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, select
from app.db_class import engine, Base, async_session
from app.models import Employer, Resume, TrainingCourse, User, Vacancy
from logger import logger




def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper

# блок методов, отвечающих за получение данных о резюме, вакансиях, пользователях, работодателях, обучающих курсах

@connection
async def get_resumes(session, filters: Optional[Dict[str, str]] = None  # словарь с фильтрами
) -> List[Resume]:
    """
    Получает список резюме из базы данных.
    При наличии словаря фильтров применяет их к запросу.
    """
    try:
        async with async_session() as session:
            resumes = (await session.scalars(select(Resume))).all()

            if filters:
                conditions = []
                for key, value in filters.items():
                    if hasattr(Resume, key):
                        logger.info(f'{key=}')
                        conditions.append(getattr(Resume, key) == value)
                if conditions:
                    logger.info(f'{conditions=}')
                    resumes = (await session.scalars(select(Resume).filter(*conditions))).all()
                    logger.info(f'После фильтра {resumes=}')
                
                
            #print(f'{resumes=}')
            return resumes
            # logger.info(f'{resumes=}')
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при получении данных о резюме {e}')
        return None



@connection
async def get_vacancyes(session, filters: Optional[Dict[str, str]] = None  # словарь с фильтрами
) -> List[Vacancy]:
    """
    Получает список вакансий из базы данных.
    При наличии словаря фильтров применяет их к запросу.
    """
    try:
        async with async_session() as session:
            vacancyes = (await session.scalars(select(Vacancy))).all()

            if filters:
                conditions = []
                for key, value in filters.items():
                    if hasattr(Vacancy, key):
                        logger.info(f'{key=}')
                        conditions.append(getattr(Vacancy, key) == value)
                if conditions:
                    logger.info(f'{conditions=}')
                    vacancyes = (await session.scalars(select(Vacancy).filter(*conditions))).all()
                    logger.info(f'После фильтра {vacancyes=}')
                
                
            #print(f'{vacancyes=}')
            return vacancyes
            # logger.info(f'{vacancyes=}')
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при получении данных о вакансиях {e}')
        return None

@connection
async def find_suitable_ones_resumes(session, filters: Dict) -> List[Resume]:
    try:
        query = select(Resume)
        conditions = []
        
        for key, value in filters.items():
            if hasattr(Resume, key):
                column = getattr(Resume, key)
                
                if key == 'age':
                    # Проверяем, что оба значения в диапазоне не пустые
                    if value[0] and value[1]:
                        min_age = int(value[0])
                        max_age = int(value[1])
                        conditions.append(and_(
                            column >= min_age,
                            column <= max_age
                        ))
                elif value:  # Добавляем условие только если значение не пустое
                    conditions.append(column == value)
        
        if conditions:
            query = query.filter(*conditions)
        
        logger.info(f"SQL запрос: {query}")
        resumes = (await session.scalars(query)).all()
        logger.info(f"Найденные резюме: {len(resumes)}")
        return resumes
    
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при получении данных о подходящих резюме: {e}')
        return []

@connection
async def find_suitable_ones_vacancyes(session, filters:dict) -> List[Vacancy]:
    '''Позволяет найти вакансии, подходящие по переданным критериям'''
    try:
        async with async_session() as session:
            vacancyes = (await session.scalars(select(Vacancy))).all()
            conditions = []
            for key, value in filters.items():
                if hasattr(Vacancy, key):
                    if value:
                        logger.info(f'Составляем условие для ключа {key=}')
                        if key == 'salary':
                            conditions.append(getattr(Vacancy, key) >= value)
                        elif key == 'experience_required' and value:
                            if value == 'Не обязателен':
                                conditions.append(getattr(Vacancy, key) == value)
                            else:
                                conditions.append(getattr(Vacancy, key) != 'Не обязателен')
                                
                        else:
                            conditions.append(getattr(Vacancy, key) == value)
                    else:
                        logger.info(f'по ключу {key} условие проверять не нужно')
            if conditions:
                logger.info(f'{conditions=}')
                vacancyes = (await session.scalars(select(Vacancy).filter(*conditions))).all()
                logger.info(f'После фильтра {vacancyes=}')
                    
            return vacancyes
                
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при получении данных о подходящих вакансиях {e}')
        return None





@connection
async def get_training_courses(session, filters: Optional[Dict[str, str]] = None  # словарь с фильтрами
) -> List[TrainingCourse]:
    """
    Получает список обучающих курсов из базы данных.
    При наличии словаря фильтров применяет их к запросу.
    """
    try:
        async with async_session() as session:
            courses = (await session.scalars(select(TrainingCourse))).all()

            if filters:
                conditions = []
                for key, value in filters.items():
                    if hasattr(TrainingCourse, key):
                        logger.info(f'{key=}')
                        conditions.append(getattr(TrainingCourse, key) == value)
                if conditions:
                    logger.info(f'{conditions=}')
                    courses = (await session.scalars(select(TrainingCourse).filter(*conditions))).all()
                    logger.info(f'После фильтра {courses=}')
                
                
            logger.info(f'{courses=}')
            return courses
            # logger.info(f'{courses=}')
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при получении данных об обучающих курсах {e}')
        return None



@connection
async def get_employers(session, filters: Optional[Dict[str, str]] = None  # словарь с фильтрами
) -> List[Employer]:
    """
    Получает список работодателей из базы данных.
    При наличии словаря фильтров применяет их к запросу.
    """
    try:
        async with async_session() as session:
            employers = (await session.scalars(select(Employer))).all()

            if filters:
                conditions = []
                for key, value in filters.items():
                    if hasattr(Employer, key):
                        logger.info(f'{key=}')
                        conditions.append(getattr(Employer, key) == value)
                if conditions:
                    logger.info(f'{conditions=}')
                    employers = (await session.scalars(select(Employer).filter(*conditions))).all()
                    logger.info(f'После фильтра {employers=}')
                
                
            logger.info(f'{employers=}')
            return employers
            # logger.info(f'{employers=}')
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при получении данных о работодателях {e}')
        return None




@connection
async def get_users(session, filters: Optional[Dict[str, str]] = None  # словарь с фильтрами
) -> List[User]:
    """
    Получает список пользователей из базы данных.
    При наличии словаря фильтров применяет их к запросу.
    """
    try:
        async with async_session() as session:
            users = (await session.scalars(select(User))).all()

            if filters:
                conditions = []
                for key, value in filters.items():
                    if hasattr(User, key):
                        logger.info(f'{key=}')
                        conditions.append(getattr(User, key) == value)
                if conditions:
                    logger.info(f'{conditions=}')
                    users = (await session.scalars(select(User).filter(*conditions))).all()
                    logger.info(f'После фильтра {users=}')
                
                
            logger.info(f'{users=}')
            return users
            # logger.info(f'{users=}')
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при получении данных о пользователях {e}')
        return None



# блок методов, отвечающих за добалвение новых данных о резюме, вакансиях, пользователях, работодателях, обучающих курсах


@connection
async def add_new_user(session, user_data:dict) -> User:
    '''Добавляет нового пользователя в таблицу users'''
    try:
        async with async_session() as session:
            user = await session.scalar(select(User).filter_by(nickname=user_data.get('nickname')))

            if not user:
                new_user = User(
                    name = user_data.get('name'),
                    surname = user_data.get('surname'),
                    nickname = user_data.get('nickname'),
                    password = user_data.get('password')
                )
                session.add(new_user)
                logger.info(f'Добавлен новый пользователь с nickname={user_data.get('nickname')}')
                await session.commit()
                logger.info('Сессия сохранена')
                return new_user
            else:
                logger.info(f'Пользователь с nickname={user_data.get('nickname')} уже существует')
                await session.commit()
                return None
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при попытке добавления нового пользователя {e}')
        return None
    

@connection
async def add_new_vacansy(session, vacancy_data:dict) -> Vacancy:
    '''Добавляет новую вакансию в таблицу vacancies'''
    try:
        async with async_session() as session:
            vacansy = await session.scalar(select(Vacancy).filter_by(company_name=vacancy_data.get('company_name'), position=vacancy_data.get('position'),
                                                                   salary=vacancy_data.get('salary'), email=vacancy_data.get('email')))

            if not vacansy:
                new_vacansy = Vacancy(
                    company_name = vacancy_data.get('company_name'),
                    position = vacancy_data.get('position'),
                    salary = vacancy_data.get('salary'),
                    work_schedule = vacancy_data.get('work_schedule'),
                    employment_type = vacancy_data.get('employment_type'),
                    experience_required = vacancy_data.get('experience_required'),
                    employer_guarantees = vacancy_data.get('employer_guarantees'),
                    additional_info = vacancy_data.get('additional_info'),
                    email = vacancy_data.get('email'),
                    phone = vacancy_data.get('phone')                
                )
                session.add(new_vacansy)
                logger.info(f'Добавлена новая вакансия по профессии {vacancy_data.get('position')}')
                await session.commit()
                logger.info('Сессия сохранена')
                return new_vacansy
            else:
                logger.info(f'Вакансия с такими параметрами уже существует')
                await session.commit()
                return None
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при попытке добавления новой вакансии {e}')
        return None



@connection
async def add_new_employer(session, employer_data:dict) -> Employer:
    '''Добавляет нового работодателя в таблицу employers'''
    try:
        async with async_session() as session:
            employers = await session.scalar(select(Employer).filter_by(nickname=employer_data.get('nickname')))

            if not employers:
                new_employer = Employer(
                    name = employer_data.get('name'),
                    surname = employer_data.get('surname'),
                    company_name = employer_data.get('company_name'),
                    nickname = employer_data.get('nickname'),
                    password = employer_data.get('password')
                )
                session.add(new_employer)
                logger.info(f'Добавлена новый работодатель с ником {employer_data.get('nickname')}')
                await session.commit()
                logger.info('Сессия сохранена')
                return new_employer
            else:
                logger.info(f'Работодатель с nickname={employer_data.get('nickname')} уже существует')
                await session.commit()
                return None
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при попытке добавления нового работодателя {e}')
        return None



@connection
async def add_new_resume(session, resume_data:dict) -> Resume:
    '''Добавляет новое резюме в таблицу resumes'''
    try:
        async with async_session() as session:
            resumes = await session.scalar(select(Resume).filter_by(
                name=resume_data.get('name'),
                surname=resume_data.get('surname'),
                email=resume_data.get('email'),
                phone=resume_data.get('phone')))

            if not resumes:
                new_resume = Resume(
                    name = resume_data.get('name'),
                    surname = resume_data.get('surname'),
                    age = resume_data.get('age'),
                    position = resume_data.get('position'),
                    experience = resume_data.get('experience'),
                    region = resume_data.get('region'),
                    about_me = resume_data.get('about_me'),
                    email = resume_data.get('email'),
                    phone = resume_data.get('phone'),
                    habits = resume_data.get('habits')
                )
                session.add(new_resume)
                logger.info(f'Добавлено новое резюме по профессии {resume_data.get('position')}')
                await session.commit()
                logger.info('Сессия сохранена')
                return new_resume
            else:
                logger.info(f'Резюме с такими данными уже добавлено')
                await session.commit()
                return None
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при попытке добавления нового резюме {e}')
        return None



if __name__ == '__main__':

    import asyncio

    async def main():
        
        logger.info('Запускаем асинхронную функцию для тестирования')
        # logger.info('Запускаем асинхронную функцию для тестирования')
        
        # проверка работы функции get_resumes без параметров
        # result = await get_resumes()
        
        # проверка работы функции get_resumes с параметрами 
        # params = dict(position='Фармацевт')
        # result = await get_resumes(filters=params)
        
        # проверка работы функции get_vacancyes без параметров
        # result = await get_vacancyes()
        
        # проверка работы функции get_vacancyes с параметрами 
        # params = dict(position='Фармацевт', employment_type='Частичная')
        # result = await get_vacancyes(filters=params)

        # проверка работы функции get_training_courses без параметров
        #result = await get_training_courses()
        
        # проверка работы функции get_training_courses с параметрами 
        # params = dict(type_of_course='Онлайн-школы')
        # result = await get_training_courses(filters=params)

        # проверка работоспособности функции add_new_user
        # user_data = {'name':"Олег", 'surname':'Золотарёв', 'nickname':'Zolot12', 'password':'Zolot12'}
        # result = await add_new_user(user_data=user_data)
        
        # проверка работоспособности функции add_new_vacansy
        # vacancy_data = {'company_name':"АЙБОЛИТ", 'position':'Фармацевт', 'salary':83000, 
        #                 'work_schedule':'пн, чт', 'employment_type':'Частичная', 'experience_required': 'от 1 года', 
        #                 'employer_guarantees':None, 'additional_info':None, 'email': 'aibolit@list.ru', 'phone': '89213456456'}
        # result = await add_new_vacansy(vacancy_data=vacancy_data)
        
        
        # проверка работоспособности функции add_new_employer
        # employer_data = {'name':"Денис", 'surname':'Токарев', 'company_name':'МЕНЕДЖ-ДРАЙВ', 
        #                 'nickname':'Den81', 'password':'Den81'}
        # result = await add_new_employer(employer_data=employer_data)

        # проверка работоспособности функции add_new_resume
        resume_data = {'name':"Томас", 'surname':'Коноплёв', 'age':41, 
                        'position':'Экономист', 'experience':'3 года','region':'Щёлково', 'about_me':'Комуникабелен и предусмотрителен',
                        'email':'tomas83@list.ru', 'phone':'89234567432', 'habits':'Отсутствуют'}
        result = await add_new_resume(resume_data=resume_data)
        
        return result

    result = asyncio.run(main())
    