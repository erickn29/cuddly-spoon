import asyncio
import datetime
from pathlib import Path

from telethon import TelegramClient, events
from core.config import cfg
import logging


logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)


class TelegramUserBot:
    api_id = cfg.TELEGRAM_API_ID
    api_hash = cfg.TELEGRAM_API_HASH

    def __init__(self, phone: str) -> None:
        self.phone = phone
        self.client = TelegramClient(
            session=f'{Path(__file__).parent}/session/79523048633',
            api_id=self.api_id,
            api_hash=self.api_hash,
        )

    async def check_me(self):
        me = await self.client.get_me()
        if me:
            return True
        return False

    @staticmethod
    def code_callback():
        # TODO прокинуть в апи
        return input('code: ')

    async def sign_in(self):
        if await self.check_me():
            return
        await self.client.start(self.phone, code_callback=self.code_callback)

    async def send_message(self, entity: str,  message: str):
        await self.client.send_message(entity, message)

    async def send_msg(self, entity: str, message: str):
        await self.client.connect()
        await self.sign_in()
        await self.send_message(entity, message)
        await self.client.disconnect()
