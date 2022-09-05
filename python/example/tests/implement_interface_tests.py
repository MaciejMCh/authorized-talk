import unittest
from asyncio import sleep
from typing import Optional

from google.protobuf.message import Message
from python.example.implement_interface import implement_interface, InvalidResultType
from python.example.one_of_all_commands import one_of_all_commands
from python.example.proto.system_pb2 import Drone, TakeOff, ReadTelemetry, Success
from python.tests.utils import TestMedium


class ImplementInterfaceTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_receive_command_in_interface(self):
        received_command: Optional[Message] = None

        def handle_command(command: Message) -> Message:
            nonlocal received_command
            received_command = command
            return TakeOff.Result(
                success=Success()
            )

        medium = TestMedium()
        implement_interface(
            actor_type=Drone,
            interface="controller",
            medium=medium,
            handle_command=handle_command,
        )

        OneOfAllCommands = one_of_all_commands(Drone)
        message = OneOfAllCommands(
            takeOff=TakeOff(),
            nonce=2,
        )
        message_bytes = message.SerializeToString()
        medium.receive_message(message_bytes)
        self.assertIsNotNone(received_command, "should receive take off command")
        self.assertIsInstance(received_command, TakeOff, "received command type should be TakeOff")

    async def test_reject_command_outside_interface(self):
        received_command: Optional[Message] = None

        def handle_command(command: Message) -> Message:
            nonlocal received_command
            received_command = command
            return Message()

        medium = TestMedium()
        implement_interface(
            actor_type=Drone,
            interface="controller",
            medium=medium,
            handle_command=handle_command,
        )

        OneOfAllCommands = one_of_all_commands(Drone)
        message = OneOfAllCommands(readTelemetry=ReadTelemetry())
        message_bytes = message.SerializeToString()
        medium.receive_message(message_bytes)
        self.assertIsNone(received_command, "should not receive read telemetry command")

    async def test_raise_exception_on_invalid_result(self):
        def handle_command(command: Message) -> Message:
            return Success()

        medium = TestMedium()
        implement_interface(
            actor_type=Drone,
            interface="controller",
            medium=medium,
            handle_command=handle_command,
        )

        OneOfAllCommands = one_of_all_commands(Drone)
        message = OneOfAllCommands(
            takeOff=TakeOff(),
            nonce=2,
        )
        message_bytes = message.SerializeToString()
        try:
            medium.receive_message(message_bytes)
            self.assertTrue(False, "should not pass ,because invalid result type was returned")
        except InvalidResultType as invalid_result_type:
            self.assertIsNotNone(invalid_result_type, "invalid result type should be thrown")


if __name__ == '__main__':
    unittest.main()
