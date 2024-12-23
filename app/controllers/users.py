from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate
from app.db.models import UserRole
from app.db.repositories.user import UserRepository
from app.exception_handlers import CustomException
from app.schemas import UserCreateSchema, UserUpdateSchema

user_blueprint = Blueprint("users", __name__)

repository = UserRepository()

def admin_middleware() -> None:
    role = repository.get_user_by_id(get_jwt_identity()).role
    if role != UserRole.ADMIN:
        raise CustomException(
            message="У пользователя отсутствуют права", 
            status_code=403
        )

@user_blueprint.route('/', methods=['GET'])
@jwt_required()
def list():
    admin_middleware()
    users = repository.get_users_all()
    return render_template('users/users.html', users=users)


@user_blueprint.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def detail(user_id):
    admin_middleware()
    user = repository.get_user_by_id(user_id)
    if not user:
        raise CustomException(message="Не найден пользователь", status_code=404)
    return render_template('users/user.html', users=user)


@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete(user_id):
    success = repository.delete_user(user_id)
    if not success:
        return CustomException(message="Не найден пользователь", status_code=404)
    return jsonify({"message": "User deleted"}), 200


@user_blueprint.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@validate(body=UserUpdateSchema)
def update(user_id, body: UserUpdateSchema):
    editted_model = repository.update_user(user_id, body)
    if not editted_model:
        return CustomException(message="Не найден пользователь", status_code=404)
    return redirect(url_for('user_detail', user=editted_model))