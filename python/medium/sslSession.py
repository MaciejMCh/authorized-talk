import asyncio
from threading import Thread

from medium.session import Session


class SslSession(Session):
    def __init__(self, websocket):
        super(SslSession, self).__init__()
        self.websocket = websocket

    def send(self, message: bytes):
        if not isinstance(message, bytes):
            raise Exception('message must be bytes')
        print(f'sending: {message}')
        if self.websocket is None:
            raise Exception(f'websocket is not initialized {self}')

        async def do():
            await self.websocket.send(message)

        thread = Thread(target=asyncio.new_event_loop().run_until_complete, args=[do()])
        thread.start()

    def close(self):
        self.websocket.close()
