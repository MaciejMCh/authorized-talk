import time
import unittest
from typing import Optional
from python.medium.websocketMedium import WebsocketMedium, WebsocketServer


class WebsocketMediumTestCase(unittest.TestCase):
    def testClosingServer(self):
        server = WebsocketServer(host='localhost', port=8765)
        # medium = WebsocketMedium(otherHost='localhost', otherPort=8765)
        server.close()

    def testSendAsClient(self):
        receivedMessage: Optional[bytes] = None
        server = WebsocketServer(host='localhost', port=8765)
        medium = WebsocketMedium(otherHost='localhost', otherPort=8765)

        def handleMessage(message: bytes):
            nonlocal receivedMessage
            receivedMessage = message

        # server.sessions[0].onMessage = handleMessage
        time.sleep(2)
        medium.send(b'hi')
        time.sleep(2)
        server.close()
        self.assertEqual(receivedMessage, b'hi')


if __name__ == '__main__':
    unittest.main()
