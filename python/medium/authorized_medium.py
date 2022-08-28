from collections import Callable
from enum import Enum
from typing import List
from python.core.interface_identity import InterfaceIdentity
from python.medium.connector import Connector
from python.medium.kinds import SourceMedium, TargetMedium, WebsocketTargetMedium
from python.medium.medium import Medium


class AuthorizedConnector(Connector):
    def __init__(self, identity_server: IdentityServer, available_source_mediums: List[SourceMedium]):
        self.identity_server = identity_server
        self.available_source_mediums = available_source_mediums

    async def establish_connection(
            self,
            interface_identity: InterfaceIdentity,
            on_message: Callable[[bytes], None],
    ) -> Medium:
        available_target_mediums = self.identity_server.get_available_mediums(interface_identity.pseudonym)
        return await CompromiseConnector(
            targets=available_target_mediums,
            sources=self.available_source_mediums,
        ).establish_connection(
            interface_identity=interface_identity,
            on_message=on_message,
        )


class Status(Enum):
    INITIAL = 1
    AUTHORIZED = 2


class AuthorizedClientMedium(Medium):
    def __init__(self, identity_server: IdentityServer, target: InterfaceIdentity,
                 available_source_mediums: List[SourceMedium]):
        super().__init__()
        self.status = Status.INITIAL
        self.identity_server = identity_server
        self.medium = AuthorizedConnector(
            identity_server=identity_server,
            available_source_mediums=available_source_mediums,
        ).establish_connection(target, self.receive_message)

    def receive_message(self, message: bytes):
        if self.status == Status.AUTHORIZED:
            self.receive_message(message)
