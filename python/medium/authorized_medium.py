from asyncio import create_task, Task, get_running_loop, Future
from enum import Enum
from typing import List, Optional
from python.connector.authorized_connector import AuthorizedConnector
from python.core.interface_identity import InterfaceIdentity
from python.encryption.encryption import Encryption
from python.identity_server.identity_server import IdentityServer
from python.medium.kinds import SourceMedium
from python.medium.medium import Medium


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
    ):
        super().__init__()
        self.status = Status.INITIAL
        self.identity_server = identity_server
        self.medium: Optional[Medium] = None
        self.introducing = get_running_loop().create_future()

        self.connected = create_task(self.connect(
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
        create_task(self.introduce(target))

    async def introduce(self, target: InterfaceIdentity):
        target_public_key = await self.identity_server.get_public_key(target.pseudonym)
        Encryption.codeWithPublicKey()
        await self.medium.send(b'hi')
        self.status = Status.INTRODUCING
        self.introducing.set_result(None)

    def receive_message(self, message: bytes):
        if self.status == Status.AUTHORIZED:
            self.receive_message(message)
