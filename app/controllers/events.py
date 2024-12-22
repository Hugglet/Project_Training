from flask import jsonify, redirect, render_template, url_for
from flask_pydantic import validate
from app.db.repositories.event import EventRepository
from app.schemas import EventCreateSchema, EventUpdateSchema
from main import app

repository = EventRepository()

@app.route('/events', methods=['GET'])
def get_events():
    events = repository.get_events_all()
    return render_template('events/events.html', events=events)


@app.route('/events', methods=['POST'])
@validate(body=EventCreateSchema)
def create_event(event: EventCreateSchema):
    created_event = repository.create_event(event)
    return redirect(url_for('event_detail', event_id=created_event))


@app.route('/events/<int:event_id>', methods=['GET'])
def event_detail(event_id):
    event = repository.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return render_template('events/event.html', event=event)


@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    success = repository.delete_event(event_id)
    if not success:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Event deleted"}), 200


@app.route('/events/<int:event_id>', methods=['PUT'])
@validate(body=EventUpdateSchema)
def edit_event(event_id, body: EventUpdateSchema):
    edited_event = repository.update_event(event_id, body)
    if not edited_event:
        return jsonify({"error": "Event not found"}), 404
    return redirect(url_for('event_detail', event_id=edited_event))
