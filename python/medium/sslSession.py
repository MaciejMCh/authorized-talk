from medium.session import Session


class SslSession(Session):
    def __init__(self, websocket):
        super(SslSession, self).__init__()
        self.websocket = websocket

    async def send(self, message: str):
        await self.websocket.send(message)
