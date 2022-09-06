import rsa


DEBUG = True


class RsaKeys:
    def __init__(self, public_key: bytes, private_key: bytes):
        self.public_key = public_key
        self.private_key = private_key

    @classmethod
    def generate(cls):
        public_key, private_key = rsa.newkeys(nbits=512)
        public_key_bytes = public_key.save_pkcs1()[31:-30]
        private_key_bytes = private_key.save_pkcs1()[32:-31]
        debug_print(f"generate:\n\tpublic:\t\t\t{public_key_bytes}\n\tprivate:\t\t{private_key_bytes}")
        return RsaKeys(
            public_key=public_key_bytes,
            private_key=private_key_bytes,
        )


def debug_print(message: str):
    if DEBUG:
        print(f"rsa keys: {message}")
