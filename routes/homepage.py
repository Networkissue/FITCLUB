from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# Initialize the APIRouter
home = APIRouter()

# Initialize Jinja2Templates to locate HTML templates
templates = Jinja2Templates(directory="template")

# Route to serve the Paytm HTML page
@home.get("/")
async def serve_paytm(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
