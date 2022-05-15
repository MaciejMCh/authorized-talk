import asyncio
import time

from encryption.unsafeEncryption import UnsafeEncryption
from medium.sslMedium import SslMedium
from talker.talkerInterfaceIdentity import TalkerInterfaceIdentity
from tests.testSuite import TestSuite
from whisper.whisper import Whisper


def main():
    encryption = UnsafeEncryption('', '')
    cypher = encryption.signWithPrivateKey('siema')
    verified = encryption.verifyWithPublicKey(cypher, 'siema')

    # encryption = UnsafeEncryption('', '')
    # cypher = encryption.codeWithPublicKey('siema')
    # encoded = encryption.encodeWithPrivateKey(cypher)
    return
    testSuite = TestSuite()
    whisper = Whisper(
        meTalker=testSuite.anna,
        target=testSuite.bob.talkerIdentity,
        targetInterface=TalkerInterfaceIdentity('hello'),
    )
    time.sleep(10)

    # result = ''
    # anna = SslMedium.local(8765)
    # bob = SslMedium.local(8766)
    # await asyncio.sleep(1.2)
    # annasSession = await anna.connectTo(bob.url())
    #
    # def handleIncomingMessageAsBob(message: str):
    #     nonlocal result
    #     result = message
    #
    # await asyncio.sleep(1.2)
    # bob.incomingSessions[0].onMessage(handleIncomingMessageAsBob)
    # await annasSession.send('hello')
    # await asyncio.sleep(.2)


if __name__ == '__main__':
    main()
