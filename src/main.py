import asyncio
import datetime

from telethon import TelegramClient, events
from config import cfg
import logging


logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)


# @client.on(events.NewMessage)
# async def send_message_to_chat(event):
#     msg = event.message
#     if event.is_channel and msg.replies and msg.replies.comments:
#         await asyncio.sleep(11)
#         comments_chat_id = msg.replies.channel_id
#         messages = await client.get_messages(comments_chat_id)
#         if not messages:
#             return
#         last_channel_message = messages[-1]
#         await client.send_message(
#             entity=comments_chat_id,
#             reply_to=last_channel_message,
#             message='ok'
#         )

async def check_me(tg_client: TelegramClient):
    me = await tg_client.get_me()
    if me:
        return True
    return False


def code_callback():
    return input('code: ')


async def sign_in(tg_client: TelegramClient, phone: str):
    if await check_me(tg_client):
        return
    await tg_client.start(phone, code_callback=code_callback)


async def send_message(tg_client: TelegramClient, message: str):
    await tg_client.send_message("ya_novikov", message)


async def async_generator(num: int):
    for i in range(num):
        yield i


async def main(tg_client: TelegramClient, phone: str):
    await tg_client.connect()
    await sign_in(tg_client, phone)
    async for _ in async_generator(3):
        await send_message(tg_client, "hello yarik")
        await asyncio.sleep(1)
    await tg_client.disconnect()


if __name__ == '__main__':
    api_id = cfg.TELEGRAM_API_ID
    api_hash = cfg.TELEGRAM_API_HASH
    client = TelegramClient('session/79523048633', api_id, api_hash)
    asyncio.run(main(client, "79523048633"))
