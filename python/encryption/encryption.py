import rsa
from rsa import PublicKey


class Encryption:
    def getPublicKey(self) -> str:
        raise Exception('dont use this base class')

    def codeWithPublicKey(self, raw: str) -> str:
        raise Exception('dont use this base class')

    def codeBytesWithOtherPublicKey(self, raw: bytes, publicKeyString: str) -> bytes:
        raise Exception('dont use this base class')

    def codeWithOtherPublicKey(self, raw: str, publicKeyString: str) -> str:
        raise Exception('dont use this base class')

    def encodeWithPrivateKey(self, raw: str) -> str:
        raise Exception('dont use this base class')

    def encodeBytesWithPrivateKey(self, raw: bytes) -> str:
        raise Exception('dont use this base class')

    def signWithPrivateKey(self, raw: str) -> str:
        raise Exception('dont use this base class')

    def verifyWithPublicKey(self, raw: str, expected: str) -> bool:
        raise Exception('dont use this base class')

    def verifyWithOtherPublicKey(self, raw, expected: str, publicKeyString: str):
        raise Exception('dont use this base class')
