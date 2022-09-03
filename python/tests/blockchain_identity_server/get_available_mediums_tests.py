import unittest
from typing import cast

from python.blockchain.blockchain import Blockchain
from python.blockchain.identity_server_contract import IdentityServerContract
from python.identity_server.blockchain_identity_server import BlockchainIdentityServer
from python.medium.kinds import WebsocketTargetMedium
from python.tests.smart_contract.test_accounts import test_accounts
from python.websocket.location import Location


class GetAvailableMediumsTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_get_mediums_for_existing_actor(self):
        blockchain = Blockchain.local()
        accounts = test_accounts(blockchain)

        contract = IdentityServerContract.deploy(
            blockchain=Blockchain.local(),
            account=accounts.admin,
        )

        contract.connect(
            account=accounts.alice,
            publicKey=b"some_public_key",
            websocketLocation=Location(host="localhost", port=9876),
        )

        server = BlockchainIdentityServer(contract)

        mediums = await server.get_available_mediums(accounts.alice.pseudonym)
        self.assertEqual(1, len(mediums), "should get only one medium")
        self.assertIsInstance(mediums[0], WebsocketTargetMedium, "the one medium should be websocket")
        websocket_medium = cast(WebsocketTargetMedium, mediums[0])
        self.assertEqual("localhost", websocket_medium.location.host, "host should match")
        self.assertEqual(9876, websocket_medium.location.port, "port should match")

    async def test_get_mediums_for_non_existing_actor(self):
        blockchain = Blockchain.local()
        accounts = test_accounts(blockchain)

        contract = IdentityServerContract.deploy(
            blockchain=Blockchain.local(),
            account=accounts.admin,
        )

        server = BlockchainIdentityServer(contract)

        mediums = await server.get_available_mediums(accounts.alice.pseudonym)
        self.assertEqual(0, len(mediums), "should get no mediums")


if __name__ == '__main__':
    unittest.main()
