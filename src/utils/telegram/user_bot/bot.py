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

    async def connect(self) -> None:
        if not self.client.is_connected():
            await self.client.connect()

    async def disconnect(self) -> None:
        if self.client.is_connected():
            await self.client.disconnect()

    # async def send_message_to_chat(self, event):
    #     msg = event.message
    #     if event.is_channel and msg.replies and msg.replies.comments:
    #         await asyncio.sleep(11)
    #         comments_chat_id = msg.replies.channel_id
    #         messages = await self.client.get_messages(comments_chat_id)
    #         if not messages:
    #             return
    #         last_channel_message = messages[-1]
    #         await self.client.send_message(
    #             entity=comments_chat_id,
    #             reply_to=last_channel_message,
    #             message='ok'
    #         )

    async def sign_in_with_code(self, code: str) -> bool:
        await self.connect()
        phone_code_hash = await cache.get(self.phone)
        is_user = False
        try:
            status = await self.client.sign_in(
                phone=self.phone,
                code=code,
                phone_code_hash=phone_code_hash,
            )
            is_user = isinstance(status, User)
        except Exception as e:  # TODO добавить нормальные исключения
            print(e)
        finally:
            await self.disconnect()
            return is_user

    async def request_verification_code(self):
        await self.connect()
        response = await self.client.send_code_request(self.phone)
        await cache.set(self.phone, response.phone_code_hash)
        await self.disconnect()

    async def send_message(self, entity: str, message: str) -> bool:
        await self.connect()
        if not await self.client.is_user_authorized():
            await self.request_verification_code()
            return False
        await self.client.start(self.phone)
        await self.client.send_message(entity, message)
        await self.disconnect()
        return True
