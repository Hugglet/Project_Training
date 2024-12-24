from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate
from app.db.models import UserRole
from app.db.repositories.user import UserRepository
from app.exception_handlers import CustomException
from app.schemas import UserCreateSchema, UserUpdateSchema
from werkzeug.security import generate_password_hash

user_blueprint = Blueprint("users", __name__)

repository = UserRepository()

def admin_middleware() -> None:
    role = repository.get_user_by_id(get_jwt_identity()).role
    if role != UserRole.ADMIN.value:
        raise CustomException(
            message="У пользователя отсутствуют права", 
            status_code=403
        )

@user_blueprint.route('/', methods=['GET'])
@jwt_required()
def list():
    admin_middleware()
    users = repository.get_users_all()
    print([user.login for user in users])
    user = repository.get_user_by_id(get_jwt_identity())
    return render_template('users/user_list.html', users=users, user=user)


@user_blueprint.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def detail(user_id):
    admin_middleware()
    user = repository.get_user_by_id(user_id)
    if not user:
        raise CustomException(message="Не найден пользователь", status_code=404)
    return render_template('users/user.html', user=user)


@user_blueprint.route('/<int:user_id>/delete', methods=['GET'])
@jwt_required()
def delete(user_id):
    success = repository.delete_user(user_id)
    if not success:
        return CustomException(message="Не найден пользователь", status_code=404)
    return redirect(url_for('users.list'))


@user_blueprint.route('/<int:user_id>', methods=['POST'])
@jwt_required()
def update(user_id):
    form_data = request.form.to_dict()
    schema = UserUpdateSchema(**form_data)
    schema.password = generate_password_hash(form_data["password"])
    model_id = repository.update_user(user_id, schema)
    if not model_id:
        return CustomException(message="Не найден пользователь", status_code=404)
    return redirect(url_for('users.detail', user_id=model_id))


# @user_blueprint.route('/<int:user_id>', methods=['GET'])
# @jwt_required()
# def edit_page(user_id):
#     user = repository.get_user_by_id(user_id)
#     return render_template("users/edit.html", user=user)