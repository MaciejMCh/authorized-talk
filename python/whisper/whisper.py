import asyncio
from threading import Thread
from typing import Optional

from encryption.encryption import Encryption
from meTalker import MeTalker
from medium.connection import SslConnection
from medium.session import Session
from messages.whisperControl_pb2 import Introduction
from talker.talkerIdentity import TalkerIdentity
from talker.talkerInterfaceIdentity import TalkerInterfaceIdentity
from whisper.whisperClientState import InitialWhisperClientState, WhisperClientState


class Whisper:
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
        signature = self.meTalker.encryption.codeWithPrivateKey(pseudonym)
        xdd = Encryption.decodeWithPublicKey(signature, self.meTalker.encryption.getPublicKey())
        introduction = Introduction(pseudonym=pseudonym, signature=signature)
        message = introduction.SerializeToString()
        session.send(message)

    def handleMessage(self, message: str):
        pass
