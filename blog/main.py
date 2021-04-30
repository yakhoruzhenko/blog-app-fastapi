from fastapi import FastAPI, Depends, status, HTTPException
import models
import schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List


models.Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}')
def delete(task_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == task_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {task_id} is not found')
    db.query(models.Blog).filter(models.Blog.id == task_id).delete(synchronize_session=False)
    db.commit()
    return f'Blog with id {task_id} has been successfully deleted'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(task_id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == task_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {task_id} is not found')
    db.query(models.Blog).filter(models.Blog.id == task_id).\
        update({'title': request.title, 'body': request.body}, synchronize_session=False)
    db.commit()
    return f'Blog with id {task_id} has been successfully updated'


@app.get('/blog', response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(task_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == task_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {task_id} is not found')
    return blog
