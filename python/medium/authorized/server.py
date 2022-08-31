from enum import Enum

from python.medium.medium import Medium


class Status(Enum):
    INITIAL = 1


class AuthorizedServerMedium(Medium):
    def __init__(self, medium: Medium):
        super().__init__()
        self.medium = medium
        self.status = Status.INITIAL
        self.setup()

    def setup(self):
        self.medium.handle_message(self.on_medium_message)

    def on_medium_message(self, message: bytes):
        if self.status == Status.INITIAL:
            self.receive_introduction(message)
            return

    def receive_introduction(self, message: bytes):
        pass
