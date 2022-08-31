from python.encryption.rsa_encryption import DecryptionFailed
from python.medium.authorized.client_status import Status
from google.protobuf.message import Message


class ClientException(Exception):
    pass


class ReceivedInvalidCipher(ClientException):
    def __init__(self, cipher: bytes, status: Status, inner: DecryptionFailed):
        self.cipher = cipher
        self.status = status
        self.inner = inner


class InvalidChallengeSignature(ClientException):
    pass


class RejectedByTarget(ClientException):
    pass


class MalformedProtoMessage(ClientException):
    def __init__(self, reason: str, message: Message):
        self.reason = reason
        self.message = message


class InvalidAccessPassSignature(ClientException):
    pass


class ChallengeFailed(ClientException):
    pass
