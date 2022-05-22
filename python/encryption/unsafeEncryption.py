import rsa
from rsa import PublicKey, PrivateKey

from encryption.encryption import Encryption


HASH_METHOD = 'SHA-1'
KEY_SIZE = 512
SLICE_SIZE = 53
CIPHER_SLICE_SIZE = 64


class UnsafeEncryption(Encryption):
    def __init__(self):
        (self.publicKey, self.privateKey) = rsa.newkeys(KEY_SIZE)

    def getPublicKey(self) -> str:
        return PublicKey.save_pkcs1(self.publicKey, format='PEM').decode('utf-8')

    def codeBytes(self, raw: bytes, publicKey: PublicKey) -> bytes:
        print(f'code bytes {len(raw)}')
        cipher = bytes()
        pointer = 0
        while True:
            if pointer + SLICE_SIZE > len(raw):
                break
            cipherSlice = rsa.encrypt(raw[pointer:pointer + SLICE_SIZE], publicKey)
            cipher += cipherSlice
            pointer += SLICE_SIZE
            print(f'append slice {pointer - SLICE_SIZE}:{pointer}')
        byteRemaining = len(raw) - pointer
        if byteRemaining > 0:
            print(f'append remaining {byteRemaining}')
            remainingBytes = raw[len(raw) - byteRemaining:len(raw)]
            cipherSlice = rsa.encrypt(remainingBytes, publicKey)
            cipher += cipherSlice
        return cipher

    def code(self, raw: str, publicKey: PublicKey):
        codedBytes = self.codeBytes(raw.encode('utf8'), publicKey)
        return codedBytes.decode('cp437')

    def codeWithPublicKey(self, raw: str) -> str:
        return self.code(raw, self.publicKey)

    def codeBytesWithOtherPublicKey(self, raw: bytes, publicKeyString: str) -> bytes:
        publicKey = self.publicKeyWithString(publicKeyString)
        return self.codeBytes(raw, publicKey)

    def publicKeyWithString(self, publicKeyString) -> PublicKey:
        keyBytes = publicKeyString.encode('utf-8')
        return PublicKey.load_pkcs1(keyBytes, format='PEM')

    def codeWithOtherPublicKey(self, raw: str, publicKeyString: str) -> str:
        return self.code(raw, self.publicKeyWithString(publicKeyString))

    def encodeBytes(self, raw: bytes, privateKey: PrivateKey) -> bytes:
        print(f'encode bytes {len(raw)}')
        cipher = bytes()
        pointer = 0
        while True:
            if pointer + CIPHER_SLICE_SIZE > len(raw):
                break
            cipherSlice = rsa.decrypt(raw[pointer:pointer + CIPHER_SLICE_SIZE], privateKey)
            cipher += cipherSlice
            pointer += CIPHER_SLICE_SIZE
            print(f'append slice {pointer - CIPHER_SLICE_SIZE}:{pointer}')
        byteRemaining = len(raw) - pointer
        if byteRemaining > 0:
            print(f'append remaining {byteRemaining}')
            remainingBytes = raw[len(raw) - byteRemaining:len(raw)]
            cipherSlice = rsa.decrypt(remainingBytes, privateKey)
            cipher += cipherSlice
        return cipher

    def encodeWithPrivateKey(self, raw: str) -> str:
        rawBytes = raw.encode('cp437')
        encodedBytes = self.encodeBytes(rawBytes, self.privateKey)
        return encodedBytes.decode('utf8')

    def encodeBytesWithPrivateKey(self, raw: bytes) -> bytes:
        return self.encodeBytes(raw, self.privateKey)

    def signWithPrivateKey(self, raw: str) -> str:
        codedBytes = rsa.sign(raw.encode('utf8'), self.privateKey, HASH_METHOD)
        return codedBytes.decode('cp437')

    def verify(self, raw: str, expected: str, publicKey: PublicKey):
        rawBytes = raw.encode('cp437')
        expectedBytes = expected.encode('utf8')
        result = rsa.verify(expectedBytes, rawBytes, publicKey)
        return result == HASH_METHOD

    def verifyWithPublicKey(self, raw: str, expected: str) -> bool:
        return self.verify(raw=raw, expected=expected, publicKey=self.publicKey)

    def verifyWithOtherPublicKey(self, raw, expected: str, publicKeyString: str):
        return self.verify(raw=raw, expected=expected, publicKey=self.publicKeyWithString(publicKeyString))
