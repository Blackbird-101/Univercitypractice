from flask import Flask
from flask_wtf import CSRFProtect

from app.utils import translate_days
from .routes import main
from logger import logger

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Настройка конфигурации
    
    app.register_blueprint(main)  # Регистрация блюпринтов
    # регистриуем пользовательские функции
    app.add_template_filter(translate_days)
    csrf = CSRFProtect(app)
    logger.info('Экземпляр app создан')


    return app
