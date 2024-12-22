from flask import jsonify, redirect, render_template, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate
from app.db.models import UserRole
from app.db.repositories.review import ReviewRepository
from app.db.repositories.user import UserRepository
from app.exception_handlers import CustomException
from app.schemas import ReviewCreateSchema, ReviewUpdateSchema
from main import app

repository = ReviewRepository()

@app.route('/review', methods=['GET'])
def get_review():
    reviews = repository.get_reviews_all()
    return render_template('review/review_list.html', reviews=reviews)


@app.route('/review', methods=['POST'])
@jwt_required()
@validate(body=ReviewCreateSchema)
def create_review(review: ReviewCreateSchema):
    created_review = repository.create_review(review)
    return redirect(url_for('review_detail', review_id=created_review))


@app.route('/review/<int:review_id>', methods=['GET'])
def review_detail(review_id):
    review = repository.get_review_by_id(review_id)
    if not review:
        raise CustomException(message="Не найден отзыв", status_code=404)
    return render_template('review/review_detail.html', review=review)


@app.route('/review/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    success = repository.delete_review(review_id)
    if not success:
        raise CustomException(message="Не найден отзыв", status_code=404)
    return jsonify({"message": "Review deleted"}), 200


@app.route('/review/<int:review_id>', methods=['PUT'])
@jwt_required()
@validate(body=ReviewUpdateSchema)
def edit_review(review_id, body: ReviewUpdateSchema):
    edited_review = repository.update_review(review_id, body)
    if not edited_review:
        raise CustomException(message="Не найден отзыв", status_code=404)
    return redirect(url_for('review_detail', review_id=edited_review))