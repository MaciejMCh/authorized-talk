import asyncio
from typing import List
from medium.medium import Medium
from websockets import connect, serve
from medium.session import Session
from medium.sslSession import SslSession


class SslMedium(Medium):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.incomingSessions: List[Session] = []

    @classmethod
    def local(cls, port: int):
        return SslMedium('localhost', port)

    async def didConnect(self, websocket, path):
        session = SslSession(websocket)
        self.incomingSessions.append(session)
        while True:
            result = await websocket.recv()
            session.handleMessage(result)

    async def openIncomingConnections(self):
        async with serve(self.didConnect, self.host, self.port):
            await asyncio.Future()

    def url(self):
        return f'ws://{self.host}:{self.port}'

    async def connectTo(self, url: str) -> Session:
        session = SslSession(None)

        async def do():
            async with connect(url) as websocket:
                session.websocket = websocket
                while True:
                    result = await websocket.recv()
                    session.handleMessage(result)

        asyncio.create_task(do())
        return session
