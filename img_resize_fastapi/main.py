from uuid import uuid4

from fastapi import FastAPI, File, UploadFile

from resize import resize

app = FastAPI()


@app.post('/resize/')
def set_task(width: int, height: int, file: UploadFile = File(...)) -> dict:
    if file.content_type not in ('image/jpeg', 'image/png'):
        raise TypeError
    elif 1 > height or height > 9999:
        raise ValueError('height value should be between 1 and 9999')
    elif 1 > width or width > 9999:
        raise ValueError('width value should be between 1 and 9999')

    uuid = str(uuid4())
    resize(width, height, file.file)
    return {'job id': uuid}


@app.get('/status/{job_id}')
def get_status(job_id: str):
    raise NotImplemented
