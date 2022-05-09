import asyncio

from medium.session import Session


class SslSession(Session):
    def __init__(self, websocket):
        super(SslSession, self).__init__()
        self.websocket = websocket

    async def send(self, message: str):
        print(f'send {self.websocket} {message}')
        # self.websocket.send(message)
        # asyncio.create_task(self.websocket.send(message))
        await self.websocket.send(message)
