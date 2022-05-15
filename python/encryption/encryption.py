import rsa
from rsa import PublicKey


class Encryption:
    def getPublicKey(self) -> str:
        raise Exception('dont use this base class')

    def codeWithPublicKey(self, raw: str) -> str:
        raise Exception('dont use this base class')

    def encodeWithPrivateKey(self, raw: str) -> str:
        raise Exception('dont use this base class')

    def signWithPrivateKey(self, raw: str) -> str:
        raise Exception('dont use this base class')

    def verifyWithPublicKey(self, raw: str, expected: str) -> bool:
        raise Exception('dont use this base class')
