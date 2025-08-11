from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from database.database import user_data, payment_due, payment_history, get_membership_plan
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.models import *
from routes.signin import send_email

signup_router = APIRouter()
templates = Jinja2Templates(directory='template')
signup_router.mount("/staticfile", StaticFiles(directory="staticfile"), name="main")

# Initialize password hashing context
pwd_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")


@signup_router.get("/signup")
async def signup_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

def generate_user_id(mobile: str) -> str:
    count = user_data.count_documents({}) + 1
    if mobile in ["8919313008", "9390086532", "8008078784", "8008984440"]:
        return f"admin{count:03d}"
    else:
        return f"user{count:03d}"

@signup_router.post("/signup")
async def signup(request: Request, background_tasks: BackgroundTasks):
    try:
        body = await request.json()
        username = body.get("username")
        email = body.get("email")
        mobile = body.get("mobile")
        password = body.get("password")
        confirm_password = body.get("confirm_password")
        gender = body.get("gender")

        print(f"Received Data: {body}")

        # Ensure password and confirm_password are received correctly
        print(f"Password: {password}, Confirm Password: {confirm_password}")


        # Validation checks
        if not all([username, email, mobile, password, confirm_password, gender]):
            return JSONResponse(status_code=400, content={"detail": "All fields are required"})

        if not username:
            return JSONResponse(status_code=400, content={"detail": "Username is required"})
        if not email:
            return JSONResponse(status_code=400, content={"detail": "Email is required"})
        if not mobile:
            return JSONResponse(status_code=400, content={"detail": "Mobile number is required"})
        
        # Continue with validations...
        if not password or not confirm_password:
            return JSONResponse(status_code=400, content={"detail": "Password and Confirm Password are required"})
        
        if password != confirm_password:
            return JSONResponse(status_code=400, content={"detail": "Passwords do not match"})
        
        if not gender:
            return JSONResponse(status_code=400, content={"detail": "Gender is required"})

        # Validate email format
        if "@" not in email or "." not in email:
            return JSONResponse(status_code=400, content={"detail": "Invalid email format"})

        if len(mobile) != 10 or not mobile.isdigit():
            return JSONResponse(status_code=400, content={"detail": "Invalid mobile number"})
        
        if user_data.find_one({"email": email}):
            return JSONResponse(status_code=400, content={"detail": "Email already exists"})
        
        if user_data.find_one({"mobile": mobile}):
            return JSONResponse(status_code=400, content={"detail": "Mobile number already exists"})
        
        # Validate password requirements  
        if len(password) < 7:
            return JSONResponse(status_code=400, content={"detail": "Password must contain at least 7 characters"})
        if password != confirm_password:
            return JSONResponse(status_code=400, content={"detail": "Passwords do not match"})
        
        # Hash the password
        hashed_password = pwd_hash.hash(password)

        user_id = generate_user_id(mobile)
        joining_date = datetime.now().strftime("%Y-%m-%d")
        next_due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        # Insert user data into the database
        user_data.insert_one({
            "id": user_id,
            "username": username,
            "email": email,
            "mobile": mobile,
            "password": hashed_password,
            "gender": gender,
            "role": "user",
            "name": username.title(),
            "joining_date": joining_date,
            "last_payment_date": None,
            "next_due_date": None,
            "created_at": datetime.now()
        })

        # Insert payment due data into the database
        payment_due.insert_one({
            "user_id": user_id,
            "last_payment": None,
            "next_due": None,
            "status": "inactive",
            "created_at": datetime.now()
        })

        # Insert payment history data into the database
        payment_history.insert_one({
            "user_id": user_id,
            "membership": "NA",
            "payment_id": "NA",             # Will be filled during real Razorpay transaction
            "amount": 0,                    # Free on signup or trial
            "status": "trial",
            "date": datetime.utcnow(),      # Use UTC for consistency
            "method": "signup",
            "remarks": "Initial signup account creation"
        })

        # User email
        background_tasks.add_task(
            send_email,
            email,
            "Welcome To The GYM!",
            f"<h2>Thanks for signing up! Your user id is {user_id}</h2>"
        )

        # Admin emails list
        admin_emails = [
            "thegymbyjohnson@gmail.com",
            "rohithvaddepally4@gmail.com"
        ]

        # Admin email
        for admin_email in admin_emails:
            background_tasks.add_task(
                send_email,
                admin_email,
                "New User Registered",
                f"""
                <h2>New User Registration</h2>
                <p><strong>Name:</strong> {username}</p>
                <p><strong>User ID:</strong> {user_id}</p>
                <p>🎉 A new user has joined The Gym!</p>
                """
            )


        return JSONResponse(status_code=201, content={"message": "Account created successfully"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
