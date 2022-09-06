import unittest
from asyncio import sleep

from python.blockchain.blockchain import Blockchain
from python.blockchain.identity_server_contract import IdentityServerContract
from python.core.interface_identity import InterfaceIdentity
from python.example.drone_simulation import DroneSimulation
from python.example.drone_simulation_controller import TakeOff
from python.example.operator import Operator
from python.tests.smart_contract.test_accounts import test_accounts
from python.websocket.location import Location


class DroneSimulationTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_command(self):
        blockchain = Blockchain.local()
        accounts = test_accounts(blockchain)
        identity_server_contract = IdentityServerContract.deploy(
            blockchain=blockchain,
            account=accounts.admin,
        )

        identity_server_contract.assign_roles(
            account=accounts.admin,
            pseudonym=accounts.alice.pseudonym,
            roles=["operator"]
        )

        identity_server_contract.add_to_whitelist(
            account=accounts.admin,
            pseudonym=accounts.bob.pseudonym,
            interface="controller",
            roles=["operator"],
        )

        drone_simulation = DroneSimulation(
            account=accounts.bob,
            websocket_location=Location(host="localhost", port=9876),
            identity_server_contract=identity_server_contract,
        )

        await sleep(1)

        operator = Operator(
            account=accounts.alice,
            target=InterfaceIdentity(
                pseudonym=accounts.bob.pseudonym,
                interface="controller",
            ),
            identity_server_contract=identity_server_contract,
        )

        await sleep(1)

        await operator.verify_drone()

        self.assertIsInstance(drone_simulation.drone_simulation_controller.command, TakeOff, "command should be take of")


if __name__ == '__main__':
    unittest.main()
