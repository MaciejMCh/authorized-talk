from asyncio import create_task
from enum import Enum
from typing import List, Optional
from python.connector.authorized_connector import AuthorizedConnector
from python.core.interface_identity import InterfaceIdentity
from python.identity_server.identity_server import IdentityServer
from python.medium.kinds import SourceMedium
from python.medium.medium import Medium


class Status(Enum):
    INITIAL = 1
    CONNECTED = 2
    AUTHORIZED = 3


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

        self.inner_medium_connected = create_task(self.connect(
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

    def receive_message(self, message: bytes):
        if self.status == Status.AUTHORIZED:
            self.receive_message(message)
