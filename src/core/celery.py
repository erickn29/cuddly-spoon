from celery import Celery
from celery.schedules import crontab

from core.config import cfg

celery_app = Celery(
    "worker",
    broker=f"redis://{cfg.REDIS_HOST}:{cfg.REDIS_PORT}/{cfg.REDIS_DB}",
    backend=f"redis://{cfg.REDIS_HOST}:{cfg.REDIS_PORT}/{cfg.REDIS_DB}",
    include=["tasks.bot_tasks"],
)


celery_app.conf.beat_schedule = {
    "run-every-minute": {
        "task": "tasks.bot_tasks.periodic_task",
        "schedule": crontab(minute="*"),
    }
}


celery_app.conf.timezone = "UTC"
