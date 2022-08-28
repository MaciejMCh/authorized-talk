from enum import Enum
from typing import Callable, Optional


class MediumKind(Enum):
    Ssl = 1


class Medium:
    def __init__(self):
        self.on_message: Optional[Callable[[bytes], None]] = None

    async def send(self, message: bytes):
        raise Exception('dont use this base class Medium.send(bytes)')

    def receive_message(self, message: bytes):
        if self.on_message is None:
            return
        self.on_message(message)
