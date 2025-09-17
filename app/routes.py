import os, sys
from typing import List

from app.base import add_new_employer, add_new_user, add_new_vacansy, find_suitable_ones_resumes, find_suitable_ones_vacancyes, get_employers, get_resumes, get_training_courses, get_users, get_vacancyes
from app.forms import AuthForm, RegisterForm
from app.models import Employer, Resume, User
from app.utils import process_professions, associate_logo, transliterate, associate_courses
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)

from flask import Blueprint, abort, render_template, request, redirect, send_from_directory, url_for, flash, session
from logger import logger
# Создаем блюпринт
main = Blueprint('main', __name__)

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static'),
                              'favicon.ico', mimetype='image/vnd.microsoft.icon')


@main.route('/')
def index():
    """Главная страница"""
    # Для примера: получаем всех пользователей
    form = AuthForm()
    error = None
    return render_template('index.html')


@main.route('/auth', methods=['GET', 'POST'])
async def auth():
    logger.info('внутри обработчика /auth')
    form = AuthForm()
    error = None
    session['user_type'] = form.user_type.data
    
    if form.validate_on_submit():
        try:
            nickname = form.nickname.data
            password = form.password.data
            user_type = form.user_type.data

            logger.info(f'{nickname=} {password=} {user_type=}')
            
            if user_type == 'user':
                logger.info('Работаем с пользователем')
                user = await get_users(filters=dict(nickname=nickname, password=password))
                if user:
                    logger.info('Пользователь с такими данными найден')
                    session['user_type'] = 'user'
                    session['nickname'] = nickname
                    session['password'] = password
                    name = f"{user[0].name} {user[0].surname}"
                    return render_template('index.html', name=name)
                else:
                    error = 'Некорректно введен никнейм или пароль'
                    logger.error(error)
                    
            else:
                logger.info('Работаем с работодателем')
                employer = await get_employers(filters=dict(nickname=nickname, password=password))
                if employer:
                    logger.info('Работодатель с такими данными найден')
                    session['user_type'] = 'employer'
                    session['nickname'] = nickname
                    session['password'] = password
                    name = f"{employer[0].name} {employer[0].surname}"
                    return render_template('index.html', name=name)
                else:
                    error = 'Некорректно введен никнейм или пароль'
                    logger.error(error)
            
            
        except Exception as e:
            flash(f'Произошла ошибка: {str(e)}')
    

    return render_template('auth.html', form=form, error=error, session=session)


@main.route('/register/<user_type>', methods=['GET', 'POST'])
async def register(user_type:str):
    logger.info('внутри /register')
    session['user_type'] = user_type
    logger.info(f'{user_type=}')
    form = RegisterForm()
    logger.info(form)
    error = None
    if form.validate_on_submit():
        try:
            # Проверка совпадения паролей
            if form.password.data != form.confirm_password.data:
                error = 'Введенные пароли не совпадают'
                return render_template('register.html', form=form, error=error, user_type=session['user_type'])
            
            # Проверка уникальности никнейма
            if user_type == 'user':
                user = await get_users(filters=dict(nickname=form.nickname.data))
                if user:
                    error = 'Пользователь с таким ником уже зарегистрирован'
                    return render_template('register.html', form=form, error=error)
                
                user_data = {
                    'name': form.name.data,
                    'surname': form.surname.data,
                    'nickname' : form.nickname.data,
                    'password' : form.password.data 
                }
                
                await add_new_user(user_data=user_data)
                
            else:
                employer = await get_employers(filters=dict(nickname=form.nickname.data))
                if employer:
                    error = 'Работодатель с таким ником уже зарегистрирован'
                    return render_template('register.html', form=form, error=error, user_type=session['user_type'])
                

                employer_data = {
                    'name': form.name.data,
                    'surname': form.surname.data,
                    'nickname' : form.nickname.data,
                    'password' : form.password.data,
                    'company_name': form.company_name.data
                }
                
                await add_new_employer(employer_data=employer_data)
                
                session['user_type'] = 'employer'
                session['nickname'] = form.nickname.data
                session['password'] = form.password.data
            session['success_add_vacansy'] = True
            session['message'] = 'Вы успешно зарегистрированы! Успехов в поиске работы!'
            
            return redirect(url_for('main.go_to_page', page_name='index'))
        except Exception as e:
            flash(f'Произошла ошибка: {str(e)}')
        return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form, error=error)



