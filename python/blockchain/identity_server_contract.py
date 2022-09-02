from python.blockchain.blockchain import Blockchain
from python.blockchain.smart_contract import SmartContract
from python.blockchain.sol_sources import sol_named
from python.websocket.location import Location


class IdentityServerContract:
    def __init__(self, smart_contract: SmartContract):
        self.contract = smart_contract.w3Contract

    @classmethod
    def deploy(cls, blockchain: Blockchain):
        smart_contract = SmartContract.deploy(
            blockchain=blockchain,
            sol_file_path=sol_named("IdentityServer"),
        )
        return IdentityServerContract(smart_contract)

    def connect(
        self,
        pseudonym: str,
        websocketLocation: Location,
        publicKey: bytes,
    ):
        tx_hash = self.contract.functions.connect(
            pseudonym,
            publicKey,
            (websocketLocation.host, websocketLocation.port),
        ).transact()
        self.contract.web3.eth.wait_for_transaction_receipt(tx_hash)
