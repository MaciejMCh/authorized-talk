from threading import Thread
from typing import Optional
from meTalker import MeTalker
from medium.connection import SslConnection
from medium.session import Session
from messages.whisperControl_pb2 import Introduction, AccessPass
from talker.talkerIdentity import TalkerIdentity
from talker.talkerInterfaceIdentity import TalkerInterfaceIdentity
from whisper.signatures import introductionSignature
from whisper.whisperMouthState import WhisperMouthState, Initial, WaitingForPass, Opened, RejectedPass


class WhisperingMouth:
    def __init__(
            self,
            meTalker: MeTalker,
            target: TalkerIdentity,
            targetInterface: TalkerInterfaceIdentity,
    ):
        self.meTalker = meTalker
        self.target = target
        self.state: WhisperMouthState = Initial()
        self.session: Optional[Session] = None

        targetConnection = meTalker.requestConnection(
            target=target,
            interface=targetInterface,
        )
        if isinstance(targetConnection, SslConnection):
            Thread(target=self.whisperUsingSsl, args=[meTalker, targetConnection, targetInterface]).start()

    def updateState(self, state: WhisperMouthState):
        print(f'update mouth state: {state}')
        self.state = state

    def whisperUsingSsl(self, meTalker: MeTalker, sslConnection: SslConnection, interface: TalkerInterfaceIdentity):
        session = meTalker.sslMedium.connectTo(sslConnection.url)
        self.session = session
        self.continueWithSession(session=session, interface=interface)

    def continueWithSession(self, session: Session, interface: TalkerInterfaceIdentity):
        session.onMessage(self.handleMessage)
        self.introduce(session=session, interface=interface)

    def introduce(self, session: Session, interface: TalkerInterfaceIdentity):
        pseudonym = self.meTalker.talkerIdentity.pseudonym
        targetInterface = interface.name
        signature = self.meTalker.encryption.signWithPrivateKey(introductionSignature(pseudonym=pseudonym, targetInterface=targetInterface))
        introduction = Introduction(pseudonym=pseudonym, targetInterface=targetInterface, signature=signature)
        targetPublicKey = self.meTalker.smartContract.getPublicKey(self.target.pseudonym)
        message: bytes = introduction.SerializeToString()
        cipher = self.meTalker.encryption.codeBytesWithOtherPublicKey(message, targetPublicKey)
        self.updateState(WaitingForPass())
        session.send(cipher)

    def handleMessage(self, message: bytes):
        if isinstance(self.state, WaitingForPass):
            self.handleMessageWaitingForPass(message)

    def handleMessageWaitingForPass(self, message: bytes):
        accessPass = AccessPass()
        accessPass.ParseFromString(message)
        publicKeyString = self.meTalker.smartContract.getPublicKey(self.target.pseudonym)
        isVerified = self.meTalker.encryption.verifyWithOtherPublicKey(
            raw=accessPass.signature,
            expected=self.target.pseudonym,
            publicKeyString=publicKeyString,
        )
        if isVerified:
            self.confirmPass()
        else:
            self.rejectPass()

    def confirmPass(self):
        self.updateState(Opened())

    def rejectPass(self):
        self.updateState(RejectedPass())
