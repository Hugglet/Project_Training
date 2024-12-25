from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from app.db.repositories.user import UserRepository
from app.exception_handlers import CustomException, handle_custom_error, handle_generic_error
from app.controllers import (
    main_blueprint,
    event_blueprint,
    place_blueprint,
    user_blueprint,
)
from app.config import Config
from dotenv import load_dotenv

load_dotenv(override=True)  # Загружаем переменные окружения

# Инициализация репозитория
repository = UserRepository()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.secret_key = "shurikgat-2704"

    # Инициализация расширений
    JWTManager(app)
    Bootstrap5(app)

    # # Инициализация LoginManager
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_view = "main.login"  # Указываем маршрут для страницы логина

    # # Прописываем user_loader
    # @login_manager.user_loader
    # def user_loader(user_id):
    #     return repository.get_user_by_id(user_id)  # Получаем пользователя по ID

    # Регистрация блюпринтов
    app.register_blueprint(main_blueprint)
    app.register_blueprint(event_blueprint, url_prefix="/events")
    app.register_blueprint(place_blueprint, url_prefix="/places")
    app.register_blueprint(user_blueprint, url_prefix="/users")

    # Регистрация обработчиков ошибок
    app.register_error_handler(CustomException, handle_custom_error)
    app.register_error_handler(Exception, handle_generic_error)

    return app
