from collections.abc import Sequence
from typing import Any, Annotated

from fastapi import Depends

from api.v1.user.schema import UserCreateInputSchema
from core.database import db_conn
from repositories.base import SQLAlchemyRepository
from core.config import cfg
from models.user import User
from pydantic import UUID4
from repositories.user import UserRepository
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession


PWD_CONTEXT = cfg.PWD_CONTEXT


class UserService:
    def __init__(self) -> None:
        self.repository = UserRepository()

    async def get(self, user_id: UUID4) -> User:
        return await self.repository.get(user_id)

    async def create(self, schema: UserCreateInputSchema) -> User:
        if schema.password:
            schema.password = self.get_password_hash(schema.password)
        return await self.repository.create(schema)

    async def delete(self, user_id: UUID4) -> UUID4:
        return await self.repository.delete(user_id)

    # async def update(self, user_id: UUID4, data: UserUpdateData) -> User:
    #     if data.password:
    #         data.password = self.get_password_hash(data.password)
    #     return await self.repository.update(user_id, data)

    async def fetch(
        self, filters: dict = None
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        return await self.repository.fetch(filters)

    async def exists(self, user_id: UUID4) -> bool:
        return await self.repository.exists(user_id)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        """Сравнивает пароль в БД и из формы, True если соль и пароль верные"""
        return PWD_CONTEXT.verify(cfg.SECRET + plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        """Хэширует пароль пользователя, нужно для регистрации или смены пароля"""
        return PWD_CONTEXT.hash(cfg.SECRET + password)

    # async def process_handler_data(
    #     self, handler_data: UserHandler, field: str = "email"
    # ):
    #     await self._check_handler_data(handler_data, field=field)
    #     data = {}
    #     if handler_data.create:
    #         data["create"] = [await self.create(obj) for obj in handler_data.create]
    #     if handler_data.update:
    #         data["update"] = [
    #             await self.update(obj.id, obj.data) for obj in handler_data.update
    #         ]
    #     if handler_data.delete:
    #         [await self.delete(obj.id) for obj in handler_data.delete]
    #     return {k: [o.id for o in v] for k, v in data.items()}
