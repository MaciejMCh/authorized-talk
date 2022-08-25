import asyncio

from python.websocket.location import Location
from python.websocket.server import run as run_server
from python.websocket.client import run as run_client


async def main():
    location = Location(host='localhost', port=8765)
    server, server_running_task = await run_server(location=location)
    client, client_running_task = await run_client(location=location)
    await asyncio.sleep(2)
    print('closing server')
    server.close()
    await server_running_task

if __name__ == "__main__":
    asyncio.run(main())
