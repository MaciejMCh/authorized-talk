import unittest

from python.example.implement_actor import implement_actor
from python.example.proto.system_pb2 import Drone


class ImplementActorsTestCase(unittest.TestCase):
    def test_implement_drone(self):
        actor = implement_actor(
            message_type=Drone,
            receive_command=None,
        )


if __name__ == '__main__':
    unittest.main()
