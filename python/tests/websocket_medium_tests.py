import unittest
from typing import Optional

from python.medium.websocket_medium import WebsocketConnector
from python.websocket.location import Location
from python.websocket.server import run_server


class WebsocketMediumTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_send_message(self):
        location = Location(host='localhost', port=8765)
        server, server_running_task = await run_server(location=location)
        medium = await WebsocketConnector.establish_connection(Location(host='localhost', port=8765))
        receivedMessage: Optional[bytes] = None

        def receiveMessageAsServer(message: bytes):
            nonlocal receivedMessage
            receivedMessage = message

        server.sessions[0].onMessage = receiveMessageAsServer
        await medium.send(b'hi')
        server.close()
        await server_running_task
        self.assertEqual(receivedMessage, b'hi', 'hi message should be received')

    async def test_receive_message(self):
        location = Location(host='localhost', port=8765)
        server, server_running_task = await run_server(location=location)
        medium = await WebsocketConnector.establish_connection(Location(host='localhost', port=8765))
        receivedMessage: Optional[bytes] = None

        def receiveMessageAsMedium(message: bytes):
            nonlocal receivedMessage
            receivedMessage = message

        medium.onMessage = receiveMessageAsMedium
        await server.sessions[0].send(b'hi')
        server.close()
        await server_running_task
        self.assertEqual(receivedMessage, b'hi', 'hi message should be received')


if __name__ == '__main__':
    unittest.main()
