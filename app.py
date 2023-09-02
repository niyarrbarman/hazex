from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils import Dehaze
# import os

'''
To run:
uvicorn app:app --reload
'''

'''
def clear_dir(PATH):
    filenames = os.listdir(PATH)
    for filename in filenames:
        os.remove(os.path.join(PATH, filename))

'''

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {"request" : request}
    return templates.TemplateResponse("index.html", context=context)

@app.get("/dehaze", response_class=HTMLResponse)
def dehaze(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context=context)