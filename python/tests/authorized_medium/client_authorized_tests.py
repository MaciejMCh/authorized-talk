import unittest
from asyncio import sleep
from typing import Optional

from python.core.interface_identity import InterfaceIdentity
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.authorized.client_status import Status
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.messages.whisper_control_pb2 import IntroductionReaction, Challenge, AccessPass
from python.tests.authorized_medium.utils import with_authorized_client
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, TestRandom, bob_private_key
from python.websocket.location import Location
from python.websocket.server import run_server


class ClientAuthorizedTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_sending_message(self):
        medium, session, close = await with_authorized_client()

        received_message: Optional[bytes] = None

        def receive_message_as_server(message: bytes):
            nonlocal received_message
            received_message = message

        session.handle_message(receive_message_as_server)

        await medium.send(b"hi")
        await sleep(0.1)
        self.assertIsNotNone(received_message, "should receive message")
        self.assertEqual(b"hi", received_message, "received message should be hi")

        await close()

    async def test_receiving_message(self):
        medium, session, close = await with_authorized_client()

        received_message: Optional[bytes] = None

        def receive_message_as_client(message: bytes):
            nonlocal received_message
            received_message = message

        medium.handle_message(receive_message_as_client)

        await session.send(b"hi")
        await sleep(0.1)
        self.assertIsNotNone(received_message, "should receive message")
        self.assertEqual(b"hi", received_message, "received message should be hi")

        await close()


if __name__ == '__main__':
    unittest.main()
