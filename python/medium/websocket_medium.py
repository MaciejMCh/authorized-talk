from typing import Callable, Coroutine
from python.medium.medium import Medium
from python.websocket.client import WebsocketClient, run_client
from python.websocket.location import Location
from python.websocket.server import WebsocketServerSession


class WebsocketMedium(Medium):
    def __init__(
            self,
            send_implementation: Callable[[bytes], Coroutine],
            handle_message: Callable[[Callable[[bytes], None]], None],
    ):
        super().__init__()
        self.send_implementation = send_implementation
        handle_message(self.handle_websocket_message)

    @classmethod
    def client(cls, websocket_client: WebsocketClient):
        return WebsocketMedium(
            send_implementation=websocket_client.send,
            handle_message=websocket_client.handle_message,
        )

    @classmethod
    def server(cls, websocket_server_session: WebsocketServerSession):
        return WebsocketMedium(
            send_implementation=websocket_server_session.send,
            handle_message=websocket_server_session.handle_message,
        )

    async def send(self, message: bytes):
        await self.send_implementation(message)

    def handle_websocket_message(self, message: bytes):
        if self.on_message is None:
            return
        self.on_message(message)


class WebsocketConnector:
    @classmethod
    async def establish_connection(cls, location: Location) -> WebsocketMedium:
        websocket_client, _ = await run_client(location)
        return WebsocketMedium.client(websocket_client)
