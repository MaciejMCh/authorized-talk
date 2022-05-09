import os
from blockchain import Blockchain
from meTalker import MeTalker
from medium.sslMedium import SslMedium


def makeGanacheBlockchain():
    return Blockchain('http://127.0.0.1:7545')


def smartContractSolFilePath():
    return os.path.join('..', '..', 'solidity', 'AuthorizedTalk.sol')


class TestSuite:
    def __init__(self):
        self.blockchain = makeGanacheBlockchain()
        self.smartContract = self.blockchain.compileAndPublishSmartContract(smartContractSolFilePath())
        self.anna = MeTalker(SslMedium.local('9991'))
        self.bob = MeTalker(SslMedium.local('9992'))
