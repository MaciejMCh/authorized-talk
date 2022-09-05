import unittest
from asyncio import sleep
from typing import Optional

from google.protobuf.message import Message
from python.example.implement_interface import implement_interface
from python.example.proto.system_pb2 import Drone, TakeOffCommand
from python.tests.utils import TestMedium


class ImplementInterfaceTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_receive_command_in_interface(self):
        received_command: Optional[Message] = None

        def handle_command(command: Message):
            nonlocal received_command
            received_command = command

        medium = TestMedium(lambda x: x)
        implementation = implement_interface(
            actor_type=Drone,
            interface="controller",
            medium=medium,
            handle_command=handle_command,
        )

        message = TakeOffCommand()
        message_bytes = message.SerializeToString()
        await medium.send(message_bytes)
        await sleep(0.1)
        self.assertIsNotNone(received_command, "should receive take off command")
        self.assertIsInstance(received_command, TakeOffCommand, "received command type should be TakeOffCommand")


if __name__ == '__main__':
    unittest.main()
