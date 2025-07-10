from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from routes.paytm import paytm as paytm
from routes.homepage import home as home 
from routes.signin import signin as login 
from routes.signup import signup as signup


app = FastAPI(default_response_class=JSONResponse)

# Configure templates folder
templates = Jinja2Templates(directory="template")

app.mount("/staticfile", StaticFiles(directory="staticfile"), name="staticfile")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/design", StaticFiles(directory="design"), name="design")


app.include_router(paytm)
app.include_router(home)
app.include_router(login)
app.include_router(signup)