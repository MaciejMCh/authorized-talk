from rsa import PublicKey, PrivateKey
import rsa

HASH_METHOD = 'SHA-1'
KEY_SIZE = 512
SLICE_SIZE = 53
CIPHER_SLICE_SIZE = 64

DEBUG = False


class RsaEncryption:
    @classmethod
    def encrypt(cls, message: bytes, public_key: bytes) -> bytes:
        return cls.encrypt_bytes(message=message, publicKey=cls.public_key_with_bytes(public_key))

    @classmethod
    def decrypt(cls, cipher: bytes, private_key: bytes) -> bytes:
        return cls.decrypt_bytes(raw=cipher, private_key=cls.private_key_with_bytes(private_key))

    @classmethod
    def sign(cls, message: bytes, private_key: bytes) -> bytes:
        return rsa.sign(message, cls.private_key_with_bytes(private_key), HASH_METHOD)

    @classmethod
    def verify(cls, message: bytes, signature: bytes, public_key: bytes) -> bool:
        result = rsa.verify(message, signature, cls.public_key_with_bytes(public_key))
        return result == HASH_METHOD

    @classmethod
    def public_key_with_bytes(cls, key_bytes: bytes) -> PublicKey:
        pem_bytes = b'-----BEGIN RSA PUBLIC KEY-----\n' + key_bytes + b'\n-----END RSA PUBLIC KEY-----\n'
        return PublicKey.load_pkcs1(pem_bytes, format='PEM')

    @classmethod
    def private_key_with_bytes(cls, key_bytes: bytes) -> PrivateKey:
        pem_bytes = b'-----BEGIN RSA PRIVATE KEY-----\n' + key_bytes + b'\n-----END RSA PRIVATE KEY-----\n'
        return PrivateKey.load_pkcs1(pem_bytes, format='PEM')

    @classmethod
    def encrypt_bytes(cls, message: bytes, publicKey: PublicKey) -> bytes:
        debug_print(f'code bytes {len(message)}')
        cipher = bytes()
        pointer = 0
        while True:
            if pointer + SLICE_SIZE > len(message):
                break
            cipher_slice = rsa.encrypt(message[pointer:pointer + SLICE_SIZE], publicKey)
            cipher += cipher_slice
            pointer += SLICE_SIZE
            debug_print(f'append slice {pointer - SLICE_SIZE}:{pointer}')
        byte_remaining = len(message) - pointer
        if byte_remaining > 0:
            debug_print(f'append remaining {byte_remaining}')
            remaining_bytes = message[len(message) - byte_remaining:len(message)]
            cipher_slice = rsa.encrypt(remaining_bytes, publicKey)
            cipher += cipher_slice
        return cipher

    @classmethod
    def decrypt_bytes(cls, raw: bytes, private_key: PrivateKey) -> bytes:
        debug_print(f'encode bytes {len(raw)}')
        cipher = bytes()
        pointer = 0
        while True:
            if pointer + CIPHER_SLICE_SIZE > len(raw):
                break
            cipherSlice = rsa.decrypt(raw[pointer:pointer + CIPHER_SLICE_SIZE], private_key)
            cipher += cipherSlice
            pointer += CIPHER_SLICE_SIZE
            debug_print(f'append slice {pointer - CIPHER_SLICE_SIZE}:{pointer}')
        byteRemaining = len(raw) - pointer
        if byteRemaining > 0:
            debug_print(f'append remaining {byteRemaining}')
            remainingBytes = raw[len(raw) - byteRemaining:len(raw)]
            cipherSlice = rsa.decrypt(remainingBytes, private_key)
            cipher += cipherSlice
        return cipher


def debug_print(msg: str):
    if DEBUG:
        print(msg)
