from typing import Callable, Optional

from encryption.encryption import Encryption
from medium.connection import Connection, SslConnection
from medium.medium import Medium, MediumKind
from medium.sslMedium import SslMedium
from medium.sslSession import SslSession
from smartContract import SmartContract
from talker.talkerIdentity import TalkerIdentity
from talker.talkerInterfaceIdentity import TalkerInterfaceIdentity
from whisper.whisperingEar import WhisperingEar


class MeTalker:
    def __init__(
        self,
        talkerIdentity: TalkerIdentity,
        encryption: Encryption,
        sslMedium: SslMedium,
        smartContract: SmartContract,
    ):
        self.talkerIdentity = talkerIdentity
        self.encryption = encryption
        self.sslMedium = sslMedium
        self.smartContract = smartContract
        self.setup()

    def setup(self):
        self.smartContract.registerTalker(
            pseudonym=self.talkerIdentity.pseudonym,
            sslUrl=self.sslMedium.url(),
            publicKey=self.encryption.getPublicKey(),
        )
        self.sslMedium.routeIncoming(self.routeIncomingSession)

    def requestConnection(self, target: TalkerIdentity, interface: TalkerInterfaceIdentity) -> Connection:
        result = self.smartContract.requestConnection(target.pseudonym, interface.name)
        return SslConnection(result)

    def routeIncomingSession(self, session: SslSession):
        WhisperingEar(session=session, smartContract=self.smartContract, encryption=self.encryption)

    def registerInterface(self, identity: TalkerInterfaceIdentity):
        pass