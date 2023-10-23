import secrets


def create_secret():
    return secrets.token_hex(16)
