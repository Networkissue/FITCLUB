from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, Response
# from routes.jwt import get_user_by

# from routes.paytm import paytm as paytm
from routes.homepage import home as home 
from routes.signin import signin_router as signin 
from routes.signup import signup_router as signup
# from routes.diet import diet as diet
from routes.payment import payment as razorpay_payment
# from routes.adminrouter import admin_router






app = FastAPI()

# Mount static and templates folders
app.mount("/staticfile", StaticFiles(directory="staticfile"), name="staticfile")
templates = Jinja2Templates(directory='template')
app.mount("/design", StaticFiles(directory="design"), name="design")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


# app.include_router(paytm)
app.include_router(home)
app.include_router(signin)
app.include_router(signup)
app.include_router(razorpay_payment)
# app.include_router(admin_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)