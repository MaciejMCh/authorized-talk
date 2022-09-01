from enum import Enum


class Status(Enum):
    INITIAL = 1
    CHALLENGED = 2
    AUTHORIZED = 3
    FAILED = 4
