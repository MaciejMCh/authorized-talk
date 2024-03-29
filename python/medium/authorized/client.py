from asyncio import create_task, Task, get_running_loop, Future
from enum import Enum
from python.core.random import Random
from typing import List, Optional
from python.connector.authorized_connector import AuthorizedConnector
from python.core.interface_identity import InterfaceIdentity
from python.core.rsa_keys import RsaKeys
from python.encryption.encryption import Encryption
from python.encryption.rsa_encryption import RsaEncryption, DecryptionFailed
from python.identity_server.identity_server import IdentityServer
from python.medium.authorized.client_exceptions import ClientException, InvalidChallengeSignature, \
    ReceivedInvalidCipher, RejectedByTarget, MalformedProtoMessage, InvalidAccessPassSignature, ChallengeFailed
from python.medium.authorized.client_status import Status
from python.medium.authorized.utils import introduction_signature, access_pass_signature
from python.medium.kinds import SourceMedium
from python.medium.medium import Medium
from python.messages.whisper_control_pb2 import Introduction, Challenge, ChallengeAnswer, AccessPass, \
    IntroductionReaction


DEBUG = False


class AuthorizedClientMedium(Medium):
    def __init__(
            self,
            pseudonym: str,
            target: InterfaceIdentity,
            identity_server: IdentityServer,
            available_source_mediums: List[SourceMedium],
            rsa_keys: RsaKeys,
            random: Random,
    ):
        debug_print(f"init\n\tpseudonym:\t\t{pseudonym}\n\tpublic key:\t\t{rsa_keys.public_key}\n\tprivate key:\t{rsa_keys.private_key}")
        super().__init__()
        self.pseudonym = pseudonym
        self.status = Status.INITIAL
        self.identity_server = identity_server
        self.random = random
        self.rsa_keys = rsa_keys
        self.medium: Optional[Medium] = None
        self.nonce: Optional[bytes] = None
        self.target_public_key: Optional[bytes] = None
        self.connected = get_running_loop().create_future()
        self.introducing = get_running_loop().create_future()
        self.challenged = get_running_loop().create_future()
        self.submitting = get_running_loop().create_future()
        self.authorized = get_running_loop().create_future()
        self.failure: Future[ClientException] = get_running_loop().create_future()

        create_task(self.connect(
            target=target,
            available_source_mediums=available_source_mediums,
        ))

    async def connect(
            self,
            target: InterfaceIdentity,
            available_source_mediums: List[SourceMedium],
    ):
        self.medium = await AuthorizedConnector(
            identity_server=self.identity_server,
            available_source_mediums=available_source_mediums,
        ).establish_connection(target, self.handle_medium_message)
        self.status = Status.CONNECTED
        self.connected.set_result(None)
        create_task(self.introduce(target))

    async def introduce(self, target: InterfaceIdentity):
        self.nonce = await self.random.generate()
        self.target_public_key = await self.identity_server.get_public_key(target.pseudonym)
        signature_message = introduction_signature(
            pseudonym=self.pseudonym,
            target_interface=target.interface,
            nonce=self.nonce,
        )
        signature = RsaEncryption.sign(
            message=signature_message,
            private_key=self.rsa_keys.private_key,
        )
        debug_print(f"introduction:\n\tsignature message:\t\t{signature_message}")

        introduction = Introduction(
            pseudonym=self.pseudonym,
            targetInterface=target.interface,
            nonce=self.nonce,
            signature=signature,
        )

        cipher = RsaEncryption.encrypt(
            message=introduction.SerializeToString(),
            public_key=self.target_public_key,
        )

        await self.medium.send(cipher)
        self.status = Status.INTRODUCING
        self.introducing.set_result(None)

    def handle_medium_message(self, message: bytes):
        if self.status == Status.INTRODUCING:
            self.receive_introduction_reaction(message)
            return
        if self.status == Status.SUBMITTING:
            self.receive_access(message)
            return
        if self.status == Status.AUTHORIZED:
            self.receive_message(message)
            return

    def receive_access(self, message: bytes):
        try:
            decrypted = RsaEncryption.decrypt(cipher=message, private_key=self.rsa_keys.private_key)
            access_pass = AccessPass()
            access_pass.ParseFromString(decrypted)
            is_verified = RsaEncryption.verify(
                message=access_pass_signature(
                    source_pseudonym=self.pseudonym,
                    passes=access_pass.passes,
                ),
                signature=access_pass.signature,
                public_key=self.target_public_key,
            )

            if is_verified:
                if access_pass.passes:
                    self.status = Status.AUTHORIZED
                    self.authorized.set_result(None)
                else:
                    self.fail(ChallengeFailed())
            else:
                self.fail(InvalidAccessPassSignature())
        except DecryptionFailed as decryption_failed:
            self.fail(ReceivedInvalidCipher(
                cipher=message,
                status=self.status,
                inner=decryption_failed,
            ))

    def receive_introduction_reaction(self, message: bytes):
        try:
            decrypted = RsaEncryption.decrypt(cipher=message, private_key=self.rsa_keys.private_key)
            reaction = IntroductionReaction()
            reaction.ParseFromString(decrypted)
            if reaction.HasField("challenge"):
                self.receive_challenge(reaction.challenge)
            elif reaction.HasField("rejection"):
                self.fail(RejectedByTarget())
            else:
                self.fail(MalformedProtoMessage(
                    reason="none of challenge or rejection is present",
                    message=reaction,
                ))
        except DecryptionFailed as decryption_failed:
            self.fail(ReceivedInvalidCipher(
                cipher=message,
                status=self.status,
                inner=decryption_failed,
            ))

    def receive_challenge(self, challenge: Challenge):
        is_verified = RsaEncryption.verify(
            message=self.nonce,
            signature=challenge.signature,
            public_key=self.target_public_key,
        )

        if is_verified:
            create_task(self.answer_challenge(challenge=challenge))
        else:
            self.fail(InvalidChallengeSignature())

    def fail(self, reason: ClientException):
        debug_print(f"fail:\t\t{reason}")
        self.status = Status.FAILED
        self.failure.set_result(reason)

    async def answer_challenge(self, challenge: Challenge):
        self.status = Status.CHALLENGED
        self.challenged.set_result(None)
        signature = RsaEncryption.sign(message=challenge.otp, private_key=self.rsa_keys.private_key)
        challenge_answer = ChallengeAnswer(signature=signature)
        message = challenge_answer.SerializeToString()
        cipher = RsaEncryption.encrypt(message=message, public_key=self.target_public_key)
        await self.medium.send(cipher)
        self.status = Status.SUBMITTING
        self.submitting.set_result(None)

    async def send(self, message: bytes):
        if self.status != Status.AUTHORIZED:
            raise Exception(f"attempt to send message in not authorized status: {self.status}")

        await self.medium.send(message)


def debug_print(message: str):
    if DEBUG:
        print(f"authorized client medium: {message}")
