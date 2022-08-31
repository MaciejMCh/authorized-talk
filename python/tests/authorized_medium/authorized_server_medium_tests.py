import unittest

from python.core.rsa_keys import RsaKeys
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.server import AuthorizedServerMedium, Status
from python.medium.authorized.utils import introduction_signature
from python.medium.websocket_medium import WebsocketMedium
from python.messages.whisper_control_pb2 import Introduction
from python.tests.utils import alice_rsa_keys, bob_public_key, bob_private_key, TestIdentityServer
from python.websocket.client import run_client
from python.websocket.location import Location
from python.websocket.server import run_server


class AuthorizedServerMediumTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_initial_state(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)
        _ = await run_client(bob_websocket_location)
        medium = AuthorizedServerMedium(
            medium=WebsocketMedium.server(server.sessions[0]),
            rsa_keys=RsaKeys(private_key=bob_private_key, public_key=bob_public_key),
            identity_server=TestIdentityServer(
                target_mediums_by_pseudonyms={'alice': []},
                public_keys_by_pseudonyms={'alice': alice_rsa_keys.public_key},
            ),
        )

        self.assertEqual(Status.INITIAL, medium.status, "initially, status should be Status.INITIAL")
        server.close()
        await server_close

    async def test_challenged_state(self):
        bob_websocket_location = Location(host='localhost', port=8765)
        server, server_close = await run_server(bob_websocket_location)
        client, _ = await run_client(bob_websocket_location)
        medium = AuthorizedServerMedium(
            medium=WebsocketMedium.server(server.sessions[0]),
            rsa_keys=RsaKeys(private_key=bob_private_key, public_key=bob_public_key),
            identity_server=TestIdentityServer(
                target_mediums_by_pseudonyms={'alice': []},
                public_keys_by_pseudonyms={'alice': alice_rsa_keys.public_key},
            ),
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
        cipher = RsaEncryption.encrypt(introduction_bytes, bob_public_key)
        await client.send(cipher)
        await medium.challenged

        server.close()
        await server_close


if __name__ == '__main__':
    unittest.main()
