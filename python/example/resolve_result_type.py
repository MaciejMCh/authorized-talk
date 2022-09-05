from python.example.proto.system_pb2 import Message
from google.protobuf.descriptor import Descriptor
from google.protobuf import symbol_database
from google.protobuf.reflection import GeneratedProtocolMessageType


def resolve_result_type(command_message: Message) -> GeneratedProtocolMessageType:
    descriptor: Descriptor = command_message.DESCRIPTOR
    if len(descriptor.nested_types) != 1:
        raise Exception(f"command should have single nested type, has {len(descriptor.nested_types)}")
    nested_type: Descriptor = descriptor.nested_types[0]
    if nested_type.name != "Result":
        raise Exception(f"result should be nested type name, is {nested_type.name}")

    database = symbol_database.Default()
    prototype = database.GetPrototype(nested_type)
    return prototype
