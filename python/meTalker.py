from typing import Callable, Optional

from medium.connection import Connection, SslConnection
from medium.medium import Medium, MediumKind
from medium.sslMedium import SslMedium
from smartContract import SmartContract
from talker.talkerIdentity import TalkerIdentity
from talker.talkerInterfaceIdentity import TalkerInterfaceIdentity


class MeTalker:
    def __init__(self, talkerIdentity: TalkerIdentity, sslMedium: SslMedium, smartContract: SmartContract):
        self.talkerIdentity = talkerIdentity
        self.sslMedium = sslMedium
        self.smartContract = smartContract
        self.setup()

    def setup(self):
        self.smartContract.registerTalker(
            pseudonym=self.talkerIdentity.pseudonym,
            sslUrl=self.sslMedium.url(),
        )

    def requestConnection(self, target: TalkerIdentity, interface: TalkerInterfaceIdentity) -> Connection:
        result = self.smartContract.requestConnection(target.pseudonym, interface.name)
        return SslConnection(result)
