from asyncio import create_task, Task, get_running_loop, Future
from enum import Enum
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
from python.messages.whisper_control_pb2 import Introduction
from python.tests.utils import bob_private_key


class Status(Enum):
    INITIAL = 1
    CONNECTED = 2
    INTRODUCING = 3
    AUTHORIZED = 4


class AuthorizedClientMedium(Medium):
    def __init__(
            self,
            target: InterfaceIdentity,
            identity_server: IdentityServer,
            available_source_mediums: List[SourceMedium],
            rsa_keys: RsaKeys,
    ):
        super().__init__()
        self.status = Status.INITIAL
        self.identity_server = identity_server
        self.rsa_keys = rsa_keys
        self.medium: Optional[Medium] = None
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
        self.target_public_key = await self.identity_server.get_public_key(target.pseudonym)
        signature = RsaEncryption.sign(
            message=introduction_signature(pseudonym=target.pseudonym, targetInterface=target.interface),
            private_key=self.rsa_keys.private_key,
        )
        introduction = Introduction(
            pseudonym=target.pseudonym,
            targetInterface=target.interface,
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
        if self.status == Status.AUTHORIZED:
            self.receive_message(message)
