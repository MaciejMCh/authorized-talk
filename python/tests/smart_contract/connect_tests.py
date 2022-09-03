import unittest
from python.blockchain.blockchain import Blockchain
from python.blockchain.identity_server_contract import IdentityServerContract
from python.tests.smart_contract.test_accounts import test_accounts
from python.websocket.location import Location


class ConnectTestCase(unittest.TestCase):
    def test_connect(self):
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
        self.assertTrue(True, "connect should pass")


if __name__ == '__main__':
    unittest.main()

# TODO: test connect as another pseudonym
# TODO: test connect from another address
