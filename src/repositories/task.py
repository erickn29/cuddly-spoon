from typing import Annotated

from repositories.base import SQLAlchemyRepository

from core.database import db_conn
from fastapi import Depends
from models.task import Task
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepository(SQLAlchemyRepository):
    model = Task

    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_conn.get_session),
        ],
        model=Task,
    ) -> None:
        super().__init__(session=session, model=model)
