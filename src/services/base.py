from collections.abc import Sequence
from typing import Any

from models.base import Base
from models.bot import Bot
from models.comment import Comment
from models.task import Task
from models.user import User
from pydantic import UUID4, BaseModel
from sqlalchemy import Row, RowMapping


class BaseService:
    repository = None

    async def get(self, obj_id: UUID4) -> User | Bot | Task | Comment:
        return await self.repository.get(obj_id)

    async def create(self, schema: BaseModel) -> Base:
        return await self.repository.create(schema)

    async def delete(self, obj_id: UUID4) -> UUID4:
        return await self.repository.delete(obj_id)

    async def update(self, obj_id: UUID4, data: BaseModel) -> Base:
        return await self.repository.update(obj_id, data)

    async def fetch(
        self, filters: dict = None
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        return await self.repository.fetch(filters)

    async def exists(self, obj_id: UUID4) -> bool:
        return await self.repository.exists(obj_id)
