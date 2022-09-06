import unittest
from asyncio import sleep
from typing import Optional

from python.core.interface_identity import InterfaceIdentity
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.authorized.client_status import Status
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.messages.whisper_control_pb2 import IntroductionReaction, Challenge, AccessPass
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, TestRandom, bob_private_key
from python.websocket.location import Location
from python.websocket.server import run_server


class ClientAuthorizedTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_sending_message(self):
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
        await sleep(0.1)

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
        await sleep(0.1)
        self.assertEqual(Status.AUTHORIZED, medium.status, 'status should be Status.AUTHORIZED')

        received_message: Optional[bytes] = None

        def receive_message_as_server(message: bytes):
            nonlocal received_message
            received_message = message

        server.sessions[0].handle_message(receive_message_as_server)

        await medium.send(b"hi")
        await sleep(0.1)
        self.assertIsNotNone(received_message, "should receive message")
        self.assertEqual(b"hi", received_message, "received message should be hi")

        server.close()
        await server_close


if __name__ == '__main__':
    unittest.main()
