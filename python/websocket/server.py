import websockets
from asyncio import Future, Task, create_task
from typing import Tuple, List, Optional, Callable
from python.websocket.location import Location

DEBUG = True


class WebsocketServerSession:
    def __init__(self, websocket):
        self.websocket = websocket
        self.on_message: Optional[Callable[[bytes], None]] = None

    def handle_message(self, handler: Callable[[bytes], None]):
        self.on_message = handler

    def receive_message(self, message: bytes):
        if self.on_message is None:
            return
        self.on_message(message)

    async def send(self, message: bytes):
        await self.websocket.send(message)

    async def close(self):
        await self.websocket.close()


class WebsocketServer:
    def __init__(self):
        self.server = None
        self.sessions: List[WebsocketServerSession] = []

    def initialize(self, server):
        self.server = server

    def connectSession(self, websocket) -> WebsocketServerSession:
        session = WebsocketServerSession(websocket)
        self.sessions.append(session)
        return session

    def close(self):
        self.server.close()


async def run_server(location: Location) -> Tuple[WebsocketServer, Task]:
    debug_print('server: will run')
    future: Future[WebsocketServer] = Future()
    task = create_task(start_task(location=location, future=future))
    server = await future
    debug_print('server: did run')
    return server, task


async def start_task(location: Location, future: Future[WebsocketServer]):
    websocketServer = WebsocketServer()

    async def client_did_connect(websocket, path):
        debug_print('server: session connected')
        session = websocketServer.connectSession(websocket)
        async for message in websocket:
            debug_print(f'server: received {message}')
            session.receive_message(message)
        await websocket.wait_closed()
        debug_print('server: session closed')

    server = await websockets.serve(client_did_connect, location.host, location.port)
    debug_print('server: opened')
    websocketServer.initialize(server)
    future.set_result(websocketServer)
    await server.wait_closed()
    debug_print('server: closed')


def debug_print(msg: str):
    if DEBUG:
        print(msg)
