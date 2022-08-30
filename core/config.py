import secrets
from datetime import timedelta
from typing import Optional, Dict, Any, List

from environs import Env
from pydantic.class_validators import validator
from pydantic.networks import PostgresDsn, AnyHttpUrl

# Environment
env = Env()
env.read_env(path=env("ENV_FILE_PATH", default=".env"))


class FastAPISettings:
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = env("SECRET_KEY", default=secrets.token_urlsafe(32))
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = timedelta(days=1)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = timedelta(days=7)

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str

    # Database Settings
    POSTGRES_USER: str = env("POSTGRES_USER", default="user")
    POSTGRES_PASSWORD: str = env("POSTGRES_PASSWORD", default="password")
    POSTGRES_HOST: str = env("POSTGRES_HOST", default="postgres")
    POSTGRES_DB: str = env("POSTGRES_DB", default="db")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # RabbitMQ Settings
    RABBITMQ_USER: str = env("RABBITMQ_USER", default="user")
    RABBITMQ_PASSWORD: str = env("RABBITMQ_PASSWORD", default="password")
    RABBITMQ_PORT: str = env.int("RABBITMQ_PORT", default=5672)

    # Celery Settings
    CELERY_BROKER_URL = (
        f"pyamqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@rabbitmq:{RABBITMQ_PORT}//"
    )
    # CELERY_RESULT_BACKEND = f"db+mysql://root:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


settings = FastAPISettings()
