from google.protobuf.message import Message

from python.example.resolve_result_type import resolve_result_type


def blank_result(command: Message) -> Message:
    Result = resolve_result_type(command)
    return Result()
