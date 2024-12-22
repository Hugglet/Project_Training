import os

class PostgresConfig:
    LOGIN = os.getenv("POSTGRES_USER", "user")
    PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    HOST = os.getenv("POSTGRES_HOST", "localhost")
    PORT = os.getenv("POSTGRES_PORT", "5432")
    DATABASE = os.getenv("POSTGRES_NAME", "mydb")

def get_postgres_url():
    return f"postgresql://{PostgresConfig.LOGIN}:{PostgresConfig.PASSWORD}@{PostgresConfig.HOST}:{PostgresConfig.PORT}/{PostgresConfig.DATABASE}"
