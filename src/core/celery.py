from celery import Celery
from celery.schedules import schedule
from core.config import cfg


celery_app = Celery(
    "worker",
    broker=f"redis://{cfg.REDIS_HOST}:{cfg.REDIS_PORT}/{cfg.REDIS_DB}",
    backend=f"redis://{cfg.REDIS_HOST}:{cfg.REDIS_PORT}/{cfg.REDIS_DB}",
    include=["tasks.bot_tasks"],
)


celery_app.conf.beat_schedule = {
    "BOT: start commenting": {
        "task": "tasks.bot_tasks.start_commenting",
        "schedule": schedule(60.0),
    }
}


celery_app.conf.timezone = "UTC"
