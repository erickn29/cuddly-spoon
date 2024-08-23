import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(f"{Path(__file__).parent.parent.parent}/secrets/.env")


class Config:
    TELEGRAM_API_ID = os.environ.get("TELEGRAM_API_ID")
    TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH")

    DEBUG = os.environ.get("DEBUG", False)

    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
    REDIS_DB = os.environ.get("REDIS_DB", 0)

    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "test")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_echo: bool = False
    POSTGRES_echo_pool: bool = False
    POSTGRES_pool_size: int = 30
    POSTGRES_max_overflow: int = 10
    POSTGRES_naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    def db_url(self, db_name: str = None) -> str:
        db_name = db_name or self.POSTGRES_DB
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{db_name}"
        )


cfg = Config()
