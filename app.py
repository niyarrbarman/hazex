from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils import Dehaze
import shutil
import os

'''
To run:
uvicorn app:app --reload
'''
def clear_dir(PATH):
    filenames = os.listdir(PATH)
    for filename in filenames:
        os.remove(os.path.join(PATH, filename))

upload_folder = 'static/uploads'
output_folder = 'static/output'

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Define a function to save the uploaded file temporarily
async def save_upload_file(upload_file: UploadFile):
    with open(f"static/uploads/{upload_file.filename}", "wb") as temp_file:
        shutil.copyfileobj(upload_file.file, temp_file)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # Clear Folders
    clear_dir(upload_folder)
    clear_dir(output_folder)
    context = {"request": request}
    return templates.TemplateResponse("index.html", context=context)

@app.post("/dehaze", response_class=HTMLResponse)
async def dehaze(request: Request, uploaded_file: UploadFile):
    # Clear Folders
    clear_dir(upload_folder)
    clear_dir(output_folder)
    # Save the uploaded file temporarily
    await save_upload_file(uploaded_file)
    # Dehaze 
    input_path = f"static/uploads/{uploaded_file.filename}"
    output_path = f"static/output/dehazed_output.png"
    Dehaze().dehaze(img_path=input_path, out_path=output_path) 
    # Context
    context = {"request": request, "dehazed_image": 1, "uploaded_filename" : uploaded_file.filename}
    return templates.TemplateResponse("index.html", context=context)