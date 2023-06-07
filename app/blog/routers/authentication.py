from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.blog import JWTtoken, schemas
from app.blog.database import get_db
from app.hashing import Hash

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
          ) -> dict[str, str]:
    user = db.query(schemas.User).filter(schemas.User.name == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There is no username with such name: {request.username}')
    if not Hash.verify(user.password, request.password):  # type: ignore [arg-type]
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Invalid password for {request.username}')

    access_token = JWTtoken.create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}
