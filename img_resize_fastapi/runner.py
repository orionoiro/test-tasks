from base64 import b64encode
from os import getcwd

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from uvicorn.config import LOGGING_CONFIG

from tasks import celery_app, resize
from transactions import to_store, to_retrieve

app = FastAPI()


@app.post('/resize/')
def set_task(width: int, height: int, file: UploadFile = File(...)) -> bool:
    if file.content_type not in ('image/jpeg', 'image/png'):
        raise HTTPException(status_code=400, detail='Wrong file type')
    elif not 1 <= height <= 9999:
        raise HTTPException(status_code=400, detail='height value should be between 1 and 9999')
    elif not 1 <= width <= 9999:
        raise HTTPException(status_code=400, detail='width value should be between 1 and 9999')

    data_bytes = file.file._file.read()  # bytes data of an image
    b64_string = b64encode(data_bytes).decode('ascii')
    task = resize.delay(width, height, b64_string)
    to_store(task.id, file.content_type)

    return task.id


@app.get('/status/{job_id}')
def get_status(job_id: str):
    if to_retrieve(job_id):
        task = celery_app.AsyncResult(id=job_id)
        if task.ready():
            img_path = f'{getcwd()}/{job_id}'
            response = FileResponse(img_path)
            response.headers['Content-Disposition'] = "attachment; filename=result"
            response.headers['Content-Type'] = to_retrieve(job_id).decode()
            return response
        else:
            payload = {'status': task.status}
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=payload)
    else:
        raise HTTPException(status_code=404, detail='Incorrect task id')


def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run(app)


if __name__ == '__main__':
    run()
