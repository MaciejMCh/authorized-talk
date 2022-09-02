from typing import List

from python.core.interface_identity import InterfaceIdentity
from python.identity_server.identity_server import IdentityServer
from python.medium.kinds import TargetMedium


class BlockchainIdentityServer(IdentityServer):

    async def get_available_mediums(self, pseudonym: str) -> List[TargetMedium]:
        return await self.smart_contract.get_available_mediums(pseudonym)

    async def get_public_key(self, pseudonym: str) -> bytes:
        return await self.smart_contract.get_public_key(pseudonym)

    async def has_access(self, source_pseudonym: str, interface_identity: InterfaceIdentity) -> bool:
        return await self.smart_contract.has_access(source_pseudonym, interface_identity.pseudonym, interface_identity.interface)
