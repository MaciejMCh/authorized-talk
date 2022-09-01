from typing import Optional, Callable, List, Dict

from python.connector.connector import Connector
from python.core.interface_identity import InterfaceIdentity
from python.core.random import Random
from python.core.rsa_keys import RsaKeys
from python.identity_server.identity_server import IdentityServer, TargetNotFound
from python.medium.kinds import TargetMedium
from python.medium.medium import Medium


class TestConnector(Connector):
    def __init__(self):
        self.testMedium: Optional[TestMedium] = None

    def establish_connection(
            self,
            interface_identity: InterfaceIdentity,
            on_message: Callable[[bytes], None],
    ) -> Medium:
        testMedium = TestMedium(on_message)
        self.testMedium = testMedium
        return testMedium


class TestMedium(Medium):
    def __init__(self, onMessage: Callable[[bytes], None]):
        super().__init__()
        self.onMessage = onMessage
        self.sentMessages: List[bytes] = []

    def send(self, message: bytes):
        self.sentMessages.append(message)

    def receive(self, message: bytes):
        self.onMessage(message)


class TestIdentityServer(IdentityServer):
    def __init__(
            self,
            target_mediums_by_pseudonyms: Dict[str, List[TargetMedium]],
            public_keys_by_pseudonyms: Dict[str, bytes],
            white_list=None,
            roles=None,
    ):
        self.target_mediums_by_pseudonyms = target_mediums_by_pseudonyms
        self.public_keys_by_pseudonyms = public_keys_by_pseudonyms
        self.white_list = white_list if white_list is not None else {}
        self.roles = roles if roles is not None else {}

    async def get_available_mediums(self, pseudonym: str) -> List[TargetMedium]:
        if pseudonym not in self.target_mediums_by_pseudonyms:
            raise TargetNotFound()

        return self.target_mediums_by_pseudonyms[pseudonym]

    async def get_public_key(self, pseudonym: str) -> bytes:
        if pseudonym not in self.target_mediums_by_pseudonyms:
            raise TargetNotFound()

        return self.public_keys_by_pseudonyms[pseudonym]

    async def has_access(self, source_pseudonym: str, interface_identity: InterfaceIdentity) -> bool:
        if interface_identity.pseudonym not in self.white_list:
            return False
        if source_pseudonym not in self.roles:
            return False

        permitted_roles = self.white_list[interface_identity.pseudonym][interface_identity.interface]
        source_roles = self.roles[source_pseudonym]
        for source_role in source_roles:
            if source_role in permitted_roles:
                return True
        return False


bob_public_key = b'MEgCQQCSzchHR/v/h4L9jVgwBPWX4W8Dlc0o+U9K22roxzGKSp78JfKAMkK4qh5A\n58shJJiM1yKvBxNVuRLoFcWxBmO5AgMBAAE='
bob_private_key = b'MIIBPAIBAAJBAJLNyEdH+/+Hgv2NWDAE9ZfhbwOVzSj5T0rbaujHMYpKnvwl8oAy\nQriqHkDnyyEkmIzXIq8HE1W5EugVxbEGY7kCAwEAAQJALj9RxtLwmlFwfLwYehg1\n3oEQXgrFNRFFX4m8JlUKE+61awIuwV/MZ3iGug3OPg3/EgbW78ZVsi+iUpqy9qp1\nYQIjAL+f1qJohhZcwXCYQ33GmbpS9m46MEXAHeRvv4zbhhKXAMUCHwDEH0TtHcwJ\n145TdPSw4nkBqyGd/CgWjkabXeGsHmUCIwCAtShiD5i4nnajXPJAIcwRlTXGVbkk\nsGSjkdd0EeLcy6YNAh59Gy1OzOkxhg3Gcx78Dxv90nq5Wvb/nHax+WtR7nkCIhQn\nYhIv8YtGa0aNePkXxBQJJTzl81MmRWzs1JGFtM5ffLI='

alice_rsa_keys = RsaKeys(
    public_key=b'MEgCQQCr9nkC4Fr1Rec0aUGykqjEzQXRcwotv6cUc+JsbSSq/lKtNv0ucZqpQJ9S\n4jyZ9GFve/LbZzKncCfev84CZWLLAgMBAAE=',
    private_key=b'MIIBPgIBAAJBAKv2eQLgWvVF5zRpQbKSqMTNBdFzCi2/pxRz4mxtJKr+Uq02/S5x\nmqlAn1LiPJn0YW978ttnMqdwJ96/zgJlYssCAwEAAQJALIkXzAvo4q7o8yTzc9kR\nxm5GvHjrwO9qyRw+HtChNnb614KMeErbWIFClLWuad7LAa+5Sj7EKlIR6yfRclYZ\nmQIjAPsMyF9gIlCoC+C0slEdFF7rP3nhIzWY/P9xh+xFH1tYQuUCHwCvWnvwv44+\nFRE2ATAkjhSiUpymP8aExHWNc4K5Q+8CIwD5yyFATQ43xM10uzbGILIZM+fH5Ky8\n8smhfZxqCekGYY7FAh8AipqBAQjIjDXmxsMlpJ9RnASkoZwjdGo9aLN3Dq2tAiMA\n7dCw8BQmO2wZVox6yChKUXSYqRNZrOaivwly08AjfiX3RA==',
)


class TestRandom(Random):
    def __init__(self, phrase: bytes):
        self.phrase = phrase

    async def generate(self) -> bytes:
        return self.phrase
