from asyncio import create_task, Task, get_running_loop, Future
from enum import Enum
from python.core.random import Random
from typing import List, Optional
from python.connector.authorized_connector import AuthorizedConnector
from python.core.interface_identity import InterfaceIdentity
from python.core.rsa_keys import RsaKeys
from python.encryption.encryption import Encryption
from python.encryption.rsa_encryption import RsaEncryption
from python.identity_server.identity_server import IdentityServer
from python.medium.authorized.utils import introduction_signature
from python.medium.kinds import SourceMedium
from python.medium.medium import Medium
from python.messages.whisper_control_pb2 import Introduction, Challenge


class Status(Enum):
    INITIAL = 1
    CONNECTED = 2
    INTRODUCING = 3
    CHALLENGED = 4
    FAILED_TO_AUTHORIZE = 5
    AUTHORIZED = 6


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
        ).establish_connection(target, self.receive_message)
        self.status = Status.CONNECTED
        self.connected.set_result(None)
        create_task(self.introduce(target))

    async def introduce(self, target: InterfaceIdentity):
        self.nonce = await self.random.generate()
        self.target_public_key = await self.identity_server.get_public_key(target.pseudonym)
        signature = RsaEncryption.sign(
            message=introduction_signature(
                pseudonym=self.pseudonym,
                target_interface=target.interface,
                nonce=self.nonce,
            ),
            private_key=self.rsa_keys.private_key,
        )

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

    def receive_message(self, message: bytes):
        if self.status == Status.INTRODUCING:
            self.receive_chellenge(message)
            return
        if self.status == Status.AUTHORIZED:
            self.receive_message(message)

    def receive_chellenge(self, message: bytes):
        decrypted = RsaEncryption.decrypt(cipher=message, private_key=self.rsa_keys.private_key)
        challenge = Challenge()
        challenge.ParseFromString(decrypted)
        is_verified = RsaEncryption.verify(
            message=self.nonce,
            signature=challenge.signature,
            public_key=self.target_public_key,
        )

        if is_verified:
            self.answer_challenge()
        else:
            self.fail('invalid challenge signature')

    def fail(self, reason: str):
        self.status = Status.FAILED_TO_AUTHORIZE

    def answer_challenge(self):
        self.status = Status.CHALLENGED
