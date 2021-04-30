from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


app = FastAPI()


@app.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from the db'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f'Blog is created with title as {request.title}'}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
