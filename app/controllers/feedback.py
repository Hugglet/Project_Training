from flask import jsonify, redirect, render_template, url_for
from flask_pydantic import validate
from app.db.repositories.review import FeedbackRepository
from app.schemas import FeedbackCreateSchema, FeedbackUpdateSchema
from main import app

repository = FeedbackRepository()

@app.route('/feedback', methods=['GET'])
def get_feedback():
    feedbacks = repository.get_feedbacks_all()
    return render_template('feedback/feedback_list.html', feedbacks=feedbacks)


@app.route('/feedback', methods=['POST'])
@validate(body=FeedbackCreateSchema)
def create_feedback(feedback: FeedbackCreateSchema):
    created_feedback = repository.create_feedback(feedback)
    return redirect(url_for('feedback_detail', feedback_id=created_feedback))


@app.route('/feedback/<int:feedback_id>', methods=['GET'])
def feedback_detail(feedback_id):
    feedback = repository.get_feedback_by_id(feedback_id)
    if not feedback:
        return jsonify({"error": "Feedback not found"}), 404
    return render_template('feedback/feedback_detail.html', feedback=feedback)


@app.route('/feedback/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    success = repository.delete_feedback(feedback_id)
    if not success:
        return jsonify({"error": "Feedback not found"}), 404
    return jsonify({"message": "Feedback deleted"}), 200


@app.route('/feedback/<int:feedback_id>', methods=['PUT'])
@validate(body=FeedbackUpdateSchema)
def edit_feedback(feedback_id, body: FeedbackUpdateSchema):
    edited_feedback = repository.update_feedback(feedback_id, body)
    if not edited_feedback:
        return jsonify({"error": "Feedback not found"}), 404
    return redirect(url_for('feedback_detail', feedback_id=edited_feedback))
