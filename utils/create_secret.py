import secrets


def create_secret():
    secret = secrets.token_hex(16)

    with open("secret", "w") as file:
        file.write(secret)

    return "secret"
