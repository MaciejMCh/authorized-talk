import unittest

from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client_exceptions import ReceivedInvalidCipher, InvalidAccessPassSignature, \
    ChallengeFailed
from python.medium.authorized.client_status import Status
from python.messages.whisper_control_pb2 import AccessPass
from python.tests.authorized_medium.utils import with_submitting_status
from python.tests.utils import alice_rsa_keys, bob_private_key


class ClientSubmittingTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_reject_invalid_cipher(self):
        medium, session, close = await with_submitting_status()
        await session.send(b'invalid cipher')
        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving invalid cipher, state should be failed")
        self.assertIsInstance(error, ReceivedInvalidCipher, "receiving invalid cipher, should raise ReceivedInvalidCipher")
        self.assertEqual(Status.SUBMITTING, error.status, "failure should occur on SUBMITTING status")

    async def test_reject_invalid_signature(self):
        medium, session, close = await with_submitting_status()
        access_pass = AccessPass(
            signature=b'invalid_signature',
            passes=True,
        )
        access_pass_bytes = access_pass.SerializeToString()
        cipher = RsaEncryption.encrypt(message=access_pass_bytes, public_key=alice_rsa_keys.public_key)
        await session.send(cipher)
        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving invalid signature, state should be failed")
        self.assertIsInstance(error, InvalidAccessPassSignature, "receiving invalid cipher, should raise InvalidAccessPassSignature")

    async def test_failing_challenge(self):
        medium, session, close = await with_submitting_status()
        access_pass_signature = RsaEncryption.sign(
            message=b'alice;0',
            private_key=bob_private_key,
        )
        access_pass = AccessPass(
            signature=access_pass_signature,
            passes=False,
        )
        access_pass_bytes = access_pass.SerializeToString()
        cipher = RsaEncryption.encrypt(message=access_pass_bytes, public_key=alice_rsa_keys.public_key)
        await session.send(cipher)
        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving rejection, state should be failed")
        self.assertIsInstance(error, ChallengeFailed, "being rejected by target, should raise ChallengeFailed")

    async def test_reject_repeated_pass(self):
        medium, session, close = await with_submitting_status()
        access_pass_signature = RsaEncryption.sign(
            message=b'alice;0',
            private_key=bob_private_key,
        )
        access_pass = AccessPass(
            signature=access_pass_signature,
            passes=True,
        )
        access_pass_bytes = access_pass.SerializeToString()
        cipher = RsaEncryption.encrypt(message=access_pass_bytes, public_key=alice_rsa_keys.public_key)
        await session.send(cipher)
        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving repeated signature of negative pass, state should be failed")
        self.assertIsInstance(error, InvalidAccessPassSignature, "receiving repeated signature of negative pass should raise InvalidAccessPassSignature exception")

# TODO: test repeated access pass


if __name__ == '__main__':
    unittest.main()
