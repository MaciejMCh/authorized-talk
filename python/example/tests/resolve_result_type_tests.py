import unittest

from python.example.proto.system_pb2 import TakeOff
from python.example.resolve_result_type import resolve_result_type


class ResolveResultTypeTestCase(unittest.TestCase):
    def test_take_off(self):
        takeOff = TakeOff()
        ResultType = resolve_result_type(takeOff)
        self.assertEqual(TakeOff.Result, ResultType)


if __name__ == '__main__':
    unittest.main()
