import asyncio
from asyncio import gather, sleep
from typing import Optional

from python.core.interface_identity import InterfaceIdentity
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.medium.medium import Medium
from python.medium.websocket_medium import WebsocketConnector
from python.messages.whisper_control_pb2 import Introduction, Challenge, ChallengeAnswer, AccessPass
from python.tests.authorized_medium.utils import with_introducing_status, with_submitting_status
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, bob_private_key, TestRandom
from python.websocket.location import Location
from python.websocket.server import run_server
from python.websocket.client import run_client


def assertTrue(condition: bool):
    print('assertTrue', condition)


async def main():
    medium, session, close = await with_submitting_status()
    await session.send(b'invalid cipher')
    error = await medium.failure
    await close()
    # self.assertEqual(medium.status, Status.FAILED, "after receiving invalid cipher, state should be failed")
    # self.assertIsInstance(error, ReceivedInvalidCipher, "receiving invalid cipher, should raise ReceivedInvalidCipher")
    # self.assertEqual(Status.INTRODUCING, error.status, "failure should occur on INTRODUCING status")

if __name__ == "__main__":
    asyncio.run(main())
