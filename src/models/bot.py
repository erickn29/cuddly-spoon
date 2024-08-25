from models.base import Base, uuid_pk
from models.comment import Comment
from models.task import Task
from sqlalchemy import JSON, UUID, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


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
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="bot",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="bot",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
