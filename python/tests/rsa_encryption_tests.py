import unittest
import rsa
from python.encryption.rsa_encryption import RsaEncryption
from python.tests.utils import bob_public_key, bob_private_key


class RsaEncryptionTestCase(unittest.TestCase):
    def test_encryption(self):
        cipher = RsaEncryption.encrypt(message=b'hello', public_key=bob_public_key)
        encoded = RsaEncryption.decrypt(cipher=cipher, private_key=bob_private_key)
        self.assertEqual(b'hello', encoded)

    def test_signing(self):
        signature = RsaEncryption.sign(message=b'hello', private_key=bob_private_key)
        self.assertTrue(RsaEncryption.verify(message=b'hello', signature=signature, public_key=bob_public_key))


if __name__ == '__main__':
    unittest.main()
