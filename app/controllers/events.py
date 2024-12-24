from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_pydantic import validate
from app.db.models import UserRole
from app.db.repositories.event import EventRepository
from app.db.repositories.record import RecordRepository
from app.db.repositories.review import ReviewRepository
from app.db.repositories.user import UserRepository
from app.exception_handlers import CustomException
from app.schemas import EventCreateSchema, EventUpdateSchema, RecordCreateSchema, ReviewCreateSchema

event_blueprint = Blueprint("events", __name__)

repository = EventRepository()
user_repository = UserRepository()
review_repository = ReviewRepository()
record_repository = RecordRepository()

def event_middleware() -> None:
    role = user_repository.get_user_by_id(get_jwt_identity()).role
    if role != UserRole.ADMIN.value and role != UserRole.HOST.value:
        raise CustomException(
            message="У пользователя отсутствуют права", 
            status_code=403
        )


@event_blueprint.route('/', methods=['GET'])
def list():
    events = repository.get_events_all()
    try:
        verify_jwt_in_request()
        user = user_repository.get_user_by_id(get_jwt_identity())
        return render_template('events/event_list.html', events=events, user=user)
    except Exception as e:
        return render_template('events/event_list.html', events=events, user=None)


@event_blueprint.route('/', methods=['POST'])
@jwt_required()
def create():
    event_middleware()
    form_data = request.form.to_dict()
    created_event = repository.create_event(EventCreateSchema(**form_data))
    return redirect(url_for('events.list'))


@event_blueprint.route('/<int:event_id>', methods=['GET'])
def detail(event_id):
    event = repository.get_event_by_id(event_id)
    if not event:
        return CustomException(message="Не найдено мероприятие", status_code=404)
    return render_template('events/event.html', event=event)


@event_blueprint.route('/<int:event_id>/delete', methods=['GET'])
@jwt_required()
def delete(event_id):
    event_middleware()
    success = repository.delete_event(event_id)
    if not success:
        return CustomException(message="Не найдено мероприятие", status_code=404)
    return redirect(url_for("events.list"))


@event_blueprint.route('/<int:event_id>', methods=['POST'])
@jwt_required()
def update(event_id):
    event_middleware()
    form_data = request.form.to_dict()
    edited_event = repository.update_event(event_id, EventUpdateSchema(**form_data))
    if not edited_event:
        return CustomException(message="Event not found", status_code=404)
    return redirect(url_for('events.detail', event_id=edited_event))


@event_blueprint.route('/<int:event_id>/reviews', methods=['GET'])
def review_list(event_id):
    reviews = review_repository.get_reviews_all()
    try:
        verify_jwt_in_request()
        user = user_repository.get_user_by_id(get_jwt_identity())
        return render_template('events/reviews/review_list.html', reviews=reviews, user=user, event_id=event_id)
    except Exception as e:
        return render_template('events/reviews/review_list.html', reviews=reviews, user=None, event_id=event_id)


@event_blueprint.route('/<int:event_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(event_id: int):

    user_id = get_jwt_identity()

    form_data = request.form.to_dict()
    form_data['user_id'] = user_id
    form_data['event_id'] = event_id
    review_id = review_repository.create_review(ReviewCreateSchema(**form_data))

    return redirect(url_for("events.review_list", event_id=event_id))


@event_blueprint.route('/<int:event_id>/reviews/<int:review_id>', methods=['GET'])
def review_detail(event_id, review_id):
    review = review_repository.get_review_by_id(review_id)
    if not review:
        raise CustomException(message="Не найден отзыв", status_code=404)
    return render_template('events/reviews/review.html', review=review)


@event_blueprint.route('/<int:event_id>/reviews/<int:review_id>/delete', methods=['GET'])
@jwt_required()
def review_delete(event_id, review_id):
    user = user_repository.get_user_by_id(get_jwt_identity())
    success = review_repository.delete_review(review_id)
    if not success:
        raise CustomException(message="Не найден отзыв", status_code=404)
    return redirect(url_for("events.review_list", event_id=event_id, user=user))


# Records routes
@event_blueprint.route('/<int:event_id>/records', methods=['GET'])
def record_list(event_id):
    records = record_repository.get_records_all()
    try:
        verify_jwt_in_request()
        user = user_repository.get_user_by_id(get_jwt_identity())
        return render_template('events/record_list.html', records=records, user=user, event_id=event_id)
    except Exception as e:
        return render_template('events/record_list.html', records=records, user=None, event_id=event_id)


@event_blueprint.route('/<int:event_id>/records', methods=['POST'])
@jwt_required()
def create_record(event_id):
    record = RecordCreateSchema(
        user_id=get_jwt_identity(),
        event_id=event_id
    )
    try:
        created_record = record_repository.create_record(record)
        flash(message="Запись успешно создана", category='success')
    except Exception as e:
        flash(message="Запись от вас уже создана", category='error')
    return redirect(url_for('events.record_list', event_id=event_id))


@event_blueprint.route('/<int:event_id>/records/<int:record_id>/delete', methods=['GET'])
@jwt_required()
def record_delete(event_id, record_id):
    success = record_repository.delete_record(record_id)
    if not success:
        raise CustomException(message="Не найдена запись", status_code=404)
    return redirect(url_for('events.record_list', event_id=event_id))