import unittest
from typing import cast

from python.blockchain.blockchain import Blockchain
from python.blockchain.identity_server_contract import IdentityServerContract
from python.identity_server.blockchain_identity_server import BlockchainIdentityServer
from python.medium.kinds import WebsocketTargetMedium
from python.tests.smart_contract.test_accounts import test_accounts
from python.websocket.location import Location


class GetPublicKeyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_get_public_key_for_existing_actor(self):
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

        public_key = await server.get_public_key(accounts.alice.pseudonym)
        self.assertEqual(b"some_public_key", public_key, "should get registered actors public key")

    async def test_get_public_key_for_non_existing_actor(self):
        blockchain = Blockchain.local()
        accounts = test_accounts(blockchain)

        contract = IdentityServerContract.deploy(
            blockchain=Blockchain.local(),
            account=accounts.admin,
        )

        server = BlockchainIdentityServer(contract)

        public_key = await server.get_public_key(accounts.alice.pseudonym)
        self.assertIsNone(public_key, "should not get public key for unknown actor")


if __name__ == '__main__':
    unittest.main()
