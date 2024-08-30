from enum import Enum
from typing import Literal

from api.v1.bot_user.crud.schema import BotCreateInputSchema, BotUpdateDataSchema
from models.bot import Bot
from pydantic import UUID4
from repositories.bot import BotRepository
from services.base import BaseService
from utils.cache import cache


class ActionChannels(Enum):
    JOIN = "join"
    LEAVE = "leave"


class BotService(BaseService):
    repository: BotRepository = BotRepository()

    async def create(self, schema: BotCreateInputSchema) -> Bot | None:
        if bot := await self.repository.create(schema):
            if bot.is_active and not bot.is_stopped:
                await self.bot_activate(bot.phone)
            return bot
        return

    async def update(self, obj_id: UUID4, data: BotUpdateDataSchema) -> Bot | None:
        if bot := await self.repository.update(obj_id, data):
            if bot.is_stopped:
                await self.bot_deactivate(bot.phone)
            return bot
        return

    async def delete(self, obj_id: UUID4) -> UUID4 | None:
        bot = await self.repository.get(obj_id)
        if bot:
            await self.bot_deactivate(bot.phone)
            return await self.repository.delete(obj_id)
        return

    @staticmethod
    async def bot_deactivate(phone: str):
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

    @staticmethod
    async def bot_activate(phone: str):
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
        else:
            await cache.set("bot:active:phones", phone, 60 * 60 * 24 * 30)

    async def update_channels(
        self,
        action: Literal[ActionChannels.JOIN.value, ActionChannels.LEAVE.value],
        bot_object: Bot,
        channels: list[str],
    ) -> None:
        bot_config: dict[str, list] = bot_object.config
        for channel in channels:
            if action == "leave":
                if channel in bot_config["channels"]:
                    bot_config["channels"].remove(channel)
            else:
                if channel not in bot_config["channels"]:
                    bot_config["channels"].append(channel)
        update_schema = BotUpdateDataSchema(config=bot_config)
        await self.update(bot_object.bot_id, update_schema)
