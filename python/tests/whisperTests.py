import unittest

from tests.testSuite import TestSuite
from whisper import Whisper


class MyTestCase(unittest.TestCase):
    def testSendWhisper(self):
        result = ""
        testSuite = TestSuite()

        def handleWhisperReceive(message: str):
            nonlocal result
            result = message

        testSuite.bob.medium.onWhisper(handleWhisperReceive)
        bobsMedium = testSuite.anna.requestMedium(testSuite.bob.identity, 'hello')
        sendWhisper(testSuite.anna.meTalker.medium, Whisper('Hello'), bobsMedium)

        self.assertEqual(result, "Hello", "Should be Hello")


if __name__ == '__main__':
    unittest.main()
