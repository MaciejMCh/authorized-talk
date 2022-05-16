from threading import Thread
from typing import Optional
from meTalker import MeTalker
from medium.connection import SslConnection
from medium.session import Session
from messages.whisperControl_pb2 import Introduction
from talker.talkerIdentity import TalkerIdentity
from talker.talkerInterfaceIdentity import TalkerInterfaceIdentity
from whisper.whisperMouthState import WhisperClientState, InitialWhisperClientState


class WhisperingMouth:
    def __init__(
            self,
            meTalker: MeTalker,
            target: TalkerIdentity,
            targetInterface: TalkerInterfaceIdentity,
    ):
        self.meTalker = meTalker
        self.clientState: WhisperClientState = InitialWhisperClientState()
        self.session: Optional[Session] = None

        targetConnection = meTalker.requestConnection(
            target=target,
            interface=targetInterface,
        )
        if isinstance(targetConnection, SslConnection):
            Thread(target=self.whisperUsingSsl, args=[meTalker, targetConnection]).start()

    def whisperUsingSsl(self, meTalker: MeTalker, sslConnection: SslConnection):
        session = meTalker.sslMedium.connectTo(sslConnection.url)
        self.session = session
        self.continueWithSession(session)

    def continueWithSession(self, session: Session):
        session.onMessage(self.handleMessage)
        self.introduce(session)

    def introduce(self, session: Session):
        pseudonym = self.meTalker.talkerIdentity.pseudonym
        signature = self.meTalker.encryption.signWithPrivateKey(pseudonym)
        introduction = Introduction(pseudonym=pseudonym, signature=signature)
        message: bytes = introduction.SerializeToString()
        session.send(message)

    def handleMessage(self, message: bytes):
        pass
