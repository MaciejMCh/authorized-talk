import websockets
from asyncio import Future, Task, create_task
from typing import Tuple
from python.websocket.location import Location

DEBUG = True


class WebsocketServer:
    def __init__(self, server):
        self.server = server

    def close(self):
        self.server.close()


async def run(location: Location) -> Tuple[WebsocketServer, Task]:
    debug_print('server: will run')
    future: Future[WebsocketServer] = Future()
    task = create_task(start_task(location=location, future=future))
    server = await future
    debug_print('server: did run')
    return server, task


async def client_did_connect(websocket, path):
    name = await websocket.recv()
    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")


async def start_task(location: Location, future: Future[WebsocketServer]):
    server = await websockets.serve(client_did_connect, location.host, location.port)
    debug_print('server: opened')
    websocketServer = WebsocketServer(server)
    future.set_result(websocketServer)
    await server.wait_closed()
    debug_print('server: closed')


def debug_print(msg: str):
    if DEBUG:
        print(msg)
