from typing import Tuple, List, Callable

from google.protobuf.reflection import GeneratedProtocolMessageType

from python.example.one_of_all_commands import one_of_all_commands
from python.medium.medium import Medium
from google.protobuf.message import Message
from google.protobuf.reflection import GeneratedProtocolMessageType
from google.protobuf.descriptor import Descriptor, FieldDescriptor


def implement_interface(
    actor_type: GeneratedProtocolMessageType,
    interface: str,
    medium: Medium,
    handle_command: Callable[[Message], None],
):
    def on_message(message: bytes):
        one_of_all = one_of_all_commands()
        one_of_all.ParseFromString(message)
        return one_of_all.one

    medium.handle_message(on_message)


def implement_actor(message_type: GeneratedProtocolMessageType, receive_command):
    descriptor: Descriptor = message_type.DESCRIPTOR
    root_type, fields = parse_system_object(descriptor)
    if root_type != "Actor":
        raise Exception(f"actor root type should be Actor, is {root_type}")
    pass
