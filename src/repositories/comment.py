from typing import Annotated

from repositories.base import SQLAlchemyRepository

from core.database import db_conn
from fastapi import Depends
from models.comment import Comment
from sqlalchemy.ext.asyncio import AsyncSession


class CommentRepository(SQLAlchemyRepository):
    model = Comment

    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_conn.get_session),
        ],
        model=Comment,
    ) -> None:
        super().__init__(session=session, model=model)
