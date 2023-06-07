from datetime import datetime, timedelta
from logging import getLogger
from typing import Any

from fastapi import HTTPException
from jose import JWTError, jwt
from starlette import status

logger = getLogger()


SECRET_KEY = "fcb83a311c0ab22310e16417b84de96d496c5f80906b4e14c00b15de44f56a8c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    logger.info(f"to_encode: {to_encode}")
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(data: str) -> None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        logger.info(f"payload: {payload}, username {username}")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
