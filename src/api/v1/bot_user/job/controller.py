from fastapi import APIRouter

from core.exceptions import exception
from utils.telegram.user_bot.bot import TelegramUserBot

router = APIRouter()


@router.get("/start/")
async def start(phone: str):
    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise exception(400, "Бот не авторизован в телеграм")
    return await bot.start_comments()
