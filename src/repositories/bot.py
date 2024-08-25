from models.bot import Bot
from repositories.base import SQLAlchemyRepository


class BotRepository(SQLAlchemyRepository):
    model = Bot
    id_column = f"{model.__tablename__.lower()}_id"
