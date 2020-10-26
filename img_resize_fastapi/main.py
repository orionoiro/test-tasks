from fastapi import FastAPI, File, UploadFile

from tasks import resize

app = FastAPI()


@app.post('/resize/')
def set_task(width: int, height: int, file: UploadFile = File(...)) -> dict:
    if file.content_type not in ('image/jpeg', 'image/png'):
        raise TypeError
    elif not 1 <= height <= 9999:
        raise ValueError('height value should be between 1 and 9999')
    elif not 1 <= width <= 9999:
        raise ValueError('width value should be between 1 and 9999')
    # change file object to bytes
    task = resize.delay(width, height, file.file)
    return task


@app.get('/status/{job_id}')
def get_status(job_id: str):
    raise NotImplemented
