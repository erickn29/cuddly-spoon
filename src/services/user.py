from collections.abc import Sequence
from typing import Any

from api.v1.user.schema import (
    UserCreateInputSchema,
    UserUpdateDataSchema,
)
from core.config import cfg
from models.user import User
from pydantic import UUID4
from repositories.user import UserRepository
from sqlalchemy import Row, RowMapping

from services.base import BaseService

PWD_CONTEXT = cfg.PWD_CONTEXT


class UserService(BaseService):
    repository: UserRepository = UserRepository()

    async def create(self, schema: UserCreateInputSchema) -> User:
        if schema.password:
            schema.password = self.get_password_hash(schema.password)
        return await self.repository.create(schema)

    async def update(self, user_id: UUID4, data: UserUpdateDataSchema) -> User:
        if data.password:
            data.password = self.get_password_hash(data.password)
        return await self.repository.update(user_id, data)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        """Сравнивает пароль в БД и из формы, True если соль и пароль верные"""
        return PWD_CONTEXT.verify(cfg.SECRET + plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        """Хэширует пароль пользователя, нужно для регистрации или смены пароля"""
        return PWD_CONTEXT.hash(cfg.SECRET + password)
