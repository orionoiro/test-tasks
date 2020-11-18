from base64 import b64encode
from os import getcwd

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from tasks import celery_app, resize

app = FastAPI()


@app.post('/resize/')
def set_task(width: int, height: int, file: UploadFile = File(...)) -> bool:
    if file.content_type not in ('image/jpeg', 'image/png'):
        raise TypeError
    elif not 1 <= height <= 9999:
        raise ValueError('height value should be between 1 and 9999')
    elif not 1 <= width <= 9999:
        raise ValueError('width value should be between 1 and 9999')

    data_bytes = file.file._file.read()  # bytes data of an image
    b64_string = b64encode(data_bytes).decode('ascii')
    task = resize.delay(width, height, b64_string)

    return task.id


@app.get('/status/{job_id}')
def get_status(job_id: str):
    job_id = job_id.split('.')[0]
    task = celery_app.AsyncResult(id=job_id)
    if task.ready():
        img_path = f'{getcwd()}/{job_id}'
        return FileResponse(img_path)
    return False
