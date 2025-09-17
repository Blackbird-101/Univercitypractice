import os, sys
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Text,
    DateTime
)
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from datetime import datetime
from typing import List

Base = declarative_base()

class SerializableMixin:
    def to_dict(self):
        ret_data = {}
        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        
        for column in columns:
            value = getattr(self, column)
            ret_data[column] = value
            
        for rel in relationships:
            related_obj = getattr(self, rel)
            if related_obj:
                if isinstance(related_obj, list):
                    ret_data[rel] = [obj.to_dict() for obj in related_obj]
                else:
                    ret_data[rel] = related_obj.to_dict()
        
        return ret_data    


# Базовая модель пользователя
class User(Base, SerializableMixin):
    __tablename__ = 'users'
    
    # Уникальный идентификатор пользователя
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Личные данные
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # Имя
    surname = mapped_column(String(100), nullable=False)  # Фамилия
    
    # Данные для авторизации
    nickname: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)  # Никнейм
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # Пароль
    
    def __repr__(self):
        return f'id-пользователя:{self.id}**Имя:{self.name}**Фамилия:{self.surname}**Никнейм:{self.nickname}**Пароль:{self.password}'


# Модель работодателя (наследует от User)
class Employer(Base, SerializableMixin):
    __tablename__ = 'employers'
    
    # Наследование от базовой таблицы users
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Личные данные
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # Имя
    surname = mapped_column(String(100), nullable=False)  # Фамилия
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)  # Название компании
    
    # Данные для авторизации
    nickname: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)  # Никнейм
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # Пароль

    def __repr__(self):
        return f'id-работодателя:{self.id}**Имя:{self.name}**Фамилия:{self.surname}**Никнейм:{self.nickname}**Пароль:{self.password}**Компания:{self.company_name}'
        


# Модель вакансии
class Vacancy(Base, SerializableMixin):
    __tablename__ = 'vacancies'
    
    # Идентификатор вакансии
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Основная информация о вакансии
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)  # Название компании
    position: Mapped[str] = mapped_column(String(255), nullable=False)  # Должность
    salary: Mapped[float] = mapped_column(Float, nullable=True)  # Зарплата
    work_schedule: Mapped[str] = mapped_column(String(100), nullable=False)  # График работы
    employment_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Тип занятости
    experience_required: Mapped[str] = mapped_column(String(100), nullable=False)  # Требуемый опыт
    
    # Дополнительная информация
    employer_guarantees: Mapped[str] = mapped_column(Text, nullable=True)  # Гарантии работодателя
    additional_info: Mapped[str] = mapped_column(Text, nullable=True)  # Дополнительная информация
    
    # Контактные данные
    email: Mapped[str] = mapped_column(String(255), nullable=False)  # Email
    phone: Mapped[str] = mapped_column(String(20), nullable=False)  # Телефон

    def __repr__(self):
        return f'id-вакансии:{self.id}**Название компании:{self.company_name}**Должность:{self.position}**Зарплата:{self.salary}**\
        График работы:{self.work_schedule}**Тип занятости:{self.employment_type}**Требуемый опыт:{self.experience_required}**\
        **Гарантии работодателя:{self.employer_guarantees}**Доп.инфо.:{self.additional_info}**Email:{self.email}**Телефон:{self.phone}'



# Модель резюме
class Resume(Base, SerializableMixin):
    __tablename__ = 'resumes'
    
    # Идентификатор резюме
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Основная информация
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # Имя
    surname = mapped_column(String(100), nullable=False)  # Фамилия
    age: Mapped[int] = mapped_column(Integer, nullable=False) # Возраст
    position: Mapped[str] = mapped_column(String(255), nullable=False)  # Искомая должность
    experience: Mapped[str] = mapped_column(String(100), nullable=False)  # Опыт работы
    region: Mapped[str] = mapped_column(String(255), nullable=False)  # Регион проживания
    
    # Дополнительная информация
    about_me: Mapped[str] = mapped_column(Text, nullable=True)  # О себе
    
    # Контактные данные
    email: Mapped[str] = mapped_column(String(255), nullable=False)  # Email
    phone: Mapped[str] = mapped_column(String(20), nullable=False)  # Телефон
    habits: Mapped[str] = mapped_column(String(255), nullable=True)  # Вредные привычки

       
    def __repr__(self):
        return f'id-резюме:{self.id}**Имя:{self.name}**Фамилия:{self.surname}**Возраст:{self.age}**Искомая должность:{self.position}\
            **Опыт работы:{self.experience}**Регион проживания:{self.region}**О себе:{self.about_me}\
                **Email:{self.email}**Телефон:{self.phone}**Вредные привычки:{self.habits}'
    

# Модель обучающего курса
class TrainingCourse(Base, SerializableMixin):
    __tablename__ = 'training_courses'
    
    # Идентификатор курса
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Основная информация о курсе
    course_name: Mapped[str] = mapped_column(String(255), nullable=False)  # Название курса
    duration: Mapped[str] = mapped_column(String(100), nullable=False)     # Продолжительность обучения
    cost: Mapped[float] = mapped_column(Float, nullable=False)              # Стоимость курса
    direction: Mapped[str] = mapped_column(String(255), nullable=False)    # Направление обучения
    type_of_course: Mapped[str] = mapped_column(String(255), nullable=False) # к какому типу относятся курсы (Курсы от работодателей, Онлайн-школы, Обучение в ВУЗах)
    
    # Расписание занятий
    days: Mapped[str] = mapped_column(String(100), nullable=False)        # Дни проведения занятий
    time: Mapped[str] = mapped_column(String(100), nullable=False)        # Время проведения занятий
    
    # Форматы обучения
    form: Mapped[str] = mapped_column(String(100), nullable=False)        # Форма занятий (групповые/индивидуальные)
    
    # Информация о преподавателе
    teacher: Mapped[str] = mapped_column(String(255), nullable=False)     # ФИО преподавателя

    def __repr__(self):
        return f'id-курса:{self.id}**Название курса:{self.course_name}**Продолжительность обучения:{self.duration}**Стоимость курса:{self.cost}\
            **Направление обучения:{self.direction}**Тип курса:{self.type_of_course}**Дни занятий:{self.days}\
                **Время занятий:{self.time}**Форма занятий:{self.form}**Преподаватель:{self.teacher}'


# Пояснения связей между таблицами:

# Связь между User и Employer/Applicant:
# - Наследование (Single Table Inheritance)
# - Один пользователь может быть либо работодателем, либо соискателем

# Связь между Employer и Vacancy:
# - Один ко многим (One-to-Many)
# - Один работодатель может размещать несколько вакансий
# - Каждая вакансия принадлежит одному работодателю

# Связь между Applicant и Resume:
# - Один ко многим (One-to-Many)
# - Один соискатель может иметь несколько резюме
# - Каждое резюме принадлежит одному соискателю

# Важные примечания:
# 1. Все связи определены через ForeignKey
# 2. Использован подход back_populates для двусторонних отношений
# 3. Все строковые поля имеют ограничение по длине
# 4. Числовые поля (например, зарплата, стоимость) хранятся в типе Float
# 5. Для текстовых полей используется тип Text



if __name__ == '__main__':

    import asyncio
    from db_class import engine
    
    
    async def create_table():
        """Вручную создает таблицу в БД"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    
    asyncio.run(create_table())