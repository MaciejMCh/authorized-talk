import unittest

from python.blockchain.blockchain import Blockchain
from python.blockchain.identity_server_contract import IdentityServerContract
from python.blockchain.smart_contract import SmartContract
from python.core.rsa_keys import RsaKeys
from python.encryption.rsa_encryption import RsaEncryption
from python.identity_server.blockchain_identity_server import BlockchainIdentityServer
from python.tests.smart_contract.test_accounts import TestAccounts, test_accounts
from python.websocket.location import Location


class BlockchainSigningTestCase(unittest.IsolatedAsyncioTestCase):
    def test_in_memory_signing(self):
        alice_keys = RsaKeys.generate()

        signature = RsaEncryption.sign(
            message=b"hi",
            private_key=alice_keys.private_key,
        )

        is_verified = RsaEncryption.verify(
            message=b"hi",
            signature=signature,
            public_key=alice_keys.public_key,
        )

        self.assertTrue(is_verified, "should be verified")

    async def test_blockchain_signing(self):
        blockchain = Blockchain.local()
        accounts = test_accounts(blockchain)
        identity_server_contract = IdentityServerContract.deploy(
            blockchain=blockchain,
            account=accounts.admin,
        )
        identity_server = BlockchainIdentityServer(identity_server_contract)

        alice_keys = RsaKeys.generate()
        identity_server_contract.connect(
            account=accounts.alice,
            websocketLocation=Location(host="", port=0),
            publicKey=alice_keys.public_key,
        )

        signature = RsaEncryption.sign(
            message=b"hi",
            private_key=alice_keys.private_key,
        )
        public_key = await identity_server.get_public_key(accounts.alice.pseudonym)
        is_verified = RsaEncryption.verify(
            message=b"hi",
            signature=signature,
            public_key=public_key,
        )
        self.assertTrue(is_verified, "should be verified")


if __name__ == '__main__':
    unittest.main()
