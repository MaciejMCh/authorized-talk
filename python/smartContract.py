from typing import Union, Type
from solcx import compile_source
from web3 import Web3
from web3.contract import Contract


class SmartContract:
    def echo(self, message: str):
        raise Exception('dont use this base class')


class SolSmartContract(SmartContract):
    def __init__(self, w3Contract: Union[Type[Contract], Contract]):
        self.w3Contract = w3Contract

    @classmethod
    def compileAndPublish(cls, w3: Web3, solFilePath: str):
        return SolSmartContract(compileAndPublish(w3, solFilePath))

    def echo(self, message: str):
        return self.w3Contract.functions.echo(message).call()


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
