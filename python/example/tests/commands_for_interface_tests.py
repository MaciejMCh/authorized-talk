import unittest

from python.example.commands_for_interface import commands_for_interface
from python.example.proto.system_pb2 import Drone


class CommandsForInterfaceTestCase(unittest.TestCase):
    def test_commands_for_interface(self):
        self.assertEqual(['takeOff'], commands_for_interface(actor_type=Drone, interface="controller"))
        self.assertEqual(['readTelemetry'], commands_for_interface(actor_type=Drone, interface="telemetry"))


if __name__ == '__main__':
    unittest.main()
