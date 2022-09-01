import unittest
from asyncio import sleep
from typing import Optional

from python.core.rsa_keys import RsaKeys
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.server import AuthorizedServerMedium, Status
from python.medium.authorized.utils import introduction_signature
from python.medium.websocket_medium import WebsocketMedium
from python.messages.whisper_control_pb2 import Introduction, ChallengeAnswer, IntroductionReaction, AccessPass
from python.tests.utils import alice_rsa_keys, bob_public_key, bob_private_key, TestIdentityServer, TestRandom
from python.websocket.client import run_client
from python.websocket.location import Location
from python.websocket.server import run_server


class AuthorizedServerMediumTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_initial_state(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)
        _ = await run_client(bob_websocket_location)
        medium = AuthorizedServerMedium(
            pseudonym="bob",
            medium=WebsocketMedium.server(server.sessions[0]),
            rsa_keys=RsaKeys(private_key=bob_private_key, public_key=bob_public_key),
            identity_server=TestIdentityServer(
                target_mediums_by_pseudonyms={'alice': []},
                public_keys_by_pseudonyms={'alice': alice_rsa_keys.public_key},
            ),
            random=TestRandom(phrase=b'some_otp'),
        )

        self.assertEqual(Status.INITIAL, medium.status, "initially, status should be Status.INITIAL")
        server.close()
        await server_close

    async def test_challenged_state(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)
        client, _ = await run_client(bob_websocket_location)
        medium = AuthorizedServerMedium(
            pseudonym="bob",
            medium=WebsocketMedium.server(server.sessions[0]),
            rsa_keys=RsaKeys(private_key=bob_private_key, public_key=bob_public_key),
            identity_server=TestIdentityServer(
                target_mediums_by_pseudonyms={'alice': []},
                public_keys_by_pseudonyms={'alice': alice_rsa_keys.public_key},
                white_list={'bob': {'some_interface': ['master']}},
                roles={'alice': ['master']}
            ),
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

        received_message: Optional[bytes] = None

        def receive_message_as_client(message: bytes):
            nonlocal received_message
            received_message = message

        client.handle_message(receive_message_as_client)

        await client.send(introduction_cipher)
        await medium.challenged
        await sleep(0.1)

        self.assertIsNotNone(received_message, "should receive reaction cipher")
        reaction_bytes = RsaEncryption.decrypt(cipher=received_message, private_key=alice_rsa_keys.private_key)
        reaction = IntroductionReaction()
        reaction.ParseFromString(reaction_bytes)
        self.assertIsNotNone(reaction.challenge, "should receive challenge")
        self.assertEqual(b'some_otp', reaction.challenge.otp, "otp should be present")
        self.assertTrue(RsaEncryption.verify(
            message=b'some_nonce',
            signature=reaction.challenge.signature,
            public_key=bob_public_key,
        ), "nonce should be verified")

        server.close()
        await server_close

    async def test_authorized_state(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)
        client, _ = await run_client(bob_websocket_location)
        medium = AuthorizedServerMedium(
            pseudonym="bob",
            medium=WebsocketMedium.server(server.sessions[0]),
            rsa_keys=RsaKeys(private_key=bob_private_key, public_key=bob_public_key),
            identity_server=TestIdentityServer(
                target_mediums_by_pseudonyms={'alice': []},
                public_keys_by_pseudonyms={'alice': alice_rsa_keys.public_key},
                white_list={'bob': {'some_interface': ['master']}},
                roles={'alice': ['master']}
            ),
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

        signature = RsaEncryption.sign(message=b'some_otp', private_key=alice_rsa_keys.private_key)
        challenge_answer = ChallengeAnswer(signature=signature)
        challenge_answer_bytes = challenge_answer.SerializeToString()
        challenge_answer_cipher = RsaEncryption.encrypt(message=challenge_answer_bytes, public_key=bob_public_key)

        received_message: Optional[bytes] = None

        def receive_message_as_client(message: bytes):
            nonlocal received_message
            received_message = message

        await client.send(challenge_answer_cipher)
        await medium.authorized
        client.handle_message(receive_message_as_client)
        await sleep(0.1)

        self.assertIsNotNone(received_message, "should receive access pass")
        pass_bytes = RsaEncryption.decrypt(cipher=received_message, private_key=alice_rsa_keys.private_key)
        access_pass = AccessPass()
        access_pass.ParseFromString(pass_bytes)
        self.assertTrue(access_pass.passes, "should pass")
        is_verified = RsaEncryption.verify(
            message=b'alice;1',
            signature=access_pass.signature,
            public_key=bob_public_key,
        )
        self.assertTrue(is_verified, "access pass should be verifier")

        server.close()
        await server_close


if __name__ == '__main__':
    unittest.main()
