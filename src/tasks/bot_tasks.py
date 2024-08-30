import asyncio
from typing import Any

from core.celery import celery_app
from pydantic import UUID4

from core.exceptions import exception
from services.bot import BotService
from utils.cache import cache
from utils.telegram.user_bot.bot import TelegramUserBot


async def run_async_commenting(phone: str):
    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise Exception("Бот не авторизован в телеграм")
    await bot.start_comments()


async def commenting():
    phones = await cache.get("bot:active:phones")
    if not phones:
        bot_service = BotService()
        bots = await bot_service.fetch({"is_stopped": False, "is_active": True})
        phones = ",".join([bot.phone for bot in bots])
        await cache.set(
            "bot:active:phones",
            phones,
            60 * 60 * 24 * 30,
        )
    tasks = [run_async_commenting(phone) for phone in phones.split(",")]
    await asyncio.gather(*tasks)


@celery_app.task
def start_commenting():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(commenting())
    else:
        loop.run_until_complete(commenting())


async def run_async_joining_channels(
    phone: str, channel_urls: list[str], task_id: UUID4
):
    from utils.telegram.user_bot.bot import TelegramUserBot

    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise Exception("Бот не авторизован в телеграм")
    await bot.join_channel(channel_urls, task_id)


async def join_channels(phone: str, channel_urls: list[str], task_id: UUID4):
    bot_service = BotService()
    await bot_service.bot_deactivate(phone)
    await asyncio.gather(run_async_joining_channels(phone, channel_urls, task_id))
    await bot_service.bot_activate(phone)


@celery_app.task
def joining_channel(phone: str, channel_urls: list[str], task_id: UUID4):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(join_channels(phone, channel_urls, task_id))
    else:
        loop.run_until_complete(join_channels(phone, channel_urls, task_id))


async def run_async_leaving_channels(
    phone: str, channel_urls: list[str], task_id: UUID4
):
    from utils.telegram.user_bot.bot import TelegramUserBot

    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise Exception("Бот не авторизован в телеграм")
    await bot.leave_channel(channel_urls, task_id)


async def leave_channels(phone: str, channel_urls: list[str], task_id: UUID4):
    bot_service = BotService()
    await bot_service.bot_deactivate(phone)
    await asyncio.gather(run_async_leaving_channels(phone, channel_urls, task_id))
    await bot_service.bot_activate(phone)


@celery_app.task
def leaving_channel(phone: str, channel_urls: list[str], task_id: UUID4):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(leave_channels(phone, channel_urls, task_id))
    else:
        loop.run_until_complete(leave_channels(phone, channel_urls, task_id))


async def run_async_update_bio(phone: str, data: dict[str, Any], task_id: UUID4):
    from utils.telegram.user_bot.bot import TelegramUserBot
    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise Exception("Бот не авторизован в телеграм")
    await bot.update_bio(task_id=task_id, **data)


async def update_bio(phone: str, data: dict[str, Any], task_id: UUID4):
    bot_service = BotService()
    await bot_service.bot_deactivate(phone)
    await asyncio.gather(run_async_update_bio(phone, data, task_id))
    await bot_service.bot_activate(phone)


@celery_app.task
def leaving_channel(phone: str, data: dict[str, Any], task_id: UUID4):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(update_bio(phone, data, task_id))
    else:
        loop.run_until_complete(update_bio(phone, data, task_id))
