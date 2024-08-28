from repositories.bot import BotRepository
from services.base import BaseService
from utils.cache import cache


class BotService(BaseService):
    repository: BotRepository = BotRepository()

    @staticmethod
    async def bot_deactivate(phone: str):
        print("start bot deactivate")
        phones = await cache.get("bot:active:phones")
        if phones:
            phones = phones.split(",")
            if phone in phones:
                phones.remove(phone)
                await cache.set(
                    "bot:active:phones",
                    ",".join(phones),
                    60 * 60 * 24 * 30,
                )
                print("bot deactivated")

    @staticmethod
    async def bot_activate(phone: str):
        print("start bot activate")
        phones = await cache.get("bot:active:phones")
        if phones:
            phones = phones.split(",")
            if phone not in phones:
                phones.append(phone)
                await cache.set(
                    "bot:active:phones",
                    ",".join(phones),
                    60 * 60 * 24 * 30,
                )
                print("bot activated")
