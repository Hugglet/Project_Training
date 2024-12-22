from flask import jsonify, redirect, render_template, url_for
from flask_pydantic import validate
from app.db.repositories.record import RecordRepository
from app.schemas import RecordCreateSchema
from main import app

repository = RecordRepository()

@app.route('/records', methods=['GET'])
def get_records():
    records = repository.get_records_all()
    return render_template('records/record_list.html', records=records)


@app.route('/records', methods=['POST'])
@validate(body=RecordCreateSchema)
def create_record(record: RecordCreateSchema):
    created_record = repository.create_record(record)
    return redirect(url_for('record_detail', record_id=created_record))


@app.route('/records/<int:record_id>', methods=['GET'])
def record_detail(record_id):
    record = repository.get_record_by_id(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return render_template('records/record_detail.html', record=record)


@app.route('/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    success = repository.delete_record(record_id)
    if not success:
        return jsonify({"error": "Record not found"}), 404
    return jsonify({"message": "Record deleted"}), 200


@app.route('/records/<int:record_id>', methods=['PUT'])
@validate(body=RecordCreateSchema)
def edit_record(record_id, body: RecordCreateSchema):
    edited_record = repository.update_record(record_id, body)
    if not edited_record:
        return jsonify({"error": "Record not found"}), 404
    return redirect(url_for('record_detail', record_id=edited_record))
