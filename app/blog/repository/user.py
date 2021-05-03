from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status
from hashing import Hash
from blog import schemas, models


def create(request: schemas.User, db):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def get_by_id(task_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == task_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {task_id} is not found')
    return user
