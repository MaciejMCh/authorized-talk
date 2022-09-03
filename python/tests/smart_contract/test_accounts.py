from python.blockchain.account import Account
from python.blockchain.blockchain import Blockchain


class TestAccounts:
    def __init__(self, admin: Account, alice: Account, bob: Account, eve: Account):
        self.admin = admin
        self.alice = alice
        self.bob = bob
        self.eve = eve


def test_accounts(blockchain: Blockchain):
    w3 = blockchain.w3
    return TestAccounts(
        admin=Account(w3.eth.accounts[0]),
        alice=Account(w3.eth.accounts[1]),
        bob=Account(w3.eth.accounts[2]),
        eve=Account(w3.eth.accounts[3]),
    )
