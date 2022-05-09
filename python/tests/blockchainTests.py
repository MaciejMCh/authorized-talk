import unittest
from tests.testSuite import makeGanacheBlockchain, smartContractSolFilePath


class BlockchainTestCase(unittest.TestCase):
    def testConnectToGanacheBlockchain(self):
        try:
            _ = makeGanacheBlockchain()
            self.assertTrue(True, 'did connect')
        except Exception as exc:
            self.assertTrue(False, f'failed to connect {exc}')

    def testCompileAndPublishSmartContract(self):
        try:
            blockchain = makeGanacheBlockchain()
            _ = blockchain.compileAndPublishSmartContract(smartContractSolFilePath())
            self.assertTrue(True, 'did compile')
        except Exception as exc:
            self.assertTrue(False, f'failed to compile {exc}')


if __name__ == '__main__':
    unittest.main()
