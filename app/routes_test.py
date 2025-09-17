from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User  # Предполагая, что у вас есть модель User
from app import db  # Импорт базы данных

# Создаем блюпринт
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Главная страница"""
    # Для примера: получаем всех пользователей
    users = User.query.all()
    return render_template('index.html', users=users)

@main.route('/add_user', methods=['POST'])
def add_user():
    """Добавление нового пользователя"""
    username = request.form.get('username')
    if username:
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь добавлен!', 'success')
    else:
        flash('Имя пользователя обязательно!', 'error')

    return redirect(url_for('main.index'))

@main.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Удаление пользователя"""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь удален!', 'success')
    else:
        flash('Пользователь не найден!', 'error')

    return redirect(url_for('main.index'))
