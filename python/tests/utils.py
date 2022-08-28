from typing import Optional, Callable, List, Dict

from python.connector.connector import Connector
from python.core.interface_identity import InterfaceIdentity
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
    ):
        self.target_mediums_by_pseudonyms = target_mediums_by_pseudonyms
        self.public_keys_by_pseudonyms = public_keys_by_pseudonyms

    async def get_available_mediums(self, pseudonym: str) -> List[TargetMedium]:
        if pseudonym not in self.target_mediums_by_pseudonyms:
            raise TargetNotFound()

        return self.target_mediums_by_pseudonyms[pseudonym]

    async def get_public_key(self, pseudonym: str) -> bytes:
        if pseudonym not in self.target_mediums_by_pseudonyms:
            raise TargetNotFound()

        return self.public_keys_by_pseudonyms[pseudonym]


bob_public_key = b'MEgCQQCSzchHR/v/h4L9jVgwBPWX4W8Dlc0o+U9K22roxzGKSp78JfKAMkK4qh5A\n58shJJiM1yKvBxNVuRLoFcWxBmO5AgMBAAE='
bob_private_key = b'MIIBPAIBAAJBAJLNyEdH+/+Hgv2NWDAE9ZfhbwOVzSj5T0rbaujHMYpKnvwl8oAy\nQriqHkDnyyEkmIzXIq8HE1W5EugVxbEGY7kCAwEAAQJALj9RxtLwmlFwfLwYehg1\n3oEQXgrFNRFFX4m8JlUKE+61awIuwV/MZ3iGug3OPg3/EgbW78ZVsi+iUpqy9qp1\nYQIjAL+f1qJohhZcwXCYQ33GmbpS9m46MEXAHeRvv4zbhhKXAMUCHwDEH0TtHcwJ\n145TdPSw4nkBqyGd/CgWjkabXeGsHmUCIwCAtShiD5i4nnajXPJAIcwRlTXGVbkk\nsGSjkdd0EeLcy6YNAh59Gy1OzOkxhg3Gcx78Dxv90nq5Wvb/nHax+WtR7nkCIhQn\nYhIv8YtGa0aNePkXxBQJJTzl81MmRWzs1JGFtM5ffLI='
