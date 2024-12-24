from os import environ as env
from typing import ClassVar
from dotenv import load_dotenv
from pydantic import BaseModel, Field, PostgresDsn, ValidationError

load_dotenv(override=True)

class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    login: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")

    @property
    def dsn(self) -> PostgresDsn:
        return f"postgresql://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}"


class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    # Атрибут класса, игнорируемый Pydantic
    JWT_TOKEN_LOCATION: ClassVar[list] = ['cookies']
    JWT_SECRET_KEY: ClassVar[str] = env.get("JWT_SECRET_KEY", "default-secret-key")


# Создание глобального объекта конфигурации
app_config = Config()
