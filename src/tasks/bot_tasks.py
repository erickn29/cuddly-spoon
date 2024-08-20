from time import sleep

from core.celery import celery_app
import datetime

from utils.telegram.user_bot.bot import TelegramUserBot


@celery_app.task
def periodic_task():
    print(f"Задача выполнена в {datetime.datetime.now()}")
    return "Задача выполнена"


@celery_app.task
def test_task(phone: str):
    sleep(1)
    print("phone:", phone)
    return
