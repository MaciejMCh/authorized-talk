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
        print('xddddd will connect as server')
        session = Session()
        self.incomingSessions.append(session)
        while True:
            result = await websocket.recv()
            print(f'xddddd got message as server {result}')
            session.handleMessage(result)

    async def openIncomingConnections(self):
        print('xddddd will open')
        async with serve(self.didConnect, self.host, self.port):
            print('xddddd did open')
            await asyncio.Future()  # run forever
            print('xddddd did close')

    def url(self):
        return f'ws://{self.host}:{self.port}'

    async def connectTo(self, url: str) -> Session:
        print('xddddd will connect as client')
        session = SslSession(None)

        async def conne():
            print('xddddd will connect as client async')

            async with connect(url) as websocket:
                session.websocket = websocket
                print('xddddd did connect as client')
                while True:
                    print(f'xddddd waiting for message')
                    result = await websocket.recv()
                    print(f'xddddd got message as client {result}')
                    session.handleMessage(result)
                print('closed connection as client')

        asyncio.create_task(conne())
        return session
