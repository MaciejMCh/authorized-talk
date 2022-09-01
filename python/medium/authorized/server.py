from asyncio import get_running_loop, create_task, Future
from enum import Enum
from typing import Optional

from python.core.interface_identity import InterfaceIdentity
from python.core.random import Random
from python.core.rsa_keys import RsaKeys
from python.encryption.rsa_encryption import RsaEncryption, DecryptionFailed
from python.identity_server.identity_server import IdentityServer
from python.medium.authorized.server_exceptions import ServerException, ReceivedInvalidCipher, \
    ReceivedInvalidIntroductionSignature, AccessDenied, ReceivedInvalidAnswerSignature
from python.medium.authorized.server_status import Status
from python.medium.authorized.utils import introduction_signature
from python.medium.medium import Medium
from python.medium.authorized.utils import access_pass_signature
from python.messages.whisper_control_pb2 import Introduction, IntroductionReaction, Challenge, ChallengeAnswer, AccessPass


class AuthorizedServerMedium(Medium):
    def __init__(
            self,
            pseudonym: str,
            medium: Medium,
            rsa_keys: RsaKeys,
            identity_server: IdentityServer,
            random: Random,
    ):
        super().__init__()
        self.pseudonym = pseudonym
        self.medium = medium
        self.rsa_keys = rsa_keys
        self.identity_server = identity_server
        self.random = random
        self.source_public_key: Optional[bytes] = None
        self.otp: Optional[bytes] = None
        self.source_pseudonym: Optional[str] = None
        self.status = Status.INITIAL
        self.challenged = get_running_loop().create_future()
        self.authorized = get_running_loop().create_future()
        self.failure: Future[ServerException] = get_running_loop().create_future()
        self.setup()

    def setup(self):
        self.medium.handle_message(self.on_medium_message)

    def on_medium_message(self, message: bytes):
        if self.status == Status.INITIAL:
            create_task(self.receive_introduction(message))
            return
        if self.status == Status.CHALLENGED:
            create_task(self.receive_challenge_answer(message))
            return

    async def receive_challenge_answer(self, message: bytes):
        try:
            decrypted_message = RsaEncryption.decrypt(cipher=message, private_key=self.rsa_keys.private_key)
            challenge_answer = ChallengeAnswer()
            challenge_answer.ParseFromString(decrypted_message)
            is_verified = RsaEncryption.verify(
                message=self.otp,
                signature=challenge_answer.signature,
                public_key=self.source_public_key,
            )
            if is_verified:
                self.status = Status.AUTHORIZED
                self.authorized.set_result(None)
                await self.send_access_pass(True)
            else:
                await self.send_access_pass(False)
                self.fail(ReceivedInvalidAnswerSignature())
        except DecryptionFailed as decryption_failed:
            self.fail(ReceivedInvalidCipher(
                cipher=message,
                status=self.status,
                inner=decryption_failed,
            ))

    async def receive_introduction(self, message: bytes):
        try:
            introduction_bytes = RsaEncryption.decrypt(cipher=message, private_key=self.rsa_keys.private_key)
            introduction = Introduction()
            introduction.ParseFromString(introduction_bytes)
            self.source_public_key = await self.identity_server.get_public_key(introduction.pseudonym)
            if_verified = RsaEncryption.verify(
                message=introduction_signature(
                    pseudonym=introduction.pseudonym,
                    target_interface=introduction.targetInterface,
                    nonce=introduction.nonce,
                ),
                signature=introduction.signature,
                public_key=self.source_public_key,
            )
            if if_verified:
                self.source_pseudonym = introduction.pseudonym
                if await self.identity_server.has_access(
                    source_pseudonym=introduction.pseudonym,
                    interface_identity=InterfaceIdentity(
                        pseudonym=self.pseudonym,
                        interface=introduction.targetInterface,
                    ),
                ):
                    await self.challenge(nonce=introduction.nonce)
                else:
                    self.fail(AccessDenied())
            else:
                self.fail(ReceivedInvalidIntroductionSignature())
        except DecryptionFailed as decryption_failed:
            self.fail(ReceivedInvalidCipher(
                cipher=message,
                status=self.status,
                inner=decryption_failed,
            ))


    async def challenge(self, nonce: bytes):
        self.otp = await self.random.generate()
        introduction_reaction = IntroductionReaction(
            challenge=Challenge(
                otp=self.otp,
                signature=RsaEncryption.sign(
                    message=nonce,
                    private_key=self.rsa_keys.private_key,
                ),
            ),
        )
        message_bytes = introduction_reaction.SerializeToString()
        cipher = RsaEncryption.encrypt(message=message_bytes, public_key=self.source_public_key)
        await self.medium.send(cipher)
        self.status = Status.CHALLENGED
        self.challenged.set_result(None)

    async def send_access_pass(self, passes: bool):
        signature = RsaEncryption.sign(
            message=access_pass_signature(
                source_pseudonym=self.source_pseudonym,
                passes=passes,
            ),
            private_key=self.rsa_keys.private_key,
        )
        access_pass = AccessPass(
            signature=signature,
            passes=passes,
        )
        access_pass_bytes = access_pass.SerializeToString()
        access_pass_cipher = RsaEncryption.encrypt(
            message=access_pass_bytes,
            public_key=self.source_public_key,
        )
        await self.medium.send(access_pass_cipher)

    def fail(self, server_exception: ServerException):
        self.status = Status.FAILED
        self.failure.set_result(server_exception)
