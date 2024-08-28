import asyncio
import logging

from pathlib import Path

from api.v1.bot_user.crud.schema import TaskUpdateSchema
from core.config import cfg
from pydantic import UUID4
from services.task import TaskService
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import User
from utils.cache import cache


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


class TelegramUserBot:
    api_id = cfg.TELEGRAM_API_ID
    api_hash = cfg.TELEGRAM_API_HASH

    def __init__(self, phone: str) -> None:
        self.phone = phone
        self.client = TelegramClient(
            session=f"{Path(__file__).parent}/session/{phone}",
            api_id=self.api_id,
            api_hash=self.api_hash,
        )

    async def connect(self) -> None:
        if not self.client.is_connected():
            await self.client.connect()

    async def disconnect(self) -> None:
        if self.client.is_connected():
            await self.client.disconnect()

    async def check_is_authorized(self) -> bool:
        await self.connect()
        if not await self.client.is_user_authorized():
            await self.disconnect()
            return False
        await self.disconnect()
        return True

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
        is_response = False
        try:
            response = await self.client.send_code_request(self.phone)
            if response and response.phone_code_hash:
                await cache.set(self.phone, response.phone_code_hash)
                is_response = True
        except Exception as e:
            print(e)
        finally:
            await self.disconnect()
        return is_response

    async def _get_new_messages_chat_id(self):
        dialogs = await self.client.get_dialogs()
        dialogs_list = []
        for dialog in dialogs:
            if (
                dialog.is_channel
                and dialog.message
                and dialog.message.replies
                and dialog.unread_count > 0
                and dialog.message.replies.comments
            ):
                messages = await self.client.get_messages(
                    dialog.message.replies.channel_id
                )
                if not messages:
                    continue
                last_channel_message = messages[-1]
                await self.client.send_read_acknowledge(dialog.entity.id)
                dialogs_list.append(
                    {
                        "chat_id": dialog.entity.id,
                        "comment_group_id": dialog.message.replies.channel_id,
                        "last_message_entity": last_channel_message,
                    }
                )
        return dialogs_list

    async def start_comments(self) -> bool:
        await self.connect()
        messages_list = await self._get_new_messages_chat_id()
        for message in messages_list:
            try:
                last_message_entity = message.get("last_message_entity")
                if last_message_entity.is_reply:
                    await self.client.send_message(
                        entity=message.get("comment_group_id"),
                        reply_to=last_message_entity.reply_to_msg_id,
                        message="ну такое..",
                    )
                    continue
                await self.client.send_message(
                    entity=message.get("comment_group_id"),
                    reply_to=message.get("last_message_entity"),
                    message="ну такое..",
                )
            except Exception as e:
                print(e)
                continue
        await self.disconnect()
        return True

    async def join_channel(self, channel_urls: list[str], task_id: UUID4):
        await self.connect()
        for channel_url in channel_urls:
            try:
                await self.client(JoinChannelRequest(channel=channel_url))
            except Exception as e:
                print(e)
                continue
        task = TaskService()
        await task.update(task_id, TaskUpdateSchema(is_executed=True))
        await self.disconnect()

    async def leave_channel(self, channel_urls: list[str], task_id: UUID4):
        await self.connect()
        for channel_url in channel_urls:
            try:
                await self.client.delete_dialog(
                    await self.client.get_entity(channel_url)
                )
                await asyncio.sleep(1)
            except Exception as e:
                print(e)
                continue
        task = TaskService()
        await task.update(task_id, TaskUpdateSchema(is_executed=True))
        await self.disconnect()

    async def send_message(self, entity: str, message: str) -> bool:
        await self.connect()
        await self.client.start(self.phone)
        await self.client.send_message(entity, message)
        await self.disconnect()
        return True

    async def update_bio(
        self,
        first_name: str = "",
        last_name: str = "",
        about: str = "",
    ) -> bool:
        await self.connect()
        status = False
        try:
            await self.client(
                UpdateProfileRequest(
                    first_name=first_name,
                    last_name=last_name,
                    about=about,
                )
            )
            status = True
        except Exception as e:
            print(e)
        finally:
            await self.disconnect()
        return status
