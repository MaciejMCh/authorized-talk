import unittest

from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.server_exceptions import ReceivedInvalidCipher, ReceivedInvalidAnswerSignature
from python.medium.authorized.server_status import Status
from python.messages.whisper_control_pb2 import ChallengeAnswer
from python.tests.authorized_medium.utils import with_challenged_status
from python.tests.utils import bob_public_key


class ServerChallengedTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_reject_invalid_cipher(self):
        medium, client, close = await with_challenged_status()
        await client.send(b'invalid cipher')
        error = await medium.failure
        await close()

        self.assertEqual(medium.status, Status.FAILED, "after receiving invalid cipher, state should be failed")
        self.assertIsInstance(error, ReceivedInvalidCipher, "receiving invalid cipher, should raise ReceivedInvalidCipher")
        self.assertEqual(Status.CHALLENGED, error.status, "failure should occur on CHALLENGED status")

    async def test_reject_invalid_signature(self):
        medium, client, close = await with_challenged_status()

        challenge_answer = ChallengeAnswer(signature=b'invalid_signature')
        challenge_answer_bytes = challenge_answer.SerializeToString()
        challenge_answer_cipher = RsaEncryption.encrypt(message=challenge_answer_bytes, public_key=bob_public_key)
        await client.send(challenge_answer_cipher)
        error = await medium.failure
        await close()

        self.assertEqual(medium.status, Status.FAILED, "after receiving invalid signature, state should be failed")
        self.assertIsInstance(error, ReceivedInvalidAnswerSignature, "receiving invalid signature, should raise ReceivedInvalidAnswerSignature")


if __name__ == '__main__':
    unittest.main()
