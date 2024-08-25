import asyncio

from core.celery import celery_app
from utils.telegram.user_bot.bot import TelegramUserBot


async def run_async_commenting(phone: str):
    # Ваша асинхронная логика здесь
    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise Exception("Бот не авторизован в телеграм")
    await bot.start_comments()


async def main(phone_list):
    # Запускаем задачи параллельно для всех телефонов в списке
    tasks = [run_async_commenting(phone) for phone in phone_list]
    await asyncio.gather(*tasks)


@celery_app.task
def start_commenting(phone: str = None):
    # Передаем телефон в список для асинхронной функции
    phones = (
        [phone] if phone else ["79523048633"]
    )  # Используем переданный телефон или значение по умолчанию
    try:
        asyncio.run(main(phones))
    except RuntimeError:
        # Если event loop уже существует, создаем задачу в нем
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main(phones))
