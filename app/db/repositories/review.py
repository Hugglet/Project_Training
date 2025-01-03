from app.db.connection import get_db_connection
from app.db.models import ReviewModel
from app.schemas import ReviewCreateSchema, ReviewUpdateSchema
from psycopg2.extras import RealDictCursor


class ReviewRepository:
    def __init__(self) -> None:
        self._connection = get_db_connection()

    def create_review(self, review: ReviewCreateSchema) -> int:
        query = """
        INSERT INTO reviews (content, mark, user_id, event_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    review.content,
                    review.mark,
                    review.user_id,
                    review.event_id,
                ),
            )
            review_id = cursor.fetchone()["id"]
            self._connection.commit()
            return review_id
        
    def get_reviews_all(self) -> list[ReviewModel]:
        query = """
        SELECT id, content, mark, user_id, event_id, created_at
        FROM reviews;
        """
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [ReviewModel(**row) for row in results]

    def get_review_by_id(self, id: int) -> ReviewModel | None:
        query = """
        SELECT id, content, mark, user_id, event_id, created_at
        FROM reviews
        WHERE id = %s;
        """
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if not result:
                return None
            return ReviewModel(**result)

    def update_review(self, id: int, review: ReviewUpdateSchema) -> int | None:
        query = """
        UPDATE reviews
        SET content = %s, mark = %s
        WHERE id = %s
        RETURNING id;
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    review.content,
                    review.mark,
                    id,
                ),
            )
            updated_id = cursor.fetchone()
            if updated_id:
                self._connection.commit()
                return updated_id["id"]
            else:
                return None

    def delete_review(self, id: int) -> int | None:
        query = """
        DELETE FROM reviews
        WHERE id = %s
        RETURNING id;
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query, (id,))
            deleted_id = cursor.fetchone()
            if deleted_id:
                self._connection.commit()
                return deleted_id["id"]
            else:
                return None