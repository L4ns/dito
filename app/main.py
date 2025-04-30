from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import os
import uuid
from .transcriber import transcribe_audio
from .utils import save_upload_file, remove_file

app = FastAPI()
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
