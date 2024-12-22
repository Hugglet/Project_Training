from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app.db.models import UserRole
from app.db.repositories.user import UserRepository
from app.schemas import UserCreateSchema, UserUpdateSchema
from main import app
from flask import jsonify, make_response, request, redirect, render_template, url_for
from flask_pydantic import validate

repository = UserRepository()

# Регистрация нового пользователя
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get('username')
        password = request.form.get('password')

        # Проверка, существует ли пользователь с таким именем
        existing_user = repository.get_user_by_username(username)
        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        # Создание пользователя
        user_data = UserCreateSchema(username=username, password=password)
        user_id = repository.create_user(user_data)
        
        return redirect(url_for('login_user'))  # Перенаправление на страницу логина после регистрации
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = repository.get_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            # Создаем JWT
            access_token = create_access_token(identity=user['id'])
            response = make_response(redirect(url_for('profile')))
            # Сохраняем токен в cookie
            response.set_cookie('access_token', access_token)
            return response

        return jsonify({"error": "Invalid credentials"}), 401
    
    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = repository.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user.role == UserRole.ADMIN:
        return render_template('admin_dashboard.html', user=user)
    elif user.role == UserRole.COMEDIAN:
        return render_template('comedian_dashboard.html', user=user)
    elif user.role == UserRole.HOST:
        return render_template('host_dashboard.html', user=user)
    elif user.role == UserRole.VIEWER:
        return render_template('viewer_dashboard.html', user=user)


@app.route('/logout', methods=['GET'])
@jwt_required()
def logout_user():
    response = make_response(redirect(url_for('login_user')))
    # Удаляем токен из cookies
    response.set_cookie('access_token', '', expires=0)
    return response