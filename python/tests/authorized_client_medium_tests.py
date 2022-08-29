import unittest
from asyncio import sleep
from typing import Optional
from python.core.interface_identity import InterfaceIdentity
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client import AuthorizedClientMedium, Status
from python.medium.kinds import WebsocketSourceMedium, WebsocketTargetMedium
from python.messages.whisper_control_pb2 import Introduction, Challenge, ChallengeAnswer
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, bob_private_key, TestRandom
from python.websocket.location import Location
from python.websocket.server import run_server


class AuthorizedClientMediumTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_initial_status(self):
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

        self.assertEqual(medium.status, Status.INITIAL, 'initial status should be INITIAL')
        self.assertEqual(len(server.sessions), 0, 'on initial status, session should not be established yet')

        server.close()
        await server_close

    async def test_connected_status(self):
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
        await medium.connected

        self.assertEqual(medium.status, Status.CONNECTED, 'connected status should be Status.CONNECTED')
        self.assertEqual(len(server.sessions), 1, 'on connected status, session should be established')

        server.close()
        await server_close

    async def test_introducing_status(self):
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

        await medium.connected

        received_message: Optional[bytes] = None

        def receive_message(message: bytes):
            nonlocal received_message
            received_message = message

        server.sessions[0].handle_message(receive_message)

        await medium.introducing
        await sleep(0.1)

        self.assertEqual(medium.status, Status.INTRODUCING, 'introducing status should be Status.INTRODUCING')
        self.assertIsNotNone(received_message)
        decrypted_message = RsaEncryption.decrypt(cipher=received_message, private_key=bob_private_key)
        introduction = Introduction()
        introduction.ParseFromString(decrypted_message)
        self.assertEqual(introduction.pseudonym, 'alice')
        self.assertEqual(introduction.targetInterface, 'some_interface')
        self.assertEqual(introduction.nonce, b'some_nonce')
        self.assertTrue(RsaEncryption.verify(
            message=b'alice;some_interface;some_nonce',
            signature=introduction.signature,
            public_key=alice_rsa_keys.public_key,
        ))

        server.close()
        await server_close

    async def test_challenged_status(self):
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
        challenge = Challenge(
            otp=b'some_otp',
            signature=RsaEncryption.sign(
                message=b'some_nonce',
                private_key=bob_private_key,
            ),
        )
        challenge_bytes = challenge.SerializeToString()
        cipher = RsaEncryption.encrypt(message=challenge_bytes, public_key=alice_rsa_keys.public_key)
        await server.sessions[0].send(cipher)
        await sleep(0.1)
        self.assertEqual(medium.status, Status.CHALLENGED)

        server.close()
        await server_close

    async def test_submitted_status(self):
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
        challenge = Challenge(
            otp=b'some_otp',
            signature=RsaEncryption.sign(
                message=b'some_nonce',
                private_key=bob_private_key,
            ),
        )
        challenge_bytes = challenge.SerializeToString()
        cipher = RsaEncryption.encrypt(message=challenge_bytes, public_key=alice_rsa_keys.public_key)

        received_message: Optional[bytes] = None

        def receive_message(message: bytes):
            nonlocal received_message
            received_message = message

        server.sessions[0].handle_message(receive_message)

        await server.sessions[0].send(cipher)
        await medium.submitted
        await sleep(0.1)

        self.assertIsNotNone(received_message)
        decrypted_message = RsaEncryption.decrypt(cipher=received_message, private_key=bob_private_key)
        challenge_answer = ChallengeAnswer()
        challenge_answer.ParseFromString(decrypted_message)
        self.assertTrue(RsaEncryption.verify(
            message=b'some_otp',
            signature=challenge_answer.signature,
            public_key=alice_rsa_keys.public_key,
        ))

        server.close()
        await server_close


# TODO: each state must reject invalid ciphers
# TODO: each state must reject invalid signatures
# TODO: each state must reject not expected messages

# TODO: introduction checks: bob has access

# TODO: challenge checks: bob signed nonce
if __name__ == '__main__':
    unittest.main()
