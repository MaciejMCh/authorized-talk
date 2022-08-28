import unittest
from typing import Optional

from python.core.interface_identity import InterfaceIdentity
from python.medium.authorized_medium import AuthorizedClientMedium, Status
from python.medium.kinds import WebsocketSourceMedium, WebsocketTargetMedium
from python.tests.utils import TestIdentityServer
from python.websocket.location import Location
from python.websocket.server import run_server


class AuthorizedClientMediumTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_initial_status(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)

        medium = AuthorizedClientMedium(
            target=InterfaceIdentity(pseudonym='bob', interface='some_interface'),
            identity_server=TestIdentityServer({'bob': [WebsocketTargetMedium(location=bob_websocket_location)]}),
            available_source_mediums=[WebsocketSourceMedium()],
        )

        self.assertEqual(medium.status, Status.INITIAL, 'initial status should be INITIAL')
        self.assertEqual(len(server.sessions), 0, 'on initial status, session should not be established yet')

        server.close()
        await server_close

    async def test_connected_status(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)

        medium = AuthorizedClientMedium(
            target=InterfaceIdentity(pseudonym='bob', interface='some_interface'),
            identity_server=TestIdentityServer({'bob': [WebsocketTargetMedium(location=bob_websocket_location)]}),
            available_source_mediums=[WebsocketSourceMedium()],
        )
        await medium.inner_medium_connected
        received_message: Optional[bytes] = None

        def receive_message(message: bytes):
            nonlocal received_message
            received_message = message

        medium.on_message = receive_message
        await server.sessions[0].send(b'hi')
        self.assertEqual(medium.status, Status.CONNECTED, 'connected status should be Status.CONNECTED')
        self.assertIsNone(received_message, 'message should not be received')

        server.close()
        await server_close


if __name__ == '__main__':
    unittest.main()
