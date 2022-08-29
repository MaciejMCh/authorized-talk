import asyncio
from asyncio import gather, sleep
from typing import Optional

from python.core.interface_identity import InterfaceIdentity
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.medium.medium import Medium
from python.medium.websocket_medium import WebsocketConnector
from python.messages.whisper_control_pb2 import Introduction
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, bob_private_key, TestRandom
from python.websocket.location import Location
from python.websocket.server import run_server
from python.websocket.client import run_client


async def main():
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
        random=TestRandom('some_nonce'),
    )

    await medium.connected

    received_message: Optional[bytes] = None

    def receive_message(message: bytes):
        nonlocal received_message
        received_message = message

    server.sessions[0].handle_message(receive_message)

    await medium.introducing
    await sleep(0.1)

    # self.assertEqual(medium.status, Status.INTRODUCING, 'introducing status should be Status.INTRODUCING')
    # self.assertIsNotNone(received_message)
    decrypted_message = RsaEncryption.decrypt(cipher=received_message, private_key=bob_private_key)
    introduction = Introduction()
    introduction.ParseFromString(decrypted_message)
    # self.assertEqual(introduction.pseudonym, 'alice')
    # self.assertEqual(introduction.targetInterface, 'some_interface')
    # self.assertEqual(introduction.nonce, 'some_nonce')
    # self.assertTrue(RsaEncryption.verify(
    #     message=b'$alice;$some_interface;$some_nonce',
    #     signature=introduction.signature,
    #     public_key=alice_rsa_keys.public_key,
    # ))

    server.close()
    await server_close

if __name__ == "__main__":
    asyncio.run(main())
