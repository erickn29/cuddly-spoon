from sqlalchemy import UUID, ForeignKey, String, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, uuid_pk


class Bot(Base):
    __tablename__ = "bot"

    bot_id: Mapped[uuid_pk]
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE", name="user_id"),
        doc="Пользователь",
    )
    phone: Mapped[str] = mapped_column(String(16), doc="Номер телефона", unique=True)
    alias: Mapped[str] = mapped_column(String(16), nullable=True, doc="Псевдоним")
    config: Mapped[dict] = mapped_column(JSON, default={}, doc="Конфиг")
    session: Mapped[dict] = mapped_column(JSON, default={}, doc="Сессия")
    is_stopped: Mapped[bool] = mapped_column(Boolean, default=False, doc="Остановлен")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, doc="Активен")

    user = relationship("User", back_populates="bots", lazy="joined")
    tasks = relationship(
        "Task",
        back_populates="bot",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    comments = relationship(
        "Comment",
        back_populates="bot",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
