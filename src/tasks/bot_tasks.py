import asyncio

from pydantic import UUID4

from core.celery import celery_app
from utils.telegram.user_bot.bot import TelegramUserBot


async def run_async_commenting(phone: str):
    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise Exception("Бот не авторизован в телеграм")
    await bot.start_comments()


async def commenting(phone_list: list[str]):
    tasks = [run_async_commenting(phone) for phone in phone_list]
    await asyncio.gather(*tasks)


@celery_app.task
def start_commenting(phone: str = None):
    phones = [phone] if phone else ["79523048633"]
    try:
        asyncio.run(commenting(phones))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(commenting(phones))


async def run_async_joining_channels(phone: str, channel_urls: list[str], task_id: UUID4):
    from utils.telegram.user_bot.bot import TelegramUserBot

    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise Exception("Бот не авторизован в телеграм")
    await bot.join_channel(channel_urls, task_id)


async def join_channels(phone: str, channel_urls: list[str], task_id: UUID4):
    await asyncio.gather(run_async_joining_channels(phone, channel_urls, task_id))


@celery_app.task
def joining_channel(phone: str, channel_urls: list[str], task_id: UUID4):
    try:
        asyncio.run(join_channels(phone, channel_urls, task_id))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(join_channels(phone, channel_urls, task_id))


async def run_async_leaving_channels(phone: str, channel_urls: list[str], task_id: UUID4):
    from utils.telegram.user_bot.bot import TelegramUserBot

    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise Exception("Бот не авторизован в телеграм")
    await bot.leave_channel(channel_urls, task_id)


async def leave_channels(phone: str, channel_urls: list[str], task_id: UUID4):
    await asyncio.gather(run_async_leaving_channels(phone, channel_urls, task_id))


@celery_app.task
def leaving_channel(phone: str, channel_urls: list[str], task_id: UUID4):
    try:
        asyncio.run(leave_channels(phone, channel_urls, task_id))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(leave_channels(phone, channel_urls, task_id))
