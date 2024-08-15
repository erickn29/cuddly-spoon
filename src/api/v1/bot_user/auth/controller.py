from fastapi import APIRouter

from utils.telegram.user_bot.bot import TelegramUserBot

router = APIRouter()


@router.get("/bot/auth/check/")
async def check_auth(phone: str):
    bot = TelegramUserBot(phone)
    user_is_authorized = await bot.check_is_authorized()
    return {"status": user_is_authorized}


@router.get("/bot/auth/request-code/")
async def request_code(phone: str):
    bot = TelegramUserBot(phone)
    code_is_sent_to_user = await bot.request_verification_code()
    return {"status": code_is_sent_to_user}


@router.get("/bot/auth/send-code/")
async def auth(phone: str, code: str):
    bot = TelegramUserBot(phone)
    auth_is_success = await bot.sign_in_with_code(code)
    return {"status": auth_is_success}
