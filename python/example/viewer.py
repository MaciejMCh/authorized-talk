from typing import Dict, Callable, List, Tuple
from google.protobuf.internal.python_message import GeneratedProtocolMessageType
from google.protobuf.descriptor import Descriptor, FieldDescriptor
from google.protobuf.message import Message
from python.core.interfaceIdentity import InterfaceIdentity
from python.example.proto.system_pb2 import TelemetryInterface, RequestTelemetryCommand, TelemetryUpdateMessage
from python.medium.connector import Connector
from python.medium.medium import Medium


def establishMedium(interfaceIdentity: InterfaceIdentity, onMessage: Callable[[bytes], None]) -> Medium:
    pass


def parseSystemObject(descriptor: Descriptor) -> Tuple[str, List[FieldDescriptor]]:
    fields: List[FieldDescriptor] = descriptor.fields
    if len(fields) == 0:
        raise Exception('declaration cant be empty')
    if fields[0].name != 'systemBase':
        raise Exception(f'first field should be system base, but is {fields[0].name}')
    if len(fields) == 1:
        raise Exception('declaration must contain some elements')
    return fields[0].message_type.name, fields[1:]


def establishConnection(
        interfaceDeclaration: GeneratedProtocolMessageType,
        interfaceIdentity: InterfaceIdentity,
        didConnect: Callable[[], None],
        failedToConnect: Callable[[], None],
        onMessage: Callable[[], None],
):
    medium = establishMedium(interfaceIdentity)


class InterfaceConnectionError:
    pass


def makeCommandsTypesWhiteList(interfaceDeclaration: GeneratedProtocolMessageType):
    result = []
    (rootSystemBase, rootFields) = parseSystemObject(interfaceDeclaration.DESCRIPTOR)
    if rootSystemBase != 'Interface':
        raise Exception(f'root system base should be Interface, but is {rootSystemBase}')

    for rootField in rootFields:
        (elementSystemBase, elementFields) = parseSystemObject(rootField.message_type)
        if elementSystemBase == 'Command':
            result.append(rootField.message_type._concrete_class)
    return result


class InterfaceConnection:
    def __init__(
            self,
            interfaceDeclaration: GeneratedProtocolMessageType,
            interfaceIdentity: InterfaceIdentity,
            onMessage: Callable[[bytes], None],
            connector: Connector,
     ):
        self.medium = connector.establishConnection(
            interfaceIdentity=interfaceIdentity,
            onMessage=onMessage,
        )
        self.commandsTypesWhiteList = makeCommandsTypesWhiteList(interfaceDeclaration)

    @classmethod
    def passWhiteList(cls, instance, classes):
        instanceClass = type(instance)
        for eachClass in classes:
            if instanceClass is eachClass:
                return True
        return False

    def command(self, command: Message):
        if not InterfaceConnection.passWhiteList(
                instance=command,
                classes=self.commandsTypesWhiteList,
        ):
            raise Exception(f'attempt to send forbidden command {command}')
        self.medium.send(command.SerializeToString())


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
