import unittest

from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client import Status
from python.medium.authorized.client_exceptions import ReceivedInvalidCipher, InvalidChallengeSignature
from python.messages.whisper_control_pb2 import Challenge
from python.tests.authorized_medium.utils import with_introducing_status
from python.tests.utils import alice_rsa_keys


class ClientIntroducingTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_reject_invalid_cipher(self):
        medium, session, close = await with_introducing_status()
        await session.send(b'invalid cipher')
        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving invalid cipher, state should be failed")
        self.assertIsInstance(error, ReceivedInvalidCipher, "receiving invalid cipher, should raise ReceivedInvalidCipher")
        self.assertEqual(Status.INTRODUCING, error.status, "failure should occur on INTRODUCING status")

    async def test_reject_invalid_signature(self):
        medium, session, close = await with_introducing_status()
        challenge = Challenge(
            otp=b'some_otp',
            signature=b'invalid_signature',
        )
        challenge_bytes = challenge.SerializeToString()
        cipher = RsaEncryption.encrypt(message=challenge_bytes, public_key=alice_rsa_keys.public_key)
        await session.send(cipher)
        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving invalid signature, state should be failed")
        self.assertIsInstance(error, InvalidChallengeSignature, "receiving invalid cipher, should raise InvalidChallengeSignature")


if __name__ == '__main__':
    unittest.main()
