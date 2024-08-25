from models.base import Base, uuid_pk
from models.bot import Bot
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[uuid_pk]
    email: Mapped[str] = mapped_column(String(32), doc="Электронная почта", unique=True)
    password: Mapped[str] = mapped_column(String(512), doc="Пароль")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, doc="Активен")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, doc="Админ")

    bots: Mapped[list["Bot"]] = relationship(
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
