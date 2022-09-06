import rsa


class RsaKeys:
    def __init__(self, public_key: bytes, private_key: bytes):
        self.public_key = public_key
        self.private_key = private_key

    @classmethod
    def generate(cls):
        public_key, private_key = rsa.newkeys(nbits=512)
        public_key_bytes = public_key.save_pkcs1()[31:-30]
        private_key_bytes = private_key.save_pkcs1()[32:]
        return RsaKeys(
            public_key=public_key_bytes,
            private_key=private_key_bytes,
        )
