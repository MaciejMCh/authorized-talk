import unittest

from python.blockchain.blockchain import Blockchain
from python.blockchain.identity_server_contract import IdentityServerContract
from python.medium.kinds import WebsocketTargetMedium
from python.tests.smart_contract.test_accounts import test_accounts
from python.websocket.location import Location


class GetMediumsTestCase(unittest.TestCase):
    def test_get_existing_actor(self):
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

        actor = contract.get_actor(pseudonym=accounts.alice.pseudonym)
        self.assertEqual(b"some_public_key", actor[0], "should retrieve proper public key")
        self.assertEqual("localhost", actor[1][0], "should retrieve proper websocket host")
        self.assertEqual(9876, actor[1][1], "should retrieve proper websocket port")
        self.assertTrue(actor[2], "should appear as connected")

    def test_get_non_existing_actor(self):
        blockchain = Blockchain.local()
        accounts = test_accounts(blockchain)

        contract = IdentityServerContract.deploy(
            blockchain=Blockchain.local(),
            account=accounts.admin,
        )

        actor = contract.get_actor(pseudonym=accounts.alice.pseudonym)
        self.assertFalse(actor[2], "should appear as not connected")


if __name__ == '__main__':
    unittest.main()
