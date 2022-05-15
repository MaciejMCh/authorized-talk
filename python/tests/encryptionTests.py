import unittest

from encryption.unsafeEncryption import UnsafeEncryption


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


if __name__ == '__main__':
    unittest.main()
