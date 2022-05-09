import asyncio

from medium.sslMedium import SslMedium


async def xdd():
    result = ''
    anna = SslMedium.local(8765)
    bob = SslMedium.local(8766)
    asyncio.create_task(anna.openIncomingConnections())
    asyncio.create_task(bob.openIncomingConnections())
    await asyncio.sleep(2)
    annasSession = await anna.connectTo(bob.url())

    def handleIncomingMessageAsBob(message: str):
        print('handle handleIncomingMessageAsBob')
        global result
        result = message

    await asyncio.sleep(1)
    bob.incomingSessions[0].onMessage(handleIncomingMessageAsBob)
    await annasSession.send('hello')
    await asyncio.sleep(2)


if __name__ == '__main__':
    asyncio.run(xdd())

# if __name__ == '__main__':
#     import asyncio
#     import websockets
#
#
#     async def echo(websocket, path):
#         async for message in websocket:
#             await websocket.send(message)
#
#
#     async def main():
#         async with websockets.serve(echo, "localhost", 8765):
#             await asyncio.Future()  # run forever
#
#
#     asyncio.run(main())