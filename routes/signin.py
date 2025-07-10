from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from models.model import signInRequest

# Initialize the APIRouter
signin = APIRouter()

# Initialize Jinja2Templates to locate HTML templates
templates = Jinja2Templates(directory="template")

# Dummy in-memory user store (replace this with real DB)
users = {
    "9876543210": {
        "captcha": "AB12CD"  # Example; in real use, you'd verify dynamically
    }
}


# Route to serve the Paytm HTML page
@signin.get("/signin")
async def serve_paytm(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@signin.post("/signin")
async def signin_user(data: signInRequest):
    mobile = data.mobile
    captcha = data.captcha

    # Validation
    if not mobile or not captcha:
        raise HTTPException(status_code=400, detail="Mobile and CAPTCHA are required")

    # Lookup user (replace with MongoDB logic)
    user = users.get(mobile)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # CAPTCHA check (replace with real validation)
    if captcha != user["captcha"]:
        raise HTTPException(status_code=401, detail="Invalid CAPTCHA")

    return {"message": "Login successful"}
