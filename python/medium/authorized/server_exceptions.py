from python.encryption.rsa_encryption import DecryptionFailed
from python.medium.authorized.server_status import Status


class ServerException(Exception):
    pass


class ReceivedInvalidCipher(ServerException):
    def __init__(self, cipher: bytes, status: Status, inner: DecryptionFailed):
        self.cipher = cipher
        self.status = status
        self.inner = inner


class ReceivedInvalidIntroductionSignature(ServerException):
    pass


class AccessDenied(ServerException):
    pass
