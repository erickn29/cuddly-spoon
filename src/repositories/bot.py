from typing import Annotated

from repositories.base import SQLAlchemyRepository

from core.database import db_conn
from fastapi import Depends
from models.bot import Bot
from sqlalchemy.ext.asyncio import AsyncSession


class BotRepository(SQLAlchemyRepository):
    model = Bot

    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_conn.get_session),
        ],
        model=Bot,
    ) -> None:
        super().__init__(session=session, model=model)
