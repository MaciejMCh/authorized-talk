import unittest
from asyncio import sleep
from typing import Optional
from python.core.interface_identity import InterfaceIdentity
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client import AuthorizedClientMedium, Status
from python.medium.kinds import WebsocketSourceMedium, WebsocketTargetMedium
from python.messages.whisper_control_pb2 import Introduction, Challenge, ChallengeAnswer, AccessPass, \
    IntroductionReaction
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

        self.assertEqual(Status.INITIAL, medium.status, 'initial status should be INITIAL')
        self.assertEqual(0, len(server.sessions), 'on initial status, session should not be established yet')

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

        self.assertEqual(Status.CONNECTED, medium.status, 'connected status should be Status.CONNECTED')
        self.assertEqual(1, len(server.sessions), 'on connected status, session should be established')

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

        self.assertEqual(Status.INTRODUCING, medium.status, 'introducing status should be Status.INTRODUCING')
        self.assertIsNotNone(received_message, 'should receive introduction cipher')
        decrypted_message = RsaEncryption.decrypt(cipher=received_message, private_key=bob_private_key)
        introduction = Introduction()
        introduction.ParseFromString(decrypted_message)
        self.assertEqual('alice', introduction.pseudonym, 'pseudonym should be source actor')
        self.assertEqual('some_interface', introduction.targetInterface, 'interface should be target')
        self.assertEqual(b'some_nonce', introduction.nonce, 'random nonce should be test phrase')
        self.assertTrue(RsaEncryption.verify(
            message=b'alice;some_interface;some_nonce',
            signature=introduction.signature,
            public_key=alice_rsa_keys.public_key,
        ), 'signature should be verified with source public key')

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
        introduction_reaction = IntroductionReaction(
            challenge = Challenge(
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
        await medium.challenged
        self.assertTrue(True, 'should pass challenged future')

        server.close()
        await server_close

    async def test_submitting_status(self):
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

        received_message: Optional[bytes] = None

        def receive_message(message: bytes):
            nonlocal received_message
            received_message = message

        server.sessions[0].handle_message(receive_message)

        await server.sessions[0].send(cipher)
        await medium.submitting
        await sleep(0.1)

        self.assertIsNotNone(received_message, 'challenge answer cipher should be received')
        decrypted_message = RsaEncryption.decrypt(cipher=received_message, private_key=bob_private_key)
        challenge_answer = ChallengeAnswer()
        challenge_answer.ParseFromString(decrypted_message)
        self.assertTrue(RsaEncryption.verify(
            message=b'some_otp',
            signature=challenge_answer.signature,
            public_key=alice_rsa_keys.public_key,
        ), 'challenge answer signature should be verified with source public key')
        self.assertEqual(Status.SUBMITTING, medium.status, 'status should be Status.SUBMITTING')

        server.close()
        await server_close

    async def test_authorized_status(self):
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

        server.close()
        await server_close


# TODO: each state must reject invalid ciphers
# TODO: each state must reject invalid signatures
# TODO: each state must reject not expected messages

# TODO: introduction checks: bob has access

# TODO: challenge checks: bob signed nonce

# TODO: test repeat attacks scenarios

if __name__ == '__main__':
    unittest.main()
