import psycopg2
from config import get_postgres_url

def get_db_connection():
    connection_url = get_postgres_url()
    return psycopg2.connect(connection_url)