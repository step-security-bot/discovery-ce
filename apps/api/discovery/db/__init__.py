import os
from logging import DEBUG, getLogger

from tortoise import Tortoise

from discovery.core import config, handler


async def init() -> None:
    await Tortoise.init(
        db_url=config.database_url, modules={"models": ["discovery.db.models"]}
    )
    if os.getenv("ENV_TYPE", "DEV") == "DEV":
        tortoise_logger = getLogger("tortoise.db_client")
        tortoise_logger.setLevel(DEBUG)
        tortoise_logger.addHandler(handler)


__all__ = ["init"]
