import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(f"{Path(__file__).parent.parent.parent}/secrets/.env")


class Config:
    TELEGRAM_API_ID = os.environ.get('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH')
    DEBUG = os.environ.get('DEBUG', False)
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    REDIS_DB = os.environ.get('REDIS_DB', 0)


cfg = Config()
