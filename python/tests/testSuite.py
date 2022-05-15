import os
from blockchain import Blockchain
from encryption.unsafeEncryption import UnsafeEncryption
from meTalker import MeTalker
from medium.sslMedium import SslMedium
from talker.talkerIdentity import TalkerIdentity


def makeGanacheBlockchain():
    return Blockchain('http://127.0.0.1:7545')


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
            sslMedium=SslMedium.local(8765),
            smartContract=self.smartContract,
        )
        self.bob = MeTalker(
            talkerIdentity=TalkerIdentity('bob'),
            encryption=UnsafeEncryption(),
            sslMedium=SslMedium.local(8766),
            smartContract=self.smartContract,
        )
