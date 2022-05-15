import asyncio
import time
import unittest
from medium.sslMedium import SslMedium


class SslMediumTestCase(unittest.TestCase):
    def testSendMessageAsClient(self):
        result = ''
        anna = SslMedium.local(8765)
        bob = SslMedium.local(8766)
        time.sleep(1.2)

        annaSession = anna.connectTo(bob.url())

        def handleIncomingMessageAsBob(message: str):
            nonlocal result
            result = message

        time.sleep(1.2)
        bob.incomingSessions[0].onMessage(handleIncomingMessageAsBob)
        annaSession.send('hello')
        time.sleep(.2)

        self.assertEqual('hello', result)
        annaSession.close()

    def testSendMessageAsServer(self):
        result = ''
        anna = SslMedium.local(8765)
        bob = SslMedium.local(8766)
        time.sleep(1.2)

        annaSession = anna.connectTo(bob.url())

        def handleIncomingMessageAsAnna(message: str):
            nonlocal result
            result = message

        time.sleep(1.2)
        annaSession.onMessage(handleIncomingMessageAsAnna)
        bob.incomingSessions[0].send('hello')
        time.sleep(.2)

        self.assertEqual('hello', result)
        annaSession.close()


if __name__ == '__main__':
    unittest.main()
