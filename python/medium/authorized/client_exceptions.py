from python.encryption.rsa_encryption import DecryptionFailed
from python.medium.authorized.client_status import Status


class ClientException(Exception):
    pass


class ReceivedInvalidCipher(ClientException):
    def __init__(self, cipher: bytes, status: Status, inner: DecryptionFailed):
        self.cipher = cipher
        self.status = status
        self.inner = inner


class InvalidChallengeSignature(ClientException):
    pass
