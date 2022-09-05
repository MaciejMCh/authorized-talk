from typing import List, Tuple
from google.protobuf.descriptor import Descriptor, FieldDescriptor


def parse_system_object(descriptor: Descriptor) -> Tuple[str, List[FieldDescriptor]]:
    fields: List[FieldDescriptor] = descriptor.fields
    if len(fields) == 0:
        raise Exception('declaration cant be empty')
    if fields[0].name != 'systemBase':
        raise Exception(f'first field should be system base, but is {fields[0].name}')
    return fields[0].message_type.name, fields[1:]
