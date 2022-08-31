import unittest
from asyncio import sleep
from typing import Optional
from python.medium.websocket_medium import WebsocketConnector, WebsocketMedium
from python.websocket.client import run_client
from python.websocket.location import Location
from python.websocket.server import run_server


class WebsocketMediumTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_send_message_as_client(self):
        location = Location(host='localhost', port=8765)
        server, server_running_task = await run_server(location=location)
        medium = await WebsocketConnector.establish_connection(Location(host='localhost', port=8765))
        received_message: Optional[bytes] = None

        def receive_message_as_server(message: bytes):
            nonlocal received_message
            received_message = message

        server.sessions[0].handle_message(receive_message_as_server)
        await medium.send(b'hi')
        server.close()
        await server_running_task
        self.assertEqual(b'hi', received_message, 'hi message should be received')

    async def test_receive_message_as_client(self):
        location = Location(host='localhost', port=8765)
        server, server_running_task = await run_server(location=location)
        medium = await WebsocketConnector.establish_connection(Location(host='localhost', port=8765))
        received_message: Optional[bytes] = None

        def receive_message_as_medium(message: bytes):
            nonlocal received_message
            received_message = message

        medium.handle_message(receive_message_as_medium)
        await server.sessions[0].send(b'hi')
        server.close()
        await server_running_task
        self.assertEqual(b'hi', received_message, 'hi message should be received')

    async def test_send_message_as_server(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)
        client, client_close = await run_client(bob_websocket_location)
        medium = WebsocketMedium.server(server.sessions[0])

        received_message: Optional[bytes] = None

        def receive_message_as_client(message: bytes):
            nonlocal received_message
            received_message = message

        client.handle_message(receive_message_as_client)

        await medium.send(b'hi')
        await sleep(0.1)
        self.assertEqual(b'hi', received_message, 'hi message should be received')
        server.close()
        await server_close

    async def test_receive_message_as_server(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)
        client, client_close = await run_client(bob_websocket_location)
        medium = WebsocketMedium.server(server.sessions[0])

        received_message: Optional[bytes] = None

        def receive_message_as_server(message: bytes):
            nonlocal received_message
            received_message = message

        medium.handle_message(receive_message_as_server)

        await client.send(b'hi')
        await sleep(0.1)
        self.assertEqual(b'hi', received_message, 'hi message should be received')


if __name__ == '__main__':
    unittest.main()
