from typing import Union, Type, Tuple
from solcx import compile_source
from web3 import Web3
from web3.contract import Contract


class SmartContract:
    def echo(self, message: str):
        raise Exception('dont use this base class')

    def requestConnection(self, targetPseudonym: str, interface: str):
        raise Exception('dont use this base class')

    def registerTalker(self, pseudonym: str, sslUrl: str):
        raise Exception('dont use this base class')

    def debug(self, val: int):
        raise Exception('dont use this base class')

    def debug2(self):
        raise Exception('dont use this base class')


class SolSmartContract(SmartContract):
    def __init__(self, w3: Web3, w3Contract: Union[Type[Contract], Contract]):
        self.w3 = w3
        self.w3Contract = w3Contract

    @classmethod
    def compileAndPublish(cls, w3: Web3, solFilePath: str):
        return SolSmartContract(w3=w3, w3Contract=compileAndPublish(w3, solFilePath))

    def waitForTransaction(self, call):
        txHash = call.transact()
        txReceipt = self.w3.eth.wait_for_transaction_receipt(txHash)

    def echo(self, message: str):
        return self.w3Contract.functions.echo(message).call()

    def requestConnection(self, targetPseudonym: str, interface: str):
        return self.w3Contract.functions.requestConnection(targetPseudonym, interface).call()

    def registerTalker(self, pseudonym: str, sslUrl: str):
        return self.waitForTransaction(self.w3Contract.functions.registerTalker(pseudonym, [sslUrl]))

    def debug(self, val: int):
        return self.waitForTransaction(self.w3Contract.functions.debug(val))

    def debug2(self):
        return self.w3Contract.functions.debug2().call()


def compileAndPublish(w3: Web3, solFilePath: str):
    file = open(solFilePath, 'r')
    source = file.read()
    compiledSol = compile_source(source, output_values=['abi', 'bin'])
    contractId, contractInterface = compiledSol.popitem()
    bytecode = contractInterface['bin']
    abi = contractInterface['abi']
    w3.eth.default_account = w3.eth.accounts[0]
    ContractType = w3.eth.contract(abi=abi, bytecode=bytecode)
    txHash = ContractType.constructor().transact()
    txReceipt = w3.eth.wait_for_transaction_receipt(txHash)
    contract = w3.eth.contract(address=txReceipt.contractAddress, abi=abi)
    return contract
