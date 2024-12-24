from app.db.connection import get_db_connection
from app.schemas import RecordCreateSchema, RecordUpdateSchema
from app.db.models import RecordModel
from psycopg2.extras import RealDictCursor


class RecordRepository:
    def __init__(self) -> None:
        self._connection = get_db_connection()

    def create_record(self, record: RecordCreateSchema) -> int:
        query = """
        INSERT INTO records (user_id, event_id)
        VALUES (%s, %s)
        RETURNING id;
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query, (record.user_id, record.event_id))
            record_id = cursor.fetchone()["id"]
            self._connection.commit()
            return record_id

    def get_records_all(self) -> list[RecordModel]:
        query = """
        SELECT id, user_id, event_id, created_at
        FROM records;
        """
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [RecordModel(**row) for row in results]

    def get_record_by_id(self, id: int) -> RecordModel | None:
        query = """
        SELECT id, user_id, event_id, created_at
        FROM records
        WHERE id = %s;
        """
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if not result:
                return None
            return RecordModel(**result)

    def update_record(self, id: int, record: RecordUpdateSchema) -> int | None:
        query = """
        UPDATE records
        SET user_id = %s, event_id = %s
        WHERE id = %s
        RETURNING id;
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query, (record.user_id, record.event_id, id))
            updated_id = cursor.fetchone()
            if updated_id:
                self._connection.commit()
                return updated_id["id"]
            else:
                return None

    def delete_record(self, id: int) -> int | None:
        query = """
        DELETE FROM records
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
