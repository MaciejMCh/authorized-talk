import asyncio
from asyncio import gather
from typing import Optional

from python.websocket.location import Location
from python.websocket.server import run as run_server
from python.websocket.client import run as run_client


async def main():
    location = Location(host='localhost', port=8765)
    server, server_running_task = await run_server(location=location)
    client, client_running_task = await run_client(location=location)

    receivedMessage: Optional[bytes] = None

    def handleMessageAsServer(message: bytes):
        nonlocal receivedMessage
        receivedMessage = message

    server.sessions[0].onMessage = handleMessageAsServer
    client.send(b'hi')
    server.close()
    await gather(server_running_task, client_running_task)
    print('xddd', receivedMessage);

if __name__ == "__main__":
    asyncio.run(main())
