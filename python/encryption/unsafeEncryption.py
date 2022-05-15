import rsa
from rsa import PublicKey

from encryption.encryption import Encryption


class UnsafeEncryption(Encryption):
    def __init__(self):
        (self.publicKey, self.privateKey) = rsa.newkeys(512)

    def getPublicKey(self) -> str:
        publicKey = PublicKey.save_pkcs1(self.publicKey, format='PEM')
        return 'asd'

    def codeWithPublicKey(self, raw: str) -> str:
        codedBytes = rsa.encrypt(raw.encode('utf8'), self.publicKey)
        return codedBytes.decode('cp437')

    def encodeWithPrivateKey(self, raw: str) -> str:
        rawBytes = raw.encode('cp437')
        encodedBytes = rsa.decrypt(rawBytes, self.privateKey)
        return encodedBytes.decode('utf8')

    def signWithPrivateKey(self, raw: str) -> str:
        codedBytes = rsa.sign(raw.encode('utf8'), self.privateKey, 'SHA-1')
        return codedBytes.decode('cp437')

    def verifyWithPublicKey(self, raw: str, expected: str) -> bool:
        rawBytes = raw.encode('cp437')
        expectedBytes = expected.encode('utf8')
        result = rsa.verify(expectedBytes, rawBytes, self.publicKey)
        return result == 'SHA-1'
