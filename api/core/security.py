import json
import pyseto

from argon2 import PasswordHasher
from pyseto import Key

from api.core.config import settings

ph = PasswordHasher()


private_key = Key.new(4, "public", settings.private_key_pem.get_secret_value())
public_key = Key.new(4, "public", settings.public_key_pem.get_secret_value())


def create_access_token(data: dict) -> bytes:
    token = pyseto.encode(
        private_key,
        payload=data,
        footer={"kid": public_key.to_paserk_id()},
        serializer=json,
        exp=settings.access_token_expire_seconds,
    )
    return token


def decode_token(token):
    return pyseto.decode(public_key, token, deserializer=json)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    return ph.verify(hashed_password, plain_password)


def get_password_hash(password: str) -> str:
    return ph.hash(password)
