from typing import Optional, Callable, List

from python.core.interfaceIdentity import InterfaceIdentity
from python.medium.connector import Connector
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
        self.onMessage = onMessage
        self.sentMessages: List[bytes] = []

    def send(self, message: bytes):
        self.sentMessages.append(message)

    def receive(self, message: bytes):
        self.onMessage(message)
