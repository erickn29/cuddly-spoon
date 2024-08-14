import asyncio
import datetime
from pathlib import Path

from telethon import TelegramClient, events
from telethon.tl.types import User

from core.config import cfg
import logging

from utils.cache import cache

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
            session=f'{Path(__file__).parent}/session/{phone}',
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
        await self.client.start(self.phone)

    async def send_message_to_chat(self, event):
        msg = event.message
        if event.is_channel and msg.replies and msg.replies.comments:
            await asyncio.sleep(11)
            comments_chat_id = msg.replies.channel_id
            messages = await self.client.get_messages(comments_chat_id)
            if not messages:
                return
            last_channel_message = messages[-1]
            await self.client.send_message(
                entity=comments_chat_id,
                reply_to=last_channel_message,
                message='ok'
            )

    async def sign_in_with_code(self, code: str) -> bool:
        await self.client.connect()
        phone_code_hash = await cache.get(self.phone)
        status = await self.client.sign_in(
            phone=self.phone,
            code=code,
            phone_code_hash=phone_code_hash,
        )
        await self.client.disconnect()
        return isinstance(status, User)

    async def send_msg(self, entity: str, message: str) -> bool:
        await self.client.connect()
        if not await self.client.is_user_authorized():
            phone_code_hash = await self.client.send_code_request(self.phone)
            cache.set(self.phone, phone_code_hash.phone_code_hash)
            await self.client.disconnect()
            return False
        await self.sign_in()
        await self.client.send_message(entity, message)
        await self.client.disconnect()
        return True
