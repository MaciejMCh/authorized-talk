from google.protobuf.reflection import GeneratedProtocolMessageType
from google.protobuf.message import Message
from google.protobuf.descriptor import Descriptor, FieldDescriptor, OneofDescriptor
from python.example.one_of_all_commands import one_of_all_commands


def field_of_type(one_of_descriptor: OneofDescriptor, message: Message):
    for field in one_of_descriptor.fields:
        if field.message_type == message.DESCRIPTOR:
            return field
    raise Exception("field not found")


def compose_command(actor_type: GeneratedProtocolMessageType, message: Message, nonce: int):
    OneOfAllCommands = one_of_all_commands(actor_type)
    command = OneOfAllCommands(nonce=nonce, takeOff=message)
    property_name: str = message.DESCRIPTOR.name
    property_name = property_name[0].lower() + property_name[1:]
    one_of_descriptor = command.DESCRIPTOR.oneofs[0]
    field = field_of_type(one_of_descriptor, message)
    message._is_present_in_parent = True
    command._oneofs = {one_of_descriptor: field}
    command._fields[field] = message
    return command
