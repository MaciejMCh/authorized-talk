import unittest

from python.medium.authorized.server import AuthorizedServerMedium, Status
from python.medium.websocket_medium import WebsocketMedium
from python.websocket.client import run_client
from python.websocket.location import Location
from python.websocket.server import run_server


class AuthorizedServerMediumTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_initial_state(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)
        _ = await run_client(bob_websocket_location)
        websocket_medium = WebsocketMedium.server(server.sessions[0])
        medium = AuthorizedServerMedium(
            medium=websocket_medium
        )

        self.assertEqual(Status.INITIAL, medium.status, "initially, status should be Status.INITIAL")
        server.close()
        await server_close


if __name__ == '__main__':
    unittest.main()
