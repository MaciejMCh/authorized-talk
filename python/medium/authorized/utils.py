def introduction_signature(pseudonym: str, targetInterface: str) -> bytes:
    return f"${pseudonym};${targetInterface}".encode()
