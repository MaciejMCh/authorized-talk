import asyncio
from threading import Thread, Lock
from typing import List, Callable, Optional
from python.medium.medium import Medium
from websockets import connect, serve
from python.medium.session import Session
from python.medium.sslSession import SslSession


class SslMedium(Medium):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.incomingSessions: List[Session] = []
        self.routeSessionHandler: Optional[Callable[[SslSession], None]] = None
        Thread(target=self.openIncomingConnections).start()

    @classmethod
    def local(cls, port: int):
        return SslMedium('localhost', port)

    async def didConnect(self, websocket, path):
        session = SslSession(websocket)
        self.incomingSessions.append(session)
        if self.routeSessionHandler is not None:
            self.routeSessionHandler(session)
        while True:
            result = await websocket.recv()
            session.handleMessage(result)

    def openIncomingConnections(self):
        async def do():
            async with serve(self.didConnect, self.host, self.port):
                await asyncio.Future()
        Thread(target=asyncio.new_event_loop().run_until_complete, args=[do()]).start()

    def url(self):
        return f'ws://{self.host}:{self.port}'

    def routeIncoming(self, routeSessionHandler: Callable[[SslSession], None]):
        self.routeSessionHandler = routeSessionHandler

    def connectTo(self, url: str) -> Session:
        session = SslSession(None)
        lock = Lock()

        async def do():
            async with connect(url) as websocket:
                session.websocket = websocket
                lock.release()
                while True:
                    result = await websocket.recv()
                    session.handleMessage(result)

        Thread(target=asyncio.new_event_loop().run_until_complete, args=[do()]).start()
        lock.acquire()
        lock.acquire()
        return session
