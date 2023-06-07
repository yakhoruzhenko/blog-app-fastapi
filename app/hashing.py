from typing import Any

from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def bcrypt(password: str) -> Any:
        return pwd_ctx.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> Any:
        return pwd_ctx.verify(plain_password, hashed_password)