@main.route('/logout')
def logout():
    session.pop('user_type', None)
    session.pop('nickname', None)
    return redirect(url_for('main.go_to_page', page_name='index'))


@main.route('/<page_name>', methods=['POST', 'GET'])
async def go_to_page(page_name:str):
    '''Переход на адрес страницы, указанной в аргументе'''
    try:
        logger.info(f'{page_name=}')
        if page_name != 'employers':
            session.pop('find_resume_flag', None)
        logger.info(f'{session=}')
        name = ''
        allowed = {'index', 'information', 'job_openings', 'employers', 'position', 'register', 'auth', 'base'}  # добавляйте свои страницы
        # if page_name not in allowed:
        #     abort(404)

        # Проверка авторизации
        if ('user_type' in session) and ('nickname' in session):
            if session['user_type'] == 'user':
                user = await get_users(filters=dict(nickname=session['nickname'], password=session['password']))
                name = f"{user[0].name} {user[0].surname}"
            else:
                employer = await get_employers(filters=dict(nickname=session['nickname'], password=session['password']))
                name = f"{employer[0].name} {employer[0].surname}"
        else:
            name = None

        vacancies_info = await get_vacancyes()
        #print(f'{vacancies_info=}')
        all_companyies = set([vacancy.company_name for vacancy in vacancies_info])
        logger.info(f'{all_companyies=}')
        positions = [vacancy.position for vacancy in vacancies_info]
        logger.info(f'{positions=}')
        vacancies = process_professions(positions)

        if request.method == 'POST':
            page_name = 'job_openings'
            logger.info('отправляем данные формы')
            filters = {}  # создаем словарь с параметрами вакансии
            
            filters.setdefault('position',request.form.get('position'))
            filters.setdefault('company_name',request.form.get('company_name'))
            filters.setdefault('salary',request.form.get('salary'))
            filters.setdefault('employment_type',request.form.get('employment_type'))
            filters.setdefault('experience_required',request.form.get('experience'))

            logger.info(f'{filters=}')
            find_vacancyes = await find_suitable_ones_vacancyes(filters=filters)
            logger.info(f'{find_vacancyes=}')
            return render_template(f'{page_name}.html', vacancies=vacancies, all_companyies=all_companyies, find_vacancyes=find_vacancyes, associate_logo=associate_logo, name=name)


        if page_name == 'job_openings':
            return render_template(f'{page_name}.html', vacancies=vacancies, all_companyies=all_companyies, associate_logo=associate_logo, name=name)
        
        if page_name == 'employers':
            logger.info('Строка 203 go_to_page ')
            #print(f'{vacancies=}')
            all_resumes = await get_resumes()
            all_regions = {resume.region for resume in all_resumes}
            logger.info(f'{all_regions=}')
            session['vacancies'] = vacancies
            session['name'] = name
            session['all_regions'] = list(all_regions)

            return render_template(f'{page_name}.html', vacancies=vacancies, all_resumes=all_resumes, name=name, all_regions=all_regions)

        # if page_name in ['index', 'favicon.ico']:
        #     return render_template(f'{page_name}.html', name=name)
        
        return render_template(f'{page_name}.html', name=name)
    except Exception as e:
        logger.error(f'Произошла ошибка {e}')
        return render_template('error.html')



@main.route('/job_opening/vacancy/<position>')
async def show_vacancy(position:str):
    '''Осуществляет переход на страницу для демонстрации вакансий по 
    конкретной профессии'''
    vacancies_info = await get_vacancyes()
    vacancies_of_position = [vacansy for vacansy in vacancies_info if vacansy.position == position ]
    logger.info(f'{vacancies_of_position=}')
    return render_template('position.html', vacancies=vacancies_of_position, position=position, transliterate=transliterate)



@main.route('/employers/resume/<position>')
async def show_resume(position:str):
    '''Осуществляет переход на страницу для демонстрации имеющихся в базе резюме по 
    конкретной профессии'''
    vacancies_info = await get_vacancyes()
    positions = [vacancy.position for vacancy in vacancies_info]
    vacancies = process_professions(positions)
    resumes_info:List[Resume] = await get_resumes()
    resumes_of_position = [resume for resume in resumes_info if resume.position == position]
    logger.info(f'{position=}')
    logger.info(f'{resumes_of_position=}')
    logger.info(f'{resumes_of_position=}')
    return render_template('employers.html', all_resumes=resumes_info, vacancies=vacancies, resumes_of_position=resumes_of_position)


