import unittest

from python.example.one_of_all_commands import one_of_all_commands
from python.example.proto.system_pb2 import Drone, TakeOff, ReadTelemetry


class OneOfAllCommandsTestCase(unittest.TestCase):
    def test_drone(self):
        OneOfAllCommands = one_of_all_commands(Drone)
        self.assertEqual(
            "takeOff",
            OneOfAllCommands(takeOff=TakeOff(), nonce=2).WhichOneof("command"),
            "one of should point to takeOff",
        )
        self.assertEqual(
            "readTelemetry",
            OneOfAllCommands(readTelemetry=ReadTelemetry(), nonce=3).WhichOneof("command"),
            "one of should point to readTelemetry",
        )


if __name__ == '__main__':
    unittest.main()
