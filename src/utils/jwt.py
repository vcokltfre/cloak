from datetime import datetime, timedelta
from os import environ
from typing import Final

from jose.jwt import decode as _jwt_decode
from jose.jwt import encode as _jwt_encode
from pydantic import BaseModel

JWT_SECRET: Final[str] = environ["JWT_SECRET"]
JWT_ALGORITHM: Final[str] = "HS256"


class Token(BaseModel):
    exp: int
    uid: int


def create_jwt(user_id: int) -> str:
    return _jwt_encode(
        {
            "exp": int((datetime.utcnow() + timedelta(days=14)).timestamp()),
            "uid": user_id,
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def jwt_decode(token: str) -> Token:
    tok = Token(**_jwt_decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM]))

    if tok.exp < int(datetime.utcnow().timestamp()):
        raise Exception("Token expired")

    return tok
