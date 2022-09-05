import unittest

from python.example.compose_command import compose_command
from python.example.proto.system_pb2 import Drone, TakeOff


class ComposeCommandTestCase(unittest.TestCase):
    def test_drone(self):
        command = compose_command(
            actor_type=Drone,
            message=TakeOff(),
            nonce=11,
        )
        self.assertEqual("takeOff", command.WhichOneof("command"))


if __name__ == '__main__':
    unittest.main()
