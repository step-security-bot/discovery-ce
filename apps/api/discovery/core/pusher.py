from enum import Enum

from pusher import Pusher


class Channels(str, Enum):
    RUNS = "runs"


class Events(str, Enum):
    RUN_CREATED = "run.created"
    RUN_STATUS_CHANGED = "run.status.changed"


def get_pusher_client() -> Pusher:
    from discovery.core import config

    pusher_config = config.pusher_config
    return Pusher(
        app_id=pusher_config.app_id,
        key=pusher_config.key,
        secret=pusher_config.secret,
        cluster=pusher_config.cluster,
        ssl=True,
    )
