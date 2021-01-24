from base64 import b64decode
from io import BytesIO

from PIL import Image
from celery import Celery

celery_app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')


@celery_app.task
def resize(width: int, height: int, b64_string: str):
    uid = resize.request.id
    data = b64decode(b64_string.encode('ascii'))
    bytes_io = BytesIO(data)
    im = Image.open(bytes_io)
    img_type = im.format
    im = im.resize((width, height))
    im.save(uid, format=img_type)
    return uid
