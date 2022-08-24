import unittest

from python.encryption.unsafeEncryption import UnsafeEncryption


class EncryptionTestCase(unittest.TestCase):
    def testEncoding(self):
        encryption = UnsafeEncryption()
        coded = encryption.codeWithPublicKey('hello')
        encoded = encryption.encodeWithPrivateKey(coded)
        self.assertEqual('hello', encoded)

    def testVerifing(self):
        encryption = UnsafeEncryption()
        coded = encryption.signWithPrivateKey('hello')
        verification = encryption.verifyWithPublicKey(coded, 'hello')
        self.assertEqual(True, verification)

    def testCodeLargeMessage(self):
        encryption = UnsafeEncryption()
        largeMessage = 'hffello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_helloX'
        coded = encryption.codeWithPublicKey(largeMessage)
        encoded = encryption.encodeWithPrivateKey(coded)
        self.assertEqual(largeMessage, encoded)


if __name__ == '__main__':
    unittest.main()
