import asyncio
from asyncio import gather
from typing import Optional

from python.medium.medium import Medium
from python.medium.websocket_medium import WebsocketConnector
from python.websocket.location import Location
from python.websocket.server import run_server
from python.websocket.client import run_client


async def main():
    location = Location(host='localhost', port=8765)
    server, server_running_task = await run_server(location=location)
    medium: Medium = await WebsocketConnector.establish_connection(Location(host='localhost', port=8765))
    receivedMessage: Optional[bytes] = None

    def receiveMessageAsMedium(message: bytes):
        nonlocal receivedMessage
        receivedMessage = message

    medium.onMessage = receiveMessageAsMedium
    await server.sessions[0].send(b'hi')
    server.close()
    await server_running_task
    print(receivedMessage, b'hi')

if __name__ == "__main__":
    asyncio.run(main())
