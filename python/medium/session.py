from typing import Callable, Optional


class Session:
    def __init__(self):
        self.handler: Optional[Callable[[bytes], None]] = None

    def send(self, message: bytes) -> None:
        raise Exception('dont use this base class')

    def handleMessage(self, message: bytes):
        print(f'receiving: {message}')
        if self.handler is not None:
            self.handler(message)

    def onMessage(self, handler: Callable[[bytes], None]):
        self.handler = handler

    def close(self):
        raise Exception('dont use this base class')