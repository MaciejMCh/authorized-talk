separator = b';'


def introduction_signature(
        pseudonym: str,
        target_interface: str,
        nonce: bytes,
) -> bytes:
    return separator.join([pseudonym.encode(), target_interface.encode(), nonce])
