from typing import Callable, Optional, List
from python.core.interfaceIdentity import InterfaceIdentity
from python.medium.connector import Connector
from python.medium.medium import Medium


class TestConnector(Connector):
    def __init__(self):
        self.testMedium: Optional[TestMedium] = None

    def establishConnection(
            self,
            interfaceIdentity: InterfaceIdentity,
            onMessage: Callable[[bytes], None],
    ) -> Medium:
        testMedium = TestMedium(onMessage)
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
