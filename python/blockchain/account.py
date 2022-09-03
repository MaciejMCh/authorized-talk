from eth_typing.evm import Address


class Account:
    def __init__(self, address: Address):
        self.address = address
        self.pseudonym = str(address)
