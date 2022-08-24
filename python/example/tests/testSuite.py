from typing import Callable, Optional
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

    def send(self, message: bytes):
        pass

    def receive(self, message: bytes):
        self.onMessage(message)
