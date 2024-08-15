from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.config import cfg
from core.exceptions import exception, BaseHTTPException
from utils.telegram.user_bot.bot import TelegramUserBot

app = FastAPI(
    docs_url="/swagger/" if cfg.DEBUG else None,
    redoc_url="/redoc/" if cfg.DEBUG else None,
)


@app.exception_handler(BaseHTTPException)
async def http_exception_handler(
    request: Request,
    exc: BaseHTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.get_response(),
    )


@app.get("/bot/auth/check/")
async def check_auth(phone: str):
    bot = TelegramUserBot(phone)
    user_is_authorized = await bot.check_is_authorized()
    return {"user_is_authorized": user_is_authorized}


@app.get("/bot/auth/request-code/")
async def request_code(phone: str):
    bot = TelegramUserBot(phone)
    code_is_sent_to_user = await bot.request_verification_code()
    return {"code_is_sent_to_user": code_is_sent_to_user}


@app.get("/bot/auth/send-code/")
async def auth(phone: str, code: str):
    bot = TelegramUserBot(phone)
    auth_is_success = await bot.sign_in_with_code(code)
    return {"auth_is_success": auth_is_success}


@app.get("/bot/start/")
async def start(phone: str):
    bot = TelegramUserBot(phone)
    if not await bot.check_is_authorized():
        raise exception(400, "Бот не авторизован в телеграм")
    return await bot.start_comments()
