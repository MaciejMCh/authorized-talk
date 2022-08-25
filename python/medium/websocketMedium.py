import asyncio
import time
from asyncio import Future
from threading import Thread
from typing import Optional, List, Callable
import websockets
from python.medium.medium import Medium


class WebsocketMedium(Medium):
    def __init__(self, otherHost: str, otherPort: int):
        self.client = WebsocketClient(host=otherHost, port=otherPort)

    def send(self, message: bytes):
        self.client.send(message)


class WebsocketClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.websocket = None
        self.connectToServer()

    def connectToServer(self):
        def runClientThread():
            async def runAsync():
                uri = f'ws://{self.host}:{self.port}'
                print('client: will connect')
                async with websockets.connect(uri) as websocket:
                    print('client: connected', websocket)
                    self.websocket = websocket
                    await websocket.wait_closed()
            asyncio.run(runAsync())
        Thread(target=runClientThread).start()

    def send(self, message: bytes):
        async def runAsync():
            print(f'client: send message {message}')
            await self.websocket.send(message)
        asyncio.run(runAsync())


class WebsocketSession:
    def __init__(self, websocket):
        self.websocket = websocket
        self.onMessage: Optional[Callable[[bytes], None]] = None

    def receiveMessage(self, message: bytes):
        print(f'server: got message {message}')
        if self.onMessage is None:
            return
        self.onMessage(message)

    def close(self):
        async def xd():
            await self.websocket.close()
        asyncio.run(xd())


class WebsocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = None
        self.sessions: List[WebsocketSession] = []
        self.stop: Optional[Future] = None
        self.startServer()

    def startServer(self):
        print('server: start')

        def runServerThread():
            async def runAsync():
                async def sessionStarted(websocket, path):
                    print(f'server: connected')
                    session = WebsocketSession(websocket)
                    self.sessions.append(session)
                    async for message in websocket:
                        session.receiveMessage(message)
                        print('debug', websocket.state)

                self.stop = asyncio.Future()
                print('stop assigned')
                self.server = await websockets.serve(sessionStarted, self.host, self.port)
                print('server: initialized')
                await self.stop
                print('server: stopped')
            asyncio.run(runAsync())

        Thread(target=runServerThread).start()

    def close(self):
        print('server: close')
        self.stop.get_loop().call_soon_threadsafe(self.stop.set_result, None)
        self.server.close()
        print('servdeb', self.server.is_serving())

        # for session in self.sessions:
        #     session.close()
