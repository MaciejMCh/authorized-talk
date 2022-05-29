from encryption.encryption import Encryption
from medium.sslSession import SslSession
from messages.whisperControl_pb2 import Introduction, AccessPass
from smartContract import SmartContract
from whisper.signatures import introductionSignature
from whisper.whisperingEarState import WhisperingEarState, WaitingForIntroduction, RejectedIntroduction, WaitingForPass, \
    Opened, RejectedPass


class WhisperingEar:
    def __init__(self, pseudonym: str, session: SslSession, smartContract: SmartContract, encryption: Encryption):
        self.pseudonym = pseudonym
        self.session = session
        self.smartContract = smartContract
        self.encryption = encryption
        self.state: WhisperingEarState = WaitingForIntroduction()
        self.session.onMessage(self.handleIncomingMessage)

    def updateState(self, state: WhisperingEarState):
        print(f'update ear state: {state}')
        self.state = state

    def handleIncomingMessage(self, message: bytes):
        print('whispearing ear: handleIncomingMessage')
        if isinstance(self.state, WaitingForIntroduction):
            self.handleMessageWaitingForIntroduction(message)

    def rejectIntroduction(self):
        self.session.close()
        self.updateState(RejectedIntroduction())

    def passIntroduction(self, sourcePseudonym: str, targetInterface: str):
        print('passed introduction')
        self.askForPass(sourcePseudonym=sourcePseudonym, targetInterface=targetInterface)

    def askForPass(self, sourcePseudonym: str, targetInterface: str):
        self.updateState(WaitingForPass())
        canAccess = self.smartContract.canAccess(sourcePseudonym=sourcePseudonym, targetInterface=targetInterface)
        if canAccess:
            self.passAccess()
        else:
            self.rejectAccess()

    def passAccess(self):
        print('passed access')
        self.updateState(Opened())
        accessPass = AccessPass()
        accessPass.signature = self.encryption.signWithPrivateKey(self.pseudonym)
        self.session.send(accessPass.SerializeToString())

    def rejectAccess(self):
        print('reject access')
        self.updateState(RejectedPass())

    def handleMessageWaitingForIntroduction(self, message: bytes):
        encodedMessage = self.encryption.encodeBytesWithPrivateKey(message)
        introduction = Introduction()
        introduction.ParseFromString(encodedMessage)
        publicKeyString = self.smartContract.getPublicKey(introduction.pseudonym)
        isVerified = self.encryption.verifyWithOtherPublicKey(
            raw=introduction.signature,
            expected=introductionSignature(
                pseudonym=introduction.pseudonym,
                targetInterface=introduction.targetInterface,
            ),
            publicKeyString=publicKeyString,
        )
        if isVerified:
            self.passIntroduction(sourcePseudonym=introduction.pseudonym, targetInterface=introduction.targetInterface)
        else:
            self.rejectIntroduction()
