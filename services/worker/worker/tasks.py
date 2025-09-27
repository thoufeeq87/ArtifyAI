from __future__ import annotations

import time

from celery import shared_task


@shared_task(name="worker.tasks.add")
def add(x: int, y: int) -> int:
    return x + y


@shared_task(name="worker.tasks.heavy")
def heavy(seconds: int = 5) -> str:
    time.sleep(seconds)
    return f"slept {seconds}s"


@shared_task(name="worker.tasks.heartbeat")
def heartbeat() -> str:
    return "tick"
