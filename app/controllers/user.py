from flask import jsonify, redirect, render_template, url_for
from flask_pydantic import validate
from app.db.repositories.user import UserRepository
from app.schemas import UserCreateSchema, UserUpdateSchema
from main import app


repository = UserRepository()

@app.route('/users', methods=['GET'])
def get_users():
    users = repository.get_users_all()
    return render_template('users/users.html', users=users)


@app.route('/users', methods=['POST'])
@validate(body=UserCreateSchema)
def create_user(user: UserCreateSchema):
    created_user = repository.create_user(user)
    return redirect(url_for('user_detail', user=created_user))


@app.route('/users/<int:user_id>', methods=['GET'])
def user_detail(user_id):
    user = repository.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return render_template('users/user.html', users=user)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = repository.delete_user(user_id)
    if not success:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200


@app.route('/users/<int:user_id>', methods=['PUT'])
@validate(body=UserUpdateSchema)
def edit_user(user_id, body: UserUpdateSchema):
    editted_model = repository.update_user(user_id, body)
    if not editted_model:
        return jsonify({"error": "User not found"}), 404
    return redirect(url_for('user_detail', user=editted_model))