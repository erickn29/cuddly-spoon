from collections.abc import Sequence
from typing import Any

from core.exceptions import exception
from pydantic import UUID4, BaseModel
from sqlalchemy import Row, RowMapping, and_, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession, model) -> None:
        self.session = session
        self.model = model

    async def get(self, obj_id: UUID4):
        query = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        obj = result.scalars().first()
        if not obj:
            raise exception(404, extra=str(obj_id))
        return obj

    async def create(self, obj: BaseModel):
        stmt = insert(self.model).values(**obj.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            await self.session.close()
            raise exception(
                400,
                "Ошибка создания объекта",
                (
                    e.args[0].split("DETAIL:  ")[-1]
                    if "DETAIL:  " in e.args[0]
                    else e.args[0]
                ),
            ) from e
        return result.scalar_one_or_none()

    async def delete(self, obj_id: UUID4) -> UUID4:
        obj = await self.get(obj_id)
        await self.session.delete(obj)
        await self.session.commit()
        return obj_id

    async def fetch(
        self,
        filters: dict = None,
        order_by: list = None,
        paginate: dict = None,
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        """
        filters = {
            "price": {"gt": 100, "lt": 200},
            "category": "electronics",
            "brand": {"in": ["Samsung", "Apple"]},
            "title": {"ilike": "phone"}
        }
        """
        operator_map = {
            "gt": lambda column, value: column > value,
            "gte": lambda column, value: column >= value,
            "lt": lambda column, value: column < value,
            "lte": lambda column, value: column <= value,
            "in": lambda column, value: column.in_(value),
            "like": lambda column, value: column.like(f"%{value}%"),
            "ilike": lambda column, value: column.ilike(f"%{value}%"),
        }
        order_by = order_by or [self.model.created_at.desc()]
        query = select(self.model)
        if not filters:
            result = await self.session.execute(query)
            return result.scalars().all()

        filter_conditions = []
        for key, value in filters.items():
            if not value:
                continue
            if isinstance(value, dict):
                column = getattr(self.model, key)
                for operator, operand in value.items():
                    condition = operator_map.get(operator)
                    if condition:
                        filter_conditions.append(condition(column, operand))
            else:
                filter_conditions.append(getattr(self.model, key) == value)
        query = select(self.model).filter(and_(*filter_conditions)).order_by(*order_by)
        if paginate:
            limit = 5 if paginate.get("limit") <= 0 else paginate.get("limit")
            page = (
                1 if paginate.get("current_page") <= 0 else paginate.get("current_page")
            )
            query = query.limit(limit).offset((page - 1) * limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def in_(self, column: str, values: list):
        query = select(self.model).where(getattr(self.model, column).in_(values))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, obj_id: UUID4, data: BaseModel):
        upd_data = data.dict(exclude_unset=True) if not isinstance(data, dict) else data
        obj = await self.session.get(self.model, obj_id)
        if not obj:
            raise exception(400, extra=str(obj_id))
        for field, value in upd_data.items():
            if value is None:
                continue
            setattr(obj, field, value)
        await self.session.commit()
        return obj

    async def exists(self, obj_id: UUID4) -> bool:
        query = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        obj = result.scalars().first()
        return obj is not None
