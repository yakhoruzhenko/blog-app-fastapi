from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': "Yaroslav"}}


@app.get('/about')
def about():
    return {'data': {'About page'}}