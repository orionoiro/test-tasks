from uuid import uuid4

from fastapi import FastAPI, File, UploadFile

from resize import resize

app = FastAPI()


@app.post('/resize/')
def set_task(width: int, height: int, file: UploadFile = File(...)) -> dict:
    uuid = str(uuid4())
    resize(width, height, file.file)
    return {'job id': uuid}


@app.get('/status/{job_id}')
def get_status(job_id: str):
    return job_id
