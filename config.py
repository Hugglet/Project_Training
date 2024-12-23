import os
from dotenv import load_dotenv

load_dotenv(override=True)

class PostgresConfig:
    LOGIN = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    HOST = os.getenv("POSTGRES_HOST")
    PORT = os.getenv("POSTGRES_PORT")
    DATABASE = os.getenv("POSTGRES_NAME")

def get_postgres_url():
    return f'postgresql://postgres:Shurikgat2704@localhost:5432/postgres'
