import asyncio
from threading import Thread

from blockchain import Blockchain
from meTalker import MeTalker
from medium.connection import SslConnection
from medium.session import Session
from talker.talker import Talker
from talker.talkerIdentity import TalkerIdentity
from talker.talkerInterfaceIdentity import TalkerInterfaceIdentity


class Whisper:
    def __init__(
            self,
            meTalker: MeTalker,
            target: TalkerIdentity,
            targetInterface: TalkerInterfaceIdentity,
    ):
        targetConnection = meTalker.requestConnection(
            target=target,
            interface=targetInterface,
        )
        if isinstance(targetConnection, SslConnection):
            Thread(target=self.whisperUsingSsl, args=[meTalker, targetConnection]).start()

    def whisperUsingSsl(self, meTalker: MeTalker, sslConnection: SslConnection):
        session = meTalker.sslMedium.connectTo(sslConnection.url)
        self.continueWithSession(session)

    def continueWithSession(self, session: Session):
        session.send("xd")
