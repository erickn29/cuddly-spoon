from typing import Annotated

from core.database import db_conn
from fastapi import Depends
from models.comment import Comment
from repositories.base import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession


class CommentRepository(SQLAlchemyRepository):
    model = Comment
    id_column = f"{model.__tablename__.lower()}_id"
