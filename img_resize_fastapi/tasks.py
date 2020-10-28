from base64 import b64encode, b64decode
from io import BytesIO
from uuid import uuid4

from PIL import Image
from celery import Celery

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')


@app.task
def resize(width: int, height: int, b64: str):
    try:
        data = b64decode(b64)
        bytes_io = BytesIO(data)
        uid = str(uuid4())
        im = Image.open(bytes_io)
        img_type = im.format
        im = im.resize((width, height))
        im.save(uid, format=img_type)
        return uid
    except ValueError:
        print('Error')

if __name__ == '__main__':
    data = open('/home/dude/Downloads/images/90935.jpg', 'rb')
    data = data.read()
    encoded = b64encode(data)
    b64d = b64decode(data)
    resize.delay(30, 30, b64d)
