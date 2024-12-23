from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from app.db.repositories.record import RecordRepository
from app.exception_handlers import CustomException
from app.schemas import RecordCreateSchema

record_blueprint = Blueprint("record", __name__)

repository = RecordRepository()

@record_blueprint.route('/', methods=['GET'])
@jwt_required()
def records_list():
    records = repository.get_records_all()
    return render_template('records/record_list.html', records=records)


@record_blueprint.route('/', methods=['POST'])
@jwt_required()
@validate(body=RecordCreateSchema)
def create_record(record: RecordCreateSchema):
    created_record = repository.create_record(record)
    return redirect(url_for('record_detail', record_id=created_record))


@record_blueprint.route('/<int:record_id>', methods=['GET'])
@jwt_required()
def record_detail(record_id):
    record = repository.get_record_by_id(record_id)
    if not record:
        raise CustomException(message="Не найдена запись", status_code=404)
    return render_template('records/record_detail.html', record=record)


@record_blueprint.route('/<int:record_id>', methods=['DELETE'])
@jwt_required()
def delete_record(record_id):
    success = repository.delete_record(record_id)
    if not success:
        raise CustomException(message="Не найдена запись", status_code=404)
    return jsonify({"message": "Record deleted"}), 200
