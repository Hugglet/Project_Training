from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from config import get_postgres_url


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def get_connection(self):
        if self._connection is None:
            connection_url = get_postgres_url()
            self._connection = psycopg2.connect(connection_url, cursor_factory=RealDictCursor)
        return self._connection

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None


# Функция для получения подключения
def get_db_connection():
    db = DatabaseConnection()
    return db.get_connection()


# Функция для закрытия подключения
def close_db_connection():
    db = DatabaseConnection()
    db.close_connection()


@contextmanager
def transaction_scope(connection):
    try:
        # Отключаем автокоммит для начала транзакции
        connection.autocommit = False
        yield connection
        # Если не возникло ошибок, коммитим изменения
        connection.commit()
    except Exception as e:
        # В случае ошибки откатываем транзакцию
        connection.rollback()
        raise e
    finally:
        # Включаем автокоммит обратно
        connection.autocommit = True
