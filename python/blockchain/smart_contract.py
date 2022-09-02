from typing import Dict, List

from solcx import compile_source
from web3.contract import Contract
from python.blockchain.blockchain import Blockchain
from eth_typing.evm import Address

Abi = List[Dict]


class SmartContract:
    def __init__(self, w3Contract: Contract, address: Address, abi: Abi):
        self.w3Contract = w3Contract
        self.address = address
        self.abi = abi

    @classmethod
    def deployed(
        cls,
        blockchain: Blockchain,
        address: Address,
        abi: Abi,
    ):
        contract = blockchain.w3.eth.contract(address=address, abi=abi)
        return SmartContract(w3Contract=contract, address=address, abi=abi)

    @classmethod
    def deploy(
            cls,
            blockchain: Blockchain,
            sol_file_path: str,
    ):
        w3 = blockchain.w3
        file = open(sol_file_path, 'r')
        source = file.read()
        file.close()
        compiled_sol = compile_source(source, output_values=['abi', 'bin'])
        contract_id, contract_interface = compiled_sol.popitem()
        bytecode = contract_interface['bin']
        abi = contract_interface['abi']
        w3.eth.default_account = w3.eth.accounts[0]
        ContractType = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = ContractType.constructor().transact()
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return cls.deployed(
            blockchain=blockchain,
            address=tx_receipt.contractAddress,
            abi=abi,
        )


def load_abi(sol_file_path: str) -> Abi:
    file = open(sol_file_path, 'r')
    source = file.read()
    file.close()
    compiled_sol = compile_source(source, output_values=['abi'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']
    return abi
