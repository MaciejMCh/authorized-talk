from typing import Tuple, List
from python.blockchain.account import Account
from python.blockchain.blockchain import Blockchain
from python.blockchain.smart_contract import SmartContract, load_abi
from python.blockchain.sol_sources import sol_named
from python.medium.kinds import TargetMedium, WebsocketTargetMedium
from python.websocket.location import Location
from eth_typing.evm import Address
from web3.exceptions import SolidityError


DEBUG = False


WebsocketLocation = Tuple[str, int]

Actor = Tuple[bytes, WebsocketLocation, bool]


class TransactionReverted(Exception):
    def __init__(self, error: str):
        self.error = error


class IdentityServerContract:
    def __init__(self, smart_contract: SmartContract):
        self.contract = smart_contract.w3Contract

    @classmethod
    def deploy(cls, blockchain: Blockchain, account: Account):
        smart_contract = SmartContract.deploy(
            blockchain=blockchain,
            account=account,
            sol_file_path=sol_named("IdentityServer"),
        )
        return IdentityServerContract(smart_contract)

    @classmethod
    def deployed(cls, blockchain: Blockchain, address: Address):
        smart_contract = SmartContract.deployed(
            blockchain=blockchain,
            address=address,
            abi=load_abi(sol_file_path=sol_named("AlwaysCompiles")),
        )
        return IdentityServerContract(smart_contract)

    def connect(
        self,
        account: Account,
        websocketLocation: Location,
        publicKey: bytes,
    ):
        try:
            debug_print(f"connect:\n\tpseudonym:\t\t{account.pseudonym}\n\tpublic key:\t\t{publicKey}")
            tx_hash = self.contract.functions.connect(
                publicKey,
                (websocketLocation.host, websocketLocation.port),
            ).transact({"from": account.address})
            self.contract.web3.eth.wait_for_transaction_receipt(tx_hash)
        except SolidityError:
            raise TransactionReverted("failed to read reason")

    def get_actor(self, pseudonym: str) -> Actor:
        return self.contract.functions.getActor(pseudonym).call()

    def assign_roles(
        self,
        account: Account,
        pseudonym: str,
        roles: List[str],
    ):
        try:
            tx_hash = self.contract.functions.assignRoles(
                pseudonym,
                roles,
            ).transact({"from": account.address})
            self.contract.web3.eth.wait_for_transaction_receipt(tx_hash)
        except SolidityError:
            raise TransactionReverted("failed to read reason")

    def add_to_whitelist(
        self,
        account: Account,
        pseudonym: str,
        interface: str,
        roles: List[str],
    ):
        try:
            tx_hash = self.contract.functions.addToWhitelist(
                pseudonym,
                interface,
                roles,
            ).transact({"from": account.address})
            self.contract.web3.eth.wait_for_transaction_receipt(tx_hash)
        except SolidityError:
            raise TransactionReverted("failed to read reason")

    def has_access(
        self,
        source_pseudonym: str,
        target_pseudonym: str,
        target_interface: str,
    ):
        return self.contract.functions.hasAccess(source_pseudonym, target_pseudonym, target_interface).call()


def debug_print(message: str):
    if DEBUG:
        print(f"contract: {message}")
