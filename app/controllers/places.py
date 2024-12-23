from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
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
    if role != UserRole.ADMIN or role != UserRole.HOST:
        raise CustomException(
            message="У пользователя отсутствуют права", 
            status_code=403
        )


@place_blueprint.route('/', methods=['GET'])
def list():
    places = repository.get_places_all()
    return render_template('places/place_list.html', places=places)


@place_blueprint.route('/', methods=['POST'])
@jwt_required()
@validate(body=PlaceCreateSchema)
def create(place: PlaceCreateSchema):
    host_middleware()
    created_place = repository.create_place(place)
    return redirect(url_for('place_detail', place_id=created_place))


@place_blueprint.route('/<int:place_id>', methods=['GET'])
def detail(place_id):
    place = repository.get_place_by_id(place_id)
    if not place:
        return jsonify({"error": "Place not found"}), 404
    return render_template('places/place_detail.html', place=place)


@place_blueprint.route('/<int:place_id>', methods=['DELETE'])
@jwt_required()
def delete(place_id):
    host_middleware()
    success = repository.delete_place(place_id)
    if not success:
        return jsonify({"error": "Place not found"}), 404
    return jsonify({"message": "Place deleted"}), 200


@place_blueprint.route('/<int:place_id>', methods=['PUT'])
@jwt_required()
@validate(body=PlaceUpdateSchema)
def update(place_id, body: PlaceUpdateSchema):
    host_middleware()
    edited_place = repository.update_place(place_id, body)
    if not edited_place:
        return jsonify({"error": "Place not found"}), 404
    return redirect(url_for('place_detail', place_id=edited_place))
