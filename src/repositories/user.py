from typing import Annotated

from repositories.base import SQLAlchemyRepository

from core.database import db_conn
from fastapi import Depends
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(SQLAlchemyRepository):
    model = User

    def __init__(
        self,
        model=User,
    ) -> None:
        super().__init__(model=model)
