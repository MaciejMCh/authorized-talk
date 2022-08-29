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
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, bob_private_key, TestRandom
from python.websocket.location import Location
from python.websocket.server import run_server
from python.websocket.client import run_client


def assertTrue(condition: bool):
    print('assertTrue', condition)


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
    await medium.submitted
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
    # self.assertEqual(Status.AUTHORIZED, medium.status, 'status should be Status.AUTHORIZED')

    server.close()
    await server_close

if __name__ == "__main__":
    asyncio.run(main())
