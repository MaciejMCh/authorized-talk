from collections import Callable
from python.core.interface_identity import InterfaceIdentity
from python.medium.medium import Medium


class Connector:
    async def establish_connection(
            self,
            interface_identity: InterfaceIdentity,
            on_message: Callable[[bytes], None],
    ) -> Medium:
        raise Exception('dont use this base class')
