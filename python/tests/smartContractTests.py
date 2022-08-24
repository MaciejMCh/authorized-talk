import unittest

from python.tests.testSuite import makeGanacheBlockchain, smartContractSolFilePath


class SmartContractTestCase(unittest.TestCase):
    def testEcho(self):
        blockchain = makeGanacheBlockchain()
        smartContract = blockchain.compileAndPublishSmartContract(smartContractSolFilePath())
        echoResponse = smartContract.echo('hi :)')
        self.assertEqual(echoResponse, 'hi :)')


if __name__ == '__main__':
    unittest.main()
