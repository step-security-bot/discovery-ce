import logging
import os
import sys


def init_handler() -> logging.StreamHandler:
    if os.getenv("ENV_TYPE", "DEV") != "DEV":
        return logging.StreamHandler()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    return handler


def init_logging(handler: logging.StreamHandler) -> logging.Logger:
    logger = logging.getLogger("discovery")
    logger.setLevel(logging.DEBUG)
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


handler = init_handler()
logger = init_logging(handler)
