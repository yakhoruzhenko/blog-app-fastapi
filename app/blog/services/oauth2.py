from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm.session import Session
from starlette import status

from app.blog.infra.database import get_db
from app.blog.infra.schemas import User
from app.blog.repositories.user import get_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "fcb83a311c0ab22310e16417b84de96d496c5f80906b4e14c00b15de44f56a8c"  # nosec
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("name")  # type: ignore[assignment]
        user_id: int = payload.get("id")  # type: ignore[assignment]
        if (user_name or user_id) is None:  # pragma: no cover
            raise credentials_exception
    except JWTError:  # pragma: no cover
        raise credentials_exception
    return get_by_id(id=user_id, db=db)


def fake_admin_token(token: str = Header()) -> None:
    if token != 'admin_token':  # nosec
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid admin token',
        )
