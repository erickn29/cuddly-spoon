from typing import Annotated

from core.database import db_conn
from fastapi import Depends
from models.bot import Bot
from repositories.base import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession


class BotRepository(SQLAlchemyRepository):
    model = Bot
    id_column = f"{model.__tablename__.lower()}_id"
