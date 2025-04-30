from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid

from .transcriber import transcribe_audio
from .utils import save_upload_file, remove_file
from starlette.middleware.base import BaseHTTPMiddleware

# Middleware untuk membatasi ukuran file upload (contoh: 200 MB)
class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_upload_size: int):
        super().__init__(app)
        self.max_upload_size = max_upload_size  # dalam byte

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > self.max_upload_size:
            return Response("413 Request Entity Too Large", status_code=413)
        return await call_next(request)

app = FastAPI()

# Middleware untuk batas upload 200 MB
app.add_middleware(LimitUploadSizeMiddleware, max_upload_size=200 * 1024 * 1024)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_audio(request: Request, file: UploadFile):
    filename = f"temp_{uuid.uuid4().hex}.mp3"
    await save_upload_file(file, filename)
    text = transcribe_audio(filename)
    remove_file(filename)
    return templates.TemplateResponse("index.html", {"request": request, "transcript": text})
