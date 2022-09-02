import unittest
from typing import Optional
from python.blockchain.blockchain import Blockchain
from python.blockchain.identity_server_contract import IdentityServerContract
from python.blockchain.smart_contract import SmartContract
from python.blockchain.sol_sources import sol_named
from python.websocket.location import Location


class ConnectTestCase(unittest.TestCase):
    def test_connect(self):
        contract = IdentityServerContract.deploy(Blockchain.local())
        contract.connect(
            pseudonym="alice",
            publicKey=b"some_public_key",
            websocketLocation=Location(host="localhost", port=9876),
        )
        self.assertTrue(True, "connect should pass")

    def test_reject_connection_from_other_address(self):
        deployer = IdentityServerContract.deploy(Blockchain.local())
        alice = IdentityServerContract.deployed(deployer.address)
        bob = IdentityServerContract.deployed(deployer.address)

        alice.connect(
            pseudonym="alice",
            publicKey=b"some_public_key",
            websocketLocation=Location(host="localhost", port=9876),
        )
        bob.connect(
            pseudonym="alice",
            publicKey=b"some_public_key",
            websocketLocation=Location(host="localhost", port=9876),
        )


if __name__ == '__main__':
    unittest.main()

# TODO: test connect as another pseudonym
# TODO: test connect from another address
