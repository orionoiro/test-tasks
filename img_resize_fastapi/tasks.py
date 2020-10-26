from PIL import Image
from celery import Celery
from uuid import uuid4

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')

@app.task
def resize(width: int, height: int, file):
    try:
        id = str(uuid4())
        im = Image.open(file)
        img_type = im.format
        im = im.resize((width, height))
        im.save(id, format=img_type)
        return id
    except:
        raise Exception

@app.task
def add(x: int, y: int):
    return x + y
