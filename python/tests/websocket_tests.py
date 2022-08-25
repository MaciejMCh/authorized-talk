import unittest
from asyncio import gather

from python.websocket.location import Location
from python.websocket.server import run as run_server
from python.websocket.client import run as run_client


class WebsocketsTestCase(unittest.TestCase):
    async def test_open_and_close_server(self):
        location = Location(host='localhost', port=8765)
        server, server_running_task = await run_server(location=location)
        server.close()
        await server_running_task
        self.assertTrue(True)

    async def test_close_server_with_session(self):
        location = Location(host='localhost', port=8765)
        server, server_running_task = await run_server(location=location)
        client, client_running_task = await run_client(location=location)
        server.close()
        await gather(server_running_task, client_running_task)
        self.assertTrue(True)

    async def test_close_client(self):
        location = Location(host='localhost', port=8765)
        server, server_running_task = await run_server(location=location)
        client, client_running_task = await run_client(location=location)
        await client.close()
        await client_running_task
        self.assertTrue(True)
        server.close()
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()
