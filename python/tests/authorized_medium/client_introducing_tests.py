import unittest

from python.encryption.rsa_encryption import RsaEncryption
from python.medium.authorized.client import Status
from python.medium.authorized.client_exceptions import ReceivedInvalidCipher, InvalidChallengeSignature, \
    RejectedByTarget, MalformedProtoMessage
from python.messages.whisper_control_pb2 import Challenge, IntroductionReaction, Rejection
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
        reaction = IntroductionReaction(
            challenge=Challenge(
                otp=b'some_otp',
                signature=b'invalid_signature',
            )
        )
        reaction_bytes = reaction.SerializeToString()
        cipher = RsaEncryption.encrypt(message=reaction_bytes, public_key=alice_rsa_keys.public_key)
        await session.send(cipher)
        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving invalid signature, state should be failed")
        self.assertIsInstance(error, InvalidChallengeSignature, "receiving invalid cipher, should raise InvalidChallengeSignature")

    async def test_reject_invalid_proto_message(self):
        medium, session, close = await with_introducing_status()
        reaction = IntroductionReaction()
        reaction_bytes = reaction.SerializeToString()
        cipher = RsaEncryption.encrypt(message=reaction_bytes, public_key=alice_rsa_keys.public_key)
        await session.send(cipher)
        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving invalid proto message, state should be failed")
        self.assertIsInstance(error, MalformedProtoMessage, "receiving invalid proto message, should raise MalformedProtoMessage")
        self.assertIsInstance(error.message, IntroductionReaction, "malformed message should be IntroductionReaction")

    async def test_being_rejected_by_target(self):
        medium, session, close = await with_introducing_status()
        reaction = IntroductionReaction(rejection=Rejection())
        reaction_bytes = reaction.SerializeToString()
        cipher = RsaEncryption.encrypt(message=reaction_bytes, public_key=alice_rsa_keys.public_key)
        await session.send(cipher)
        error = await medium.failure
        await close()
        self.assertEqual(medium.status, Status.FAILED, "after receiving rejection, state should be failed")
        self.assertIsInstance(error, RejectedByTarget, "being rejected by target, should raise RejectedByTarget")


# TODO: test repeated rejection
# TODO: test repeated challenge


if __name__ == '__main__':
    unittest.main()
