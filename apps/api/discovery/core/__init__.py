from .config import Config
from .logger import handler, logger

config = Config()
__all__ = ["handler", "logger", "config"]
