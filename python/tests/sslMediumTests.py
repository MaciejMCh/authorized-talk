import asyncio
import unittest
from unittest import IsolatedAsyncioTestCase
from medium.sslMedium import SslMedium


class SslMediumTestCase(IsolatedAsyncioTestCase):
    async def testSendMessage(self):
        result = ''
        anna = SslMedium.local(8765)
        bob = SslMedium.local(8766)
        asyncio.create_task(anna.openIncomingConnections())
        asyncio.create_task(bob.openIncomingConnections())
        await asyncio.sleep(2)
        annasSession = await anna.connectTo(bob.url())

        def handleIncomingMessageAsBob(message: str):
            nonlocal result
            result = message

        await asyncio.sleep(1)
        bob.incomingSessions[0].onMessage(handleIncomingMessageAsBob)
        await annasSession.send('hello')
        await asyncio.sleep(2)

        self.assertEqual('hello', result)


if __name__ == '__main__':
    unittest.main()
