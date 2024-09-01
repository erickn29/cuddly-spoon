import asyncio
import logging
import random

from pathlib import Path

from api.v1.bot_user.crud.schema import CommentInputSchema, TaskUpdateSchema
from core.config import cfg
from models.bot import Bot
from pydantic import UUID4
from services.bot import BotService
from services.comment import CommentService
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
        message_ = "ok"
        if comments := await cache.get(f"bot:{self.phone}:comments"):
            comments_list = [comment for comment in comments.split(";")]
            message_ = random.choice(comments_list) or "ok"
        bot_service = BotService()
        bot_objs = await bot_service.fetch({"phone": self.phone})
        if not bot_objs:
            return False
        bot_obj: Bot = bot_objs[0]
        for message in messages_list:
            try:
                reply_to = message.get("last_message_entity")
                if reply_to.is_reply:
                    reply_to = reply_to.reply_to_msg_id
                await self.client.send_message(
                    entity=message.get("comment_group_id"),
                    reply_to=reply_to,
                    message=message_,
                )
                post_url = (
                    f"https://t.me/"
                    f"{message["last_message_entity"].sender.username}/"
                    f"{message["last_message_entity"].fwd_from.channel_post}"
                )
                comment_service = CommentService()
                await comment_service.create(
                    CommentInputSchema(
                        bot_id=bot_obj.bot_id,
                        post_url=post_url,
                        text=message_,
                    )
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
        task_id: UUID4,
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
            task = TaskService()
            await task.update(task_id, TaskUpdateSchema(is_executed=True))
        except Exception as e:
            print(e)
        finally:
            await self.disconnect()
        return status
