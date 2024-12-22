from flask import jsonify, redirect, render_template, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate
from app.db.models import UserRole
from app.db.repositories.event import EventRepository
from app.db.repositories.user import UserRepository
from app.exception_handlers import CustomException
from app.schemas import EventCreateSchema, EventUpdateSchema
from main import app

repository = EventRepository()
user_repository = UserRepository()

def event_middleware() -> None:
    role = user_repository.get_user_by_id(get_jwt_identity()).role
    if role != UserRole.ADMIN or role != UserRole.HOST:
        raise CustomException(
            message="У пользователя отсутствуют права", 
            status_code=403
        )


@app.route('/events', methods=['GET'])
def get_events():
    events = repository.get_events_all()
    return render_template('events/events.html', events=events)


@app.route('/events', methods=['POST'])
@jwt_required()
@validate(body=EventCreateSchema)
def create_event(event: EventCreateSchema):
    event_middleware()
    created_event = repository.create_event(event)
    return redirect(url_for('event_detail', event_id=created_event))


@app.route('/events/<int:event_id>', methods=['GET'])
def event_detail(event_id):
    event = repository.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return render_template('events/event.html', event=event)


@app.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    event_middleware()
    success = repository.delete_event(event_id)
    if not success:
        return CustomException(message="Не найдено мероприятие", status_code=404)
    return jsonify({"message": "Event deleted"}), 200


@app.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
@validate(body=EventUpdateSchema)
def edit_event(event_id, body: EventUpdateSchema):
    event_middleware()
    edited_event = repository.update_event(event_id, body)
    if not edited_event:
        return jsonify({"error": "Event not found"}), 404
    return redirect(url_for('event_detail', event_id=edited_event))
