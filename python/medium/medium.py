from enum import Enum
from typing import Callable


class MediumKind(Enum):
    Ssl = 1


class Medium:
    def send(self, message: bytes):
        raise Exception('dont use this base class Medium.send(bytes)')
