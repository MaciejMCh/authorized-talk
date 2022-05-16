from medium.sslSession import SslSession
from messages.whisperControl_pb2 import Introduction
from smartContract import SmartContract
from whisper.whisperingEarState import WhisperingEarState, WaitingForIntroduction


class WhisperingEar:
    def __init__(self, session: SslSession, smartContract: SmartContract):
        self.smartContract = smartContract
        self.session = session
        self.state: WhisperingEarState = WaitingForIntroduction()
        self.session.onMessage(self.handleIncomingMessage)

    def handleIncomingMessage(self, message: bytes):
        print('whispearing ear: handleIncomingMessage')
        if isinstance(self.state, WaitingForIntroduction):
            self.handleMessageWaitingForIntroduction(message)

    def handleMessageWaitingForIntroduction(self, message: bytes):
        introduction = Introduction()
        introduction.ParseFromString(message)
        # self.smartContract.getPublicKey(introduction.pseudonym)