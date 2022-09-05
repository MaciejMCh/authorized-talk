from typing import Tuple, List, Callable

from google.protobuf.reflection import GeneratedProtocolMessageType

from python.example.commands_for_interface import commands_for_interface
from python.example.one_of_all_commands import one_of_all_commands
from python.example.protobuf_utils import parse_system_object
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
    OneOfAllCommands = one_of_all_commands(actor_type)
    commands_whitelist = commands_for_interface(actor_type=actor_type, interface=interface)

    def on_message(message: bytes):
        one_of_all = OneOfAllCommands()
        one_of_all.ParseFromString(message)
        the_one_key = one_of_all.WhichOneof("command")

        if the_one_key not in commands_whitelist:
            return

        the_one_property = getattr(one_of_all, the_one_key)
        handle_command(the_one_property)

    medium.handle_message(on_message)


def implement_actor(message_type: GeneratedProtocolMessageType, receive_command):
    descriptor: Descriptor = message_type.DESCRIPTOR
    root_type, fields = parse_system_object(descriptor)
    if root_type != "Actor":
        raise Exception(f"actor root type should be Actor, is {root_type}")
    pass
