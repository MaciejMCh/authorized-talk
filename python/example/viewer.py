from typing import Callable
from python.core.interfaceIdentity import InterfaceIdentity
from python.example.proto.system_pb2 import TelemetryInterface, RequestTelemetryCommand, TelemetryUpdateMessage
from python.medium.connector import Connector
from python.medium.interfaceConnection import InterfaceConnection


class Viewer:
    def __init__(
            self,
            targetPseudonym: str,
            onTelemetryUpdate: Callable[[TelemetryUpdateMessage], None],
            connector: Connector,
    ):
        self.onTelemetryUpdate = onTelemetryUpdate
        interfaceIdentity = InterfaceIdentity(
            pseudonym=targetPseudonym,
            interface='telemetry',
        )
        self.telemetryConnection = InterfaceConnection(
            interfaceDeclaration=TelemetryInterface,
            interfaceIdentity=interfaceIdentity,
            onMessage=self.onMessage,
            connector=connector,
        )

    def requestTelemetry(self):
        self.telemetryConnection.command(RequestTelemetryCommand(updatePeriod=0.1))

    def onMessage(self, message: bytes):
        telemetryUpdateMessage = TelemetryUpdateMessage()
        telemetryUpdateMessage.ParseFromString(message)
        self.onTelemetryUpdate(telemetryUpdateMessage)
