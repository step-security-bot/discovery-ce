import asyncio

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown
from tortoise import Tortoise

from discovery.core import config
from discovery.db import init as init_database

celery = Celery(
    "discovery",
    broker=config.celery_config.broker_url,
    backend=config.celery_config.result_backend,
    include=["discovery.runs.registry"],
    broker_connection_retry_on_startup=True,
)


@worker_process_init.connect
def worker_init(**kwargs) -> None:
    asyncio.run(init_database())


@worker_process_shutdown.connect
def worker_shutdown(**kwargs) -> None:
    asyncio.run(Tortoise.close_connections())


__all__ = [
    "celery",
]
