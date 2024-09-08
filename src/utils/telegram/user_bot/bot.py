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
from telethon.tl.custom import Dialog
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import Chat, Message, User
from utils.cache import cache
from utils.requests import fetch_url_post


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
        # await self.client.get_me()
        if not await self.client.is_user_authorized():
            await self.disconnect()
            return False
        await self.disconnect()
        return True

    async def sign_in_with_code(self, code: str) -> bool:
        """Авторизует бота в тг

        Args:
            code (str): код от тг

        Returns:
            bool: результат действия
        """
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

    async def request_verification_code(self) -> bool:
        """Запрашивает код подтверждение для авторизации

        Returns:
            bool: результат действия
        """
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

    async def _get_last_chat_messages(self, dialog: Dialog) -> list[Message]:
        """Возвращает последний пост в канале списком

        Args:
            dialog (Dialog): диалог (канал или чат)

        Returns:
            list[Message]: список из постов (по умолчанию последний)
        """
        try:
            messages = await self.client.get_messages(dialog.message.replies.channel_id)
            return messages
        except Exception as e:
            print(e)
            print(dialog.name)
            return []

    async def _get_channel_dialogs_unread(self) -> list[Dialog]:
        """Возвращает каналы с непрочитанными сообщениями

        Returns:
            list[Dialog]: список чатов и каналов
        """
        dialogs = await self.client.get_dialogs()
        return [
            dialog
            for dialog in dialogs
            if all(
                [
                    dialog.is_channel,
                    dialog.message,
                    dialog.message.replies,
                    dialog.unread_count > 0,
                ]
            )
        ]

    async def _get_new_messages_chat_id(self) -> list[dict[str, any]]:
        """Возвращает список словарей с данными, необходимыми для комментария

        Returns:
            list[dict[str, any]]: _description_
        """
        dialogs = await self._get_channel_dialogs_unread()
        dialogs_list = []
        for dialog in dialogs:
            messages = await self._get_last_chat_messages(dialog)
            if not messages:
                continue
            last_channel_message: Message = messages[-1]
            await self.client.send_read_acknowledge(dialog.entity.id)
            dialogs_list.append(
                {
                    "chat_id": dialog.entity.id,
                    "comment_group_id": dialog.message.replies.channel_id,
                    "last_message_entity": last_channel_message,
                    "text": dialog.message.text,
                }
            )
        return dialogs_list

    @staticmethod
    def _get_post_url(message: dict) -> str:
        """Возвращает ссылку на пост в канале"""
        post_id = "unknown"
        channel_name: Chat = message["chat_id"]
        message_obj: Message = message["last_message_entity"]
        if message_obj and message_obj.fwd_from:
            post_id = message_obj.fwd_from.channel_post
        # post_id = message["last_message_entity"].fwd_from.channel_post if \
        #     message["last_message_entity"].fwd_from else ""  # TODO разобраться!
        if message_obj.fwd_from.from_name:
            channel_name = message_obj.fwd_from.from_name
        post_url = f"https://t.me/" f"{channel_name}/" f"{post_id}"
        return post_url

    async def _log_bot_comment(self, message: dict, comment_text: str) -> None:
        """Записывает комментарий в БД"""
        bot_service = BotService()
        bot_objs = await bot_service.fetch({"phone": self.phone})
        if not bot_objs:
            return
        bot_obj: Bot = bot_objs[0]
        comment_service = CommentService()
        post_url = self._get_post_url(message)
        await comment_service.create(
            CommentInputSchema(
                bot_id=bot_obj.bot_id,
                post_url=post_url,
                text=comment_text,
            )
        )

    async def _get_message_text(self, message: dict) -> str:
        """Возвращает текст комментария"""
        if prompt := await cache.get(f"bot:{self.phone}:prompt"):
            return await self._get_ai_message(prompt.split(";")[0], message)
        if comments := await cache.get(f"bot:{self.phone}:comments"):
            comments_list = [comment for comment in comments.split(";")]
            return random.choice(comments_list) or "ok"
        return "ok"

    @staticmethod
    async def _get_ai_message(prompt: str, message: dict) -> str:
        """Получает комментарий от AI"""
        content = (
            f"напиши осмысленный нейтральный комментарий к этой новости, "
            f"максимум 10 слов. Новость: {message.get('text')}"
        )
        response = await fetch_url_post(
            "http://localhost:1234/v1/chat/completions",
            {
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content},
                ],
                "temperature": 0.7,
                "max_tokens": -1,
                "stream": False,
            },
        )
        if (
            response
            and response.get("choices")
            and response["choices"][0].get("message")
            and response["choices"][0]["message"].get("content")
        ):
            message_ = (
                response["choices"][0]["message"]["content"]
                .replace('"', "")
                .replace("'", "")
                .replace("«", "")
                .replace("»", "")
                .strip()
            )
            return message_

    async def start_comments(self) -> bool:
        """Комментирует новые посты"""
        await self.connect()
        messages_list = await self._get_new_messages_chat_id()
        for message in messages_list:
            message_ = await self._get_message_text()
            if not message_:
                continue
            reply_to = message.get("last_message_entity")
            if not reply_to:
                continue
            if reply_to.is_reply:
                reply_to = reply_to.reply_to_msg_id
            try:
                await self.client.send_message(
                    entity=message.get("comment_group_id"),
                    reply_to=reply_to,
                    message=message_,
                )
            except Exception as e:
                print(e)
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
