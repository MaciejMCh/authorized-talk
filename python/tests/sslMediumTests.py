import time
import unittest
from python.medium.sslMedium import SslMedium


class SslMediumTestCase(unittest.TestCase):
    def testSendMessageAsClient(self):
        result = b''
        anna = SslMedium.local(8765)
        bob = SslMedium.local(8766)

        annaSession = anna.connectTo(bob.url())

        def handleIncomingMessageAsBob(message: str):
            nonlocal result
            result = message

        bob.incomingSessions[0].onMessage(handleIncomingMessageAsBob)
        annaSession.send(b'hello')
        time.sleep(0.3)

        self.assertEqual(b'hello', result)
        annaSession.close()
        bob.incomingSessions[0].close()

    def testSendMessageAsServer(self):
        result = ''
        anna = SslMedium.local(8768)
        bob = SslMedium.local(8769)
        time.sleep(1.2)

        annaSession = anna.connectTo(bob.url())

        def handleIncomingMessageAsAnna(message: str):
            nonlocal result
            result = message

        time.sleep(1.2)
        annaSession.onMessage(handleIncomingMessageAsAnna)
        bob.incomingSessions[0].send(b'hello')
        time.sleep(.2)

        self.assertEqual(b'hello', result)
        annaSession.close()


if __name__ == '__main__':
    unittest.main()
