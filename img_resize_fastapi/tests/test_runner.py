from io import BytesIO, TextIOWrapper
import random
import pytest
from PIL import Image, ImageDraw
from fastapi import HTTPException
from fastapi.datastructures import UploadFile

from runner import set_task, get_status
from tasks import resize
from transactions import to_store, to_retrieve

def gen_image(x, y, extension):
    im = Image.new('RGB', (x, y))
    draw = ImageDraw.Draw(im)
    draw.line((x / 3, y - y / 5) + (x / 3, y / 8), width=1, fill='grey')
    draw.line((x / 3, y - y / 5) + (x - x / 3, y - y / 5), width=1, fill='grey')
    im.show()
    b = BytesIO()
    im.save(b, format=extension)
    fp = TextIOWrapper(b)
    return fp

@pytest.fixture #(scope="module", params=[(300, 300, 'jpg'), (500,500, 'bmp')])
def test_image():
    return gen_image(300, 300, 'bmp')

def test_img_type(test_image):
    with pytest.raises(HTTPException):
        set_task(400, 400, test_image)

# class TestPostCase():
#
#     def test_img_type(self, gen_image):
#         with pytest.raises('HTTPException'):
#             set_task(400, 400, gen_image)
#
#     def test_img_height(self):
#         with pytest.raises('HTTPException'):
#             set_task()
#
#     def test_img_width(self):
#         with pytest.raises('HTTPException'):
#             set_task()
#
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


if __name__ == '__main__':
    print('...starting tests...')