import asyncio
import websockets


class Controller:
    def __init__(self):
        self.server = None


async def hello(websocket, path):
    print(f'server: connected {websocket}')
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")


async def runServer(controller: Controller):
    print('server: starting')
    server = await websockets.serve(hello, "localhost", 8765)
    controller.server = server
    print(f'server: started {server}')
    await server.wait_closed()
    print('server: closed')


async def client():
    print('client: starting')
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = 'name'
        await websocket.send(name)
        greeting = await websocket.recv()
    print('client: closed')


async def runController(controller: Controller):
    await asyncio.sleep(2)
    print(print('controller.server', controller.server))
    controller.server.close()


async def main():
    controller = Controller()
    await asyncio.gather(
        runServer(controller),
        client(),
        runController(controller),
    )
    print('main closed')

if __name__ == "__main__":
    asyncio.run(main())
