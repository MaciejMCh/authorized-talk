from typing import List

from python.blockchain.identity_server_contract import IdentityServerContract
from python.core.interface_identity import InterfaceIdentity
from python.identity_server.identity_server import IdentityServer
from python.medium.kinds import TargetMedium, WebsocketTargetMedium
from python.websocket.location import Location


class BlockchainIdentityServer(IdentityServer):
    def __init__(self, identity_server_contract: IdentityServerContract):
        self.identity_server_contract = identity_server_contract

    async def get_available_mediums(self, pseudonym: str) -> List[TargetMedium]:
        actor = self.identity_server_contract.get_actor(pseudonym)

        if not actor[2]:
            return []

        return [WebsocketTargetMedium(Location(
            host=actor[1][0],
            port=actor[1][1],
        ))]

    async def get_public_key(self, pseudonym: str) -> bytes:
        return await self.identity_server_contract.get_public_key(pseudonym)

    async def has_access(self, source_pseudonym: str, interface_identity: InterfaceIdentity) -> bool:
        return await self.identity_server_contract.has_access(source_pseudonym, interface_identity.pseudonym, interface_identity.interface)
