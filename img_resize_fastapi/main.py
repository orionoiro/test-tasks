from base64 import b64encode

from fastapi import FastAPI, File, UploadFile

from tasks import resize

app = FastAPI()


@app.post('/resize/')
async def set_task(width: int, height: int, file: UploadFile = File(...)) -> dict:
    if file.content_type not in ('image/jpeg', 'image/png'):
        raise TypeError
    elif not 1 <= height <= 9999:
        raise ValueError('height value should be between 1 and 9999')
    elif not 1 <= width <= 9999:
        raise ValueError('width value should be between 1 and 9999')

    data_bytes = file.file._file.read()  # bytes data of an image
    b64_string = b64encode(data_bytes).decode('ascii')
    result = resize.delay(width, height, b64_string)
    return {'OK': result.get()}


@app.get('/status/{job_id}')
def get_status(job_id: str):
    raise NotImplemented
