from asyncio import create_task
from typing import Tuple, List, Callable
from python.example.commands_for_interface import commands_for_interface
from python.example.one_of_all_commands import one_of_all_commands
from python.example.proto.system_pb2 import Result
from python.example.protobuf_utils import parse_system_object
from python.example.resolve_result_type import resolve_result_type
from python.medium.medium import Medium
from google.protobuf.message import Message
from google.protobuf.reflection import GeneratedProtocolMessageType
from google.protobuf.descriptor import Descriptor, FieldDescriptor


class InvalidResultType(Exception):
    def __init__(self, result: Message, expected_type: GeneratedProtocolMessageType):
        self.result = result
        self.expected_type = expected_type


def implement_interface(
    actor_type: GeneratedProtocolMessageType,
    interface: str,
    medium: Medium,
    handle_command: Callable[[Message], Message],
):
    OneOfAllCommands = one_of_all_commands(actor_type)
    commands_whitelist = commands_for_interface(actor_type=actor_type, interface=interface)

    async def send_result_back(result: Message, nonce: int):
        result = Result(
            requestNonce=nonce,
            result=result.SerializeToString(),
        )
        await medium.send(result.SerializeToString())

    def on_message(message: bytes):
        one_of_all = OneOfAllCommands()
        one_of_all.ParseFromString(message)
        the_one_key = one_of_all.WhichOneof("command")

        if the_one_key not in commands_whitelist:
            return

        the_one_property = getattr(one_of_all, the_one_key)
        ResultType = resolve_result_type(the_one_property)
        result = handle_command(the_one_property)
        if result.DESCRIPTOR is not ResultType.DESCRIPTOR:
            raise InvalidResultType(result=result, expected_type=ResultType)
        create_task(send_result_back(result=result, nonce=one_of_all.nonce))

    medium.handle_message(on_message)


def implement_actor(message_type: GeneratedProtocolMessageType, receive_command):
    descriptor: Descriptor = message_type.DESCRIPTOR
    root_type, fields = parse_system_object(descriptor)
    if root_type != "Actor":
        raise Exception(f"actor root type should be Actor, is {root_type}")
    pass
