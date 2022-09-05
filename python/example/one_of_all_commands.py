from typing import List

from google.protobuf.reflection import GeneratedProtocolMessageType
from google.protobuf.descriptor import Descriptor, FieldDescriptor, OneofDescriptor
from google.protobuf.message_factory import MessageFactory
from google.protobuf.descriptor_pool import DescriptorPool
from python.example.protobuf_utils import parse_system_object


def one_of_all_commands(actor_type: GeneratedProtocolMessageType):
    fields_descriptors = commands_fields_descriptors(actor_type)
    prototype = make_one_of_prototype(fields_descriptors)
    return prototype


def commands_fields_descriptors(actor_type: GeneratedProtocolMessageType):
    result: List[FieldDescriptor] = []
    descriptor: Descriptor = actor_type.DESCRIPTOR
    actor_object_type, interfaces_fields = parse_system_object(descriptor)
    if actor_object_type != "Actor":
        raise Exception(f"actor type should be Actor, is {actor_object_type}")
    for interface_field in interfaces_fields:
        interface_object_type, messages_fields = parse_system_object(interface_field.message_type)
        if interface_object_type != "Interface":
            raise Exception(f"interface type should be Interface, is {interface_object_type}")
        for message_field in messages_fields:
            message_object_type, _ = parse_system_object(message_field.message_type)
            if message_object_type == "Command":
                result.append(message_field)
    return result


def make_one_of_prototype(fields_descriptors: List[FieldDescriptor]):
    pool = DescriptorPool()
    for field_descriptor in fields_descriptors:
        pool.AddDescriptor(field_descriptor.message_type)
    factory = MessageFactory(pool)

    index = 0
    fields_descriptors_in_one_of: List[FieldDescriptor] = []
    for field_descriptor in fields_descriptors:
        fields_descriptors_in_one_of.append(FieldDescriptor(
            name=field_descriptor.name,
            full_name=field_descriptor.full_name,
            index=index,
            containing_type=None,
            cpp_type=field_descriptor.cpp_type,
            default_value=field_descriptor.default_value,
            enum_type=field_descriptor.enum_type,
            extension_scope=field_descriptor.extension_scope,
            is_extension=field_descriptor.is_extension,
            label=field_descriptor.label,
            message_type=field_descriptor.message_type,
            number=index + 1,
            type=field_descriptor.type,
        ))
        index += 1

    one_of_descriptor = OneofDescriptor(
        name="command",
        full_name="command",
        index=1,
        containing_type=None,
        fields=fields_descriptors_in_one_of,
    )

    for field_descriptor_in_one_of in fields_descriptors_in_one_of:
        field_descriptor_in_one_of.containing_oneof = one_of_descriptor

    oneOfAllCommandsDescriptor = Descriptor(
        name="OneOfAllCommands",
        full_name="OneOfAllCommands",
        filename="system.proto",
        containing_type=None,
        fields=fields_descriptors_in_one_of,
        nested_types={},
        enum_types=[],
        extensions=[],
        oneofs=[one_of_descriptor],
        syntax="proto3",
    )
    return factory.CreatePrototype(oneOfAllCommandsDescriptor)
