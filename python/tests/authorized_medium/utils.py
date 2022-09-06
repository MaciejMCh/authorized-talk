from typing import Tuple, Coroutine, Any, Callable, Optional

from python.core.interface_identity import InterfaceIdentity
from python.core.rsa_keys import RsaKeys
from python.encryption.rsa_encryption import RsaEncryption
from python.identity_server.identity_server import IdentityServer
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.authorized.server import AuthorizedServerMedium
from python.medium.authorized.utils import introduction_signature
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.medium.websocket_medium import WebsocketMedium
from python.messages.whisper_control_pb2 import IntroductionReaction, Challenge, Introduction, AccessPass
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, TestRandom, bob_private_key
from python.websocket.client import run_client
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


async def with_initial_status(identity_server: Optional[IdentityServer] = None):
    identity_server = TestIdentityServer(
            target_mediums_by_pseudonyms={'alice': []},
            public_keys_by_pseudonyms={'alice': alice_rsa_keys.public_key},
            white_list={'bob': {'some_interface': ['master']}},
            roles={'alice': ['master']}
        ) if identity_server is None else identity_server
    bob_websocket_location = Location(host='localhost', port=8765)
    server, server_close = await run_server(bob_websocket_location)
    client, _ = await run_client(bob_websocket_location)
    medium = AuthorizedServerMedium(
        pseudonym="bob",
        medium=WebsocketMedium.server(server.sessions[0]),
        rsa_keys=RsaKeys(private_key=bob_private_key, public_key=bob_public_key),
        identity_server=identity_server,
        random=TestRandom(phrase=b'some_otp'),
    )

    async def close():
        server.close()
        await server_close

    return medium, client, close


async def with_challenged_status(identity_server: Optional[IdentityServer] = None):
    identity_server = TestIdentityServer(
            target_mediums_by_pseudonyms={'alice': []},
            public_keys_by_pseudonyms={'alice': alice_rsa_keys.public_key},
            white_list={'bob': {'some_interface': ['master']}},
            roles={'alice': ['master']}
        ) if identity_server is None else identity_server
    bob_websocket_location = Location(host='localhost', port=8765)
    server, server_close = await run_server(bob_websocket_location)
    client, _ = await run_client(bob_websocket_location)
    medium = AuthorizedServerMedium(
        pseudonym="bob",
        medium=WebsocketMedium.server(server.sessions[0]),
        rsa_keys=RsaKeys(private_key=bob_private_key, public_key=bob_public_key),
        identity_server=identity_server,
        random=TestRandom(phrase=b'some_otp'),
    )

    signature = RsaEncryption.sign(
        message=introduction_signature(
            pseudonym='alice',
            target_interface='some_interface',
            nonce=b'some_nonce',
        ),
        private_key=alice_rsa_keys.private_key,
    )
    introduction = Introduction(
        pseudonym='alice',
        targetInterface='some_interface',
        nonce=b'some_nonce',
        signature=signature,
    )
    introduction_bytes = introduction.SerializeToString()
    introduction_cipher = RsaEncryption.encrypt(introduction_bytes, bob_public_key)

    await client.send(introduction_cipher)
    await medium.challenged

    async def close():
        server.close()
        await server_close

    return medium, client, close


async def with_authorized_client():
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

    access_pass_signature = RsaEncryption.sign(
        message=b'alice;1',
        private_key=bob_private_key,
    )
    access_pass = AccessPass(
        signature=access_pass_signature,
        passes=True,
    )
    access_pass_cipher = RsaEncryption.encrypt(
        message=access_pass.SerializeToString(),
        public_key=alice_rsa_keys.public_key,
    )
    await server.sessions[0].send(access_pass_cipher)
    await medium.authorized

    async def close():
        server.close()
        await server_close

    return medium, server.sessions[0], close
