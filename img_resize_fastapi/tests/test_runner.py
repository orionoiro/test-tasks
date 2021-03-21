from io import BytesIO
from os import getcwd

import pytest
from PIL import Image, ImageDraw
from fastapi import HTTPException
from fastapi.datastructures import UploadFile
from magic import from_buffer

from runner import set_task
from tasks import celery_app


def gen_image(x, y, extension):
    im = Image.new('RGB', (x, y))
    draw = ImageDraw.Draw(im)
    draw.line((x / 3, y - y / 5) + (x / 3, y / 8), width=1, fill='grey')
    draw.line((x / 3, y - y / 5) + (x - x / 3, y - y / 5), width=1, fill='grey')
    # creating a buffer object for an image to save
    b = BytesIO()
    im.save(b, format=extension)
    # moving a cursor to the beginning
    b.seek(0)
    # creating UploadFile object from buffer
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
def test_wrong_img_height(arrange_image):
    with pytest.raises(HTTPException):
        set_task(400, 0, arrange_image)
    with pytest.raises(HTTPException):
        set_task(400, 10000, arrange_image)


@pytest.mark.parametrize('arrange_image', [(300, 300, 'png'), (500, 500, 'jpeg')], indirect=True)
def test_wrong_img_width(arrange_image):
    with pytest.raises(HTTPException):
        set_task(10000, 400, arrange_image)
    with pytest.raises(HTTPException):
        set_task(0, 400, arrange_image)


@pytest.mark.parametrize('arrange_image', [(300, 300, 'png'), (500, 500, 'jpeg')], indirect=True)
def test_correct_flow(arrange_image):
    height, width = 400, 400
    id = set_task(height, width, arrange_image)
    task = celery_app.AsyncResult(id=id)
    while True:
        if task.ready():
            break
    image = Image.open(f'{getcwd()}/{id}', 'r')
    assert image.size == (height, width)
    assert image.format.lower() == arrange_image.content_type.split('/')[1]
