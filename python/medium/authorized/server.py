from asyncio import get_running_loop, create_task
from enum import Enum
from typing import Optional

from python.core.rsa_keys import RsaKeys
from python.encryption.rsa_encryption import RsaEncryption
from python.identity_server.identity_server import IdentityServer
from python.medium.authorized.utils import introduction_signature
from python.medium.medium import Medium
from python.messages.whisper_control_pb2 import Introduction


class Status(Enum):
    INITIAL = 1
    CHALLENGED = 2


class AuthorizedServerMedium(Medium):
    def __init__(
            self,
            medium: Medium,
            rsa_keys: RsaKeys,
            identity_server: IdentityServer,
    ):
        super().__init__()
        self.medium = medium
        self.rsa_keys = rsa_keys
        self.identity_server = identity_server
        self.source_public_key: Optional[bytes] = None
        self.status = Status.INITIAL
        self.challenged = get_running_loop().create_future()
        self.setup()

    def setup(self):
        self.medium.handle_message(self.on_medium_message)

    def on_medium_message(self, message: bytes):
        if self.status == Status.INITIAL:
            create_task(self.receive_introduction(message))
            return

    async def receive_introduction(self, message: bytes):
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
            self.challenge()
        else:
            self.fail('not verified')

    def challenge(self):
        self.status = Status.CHALLENGED
        self.challenged.set_result(None)
