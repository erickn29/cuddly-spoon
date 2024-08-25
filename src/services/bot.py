from repositories.bot import BotRepository
from services.base import BaseService


class BotService(BaseService):
    repository: BotRepository = BotRepository()
