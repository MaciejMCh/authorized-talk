from asyncio import Task, Future, create_task
from typing import Tuple
import websockets
from python.websocket.location import Location

DEBUG = True


class WebsocketClient:
    def __init__(self, websocket):
        self.websocket = websocket

    async def close(self):
        await self.websocket.close()


async def run(location: Location) -> Tuple[WebsocketClient, Task]:
    debug_print('client: will run')
    future: Future[WebsocketClient] = Future()
    task = create_task(start_task(location=location, future=future))
    client = await future
    debug_print('client: did run')
    return client, task


async def start_task(location: Location, future: Future[WebsocketClient]):
    uri = f'ws://{location.host}:{location.port}'
    websocket = await websockets.connect(uri)
    debug_print('client: opened')
    websocket_client = WebsocketClient(websocket)
    future.set_result(websocket_client)
    await websocket.wait_closed()
    debug_print('client: closed')


def debug_print(msg: str):
    if DEBUG:
        print(msg)
