from typing import Optional, Callable, List, Dict

from python.connector.connector import Connector
from python.core.interface_identity import InterfaceIdentity
from python.identity_server.identity_server import IdentityServer, TargetNotFound
from python.medium.kinds import TargetMedium
from python.medium.medium import Medium


class TestConnector(Connector):
    def __init__(self):
        self.testMedium: Optional[TestMedium] = None

    def establish_connection(
            self,
            interface_identity: InterfaceIdentity,
            on_message: Callable[[bytes], None],
    ) -> Medium:
        testMedium = TestMedium(on_message)
        self.testMedium = testMedium
        return testMedium


class TestMedium(Medium):
    def __init__(self, onMessage: Callable[[bytes], None]):
        super().__init__()
        self.onMessage = onMessage
        self.sentMessages: List[bytes] = []

    def send(self, message: bytes):
        self.sentMessages.append(message)

    def receive(self, message: bytes):
        self.onMessage(message)


class TestIdentityServer(IdentityServer):
    def __init__(self, target_mediums_by_pseudonyms: Dict[str, List[TargetMedium]]):
        self.target_mediums_by_pseudonyms = target_mediums_by_pseudonyms

    async def get_available_mediums(self, pseudonym: str) -> List[TargetMedium]:
        if pseudonym not in self.target_mediums_by_pseudonyms:
            raise TargetNotFound()

        return self.target_mediums_by_pseudonyms[pseudonym]
