from encryption.encryption import Encryption
from medium.sslSession import SslSession
from messages.whisperControl_pb2 import Introduction
from smartContract import SmartContract
from whisper.whisperingEarState import WhisperingEarState, WaitingForIntroduction, RejectedIntroduction


class WhisperingEar:
    def __init__(self, session: SslSession, smartContract: SmartContract, encryption: Encryption):
        self.session = session
        self.smartContract = smartContract
        self.encryption = encryption
        self.state: WhisperingEarState = WaitingForIntroduction()
        self.session.onMessage(self.handleIncomingMessage)

    def handleIncomingMessage(self, message: bytes):
        print('whispearing ear: handleIncomingMessage')
        if isinstance(self.state, WaitingForIntroduction):
            self.handleMessageWaitingForIntroduction(message)

    def rejectIntroduction(self):
        self.session.close()
        self.state = RejectedIntroduction()

    def passIntroduction(self):
        print('passed introduction')

    def handleMessageWaitingForIntroduction(self, message: bytes):
        encodedMessage = self.encryption.encodeBytesWithPrivateKey(message)
        introduction = Introduction()
        introduction.ParseFromString(encodedMessage)
        publicKeyString = self.smartContract.getPublicKey(introduction.pseudonym)
        isVerified = self.encryption.verifyWithOtherPublicKey(
            raw=introduction.signature,
            expected=introduction.pseudonym,
            publicKeyString=publicKeyString,
        )
        if isVerified:
            self.passIntroduction()
        else:
            self.rejectIntroduction()
