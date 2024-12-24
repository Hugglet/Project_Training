from app.db.connection import get_db_connection
from app.db.models import EventModel
from app.schemas import EventCreateSchema, EventUpdateSchema
from psycopg2.extras import RealDictCursor


class EventRepository:
    def __init__(self) -> None:
        self._connection = get_db_connection()

    def create_event(self, event: EventCreateSchema) -> int:
        query = """
        INSERT INTO events (title, description, place_id, started_at)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query, (event.title, event.description, event.place_id, event.started_at))
            event_id = cursor.fetchone()["id"]
            self._connection.commit()
            return event_id

    def get_events_all(self) -> list[EventModel]:
        query = "SELECT * FROM events;"
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [EventModel(**row) for row in results]

    def get_event_by_id(self, id: int) -> EventModel | None:
        query = """
        SELECT *
        FROM events
        WHERE id = %s;
        """
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if not result:
                return None
            return EventModel(**result)

    def update_event(self, id: int, event: EventUpdateSchema) -> int | None:
        query = """
        UPDATE events
        SET title = %s, description = %s, place_id = %s, started_at = %s
        WHERE id = %s
        RETURNING id;
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query, (event.title, event.description, event.place_id, event.started_at, id))
            updated_id = cursor.fetchone()
            if updated_id:
                self._connection.commit()
                return updated_id["id"]
            else:
                return None

    def delete_event(self, id: int) -> int | None:
        query = """
        DELETE FROM events
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