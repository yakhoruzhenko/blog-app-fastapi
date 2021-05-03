from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from blog import JWTtoken


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    JWTtoken.verify_token(token)
    return JWTtoken.verify_token(token)
