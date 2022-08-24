from collections import Callable
from python.core.interfaceIdentity import InterfaceIdentity
from python.medium.medium import Medium


class Connector:
    def establishConnection(
            self,
            interfaceIdentity: InterfaceIdentity,
            onMessage: Callable[[bytes], None],
    ) -> Medium:
        raise Exception('dont use this base class')
