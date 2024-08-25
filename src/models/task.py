from models.base import Base, uuid_pk
from sqlalchemy import JSON, UUID, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Task(Base):
    __tablename__ = "task"

    task_id: Mapped[uuid_pk]
    bot_id: Mapped[UUID] = mapped_column(
        ForeignKey("bot.bot_id", ondelete="CASCADE", name="bot_id"), doc="Бот"
    )
    is_executed: Mapped[bool] = mapped_column(Boolean, default=False, doc="Выполнено")
    data: Mapped[dict] = mapped_column(JSON, default={}, doc="Задачи")

    bot = relationship("Bot", back_populates="tasks", lazy="joined")
