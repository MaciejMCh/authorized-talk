import asyncio
import signal
import threading
import time
from asyncio import Event, Future
from collections import Callable
from threading import Thread
from typing import Optional

import websockets

from encryption.unsafeEncryption import UnsafeEncryption
from python.medium.sslMedium import SslMedium
from talker.talkerInterfaceIdentity import TalkerInterfaceIdentity
from tests.testSuite import TestSuite
from whisper.whisperingMouth import WhisperingMouth


class WebsocketClient:
    def __init__(self):
        self.connectToServer()

    def connectToServer(self):
        async def runAsync():
            uri = "ws://localhost:8765"
            print('client: will connect')
            async with websockets.connect(uri) as websocket:
                print('client: connected', websocket)
                await websocket.send('xdd')
        asyncio.run(runAsync())


class WebsocketServer:
    def __init__(self):
        self.server = None
        self.stop: Optional[Future] = None
        self.startServer()

    def startServer(self):
        print('server: start')

        def runServerThread():
            async def runAsync():
                async def hello(websocket, path):
                    print(f'server: connected')

                self.stop = asyncio.Future()
                self.server = await websockets.serve(hello, "localhost", 8765)
                await self.stop
            asyncio.run(runAsync())

        Thread(target=runServerThread).start()

    def close(self):
        self.stop.get_loop().call_soon_threadsafe(self.stop.set_result, None)


def main():
    server = WebsocketServer()
    time.sleep(0.5)
    client = WebsocketClient()
    time.sleep(0.5)
    server.close()


if __name__ == '__main__':
    main()
