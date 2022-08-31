from enum import Enum


class Status(Enum):
    INITIAL = 1
    CONNECTED = 2
    INTRODUCING = 3
    CHALLENGED = 4
    FAILED = 5
    SUBMITTING = 6
    ANSWERED = 7
    AUTHORIZED = 8
