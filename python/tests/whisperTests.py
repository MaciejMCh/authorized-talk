import time
import unittest

from talker.talkerInterfaceIdentity import TalkerInterfaceIdentity
from tests.testSuite import TestSuite
from whisper.whisperingMouth import WhisperingMouth


class WhisperTestCase(unittest.TestCase):
    def testSendWhisper(self):
        result = ""
        testSuite = TestSuite()

        def handleWhisperReceive(message: str):
            nonlocal result
            result = message

        WhisperingMouth(
            meTalker=testSuite.anna,
            target=testSuite.bob.talkerIdentity,
            targetInterface=TalkerInterfaceIdentity('hello'),
        )

        time.sleep(2)

        self.assertEqual(result, "Hello", "Should be Hello")


if __name__ == '__main__':
    unittest.main()
