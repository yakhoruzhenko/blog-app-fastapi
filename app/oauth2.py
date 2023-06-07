from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.blog import JWTtoken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_user(data: str = Depends(oauth2_scheme)) -> None:
    JWTtoken.verify_token(data)
