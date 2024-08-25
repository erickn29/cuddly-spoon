from models.base import Base, uuid_pk
from sqlalchemy import UUID, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Comment(Base):
    __tablename__ = "comment"

    comment_id: Mapped[uuid_pk]
    bot_id: Mapped[UUID] = mapped_column(
        ForeignKey("bot.bot_id", ondelete="CASCADE", name="bot_id"), doc="Бот"
    )
    post_url: Mapped[str] = mapped_column(String(512), doc="Ссылка на пост")
    text: Mapped[str] = mapped_column(Text, doc="Текст комментария")

    bot = relationship("Bot", back_populates="comments", lazy="joined")
