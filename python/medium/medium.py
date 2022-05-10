from enum import Enum
from typing import Callable


class MediumKind(Enum):
    Ssl = 1


class Medium:
    def onWhisper(self, handler: Callable[[str], None]):
        pass
