import time

from encryption.unsafeEncryption import UnsafeEncryption
from talker.talkerInterfaceIdentity import TalkerInterfaceIdentity
from tests.testSuite import TestSuite
from whisper.whisperingMouth import WhisperingMouth


def main():
    # encryption = UnsafeEncryption()
    # largeMessage = 'helasdsdlo_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_helloX'
    # coded = encryption.codeWithPublicKey(largeMessage)
    # encoded = encryption.encodeWithPrivateKey(coded)
    # return
    testSuite = TestSuite()

    WhisperingMouth(
        meTalker=testSuite.anna,
        target=testSuite.bob.talkerIdentity,
        targetInterface=TalkerInterfaceIdentity('hello'),
    )

    time.sleep(2)


if __name__ == '__main__':
    main()
