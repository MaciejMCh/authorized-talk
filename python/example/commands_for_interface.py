from typing import List

from google.protobuf.reflection import GeneratedProtocolMessageType
from google.protobuf.descriptor import Descriptor, FieldDescriptor, OneofDescriptor
from google.protobuf.message_factory import MessageFactory
from google.protobuf.descriptor_pool import DescriptorPool
from python.example.protobuf_utils import parse_system_object


def commands_for_interface(actor_type: GeneratedProtocolMessageType, interface: str):
    result: List[str] = []
    descriptor: Descriptor = actor_type.DESCRIPTOR
    actor_object_type, interfaces_fields = parse_system_object(descriptor)
    if actor_object_type != "Actor":
        raise Exception(f"actor type should be Actor, is {actor_object_type}")
    interface_field = next(x for x in interfaces_fields if x.name == interface)
    interface_object_type, messages_fields = parse_system_object(interface_field.message_type)
    if interface_object_type != "Interface":
        raise Exception(f"interface type should be Interface, is {interface_object_type}")
    for message_field in messages_fields:
        message_object_type, _ = parse_system_object(message_field.message_type)
        if message_object_type == "Command":
            result.append(message_field.name)
    return result
