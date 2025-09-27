import os
from celery import Celery
from kombu import Exchange, Queue
from artify_common import settings
from artify_common.logging import env_configure_from_vars

env_configure_from_vars()

celery = Celery(
    "artify",
    broker=settings.broker_url,
    backend=settings.result_backend,
)

celery.conf.update(
    task_default_queue=settings.queue_default,
    task_queues=[
        Queue(settings.queue_high, Exchange("celery"), routing_key=settings.queue_high),
        Queue(settings.queue_default, Exchange("celery"), routing_key=settings.queue_default),
        Queue(settings.queue_low, Exchange("celery"), routing_key=settings.queue_low),
    ],
    task_routes={
        "worker.tasks.add": {"queue": settings.queue_default},
        "worker.tasks.heavy": {"queue": settings.queue_high},
        "worker.tasks.heartbeat": {"queue": settings.queue_low},
    },
)

celery.autodiscover_tasks(["worker"])


def main_worker() -> None:
    from celery.bin.worker import worker as worker_cmd
    w = worker_cmd.worker(app=celery)
    concurrency = int(os.getenv("WORKER_CONCURRENCY", str(settings.worker_concurrency)))
    w.run(loglevel=os.getenv("LOG_LEVEL", "INFO"), concurrency=concurrency, queues="high,default,low")


def main_flower() -> None:
    from celery.bin.flower import flower as flower_cmd
    flower_cmd(app=celery).run(
        port=os.getenv("FLOWER_PORT", str(settings.flower_port)),
        url_prefix="/",
    )
