from psycopg2.extras import RealDictCursor
from app.db.connection import get_db_connection
from app.db.models import PlaceModel
from app.schemas import PlaceCreateSchema, PlaceUpdateSchema


class PlaceRepository:
    def __init__(self) -> None:
        self._connection = get_db_connection()

    def create_place(self, place: PlaceCreateSchema) -> int:
        query = """
        INSERT INTO places (name, owner, city)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query, (place.name, place.owner, place.city))
            place_id = cursor.fetchone()["id"]
            self._connection.commit()
            return place_id

    def get_places_all(self) -> list[PlaceModel]:
        query = "SELECT id, name, owner, city FROM places;"
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [PlaceModel(**row) for row in results]

    def get_place_by_id(self, id: int) -> PlaceModel | None:
        query = """
        SELECT id, name, owner, city
        FROM places
        WHERE id = %s;
        """
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if not result:
                return None
            return PlaceModel(**result)

    def delete_place(self, id: int) -> int | None:
        query = """
        DELETE FROM places
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
            
    def update_place(self, id: int, place: PlaceUpdateSchema) -> int | None:
        query = """
        UPDATE places
        SET name = %s, owner = %s, city = %s
        WHERE id = %s
        RETURNING id;
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query, (place.name, place.owner, place.city, id))
            updated_id = cursor.fetchone()
            if updated_id:
                self._connection.commit()
                return updated_id["id"]
            else:
                return None