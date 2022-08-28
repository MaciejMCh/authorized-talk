from typing import List, Callable
from python.connector.compromise_connector import CompromiseConnector
from python.connector.connector import Connector
from python.core.interface_identity import InterfaceIdentity
from python.identity_server.identity_server import IdentityServer
from python.medium.kinds import SourceMedium
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
