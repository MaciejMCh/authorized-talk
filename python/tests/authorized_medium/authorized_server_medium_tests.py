import unittest

from python.medium.websocket_medium import WebsocketMedium
from python.websocket.client import run_client
from python.websocket.location import Location
from python.websocket.server import run_server


class AuthorizedServerMediumTestCase(unittest.TestCase):
    def test_initial_state(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)
        client, client_close = await run_client(bob_websocket_location)
        asad = WebsocketMedium.server(server.sessions[0])


if __name__ == '__main__':
    unittest.main()
