from typing import Annotated

from fastapi import APIRouter, Body

from api.v1.bot_user.job.schema import TestSchema
from core.exceptions import exception
from tasks.bot_tasks import test_task
from utils.telegram.user_bot.bot import TelegramUserBot

router = APIRouter()


@router.get("/start/")
async def start(phone: str):
    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise exception(400, "Бот не авторизован в телеграм")
    return await bot.start_comments()


@router.post("/test/")
async def test(
    schema: Annotated[TestSchema, Body(...)],
):
    bot = TelegramUserBot(schema.phone)
    test_task.delay(bot.phone)
    return True
