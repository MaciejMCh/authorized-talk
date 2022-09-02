import unittest

from python.blockchain.blockchain import Blockchain
from python.blockchain.smart_contract import SmartContract, load_abi
from python.blockchain.sol_sources import sol_named


class BlockchainTestCase(unittest.TestCase):
    def test_connect_to_local_blockchain(self):
        try:
            _ = Blockchain.local()
            self.assertTrue(True, "should connect to blockchain")
        except Exception as exc:
            self.assertTrue(False, f"failed to connect {exc}")

    def test_deploy_smart_contract(self):
        blockchain = Blockchain.local()
        smart_contract = SmartContract.deploy(blockchain=blockchain, sol_file_path=sol_named("AlwaysCompiles"))
        self.assertIsNotNone(smart_contract.w3Contract, "should deploy smart contract")

    def test_get_deployed_smart_contract(self):
        blockchain = Blockchain.local()
        deployed = SmartContract.deploy(
            blockchain=blockchain,
            sol_file_path=sol_named("AlwaysCompiles"),
        )
        got = SmartContract.deployed(
            blockchain=blockchain,
            address=deployed.address,
            abi=deployed.abi,
        )

        self.assertIsNotNone(got.w3Contract, "should get deployed smart contract")

    def test_get_abi(self):
        blockchain = Blockchain.local()
        deployed = SmartContract.deploy(
            blockchain=blockchain,
            sol_file_path=sol_named("AlwaysCompiles"),
        )
        got = SmartContract.deployed(
            blockchain=blockchain,
            address=deployed.address,
            abi=load_abi(sol_file_path=sol_named("AlwaysCompiles")),
        )

        self.assertIsNotNone(got.w3Contract, "should get deployed smart contract")


if __name__ == '__main__':
    unittest.main()
