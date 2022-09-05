import unittest

from python.blockchain.blockchain import Blockchain
from python.blockchain.identity_server_contract import IdentityServerContract
from python.example.drone_simulation import DroneSimulation
from python.tests.smart_contract.test_accounts import test_accounts
from python.websocket.location import Location


class DroneSimulationTestCase(unittest.TestCase):
    def test_command(self):
        blockchain = Blockchain.local()
        accounts = test_accounts(blockchain)
        identity_server_contract = IdentityServerContract.deploy(
            blockchain=blockchain,
            account=accounts.admin,
        )

        drone_simulation = DroneSimulation(
            identity_server_contract=identity_server_contract,
            websocket_location=Location(host="localhost", port=9876),
            account=accounts.bob,
        )

        # operator = Operator(
        #     identity_server_contract=identity_server_contract,
        #     account=accounts.alice,
        # )


if __name__ == '__main__':
    unittest.main()