@main.route('/training_courses/<course_type>')
async def show_courses(course_type:str):
    '''Отображает на странице обучающие курсы, в зависимости от
    переданного в аргументе типа курсов'''
    find_courses = await get_training_courses(filters={'type_of_course': course_type})
    logger.info(f'{find_courses=}')
    return render_template('training_courses.html', course_type=course_type, find_courses=find_courses, associate_courses=associate_courses)


@main.route('/employers/find_resumes_by_params', methods=['POST'])
async def find_resume_by_params():
    '''Отвечает за обработку формы поиска резюме по критериям'''
    logger.info('find_resume_by_params: Внутри формы')
    session['find_resume_flag'] = True
    filters = {}  # создаем словарь с параметрами вакансии
    filters.setdefault('position',request.form.get('profession'))
    filters.setdefault('age',[request.form.get('age_from'), request.form.get('age_to')])
    filters.setdefault('region',request.form.get('region'))
    logger.info(f'{filters=}')
    find_resumes = await find_suitable_ones_resumes(filters=filters)
    logger.info(f'{find_resumes=}')

    name = session.get('name')
    vacancies = session.get('vacancies')
    all_resumes = session.get('all_resumes')
    all_regions = session.get('all_regions')
    all_resumes = await get_resumes()
    
    return render_template(f'employers.html', vacancies=vacancies, all_resumes=all_resumes, 
                           name=name, all_regions=all_regions, 
                           find_resumes=find_resumes)


@main.route('/employers/add_new_vacancy', methods=['POST'])
async def add_new_vacansi():
    '''Отвечает за обработку формы добавления новой вакансии работодателем'''
    logger.info('add_new_vacansy: Внутри формы')
    name, surname = [item.strip() for item in session.get('name', '').split(' ')]

    filters = {
        'name': name,
        'surname': surname
    }

    employer = await get_employers(filters=filters)
    
    work_schedule = ','.join(request.form.getlist('choise', None))
    vacancy_info = {}
    vacancy_info.setdefault('company_name', employer[0].company_name)
    vacancy_info.setdefault('position', request.form.get('position'))
    vacancy_info.setdefault('post', request.form.get('post'))
    vacancy_info.setdefault('salary', float(request.form.get('cost')))
    vacancy_info.setdefault('position', request.form.get('position'))
    vacancy_info.setdefault('work_schedule', work_schedule)
    vacancy_info.setdefault('employment_type', request.form.get('employment'))
    vacancy_info.setdefault('experience_required', request.form.get('experience'))
    vacancy_info.setdefault('employer_guarantees', request.form.get('employer_guarantees'))
    vacancy_info.setdefault('additional_info', request.form.get('additional_info'))
    vacancy_info.setdefault('email', request.form.get('email'))
    vacancy_info.setdefault('phone', request.form.get('phone'))

    await add_new_vacansy(vacancy_data=vacancy_info)

    session['success_add_vacansy'] = True
    session['message'] = 'Новая вакансия успешно добавлена. Спасибо, что даете возможность людям работать!'

    return redirect(url_for('main.go_to_page', page_name='index'))
    


@main.route('/clear_session/<session_key>')
def clear_session(session_key:str):
    '''Позволяет удалить из сессии значения по переданному ключу'''
    session.pop(session_key, None)
    logger.info(f'Удаление ключа {session_key} из session успешно проведено')
    return redirect(url_for('main.go_to_page', page_name='index'))


@main.route('/information/send_message', methods=['POST'])
def send_message():
    '''Обрабатывает отправку данных формы со страницы information.html'''
    logger.info('send_message: Внутри формы')
    session['success_add_vacansy'] = True
    session['message'] = 'Ваше сообщение отправлено и будет рассмотрено администрацией сайта в ближайшее время'
    return redirect(url_for('main.go_to_page', page_name='index'))


@main.errorhandler(404)
@main.errorhandler(500)
def handle_errors(e):
    error_info = {
        404: {
            'title': 'Страница не найдена',
            'message': 'Запрошенная страница не существует'
        },
        500: {
            'title': 'Внутренняя ошибка сервера',
            'message': 'Извините за неудобства, наши специалисты уже работают над решением проблемы'
        }
    }
    
    logger.error(f"Произошла ошибка {e.code}: {str(e)}")
    return render_template('error.html', 
                           title=error_info[e.code]['title'], 
                           message=error_info[e.code]['message']), e.code






