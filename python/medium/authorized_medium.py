from enum import Enum
from typing import List
from python.connector.authorized_connector import AuthorizedConnector
from python.core.interface_identity import InterfaceIdentity
from python.identity_server.identity_server import IdentityServer
from python.medium.kinds import SourceMedium
from python.medium.medium import Medium


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
