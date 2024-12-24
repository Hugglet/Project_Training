from flask import Blueprint, jsonify, make_response, redirect, render_template, request, url_for
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, verify_jwt_in_request
from flask_login import login_manager, login_user
from pydantic import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from app.db.models import UserRole
from app.db.repositories.user import UserRepository
from app.exception_handlers import CustomException
from app.schemas import UserCreateSchema

main_blueprint = Blueprint("main", __name__)
repository = UserRepository()

@main_blueprint.route('/', methods=['GET'])
def index():
    try:
        # Пытаемся проверить наличие токена в запросе
        verify_jwt_in_request()
        user_identity = get_jwt_identity()
        user = repository.get_user_by_id(user_identity)
        return render_template('index.html', user=user)
    except Exception:
        # Если токен не передан или некорректен, передаем значение None для неаутентифицированного пользователя
        return render_template('index.html', user=None)
    

# Регистрация нового пользователя
@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные из формы
        form_data = request.form.to_dict()

        # Проверка, существует ли пользователь с таким именем
        existing_user = repository.get_user_by_username(form_data["login"])
        if existing_user:
            raise CustomException(message="User login already exists", status_code=400, redirect_page="main.register")
        existing_user = repository.get_user_by_email(form_data["email"])
        if existing_user:
            raise CustomException(message="User email already exists", status_code=400, redirect_page="main.register")

        hashed_password = generate_password_hash(form_data['password'])

        try:
            user_schema = UserCreateSchema(**form_data)
            user_schema.password = hashed_password
        except ValidationError as e:
            raise CustomException(message="Invalid user data", status_code=422, redirect_page="main.register")
        
        user_id = repository.create_user(user_schema)
        
        return render_template('login.html')  # Перенаправление на страницу логина после регистрации
    
    return render_template('register.html')


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')

        user = repository.get_user_by_username(username)
        if user:
            if check_password_hash(user.password, password):
                # Создаем JWT
                access_token = create_access_token(identity=str(user.id))
                response = make_response(render_template("dashboard.html", user=user))
                # Сохраняем токен в cookie
                set_access_cookies(response, access_token)
                return response
            
        error_message = "Invalid username or password"
        return render_template('login.html', error=error_message)
        
    return render_template('login.html')


@main_blueprint.route('/dashboard', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = repository.get_user_by_id(user_id)
    if not user:
        return CustomException(message="User not found", status_code=404)
    
    return render_template('dashboard.html', user=user)


@main_blueprint.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    response = make_response(render_template("index.html"))
    # Удаляем токен из cookies
    response.delete_cookie('access_token_cookie')
    return response