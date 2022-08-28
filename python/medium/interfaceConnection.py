from typing import Callable, Tuple, List
from google.protobuf.message import Message
from google.protobuf.internal.python_message import GeneratedProtocolMessageType
from google.protobuf.descriptor import Descriptor, FieldDescriptor

from python.connector.connector import Connector
from python.core.interface_identity import InterfaceIdentity


class InterfaceConnection:
    def __init__(
            self,
            interfaceDeclaration: GeneratedProtocolMessageType,
            interfaceIdentity: InterfaceIdentity,
            on_message: Callable[[bytes], None],
            connector: Connector,
     ):
        self.medium = connector.establish_connection(
            interface_identity=interfaceIdentity,
            on_message=on_message,
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


def parseSystemObject(descriptor: Descriptor) -> Tuple[str, List[FieldDescriptor]]:
    fields: List[FieldDescriptor] = descriptor.fields
    if len(fields) == 0:
        raise Exception('declaration cant be empty')
    if fields[0].name != 'systemBase':
        raise Exception(f'first field should be system base, but is {fields[0].name}')
    if len(fields) == 1:
        raise Exception('declaration must contain some elements')
    return fields[0].message_type.name, fields[1:]