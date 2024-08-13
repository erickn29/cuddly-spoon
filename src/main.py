from fastapi import FastAPI

from core.config import cfg
from utils.telegram.user_bot.bot import TelegramUserBot

app = FastAPI(
    docs_url="/swagger/" if cfg.DEBUG else None,
    redoc_url="/redoc/" if cfg.DEBUG else None,
)


@app.get("/")
async def root(phone: str, entity: str, message: str):
    bot = TelegramUserBot(phone)
    await bot.send_msg(entity, message)
    return {"status": "sent"}
