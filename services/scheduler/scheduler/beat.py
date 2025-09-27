import os
from celery.schedules import crontab
from artify_common import settings
from artify_common.logging import env_configure_from_vars
from worker.celery_app import celery

env_configure_from_vars()

celery.conf.beat_schedule = {
    "heartbeat-every-minute": {
        "task": "worker.tasks.heartbeat",
        "schedule": 60.0,
    },
    "add-hourly": {
        "task": "worker.tasks.add",
        "schedule": crontab(minute=0),
        "args": (1, 2),
    },
}


def main() -> None:
    from celery.bin.beat import beat
    beat(app=celery).run(loglevel=os.getenv("LOG_LEVEL", "INFO"))
