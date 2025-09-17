from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import DataRequired

class AuthForm(FlaskForm):
    nickname = StringField('Никнейм')
    password = PasswordField('Пароль')
    user_type = RadioField('Тип пользователя', choices=[('user', 'Пользователь'), ('employer', 'Работодатель')], validators=[DataRequired()], default='user')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    company_name = StringField('Название организации')
    user_type = RadioField('Тип пользователя', choices=[('user', 'Пользователь'), ('employer', 'Работодатель')], validators=[DataRequired()], default='user' )
    submit = SubmitField('Зарегистрироваться')