from web3 import Web3


class Blockchain:
    def __init__(self, blockchainProviderUrl):
        provider = Web3.HTTPProvider(blockchainProviderUrl)
        self.w3 = Web3(provider)
        if not self.w3.isConnected():
            raise Exception('failed to connect to blockchain')

    @classmethod
    def local(cls):
        return Blockchain('http://127.0.0.1:8545')
