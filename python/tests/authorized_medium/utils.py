from typing import Tuple, Coroutine, Any, Callable

from python.core.interface_identity import InterfaceIdentity
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.messages.whisper_control_pb2 import IntroductionReaction, Challenge
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, TestRandom, bob_private_key
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


async def with_submitting_status():
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

    await medium.introducing
    introduction_reaction = IntroductionReaction(
        challenge=Challenge(
            otp=b'some_otp',
            signature=RsaEncryption.sign(
                message=b'some_nonce',
                private_key=bob_private_key,
            ),
        ),
    )
    introduction_reaction_bytes = introduction_reaction.SerializeToString()
    cipher = RsaEncryption.encrypt(message=introduction_reaction_bytes, public_key=alice_rsa_keys.public_key)
    await server.sessions[0].send(cipher)
    await medium.submitting

    async def close():
        server.close()
        await server_close

    return medium, server.sessions[0], close
