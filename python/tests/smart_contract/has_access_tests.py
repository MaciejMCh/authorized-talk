import unittest

from python.blockchain.blockchain import Blockchain
from python.blockchain.identity_server_contract import IdentityServerContract
from python.tests.smart_contract.test_accounts import test_accounts
from python.websocket.location import Location


class HasAccessTestCase(unittest.TestCase):
    def test_has_access(self):
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

        contract.connect(
            account=accounts.bob,
            publicKey=b"some_public_key",
            websocketLocation=Location(host="localhost", port=9876),
        )

        contract.assign_roles(
            account=accounts.admin,
            pseudonym=accounts.alice.pseudonym,
            roles=["bob_reader"],
        )

        contract.add_to_whitelist(
            account=accounts.admin,
            pseudonym=accounts.bob.pseudonym,
            interface="read_data",
            roles=["bob_reader"],
        )

        has_access = contract.has_access(
            source_pseudonym=accounts.alice.pseudonym,
            target_pseudonym=accounts.bob.pseudonym,
            target_interface="read_data",
        )

        self.assertTrue(has_access, "should have access with this configuration")

    def test_no_access_for_empty_whitelist(self):
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

        contract.connect(
            account=accounts.bob,
            publicKey=b"some_public_key",
            websocketLocation=Location(host="localhost", port=9876),
        )

        contract.assign_roles(
            account=accounts.admin,
            pseudonym=accounts.alice.pseudonym,
            roles=["bob_reader"],
        )

        has_access = contract.has_access(
            source_pseudonym=accounts.alice.pseudonym,
            target_pseudonym=accounts.bob.pseudonym,
            target_interface="read_data",
        )

        self.assertFalse(has_access, "should not have access, because target whitelist is empty")

    def test_no_sufficient_role(self):
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

        contract.connect(
            account=accounts.bob,
            publicKey=b"some_public_key",
            websocketLocation=Location(host="localhost", port=9876),
        )

        contract.add_to_whitelist(
            account=accounts.admin,
            pseudonym=accounts.bob.pseudonym,
            interface="read_data",
            roles=["bob_reader"],
        )

        has_access = contract.has_access(
            source_pseudonym=accounts.alice.pseudonym,
            target_pseudonym=accounts.bob.pseudonym,
            target_interface="read_data",
        )

        self.assertFalse(has_access, "should not have access, because has not sufficient role")


if __name__ == '__main__':
    unittest.main()
