separator = b';'


def introduction_signature(
        pseudonym: str,
        target_interface: str,
        nonce: bytes,
) -> bytes:
    return separator.join([pseudonym.encode(), target_interface.encode(), nonce])


def access_pass_signature(
        source_pseudonym: str,
        passes: bool,
) -> bytes:
    return separator.join([source_pseudonym.encode(), b'1' if passes else b'0'])
