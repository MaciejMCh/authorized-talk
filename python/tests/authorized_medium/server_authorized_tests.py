import unittest
from asyncio import sleep

from blib2to3.pytree import Optional

from python.tests.authorized_medium.utils import with_authorized_server


class ServerAuthorizedTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_sending_message(self):
        medium, client, close = await with_authorized_server()

        received_message: Optional[bytes] = None

        def receive_message_as_client(message: bytes):
            nonlocal received_message
            received_message = message

        client.handle_message(receive_message_as_client)

        await medium.send(b"hi")
        await sleep(0.1)

        self.assertIsNotNone(received_message, "client should receive message from authorized server medium")
        self.assertEqual(b"hi", received_message, "message should be hi")

        await close()

    async def test_receiving_message(self):
        medium, client, close = await with_authorized_server()

        received_message: Optional[bytes] = None

        def receive_message_as_server(message: bytes):
            nonlocal received_message
            received_message = message

        medium.handle_message(receive_message_as_server)

        await client.send(b"hi")
        await sleep(0.1)

        self.assertIsNotNone(received_message, "server should receive message as authorized server medium")
        self.assertEqual(b"hi", received_message, "message should be hi")

        await close()


if __name__ == '__main__':
    unittest.main()
