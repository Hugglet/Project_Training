from psycopg2.extras import RealDictCursor
from app.db.connection import get_db_connection, transaction_scope
from app.db.models import UserModel
from app.schemas import UserCreateSchema, UserUpdateSchema


class UserRepository:
    def __init__(self) -> None:
        self._connection = get_db_connection()

    def create_user(self, user: UserCreateSchema) -> int:
        query = """
        INSERT INTO users (login, password, email, name, date_birth, role, city)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        with transaction_scope(self._connection):
            with self._connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        user.login,
                        user.password,
                        user.email,
                        user.name,
                        user.date_birth,
                        user.role.value,
                        user.city,
                    ),
                )
                user_id = cursor.fetchone()["id"]
                self._connection.commit()
                return user_id

    def get_users_all(self) -> list[UserModel]:
        query = "SELECT id, login, password, email, name, date_birth, role, city FROM users;"
        with transaction_scope(self._connection):
            with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return [UserModel(**row) for row in results]

    def get_user_by_id(self, id: int) -> UserModel | None:
        query = """
        SELECT id, login, password, email, name, date_birth, role, city
        FROM users
        WHERE id = %s;
        """
        with transaction_scope(self._connection):
            with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (id,))
                result = cursor.fetchone()
                if not result:
                    return None
                return UserModel(**result)
        
    def get_user_by_username(self, username: str) -> UserModel | None:
        query = "SELECT * FROM users WHERE login = %s;"
        with transaction_scope(self._connection):
            with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                if not result:
                    return None
                return UserModel(**result)
            
    def get_user_by_email(self, email: str) -> UserModel | None:
        query = "SELECT * FROM users WHERE email = %s;"
        with transaction_scope(self._connection):
            with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                if not result:
                    return None
                return UserModel(**result)

    def update_user(self, id: int, user: UserUpdateSchema) -> int | None:
        query = """
        UPDATE users
        SET login = %s, password = %s, email = %s, name = %s, date_birth = %s, role = %s, city = %s
        WHERE id = %s
        RETURNING id;
        """
        with transaction_scope(self._connection):
            with self._connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        user.login,
                        user.password,
                        user.email,
                        user.name,
                        user.date_birth,
                        user.role.value,
                        user.city,
                        id,
                    ),
                )
                updated_id = cursor.fetchone()
                if updated_id:
                    self._connection.commit()
                    return updated_id[0]
                else:
                    return None

    def delete_user(self, id: int) -> int | None:
        query = """
        DELETE FROM users
        WHERE id = %s
        RETURNING id;
        """
        with transaction_scope(self._connection):
            with self._connection.cursor() as cursor:
                cursor.execute(query, (id,))
                deleted_id = cursor.fetchone()
                if deleted_id:
                    self._connection.commit()
                    return deleted_id[0]
                else:
                    return None
