import unittest
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

    def test_encrypt_large_message(self):
        largeMessage = b'hffello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_hello_helloX'
        cipher = RsaEncryption.encrypt(message=largeMessage, public_key=bob_public_key)
        encoded = RsaEncryption.decrypt(cipher=cipher, private_key=bob_private_key)
        self.assertEqual(largeMessage, encoded)


if __name__ == '__main__':
    unittest.main()
