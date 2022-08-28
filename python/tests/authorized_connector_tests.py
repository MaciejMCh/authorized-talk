import unittest

from python.connector.authorized_connector import AuthorizedConnector
from python.core.interface_identity import InterfaceIdentity
from python.identity_server.identity_server import TargetNotFound
from python.medium.kinds import WebsocketSourceMedium
from python.tests.utils import TestIdentityServer, bob_public_key


class AuthorizedConnectorTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_unknown_target_access_attempt(self):
        try:
            medium = await AuthorizedConnector(
                identity_server=TestIdentityServer(
                    target_mediums_by_pseudonyms={'bob': []},
                    public_keys_by_pseudonyms={'bob': bob_public_key},
                ),
                available_source_mediums=[WebsocketSourceMedium()],
            ).establish_connection(
                interface_identity=InterfaceIdentity(pseudonym='alice', interface='some_interface'),
                on_message=lambda x: x,
            )
            self.assertIsNone(medium, 'should not resolve medium, but raise exception')
        except TargetNotFound as exception:
            self.assertIsNotNone(exception, 'should raise target not found exception')


if __name__ == '__main__':
    unittest.main()
