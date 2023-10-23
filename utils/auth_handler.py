# This file is responsible for signing , encoding , decoding and returning JWTs
import os
import time
from typing import Dict
import jwt
from decouple import config

# JWT_ALGORITHM = config()


def token_response(token: str):
    return {"access_token": token}


# function used for signing the JWT string
def signJWT(email: str, role: str, secret) -> Dict[str, str]:
    payload = {
        "email": email,
        "role": role,
        "expires": time.time() + 93600,
    }
    token = jwt.encode(payload, secret, algorithm="HS256")

    return token_response(token)


def decodeJWT(token: str, secret) -> dict:
    try:
        decoded_token = jwt.decode(token, secret, algorithms=["HS256"])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
