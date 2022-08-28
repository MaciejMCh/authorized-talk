import unittest

from python.core.interface_identity import InterfaceIdentity
from python.medium.compromise_connector import CompromiseConnector, FailedToResolveMedium
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.websocket.location import Location
from python.websocket.server import run_server


class CompromiseConnectorTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_compromise_not_found_when_none_sources(self):
        connector = CompromiseConnector(
            sources=[],
            targets=[WebsocketTargetMedium(location=Location(host='localhost', port=8765))],
        )
        try:
            medium = await connector.establish_connection(
                interface_identity=InterfaceIdentity(
                    pseudonym='test',
                    interface='test',
                ),
                on_message=lambda x: x,
            )
            self.assertIsNone(medium)
        except FailedToResolveMedium as exception:
            self.assertIsNotNone(exception)

    async def test_compromise_not_found_when_none_targets(self):
        connector = CompromiseConnector(
            sources=[WebsocketSourceMedium()],
            targets=[],
        )
        try:
            medium = await connector.establish_connection(
                interface_identity=InterfaceIdentity(
                    pseudonym='test',
                    interface='test',
                ),
                on_message=lambda x: x,
            )
            self.assertIsNone(medium)
        except FailedToResolveMedium as exception:
            self.assertIsNotNone(exception)

    async def test_websocket_compromise(self):
        location = Location(host='localhost', port=8765)
        server, server_close_task = await run_server(location)

        connector = CompromiseConnector(
            sources=[WebsocketSourceMedium()],
            targets=[WebsocketTargetMedium(location=location)],
        )
        medium = await connector.establish_connection(
            interface_identity=InterfaceIdentity(
                pseudonym='test',
                interface='test',
            ),
            on_message=lambda x: x,
        )
        self.assertIsNotNone(medium)
        server.close()
        await server_close_task


if __name__ == '__main__':
    unittest.main()
