from typing import List

from python.core.interface_identity import InterfaceIdentity
from python.medium.kinds import TargetMedium


class TargetNotFound(Exception):
    pass


class IdentityServer:
    async def get_available_mediums(self, pseudonym: str) -> List[TargetMedium]:
        raise Exception('dont use this base class')

    async def get_public_key(self, pseudonym: str) -> bytes:
        raise Exception('dont use this base class')

    async def has_access(self, source_pseudonym: str, interface_identity: InterfaceIdentity) -> bool:
        raise Exception('dont use this base class')
