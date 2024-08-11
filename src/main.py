import asyncio
import datetime

from telethon import TelegramClient, events
from config import cfg
import logging


logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)


api_id = cfg.TELEGRAM_API_ID
api_hash = cfg.TELEGRAM_API_HASH
client = TelegramClient('anon', api_id, api_hash)


@client.on(events.NewMessage)
async def send_message_to_chat(event):
    msg = event.message
    if event.is_channel and msg.replies and msg.replies.comments:
        await asyncio.sleep(11)
        comments_chat_id = msg.replies.channel_id
        messages = await client.get_messages(comments_chat_id)
        if not messages:
            return
        last_channel_message = messages[-1]
        await client.send_message(
            entity=comments_chat_id,
            reply_to=last_channel_message,
            message='ok'
        )


async def main():
    pass


if __name__ == '__main__':
    print(f"Starting [{datetime.datetime.now(datetime.timezone.utc)}]")
    client.start()
    print(f"Started [{datetime.datetime.now(datetime.timezone.utc)}]")
    client.run_until_disconnected()
    print(f"Done [{datetime.datetime.now(datetime.timezone.utc)}]")
