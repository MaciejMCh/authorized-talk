from enum import Enum
from python.websocket.location import Location


class MediumKind(Enum):
    WEBSOCKET = 1


class SourceMedium:
    def __init__(self, kind: MediumKind):
        self.kind = kind


class TargetMedium:
    def __init__(self, kind: MediumKind):
        self.kind = kind


class WebsocketSourceMedium(SourceMedium):
    def __init__(self):
        super().__init__(MediumKind.WEBSOCKET)


class WebsocketTargetMedium(TargetMedium):
    def __init__(self, location: Location):
        super().__init__(MediumKind.WEBSOCKET)
        self.location = location
