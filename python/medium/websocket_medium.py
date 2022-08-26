from python.medium.medium import Medium
from python.websocket.client import WebsocketClient, run_client
from python.websocket.location import Location


class WebsocketMedium(Medium):
    def __init__(self, websocket_client: WebsocketClient):
        super().__init__()
        self.websocket_client = websocket_client
        self.websocket_client.onMessage = self.handleMessage

    async def send(self, message: bytes):
        await self.websocket_client.send(message)

    def handleMessage(self, message: bytes):
        if self.onMessage is None:
            return
        self.onMessage(message)


class WebsocketConnector:
    @classmethod
    async def establish_connection(cls, location: Location) -> WebsocketMedium:
        websocket_client, _ = await run_client(location)
        return WebsocketMedium(websocket_client)
