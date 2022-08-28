import asyncio
from asyncio import gather
from typing import Optional

from python.core.interface_identity import InterfaceIdentity
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.medium.medium import Medium
from python.medium.websocket_medium import WebsocketConnector
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys
from python.websocket.location import Location
from python.websocket.server import run_server
from python.websocket.client import run_client


async def main():
    bob_websocket_location = Location(host='localhost', port=8765)
    server, server_close = await run_server(bob_websocket_location)

    medium = AuthorizedClientMedium(
        target=InterfaceIdentity(pseudonym='bob', interface='some_interface'),
        identity_server=TestIdentityServer(
            target_mediums_by_pseudonyms={'bob': [WebsocketTargetMedium(location=bob_websocket_location)]},
            public_keys_by_pseudonyms={'bob': bob_public_key},
        ),
        available_source_mediums=[WebsocketSourceMedium()],
        rsa_keys=alice_rsa_keys,
    )
    await medium.introducing
    received_message: Optional[bytes] = None

    def receive_message(message: bytes):
        nonlocal received_message
        received_message = message

    server.sessions[0].handle_message(receive_message)
    # self.assertEqual(medium.status, Status.INTRODUCING, 'introducing status should be Status.INTRODUCING')
    # self.assertEqual('xddd', received_message)

    server.close()
    await server_close

if __name__ == "__main__":
    asyncio.run(main())
