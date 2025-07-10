import json
import hashlib
import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from models.model import PaymentRequest
import os
from dotenv import load_dotenv

# Load Paytm credentials from .env file
load_dotenv()
PAYTM_MID = os.getenv("PAYTM_MID")
PAYTM_SECRET_KEY = os.getenv("PAYTM_SECRET_KEY")
PAYTM_WEBSITE = os.getenv("PAYTM_WEBSITE")

paytm = APIRouter()

# Initialize Jinja2Templates to locate HTML templates
templates = Jinja2Templates(directory="template")

# Mount static files directory for static
paytm.mount("/staticfile", StaticFiles(directory="staticfile"), name="static")

# Helper function to generate checksum
def generate_checksum(params):
    sorted_params = '&'.join(f'{k}={v}' for k, v in sorted(params.items()))
    checksum = hashlib.sha256(f"{sorted_params}|{PAYTM_SECRET_KEY}".encode()).hexdigest()
    return checksum

# Route to serve the Paytm HTML page
@paytm.get("/paytm")
async def serve_paytm(request: Request):
    return templates.TemplateResponse("paytm.html", {"request": request})


@paytm.post("/create-paytm-payment")
async def create_paytm_payment(request: PaymentRequest):
    order_id = request.orderId
    amount = request.amount

    params = {
        "MID": PAYTM_MID,
        "ORDER_ID": order_id,
        "CUST_ID": "customer123",
        "TXN_AMOUNT": amount,
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": PAYTM_WEBSITE,
        "CALLBACK_URL": "http://localhost:8000/payment-callback",
        "EMAIL": "customer@example.com",
        "MOBILE_NO": "9999999999"
    }

    checksum = generate_checksum(params)
    params["CHECKSUMHASH"] = checksum

    # Send request to Paytm API for payment initiation
    try:
        response = requests.post('https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction', data=params)
        response_data = response.json()
        if response.status_code == 200:
            return JSONResponse(content={"orderId": order_id, "amount": amount, "checksum": checksum})
        else:
            raise HTTPException(status_code=400, detail="Payment initiation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@paytm.post("/payment-callback")
async def payment_callback(request: dict):
    checksum = request.get('CHECKSUMHASH')
    params = request.copy()
    params.pop('CHECKSUMHASH', None)

    generated_checksum = generate_checksum(params)

    if checksum == generated_checksum:
        if request.get('STATUS') == 'TXN_SUCCESS':
            return {"status": "✅ Payment successful"}
        else:
            return {"status": "❌ Payment failed"}
    else:
        return {"status": "Checksum mismatch, payment failed"}
