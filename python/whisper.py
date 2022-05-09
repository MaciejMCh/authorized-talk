from blockchain import Blockchain
from meTalker import MeTalker
from talker import Talker


class Whisper:
    def __init__(self, message: str):
        self.message = message


def sendWhisper(blockchain: Blockchain, whisper: Whisper, receiver: Talker):
    medium = blockchain.requestMedium(receiver)
