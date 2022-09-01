import unittest
from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.server_exceptions import ReceivedInvalidCipher, ReceivedInvalidIntroductionSignature, AccessDenied
from python.medium.authorized.server_status import Status
from python.medium.authorized.utils import introduction_signature
from python.messages.whisper_control_pb2 import Introduction
from python.tests.authorized_medium.utils import with_initial_status
from python.tests.utils import bob_public_key, TestIdentityServer, alice_rsa_keys


class ServerInitialTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_reject_invalid_cipher(self):
        medium, client, close = await with_initial_status()
        await client.send(b'invalid cipher')
        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving invalid cipher, state should be failed")
        self.assertIsInstance(error, ReceivedInvalidCipher, "receiving invalid cipher, should raise ReceivedInvalidCipher")
        self.assertEqual(Status.INITIAL, error.status, "failure should occur on INITIAL status")

    async def test_reject_invalid_signature(self):
        medium, client, close = await with_initial_status()

        introduction = Introduction(
            pseudonym="alice",
            targetInterface="some_interface",
            nonce=b"some_nonce",
            signature=b"invalid_signature",
        )
        introduction_bytes = introduction.SerializeToString()
        introduction_cipher = RsaEncryption.encrypt(message=introduction_bytes, public_key=bob_public_key)

        await client.send(introduction_cipher)

        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving invalid signature, state should be failed")
        self.assertIsInstance(error, ReceivedInvalidIntroductionSignature, "receiving invalid signature, should raise ReceivedInvalidIntroductionSignature")

    async def test_deny_access(self):
        medium, client, close = await with_initial_status(TestIdentityServer(
            target_mediums_by_pseudonyms={'alice': []},
            public_keys_by_pseudonyms={'alice': alice_rsa_keys.public_key},
            white_list={'bob': {'some_interface': ['master']}},
            roles={'alice': []}
        ))

        signature = RsaEncryption.sign(
            message=introduction_signature(
                pseudonym="alice",
                target_interface="some_interface",
                nonce=b"some_nonce",
            ),
            private_key=alice_rsa_keys.private_key,
        )

        introduction = Introduction(
            pseudonym="alice",
            targetInterface="some_interface",
            nonce=b"some_nonce",
            signature=signature,
        )
        introduction_bytes = introduction.SerializeToString()
        introduction_cipher = RsaEncryption.encrypt(message=introduction_bytes, public_key=bob_public_key)

        await client.send(introduction_cipher)

        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "not authorized actor should be rejected")
        self.assertIsInstance(error, AccessDenied, "receiving introduction from not authorized actor should raise AccessDenied")


if __name__ == '__main__':
    unittest.main()
