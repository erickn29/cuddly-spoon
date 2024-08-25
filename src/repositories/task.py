from typing import Annotated

from core.database import db_conn
from fastapi import Depends
from models.task import Task
from repositories.base import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepository(SQLAlchemyRepository):
    model = Task
    id_column = f"{model.__tablename__.lower()}_id"
