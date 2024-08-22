import uuid

from datetime import datetime
from typing import Annotated

from core.config import cfg
from sqlalchemy import UUID, MetaData
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    ),
]
created_at = Annotated[
    datetime,
    mapped_column(default=datetime.utcnow, doc="Дата создания"),
]
updated_at = Annotated[
    datetime,
    mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="Дата изменения",
    ),
]


class Base(DeclarativeBase):
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    metadata = MetaData(naming_convention=cfg.db.naming_convention)
