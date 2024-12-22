from flask import jsonify, redirect, render_template, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate
from app.db.models import UserRole
from app.db.repositories.user import UserRepository
from app.exception_handlers import CustomException
from app.schemas import UserCreateSchema, UserUpdateSchema
from main import app


repository = UserRepository()

@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    user = repository.get_user_by_id(user_id)
    if user.role != UserRole.ADMIN:
        raise CustomException(
            message="У пользователя отсутствуют права админа", 
            status_code=403
        )

    users = repository.get_users_all()
    return render_template('users/users.html', users=users)


@app.route('/users', methods=['POST'])
@jwt_required()
@validate(body=UserCreateSchema)
def create_user(user: UserCreateSchema):
    created_user = repository.create_user(user)
    return redirect(url_for('user_detail', user=created_user))


@app.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def user_detail(user_id):
    user = repository.get_user_by_id(user_id)
    if not user:
        raise CustomException(message="Не найден пользователь", status_code=404)
    return render_template('users/user.html', users=user)


@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    success = repository.delete_user(user_id)
    if not success:
        return CustomException(message="Не найден пользователь", status_code=404)
    return jsonify({"message": "User deleted"}), 200


@app.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@validate(body=UserUpdateSchema)
def edit_user(user_id, body: UserUpdateSchema):
    editted_model = repository.update_user(user_id, body)
    if not editted_model:
        return CustomException(message="Не найден пользователь", status_code=404)
    return redirect(url_for('user_detail', user=editted_model))