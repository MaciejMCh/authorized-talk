import unittest
from typing import Optional
from python.core.interface_identity import InterfaceIdentity
from python.medium.authorized_medium import AuthorizedClientMedium, Status
from python.medium.kinds import WebsocketSourceMedium, WebsocketTargetMedium
from python.tests.utils import TestIdentityServer, bob_public_key
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
        await medium.connected

        await server.sessions[0].send(b'hi')
        self.assertEqual(medium.status, Status.CONNECTED, 'connected status should be Status.CONNECTED')
        self.assertEqual(len(server.sessions), 1, 'on connected status, session should be established')

        server.close()
        await server_close

    async def test_introducing_status(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)

        medium = AuthorizedClientMedium(
            target=InterfaceIdentity(pseudonym='bob', interface='some_interface'),
            identity_server=TestIdentityServer(
                target_mediums_by_pseudonyms={'bob': [WebsocketTargetMedium(location=bob_websocket_location)]},
                public_keys_by_pseudonyms={'bob': bob_public_key},
            ),
            available_source_mediums=[WebsocketSourceMedium()],
        )
        await medium.introducing
        received_message: Optional[bytes] = None

        def receive_message(message: bytes):
            nonlocal received_message
            received_message = message

        server.sessions[0].onMessage = receive_message
        self.assertEqual(medium.status, Status.INTRODUCING, 'introducing status should be Status.INTRODUCING')
        self.assertEqual('xddd', received_message)

        server.close()
        await server_close


# TODO: each state must reject invalid ciphers
# TODO: each state must reject invalid signatures
# TODO: each state must reject not expected messages

# TODO: introduction checks: bob has access
if __name__ == '__main__':
    unittest.main()
