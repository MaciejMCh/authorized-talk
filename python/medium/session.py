from typing import Callable, Optional


class Session:
    def __init__(self):
        self.handler: Optional[Callable[[str], None]] = None

    def send(self, message: str) -> None:
        raise Exception('dont use this base class')

    def handleMessage(self, message: str):
        print(f'receiving: {message}')
        if self.handler is not None:
            self.handler(message)

    def onMessage(self, handler: Callable[[str], None]):
        self.handler = handler

    def close(self):
        raise Exception('dont use this base class')