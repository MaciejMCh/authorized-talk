import asyncio
from asyncio import gather, sleep
from typing import Optional

from python.core.interface_identity import InterfaceIdentity
from python.core.rsa_keys import RsaKeys
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.authorized.server import AuthorizedServerMedium
from python.medium.authorized.utils import introduction_signature
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.medium.medium import Medium
from python.medium.websocket_medium import WebsocketConnector, WebsocketMedium
from python.messages.whisper_control_pb2 import Introduction, Challenge, ChallengeAnswer, AccessPass
from python.tests.authorized_medium.utils import with_introducing_status, with_submitting_status
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, bob_private_key, TestRandom
from python.websocket.location import Location
from python.websocket.server import run_server
from python.websocket.client import run_client


def assertTrue(condition: bool):
    print('assertTrue', condition)


async def main():
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

    client.handle_message(receive_message_as_client)

    await client.send(challenge_answer_cipher)
    await medium.authorized
    await sleep(0.1)

    # self.assertIsNotNone(received_message, "should receive access pass")
    pass_bytes = RsaEncryption.decrypt(cipher=received_message, private_key=alice_rsa_keys.private_key)
    access_pass = AccessPass()
    access_pass.ParseFromString(pass_bytes)

    server.close()
    await server_close

if __name__ == "__main__":
    asyncio.run(main())
