from io import BytesIO
from os import getcwd

import pytest
from PIL import Image, ImageDraw
from magic import from_buffer

from fastapi import HTTPException
from fastapi.datastructures import UploadFile

from runner import set_task, get_status
from tasks import celery_app, resize
from transactions import to_store, to_retrieve


def gen_image(x, y, extension):
    im = Image.new('RGB', (x, y))
    draw = ImageDraw.Draw(im)
    draw.line((x / 3, y - y / 5) + (x / 3, y / 8), width=1, fill='grey')
    draw.line((x / 3, y - y / 5) + (x - x / 3, y - y / 5), width=1, fill='grey')
    b = BytesIO()
    im.save(b, format=extension)
    b.seek(0)
    upload_file = UploadFile(b)
    upload_file.content_type = from_buffer(b.getvalue(), mime=True)
    upload_file.file._file = b

    return upload_file


@pytest.fixture()
def arrange_image(request):
    return gen_image(request.param[0], request.param[1], request.param[2])


@pytest.mark.parametrize('arrange_image', [(300, 300, 'webp'), (500, 500, 'bmp'), (700, 700, 'gif')], indirect=True)
def test_wrong_img_type(arrange_image):
    with pytest.raises(HTTPException):
        set_task(400, 400, arrange_image)


@pytest.mark.parametrize('arrange_image', [(300, 300, 'png'), (500, 500, 'jpeg')], indirect=True)
def test_correct_img_type(arrange_image):
    height, width = 400, 400
    id = set_task(height, width, arrange_image)
    task = celery_app.AsyncResult(id=id)
    while True:
        if task.ready():
            break
    image = Image.open(f'{getcwd()}/{id}', 'r')
    assert image.size == (height, width)
    assert image.format.lower() == arrange_image.content_type.split('/')[1]


def test_img_height():
    ...


def test_img_width():
    ...

# class TestPostCase():
#     def test_redis_transaction(self):
#         ...
#
#     def test_celery_job(self):
#         ...
#
#
# class GetTestCase():
#     ...
#
#
# class CeleryTaskTest():
#     ...
#
#
# class RedisTests():
#     def test_to_store(self):
#         ...
#
#     def test_to_retrieve(self):
#         ...
