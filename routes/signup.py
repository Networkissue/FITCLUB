from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from database.database import user_data
from passlib.context import CryptContext
from models.model import signup
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



signup = APIRouter()
pwd_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory='template')

signup.mount("/staticfile", StaticFiles(directory="staticfile"), name="main")

# Route to serve the Paytm HTML page
@signup.get("/signup")
async def signup_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@signup.post("/signup")
async def signup_api(request: Request):
    try:
        data = await request.json()
        Uname = data.get("username")
        email = data.get("email")
        mobile = data.get("mobile")
        gender = data.get("gender")

        # Validate fields
        if not all([Uname, email, mobile, gender]):
            return JSONResponse(status_code=400, content={"detail": "All fields are required"})

        if user_data.find_one({"email": email}):
            return JSONResponse(status_code=400, content={"detail": "Email already registered"})

        if user_data.find_one({"mobile": mobile}):
            return JSONResponse(status_code=400, content={"detail": "Mobile number already registered"})

        new_user = signup(
            username=Uname,
            email=email,
            mobile=mobile,
            gender=gender,
            Role="user",
        )

        user_data.insert_one(dict(new_user))

        return JSONResponse(content={"message": "User registered successfully✅"}, status_code=201)

    except HTTPException as e:
        return JSONResponse(content={"detail": e.detail}, status_code=e.status_code)

    except Exception as e:
        return JSONResponse(content={"detail": f"Internal Server Error: {str(e)}"}, status_code=500)
