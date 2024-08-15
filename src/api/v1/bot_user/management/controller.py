from typing import Annotated

from fastapi import APIRouter, Body

from api.v1.bot_user.management.schema import UpdateBotBioInputSchema
from core.exceptions import exception
from utils.telegram.user_bot.bot import TelegramUserBot


router = APIRouter()


@router.post("/update/bio/")
async def update_bot_bio(schema: Annotated[UpdateBotBioInputSchema, Body(...)]):
    bot = TelegramUserBot(schema.phone)
    if not await bot.check_is_authorized():
        raise exception(400, "Бот не авторизован в телеграм")
    result = await bot.update_bio(schema.first_name, schema.last_name, schema.about)
    return {"result": result}
