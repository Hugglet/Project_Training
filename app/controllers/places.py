from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_pydantic import validate
from app.db.models import UserRole
from app.db.repositories.place import PlaceRepository
from app.db.repositories.user import UserRepository
from app.exception_handlers import CustomException
from app.schemas import PlaceCreateSchema, PlaceUpdateSchema

place_blueprint = Blueprint("places", __name__)

repository = PlaceRepository()
user_repository = UserRepository()

def host_middleware() -> None:
    role = user_repository.get_user_by_id(get_jwt_identity()).role
    if role != UserRole.ADMIN.value and role != UserRole.HOST.value:
        raise CustomException(
            message="У пользователя отсутствуют права", 
            status_code=403
        )


@place_blueprint.route('/', methods=['GET'])
def list():
    places = repository.get_places_all()
    try:
        verify_jwt_in_request()
        user = user_repository.get_user_by_id(get_jwt_identity())
        return render_template('places/place_list.html', places=places, user=user)
    except Exception as e:
        return render_template('places/place_list.html', places=places, user=None)


@place_blueprint.route('/', methods=['POST'])
@jwt_required()
def create():
    host_middleware()
    form_data = request.form.to_dict()
    created_place = repository.create_place(PlaceCreateSchema(**form_data))
    return redirect(url_for('places.list'))


@place_blueprint.route('/<int:place_id>', methods=['GET'])
def detail(place_id):
    place = repository.get_place_by_id(place_id)
    if not place:
        raise CustomException(message="Place not found", status_code=404, redirect_page="places.list")
    return render_template('places/place_detail.html', place=place)


@place_blueprint.route('/<int:place_id>/delete', methods=['GET'])
@jwt_required()
def delete(place_id):
    host_middleware()
    success = repository.delete_place(place_id)
    if not success:
        raise CustomException(message="Place not found", status_code=404, redirect_page="places.list")
    return redirect(url_for('places.list'))


@place_blueprint.route('/<int:place_id>', methods=['POST'])
@jwt_required()
def update(place_id):
    host_middleware()
    form_data = request.form.to_dict()
    edited_place = repository.update_place(place_id, PlaceUpdateSchema(**form_data))
    if not edited_place:
        raise CustomException(message="Place not found", status_code=404, redirect_page="places.list")
    return redirect(url_for('place_detail', place_id=edited_place))
