import os
from python.blockchain import Blockchain
from python.encryption.unsafeEncryption import UnsafeEncryption
from python.meTalker import MeTalker
from python.medium.sslMedium import SslMedium
from python.talker.talkerIdentity import TalkerIdentity


def makeGanacheBlockchain():
    return Blockchain('http://127.0.0.1:8545')


def smartContractSolFilePath():
    path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'solidity', 'AuthorizedTalk.sol'))
    return path


class TestSuite:
    def __init__(self):
        self.blockchain = makeGanacheBlockchain()
        self.smartContract = self.blockchain.compileAndPublishSmartContract(smartContractSolFilePath())
        self.anna = MeTalker(
            talkerIdentity=TalkerIdentity('anna'),
            encryption=UnsafeEncryption(),
            sslMedium=SslMedium.local(8771),
            smartContract=self.smartContract,
        )
        self.bob = MeTalker(
            talkerIdentity=TalkerIdentity('bob'),
            encryption=UnsafeEncryption(),
            sslMedium=SslMedium.local(8772),
            smartContract=self.smartContract,
        )
