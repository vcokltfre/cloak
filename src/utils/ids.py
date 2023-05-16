from datetime import datetime
from time import time
from typing import Final

_epoch: Final[int] = int(datetime(2023, 1, 1).timestamp() * 1000)
_increment = 0


def create_id() -> int:
    global _increment

    timestamp = int(time() * 1000) - _epoch
    increment = _increment

    _increment = (_increment + 1) % 256

    return (timestamp << 8) | increment
