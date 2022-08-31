from typing import Tuple, Coroutine, Any, Callable

from python.core.interface_identity import InterfaceIdentity
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, TestRandom
from python.websocket.location import Location
from python.websocket.server import run_server, WebsocketServerSession


async def with_introducing_status():
    bob_websocket_location = Location(host='localhost', port=8765)
    server, server_close = await run_server(bob_websocket_location)

    medium = AuthorizedClientMedium(
        pseudonym='alice',
        target=InterfaceIdentity(pseudonym='bob', interface='some_interface'),
        identity_server=TestIdentityServer(
            target_mediums_by_pseudonyms={'bob': [WebsocketTargetMedium(location=bob_websocket_location)]},
            public_keys_by_pseudonyms={'bob': bob_public_key},
        ),
        available_source_mediums=[WebsocketSourceMedium()],
        rsa_keys=alice_rsa_keys,
        random=TestRandom(b'some_nonce'),
    )

    async def close():
        server.close()
        await server_close

    await medium.introducing
    return medium, server.sessions[0], close
