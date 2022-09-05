import unittest
from asyncio import sleep
from typing import Optional

from google.protobuf.message import Message
from python.example.implement_interface import implement_interface
from python.example.one_of_all_commands import one_of_all_commands
from python.example.proto.system_pb2 import Drone, TakeOff, ReadTelemetry
from python.tests.utils import TestMedium


class ImplementInterfaceTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_receive_command_in_interface(self):
        received_command: Optional[Message] = None

        def handle_command(command: Message):
            nonlocal received_command
            received_command = command

        medium = TestMedium()
        implement_interface(
            actor_type=Drone,
            interface="controller",
            medium=medium,
            handle_command=handle_command,
        )

        OneOfAllCommands = one_of_all_commands(Drone)
        message = OneOfAllCommands(takeOff=TakeOff())
        message_bytes = message.SerializeToString()
        medium.receive_message(message_bytes)
        self.assertIsNotNone(received_command, "should receive take off command")
        self.assertIsInstance(received_command, TakeOff, "received command type should be TakeOff")

    async def test_reject_command_outside_interface(self):
        received_command: Optional[Message] = None

        def handle_command(command: Message):
            nonlocal received_command
            received_command = command

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


if __name__ == '__main__':
    unittest.main()
