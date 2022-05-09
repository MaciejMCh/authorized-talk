from web3 import Web3

from smartContract import SmartContract, SolSmartContract


class Blockchain:
    def __init__(self, blockchainProviderUrl):
        provider = Web3.HTTPProvider(blockchainProviderUrl)
        self.w3 = Web3(provider)
        if not self.w3.isConnected():
            raise Exception('failed to connect to blockchain')

    def compileAndPublishSmartContract(self, solFilePath: str) -> SmartContract:
        return SolSmartContract.compileAndPublish(self.w3, solFilePath)
